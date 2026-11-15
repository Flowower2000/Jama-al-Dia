import json
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import httpx
import numpy as np
import pandas as pd
import pytest
import respx

from corredor.jama_al_dia import cierres, pagina
from corredor.jama_al_dia.estado import (
    actual,
    bloques,
    estado_ar,
    estado_cl,
    horas,
    serie,
    ultima_consulta,
)
from corredor.jama_al_dia.pronostico import (
    Medida,
    Pronostico72,
    banner,
    climatologia_rafagas,
    elegir,
    pronostico_72h,
)
from corredor.jama_al_dia.telegram import (
    AVISO_OMITIDO,
    PIE,
    Publicado,
    TelegramAPI,
    TelegramError,
    notificar,
)
from corredor.models import CriticalPoint, JamaEstado

TOKEN = "123456:SECRETO-de-prueba"  # noqa: S105 — fake token for the mocked API
CHAT = "@canal_prueba"
NOW = datetime(2026, 11, 15, 15, 17, tzinfo=UTC)  # 12:17 in Argentina
OLD_PARTE = datetime(2026, 11, 9, 11, 0, tzinfo=UTC)  # 08:00 local


def ar(ts: datetime, prioridad: str = "ABIERTO", vialidad: str = "HABILITADA") -> JamaEstado:
    rec = {
        "estado_prioridad": prioridad,
        "estado_vialidad": vialidad,
        "fecha_hora_consulta": (ts - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
        "fecha_schema": "09:00-19:15",
        "id": 19,
        "nombre_paso": "Jama",
    }
    return JamaEstado(fuente="argentina_gob_ar", fetched_at=ts, payload_json=json.dumps([rec]))


def cl(
    ts: datetime,
    trans: str = "TRÁNSITO SIN RESTRICCIÓN",
    fecha: datetime | None = None,
    **extra: object,
) -> JamaEstado:
    f = fecha or ts
    loc = f - timedelta(hours=3)
    hora = (loc.hour * 60 + loc.minute) * 60_000
    day = datetime(loc.year, loc.month, loc.day, 12, tzinfo=UTC)
    rec = {
        "TRANSITABILIDAD": trans, "FECHA": int(day.timestamp() * 1000), "HORA": hora, **extra
    }  # fmt: skip
    return JamaEstado(fuente="mop_cl", fetched_at=ts, payload_json=json.dumps([rec]))


def err(fuente: str, ts: datetime) -> JamaEstado:
    return JamaEstado(fuente=fuente, fetched_at=ts, error="HTTP 503")  # type: ignore[arg-type]


# ------------------------------------------------------------------ estado
def test_ar_states_and_schedule() -> None:
    night = datetime(2026, 11, 15, 6, 43, tzinfo=UTC)  # 03:43 local, outside 09:00-19:15
    day = datetime(2026, 11, 15, 15, 0, tzinfo=UTC)  # 12:00 local
    assert estado_ar(ar(day)).estado == "abierto"
    e = estado_ar(ar(night, "CERRADO"))
    assert (e.estado, e.por_horario) == ("cerrado", True)
    e = estado_ar(ar(day, "CERRADO"))
    assert (e.estado, e.por_horario) == ("cerrado", False)
    assert estado_ar(ar(day, "ABIERTO", "CERRADA")).estado == "cerrado"
    assert estado_ar(ar(day, "ABIERTO", "CONDICIONADA")).estado == "restringido"
    e = estado_ar(ar(night, "CERRADO", "CONDICIONADA"))
    assert (e.estado, e.por_horario) == ("cerrado", False)
    assert estado_ar(ar(day, "???")).estado is None
    assert estado_ar(err("argentina_gob_ar", day)).error == "HTTP 503"


def test_cl_states() -> None:
    assert estado_cl(cl(NOW)).estado == "abierto"
    assert estado_cl(cl(NOW, "CERRADO")).estado == "cerrado"
    assert estado_cl(cl(NOW, "SÓLO VEHÍCULOS 4X4")).estado == "restringido"
    assert estado_cl(cl(NOW, "TRÁNSITO SIN RESTRICCIÓN", HABILITADO="NO")).estado == "cerrado"
    e = estado_cl(cl(NOW, fecha=OLD_PARTE))
    assert e.hora_oficial == "2026-11-09 08:00"


def test_actual_since_and_errors_keep_last_state() -> None:
    snaps = [
        cl(NOW - timedelta(hours=10), "CERRADO"),
        cl(NOW - timedelta(hours=5)),
        cl(NOW - timedelta(hours=4)),
        err("mop_cl", NOW - timedelta(hours=1)),
    ]
    a = actual(serie(snaps, "CL"), NOW)
    assert a.ultimo is not None
    assert a.ultimo.estado == "abierto"
    assert a.desde == NOW - timedelta(hours=5)
    assert not a.desde_al_menos
    assert a.viejo  # last good one is 4 h old
    assert horas(a.desde, NOW) == 5
    first = actual(serie([cl(NOW - timedelta(hours=2))], "CL"), NOW)
    assert first.desde_al_menos


def test_bloques_carry_at_most_three_hours() -> None:
    snaps = [cl(NOW - timedelta(hours=8), "CERRADO")]
    filas = bloques(serie(snaps, "CL"), NOW)
    assert len(filas) == 7
    assert all(len(f["celdas"]) == 24 for f in filas)
    hoy = filas[-1]["celdas"]  # NOW = 12:17 local; snapshot at 04:17 local
    assert hoy[3] is None
    assert hoy[4:8] == ["cerrado"] * 4
    assert hoy[8] is None
    assert hoy[13] == "futuro"


# ------------------------------------------------------------------ telegram
def _actuales(ar_state: str = "ABIERTO", cl_state: str = "TRÁNSITO SIN RESTRICCIÓN"):  # type: ignore[no-untyped-def]
    snaps = [ar(NOW - timedelta(minutes=5), ar_state), cl(NOW - timedelta(minutes=5), cl_state)]
    return actual(serie(snaps, "AR"), NOW), actual(serie(snaps, "CL"), NOW)


@pytest.fixture
def tg() -> respx.MockRouter:
    with respx.mock(base_url="https://api.telegram.org", assert_all_called=False) as router:
        router.post(f"/bot{TOKEN}/sendMessage").mock(
            return_value=httpx.Response(200, json={"ok": True, "result": {}})
        )
        router.post(f"/bot{TOKEN}/getChatMemberCount").mock(
            return_value=httpx.Response(200, json={"ok": True, "result": 42})
        )
        yield router


def _sent(router: respx.MockRouter) -> list[str]:
    return [
        json.loads(c.request.content)["text"]
        for c in router.calls
        if c.request.url.path.endswith("/sendMessage")
    ]


def test_empty_state_file_loads_as_new(tmp_path: Path) -> None:
    (tmp_path / "t.json").write_text("")
    assert Publicado.load(tmp_path / "t.json") == Publicado()


def test_without_secrets_skips(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    a, c = _actuales()
    caplog.set_level("INFO")
    assert notificar(None, a, c, tmp_path / "t.json", NOW, url="") == [AVISO_OMITIDO]
    assert AVISO_OMITIDO in caplog.text
    assert not (tmp_path / "t.json").exists()


def test_posts_only_on_change(tmp_path: Path, tg: respx.MockRouter) -> None:
    path = tmp_path / "t.json"
    api = TelegramAPI(TOKEN, CHAT)
    a, c = _actuales()
    url = "https://emiliano-f.github.io/corredor-quebrada-puna/"
    assert "estado inicial guardado" in notificar(api, a, c, path, NOW, url=url)
    assert _sent(tg) == []
    notificar(api, a, c, path, NOW + timedelta(hours=1), url=url)
    assert _sent(tg) == []
    a2, c2 = _actuales(cl_state="CERRADO")
    assert "cambio" in notificar(api, a2, c2, path, NOW + timedelta(hours=2), url=url)
    (msg,) = _sent(tg)
    lineas = msg.split("\n")
    assert len(lineas) <= 4
    assert lineas[0].startswith("🟢 Jama — Argentina ABIERTO desde")
    assert lineas[1].startswith("🔴 Chile: CERRADO desde")
    assert lineas[2] == PIE == "Fuente: Pasos Fronterizos (AR) · MOP (CL). No es un canal oficial."
    assert lineas[3] == url
    assert "Resolución" not in msg
    assert "parte hoy" not in msg
    notificar(api, a2, c2, path, NOW + timedelta(hours=3), url=url)
    assert len(_sent(tg)) == 1
    pub = Publicado.load(path)
    assert pub.clave == "AR=abierto;CL=cerrado"
    assert pub.suscriptores == 42


def test_nightly_schedule_closure_is_not_posted(tmp_path: Path, tg: respx.MockRouter) -> None:
    path = tmp_path / "t.json"
    api = TelegramAPI(TOKEN, CHAT)
    day = datetime(2026, 11, 15, 15, 0, tzinfo=UTC)
    night = datetime(2026, 11, 16, 1, 0, tzinfo=UTC)  # 22:00 local
    for ts, st in ((day, "ABIERTO"), (night, "CERRADO")):
        snaps = [ar(ts, st), cl(ts)]
        a, c = actual(serie(snaps, "AR"), ts), actual(serie(snaps, "CL"), ts)
        notificar(api, a, c, path, ts, url="")
    assert _sent(tg) == []
    notificar(api, a, c, path, night, url="", avisar_horario=True)
    assert len(_sent(tg)) == 1


def test_real_closure_running_into_the_night_is_not_a_change(
    tmp_path: Path, tg: respx.MockRouter
) -> None:
    path = tmp_path / "t.json"
    api = TelegramAPI(TOKEN, CHAT)
    day = datetime(2026, 11, 15, 15, 0, tzinfo=UTC)
    night = datetime(2026, 11, 16, 1, 0, tzinfo=UTC)
    for ts, st in ((day, "ABIERTO"), (day + timedelta(hours=1), "CERRADO"), (night, "CERRADO")):
        snaps = [ar(ts, st), cl(ts)]
        notificar(
            api, actual(serie(snaps, "AR"), ts), actual(serie(snaps, "CL"), ts), path, ts, url=""
        )
    assert len(_sent(tg)) == 1  # only the real closure at 13:00
    assert Publicado.load(path).clave == "AR=cerrado;CL=abierto"


def test_first_run_at_night_then_opening_hours_is_not_a_change(
    tmp_path: Path, tg: respx.MockRouter
) -> None:
    path = tmp_path / "t.json"
    api = TelegramAPI(TOKEN, CHAT)
    night = datetime(2026, 11, 16, 1, 0, tzinfo=UTC)
    morning = datetime(2026, 11, 16, 13, 0, tzinfo=UTC)
    for ts, st in ((night, "CERRADO"), (morning, "ABIERTO")):
        snaps = [ar(ts, st), cl(ts)]
        notificar(
            api, actual(serie(snaps, "AR"), ts), actual(serie(snaps, "CL"), ts), path, ts, url=""
        )
    assert _sent(tg) == []
    assert Publicado.load(path).clave == "AR=abierto;CL=abierto"


def test_side_outage_does_not_post(tmp_path: Path, tg: respx.MockRouter) -> None:
    path = tmp_path / "t.json"
    api = TelegramAPI(TOKEN, CHAT)
    a, c = _actuales()
    notificar(api, a, c, path, NOW, url="")
    out = actual(serie([err("mop_cl", NOW)], "CL"), NOW)
    notificar(api, a, out, path, NOW + timedelta(hours=1), url="")
    assert _sent(tg) == []


def test_daily_summary_once_at_eight(tmp_path: Path, tg: respx.MockRouter) -> None:
    path = tmp_path / "t.json"
    api = TelegramAPI(TOKEN, CHAT)
    a, c = _actuales()
    notificar(api, a, c, path, NOW, url="")
    eight = datetime(2026, 11, 16, 11, 17, tzinfo=UTC)  # 08:17 local
    assert "resumen" in notificar(api, a, c, path, eight, url="")
    notificar(api, a, c, path, eight + timedelta(minutes=30), url="")
    msgs = _sent(tg)
    assert len(msgs) == 1
    assert msgs[0].startswith("🟢 Jama — Argentina ABIERTO")
    assert len(msgs[0].split("\n")) <= 4


def test_change_at_eight_doubles_as_the_summary(tmp_path: Path, tg: respx.MockRouter) -> None:
    path = tmp_path / "t.json"
    Publicado(clave="AR=abierto;CL=abierto").save(path)
    a, c = _actuales(cl_state="CERRADO")
    eight = datetime(2026, 11, 16, 11, 17, tzinfo=UTC)
    hechos = notificar(TelegramAPI(TOKEN, CHAT), a, c, path, eight, url="")
    assert "cambio" in hechos
    assert "resumen" in hechos
    assert len(_sent(tg)) == 1  # no identical second post
    pub = Publicado.load(path)
    assert pub.clave == "AR=abierto;CL=cerrado"
    assert pub.resumen_fecha == "2026-11-16"


def test_change_is_saved_even_if_a_later_post_fails(tmp_path: Path) -> None:
    path = tmp_path / "t.json"
    Publicado(clave="AR=abierto;CL=abierto", resumen_fecha="2026-11-15").save(path)
    a, c = _actuales(cl_state="CERRADO")
    nine = datetime(2026, 11, 16, 12, 17, tzinfo=UTC)
    with respx.mock(base_url="https://api.telegram.org") as router:
        router.post(f"/bot{TOKEN}/sendMessage").mock(
            return_value=httpx.Response(200, json={"ok": True, "result": {}})
        )
        router.post(f"/bot{TOKEN}/getChatMemberCount").mock(
            return_value=httpx.Response(500, json={"ok": False})
        )
        notificar(TelegramAPI(TOKEN, CHAT), a, c, path, nine, url="")
    assert Publicado.load(path).clave == "AR=abierto;CL=cerrado"


def test_test_post(tmp_path: Path, tg: respx.MockRouter) -> None:
    a, c = _actuales()
    notificar(TelegramAPI(TOKEN, CHAT), a, c, tmp_path / "t.json", NOW, url="", prueba=True)
    (msg,) = _sent(tg)
    assert msg.startswith("[Prueba] 🟢 Jama — Argentina ABIERTO")
    assert PIE in msg


def test_errors_never_carry_the_token() -> None:
    with respx.mock(base_url="https://api.telegram.org") as router:
        router.post(f"/bot{TOKEN}/sendMessage").mock(
            return_value=httpx.Response(401, json={"ok": False, "description": "Unauthorized"})
        )
        with pytest.raises(TelegramError) as exc:
            TelegramAPI(TOKEN, CHAT).send_message("x")
    assert TOKEN not in str(exc.value)
    assert "401" in str(exc.value)
    with respx.mock(base_url="https://api.telegram.org") as router:
        router.post(f"/bot{TOKEN}/sendMessage").mock(side_effect=httpx.ConnectError("boom"))
        with pytest.raises(TelegramError) as exc:
            TelegramAPI(TOKEN, CHAT).send_message("x")
    assert TOKEN not in str(exc.value)


def test_stale_side_shows_sin_dato_reciente_and_never_posts(
    tmp_path: Path, tg: respx.MockRouter
) -> None:
    old = NOW - timedelta(hours=3)
    snaps = [ar(old), cl(old, "CERRADO")]
    a, c = actual(serie(snaps, "AR"), NOW), actual(serie(snaps, "CL"), NOW)
    assert a.viejo
    html = pagina._lado("Chile", c, NOW)
    assert "Estado no confirmado" in html
    assert "Último dato: Cerrado, hoy 09:17" in html
    assert 'class="lado viejo"' in html  # amber, never a big CERRADO
    assert "CERRADO</div>" not in html
    path = tmp_path / "t.json"
    Publicado(clave="AR=abierto;CL=abierto").save(path)
    notificar(TelegramAPI(TOKEN, CHAT), a, c, path, NOW, url="")
    assert _sent(tg) == []
    assert Publicado.load(path).clave == "AR=abierto;CL=abierto"


def test_header_shows_page_and_last_consulted_times() -> None:
    snaps = [ar(NOW - timedelta(minutes=40)), cl(NOW - timedelta(minutes=30))]
    a, c = actual(serie(snaps, "AR"), NOW), actual(serie(snaps, "CL"), NOW)
    datos = pagina.Datos(
        now=NOW, ar=a, cl=c, bloques={}, por_mes_anio=[], por_anio=[], duraciones={"n": 0},
        pronostico=[],
    )  # fmt: skip
    assert ultima_consulta(snaps) == NOW - timedelta(minutes=30)
    assert "Datos de las 11:37" in pagina.index(datos)  # the older of the two sides


def test_schedule_closure_is_its_own_grey_state() -> None:
    night = datetime(2026, 11, 16, 1, 0, tzinfo=UTC)  # 22:00 local
    s = serie([ar(night, "CERRADO")], "AR")
    a = actual(s, night + timedelta(minutes=10))
    html = pagina._lado("Argentina", a, night + timedelta(minutes=10))
    assert "Cerrado por horario" in html
    assert "Abre a las 09:00" in html
    assert 'class="lado horario"' in html
    assert 'class="lado cerrado"' not in html
    from corredor.jama_al_dia.telegram import _linea

    assert _linea("Jama — Argentina", a, night + timedelta(minutes=10)) == (
        "⚪ Jama — Argentina fuera de horario, abre a las 09:00"
    )
    late = night + timedelta(hours=3)
    assert _linea("Jama — Argentina", actual(s, late), late).startswith(
        "🟡 Jama — Argentina sin dato reciente (último: Cerrado por horario"
    )
    filas = bloques(s, night + timedelta(minutes=10))
    assert "horario" in filas[-1]["celdas"]
    assert "cerrado" not in filas[-1]["celdas"]
    datos = pagina.Datos(
        now=night,
        ar=a,
        cl=a,
        bloques={},
        por_mes_anio=[],
        por_anio=[],
        duraciones={"n": 0},
        pronostico=[],
    )
    assert "fuera de horario</span>" in pagina.index(datos)


def test_old_official_report_is_flagged_in_days() -> None:
    e = estado_cl(cl(NOW, fecha=OLD_PARTE))  # parte 2026-11-09 08:00, NOW 15/11 12:17 local
    assert e.parte_dias(NOW) == 6
    html = pagina._lado("Chile", actual([e], NOW), NOW)
    assert "Sin parte nuevo" in html  # describes the source, not our check
    assert "Estado no confirmado" not in html
    assert "Último parte oficial (09/11 08:00): Abierto" in html
    assert "Chile no actualiza este parte desde el 09/11. Consultá el estado oficial" in html
    assert 'class="lado viejo"' in html  # stays amber
    viejo = pagina._lado("Chile", actual([e], NOW + timedelta(hours=3)), NOW + timedelta(hours=3))
    assert "Estado no confirmado" in viejo  # our own check is stale: that wins
    from corredor.jama_al_dia.telegram import _linea

    assert _linea("Chile:", actual([e], NOW), NOW) == (
        "🟡 Chile: sin parte nuevo desde el 09/11 (último: Abierto)"
    )
    assert estado_ar(ar(NOW)).parte_dias(NOW) is None


# ------------------------------------------------------------------ cierres
def test_cierres_export_and_stats() -> None:
    eventos = pd.DataFrame(
        [
            {"punto_id": "rn52_paso_jama", "tipo_corte": "total", "fecha": date(2024, 6, 1),
             "fecha_inicio": date(2024, 6, 1), "fecha_fin": date(2024, 6, 4), "causa": "nieve",
             "lado": "CL", "n_medios": 2, "fuentes": ["u1", "u2"]},
            {"punto_id": "rn52_paso_jama", "tipo_corte": "total", "fecha": date(2024, 7, 1),
             "fecha_inicio": date(2024, 7, 1), "fecha_fin": date(2024, 7, 2), "causa": "nieve",
             "lado": "CL", "n_medios": 1, "fuentes": ["u3", "u4"]},
            {"punto_id": "rn52_paso_jama", "tipo_corte": "precaucion", "fecha": date(2024, 7, 9),
             "fecha_inicio": date(2024, 7, 9), "fecha_fin": date(2024, 7, 9), "causa": "otro",
             "lado": "AR", "n_medios": 1, "fuentes": ["u5"]},
            {"punto_id": "rn52_susques", "tipo_corte": "total", "fecha": date(2024, 7, 9),
             "fecha_inicio": date(2024, 7, 9), "fecha_fin": date(2024, 7, 9), "causa": "otro",
             "lado": None, "n_medios": 1, "fuentes": ["u6"]},
        ]
    )  # fmt: skip
    articulos = pd.DataFrame(
        [
            {"url": "u1", "fecha": date(2024, 6, 1), "titular": "Cerrado Jama", "bajada": ""},
            {"url": "u2", "fecha": date(2024, 6, 4), "titular": "Habilitaron Jama", "bajada": ""},
            {"url": "u3", "fecha": date(2024, 7, 1), "titular": "Cerrado Jama", "bajada": ""},
            {"url": "u4", "fecha": date(2024, 7, 2), "titular": "Sigue cerrado Jama", "bajada": ""},
        ]
    )  # fmt: skip
    out = cierres.exportar(eventos, articulos)
    assert [c["reapertura"] for c in out] == [True, False]
    assert out[0]["url_reapertura"] == "u2"
    meses = {k: (a, b) for k, a, b in cierres.por_mes_del_anio(out)}
    assert meses[6] == (1, 0)
    assert meses[7] == (1, 0)
    assert meses[1] == (0, 0)
    assert list(meses) == list(range(1, 13))
    anios = dict(cierres.por_anio(out, date(2026, 11, 15)))
    assert anios[2024] == 2
    assert anios[2016] == 0
    assert list(anios)[-1] == 2026
    d = cierres.duraciones(out)
    assert d == {
        "n": 1, "mediana": 3, "p75": 3, "min": 3, "max": 3, "total": 2, "administrativos": []
    }  # fmt: skip


def _c(inicio: str, fin: str, **kw: object) -> dict[str, object]:
    base = {
        "fecha_inicio": inicio, "fecha_fin": fin, "reapertura": True, "causa": "nieve",
        "tipo_corte": "total", "confianza": "alta", "administrativo": False,
    }  # fmt: skip
    return {**base, **kw}


def test_chart_counts_only_total_or_partial_without_low_confidence_stacked() -> None:
    lista = [
        _c("2024-06-01", "2024-06-02"),
        _c("2024-06-10", "2024-06-10", causa="otro", tipo_corte="parcial"),
        _c("2024-06-12", "2024-06-12", tipo_corte="desconocido"),
        _c("2024-06-15", "2024-06-15", confianza="baja"),
    ]
    meses = {k: (a, b) for k, a, b in cierres.por_mes_del_anio(lista)}
    assert meses[6] == (1, 1)
    assert len(cierres.contables(lista)) == 2


def test_desde_text_by_age() -> None:
    from corredor.jama_al_dia.estado import Actual, desde_txt

    def a(h: float) -> Actual:
        return Actual(None, NOW - timedelta(hours=h), False, False, None)

    assert desde_txt(a(0.5), NOW) == "desde las 11:47"
    assert desde_txt(a(5), NOW) == "desde hace 5 h"
    assert desde_txt(a(72), NOW) == "desde el 12/11"


def test_durations_leave_administrative_closures_out_and_say_dia() -> None:
    lista = [
        _c("2024-06-01", "2024-06-02"),
        _c("2024-06-05", "2024-06-06"),
        _c("2020-06-08", "2020-06-20", causa="otro", administrativo=True),
    ]
    d = cierres.duraciones(lista)
    assert (d["n"], d["mediana"], d["max"]) == (2, 1, 1)
    assert d["administrativos"] == [{"fecha_inicio": "2020-06-08", "dias": 12}]
    html = pagina._duracion(d)
    assert "La mitad de los cierres duró <strong>1 día o menos" in html
    assert "1 días" not in html
    assert "Rango" not in html  # the max chains several closures via dedup
    assert "Sobre 3 cierres de Jama en el catálogo, 2016–2026" in html
    assert "No incluye 1 cierre administrativo (junio 2020)." in html
    assert [c["fecha_inicio"] for c in cierres.mas_largos(lista, 1)] == ["2020-06-08"]


# ------------------------------------------------------------------ pronóstico 72 h
class FakeClient:
    def __init__(self, fail: bool = False, snow: float = 0.5) -> None:
        self.fail = fail
        self.snow = snow

    def forecast(self, point, hours, variables):  # type: ignore[no-untyped-def]
        if self.fail:
            raise OSError("sin red")
        t = pd.date_range("2026-11-08 12:00", periods=7 * 24 + hours + 1, freq="h")
        if "wind_gusts_10m" in variables:
            return pd.DataFrame({"time": t, "rafaga_kmh": 30.0})
        return pd.DataFrame({"time": t, "precipitacion_mm": 0.0, "nieve_cm": self.snow})

    def historical_forecast(self, point, start, end, model, variables):  # type: ignore[no-untyped-def]
        t = pd.date_range("2024-01-01", "2026-11-14 23:00", freq="h")
        rng = np.random.default_rng(0)
        if "wind_gusts_10m" in variables:
            return pd.DataFrame({"time": t, "rafaga_kmh": rng.uniform(20, 120, len(t))})
        snow = np.where(rng.random(len(t)) < 0.01, 1.0, 0.0)
        return pd.DataFrame({"time": t, "precipitacion_mm": 0.0, "nieve_cm": snow})


def _pt() -> CriticalPoint:
    return CriticalPoint(
        id="rn52_paso_jama", nombre="Paso de Jama", ruta="RN52", lat=-23.2, lon=-67.0
    )


def test_pronostico_72h_snow_and_gusts() -> None:
    now = datetime(2026, 11, 15, 12, 0)
    kw = {"model": "m", "clim_start": date(2024, 1, 1), "now_local": now, "alto": 90}
    (p,) = pronostico_72h(FakeClient(), [_pt()], **kw)  # type: ignore[arg-type]
    assert p.nieve.valor == 36.0
    assert p.nieve.nivel == "alto"
    assert p.rafaga.valor == 30.0
    assert p.rafaga.nivel == "normal"  # 72 h max of 20-120 random gusts is far above 30
    assert p.rafaga.percentil is not None
    (f,) = pronostico_72h(FakeClient(fail=True), [_pt()], **kw)  # type: ignore[arg-type]
    assert f.nieve.nivel is None
    assert f.rafaga.error


def test_cutoff_uses_unrounded_values() -> None:
    from corredor.jama_al_dia.pronostico import _nivel

    assert _nivel(5.0, 89.6, 90, True, 2021).nivel == "normal"
    small = _nivel(0.04, 95.0, 90, True, 2021)
    assert small.nivel == "alto"
    assert small.percentil == 95


def test_detail_without_climatology_keeps_the_value() -> None:
    m = Medida(12.5, None, None, "faltan horas de pronóstico o climatología", 2021)
    assert pagina._detalle(m, "Nieve", "cm") == "Nieve: 12,5 cm · sin climatología para comparar"


def test_snow_zero_has_no_percentile() -> None:
    now = datetime(2026, 11, 15, 12, 0)
    kw = {"model": "m", "clim_start": date(2024, 1, 1), "now_local": now, "alto": 90}
    (p,) = pronostico_72h(FakeClient(snow=0.0), [_pt()], **kw)  # type: ignore[arg-type]
    assert p.nieve == Medida(0.0, None, "normal", desde=2024)
    html = pagina._pronostico([p], NOW)
    assert "Nieve: no se espera" in html
    assert "Nieve: no se espera" in html
    assert "percentil" not in html.split("<details>")[0]


def test_percentiles_compare_72h_sums_and_maxima() -> None:
    class Flat(FakeClient):
        def historical_forecast(self, point, start, end, model, variables):  # type: ignore[no-untyped-def]
            t = pd.date_range("2024-01-01", "2026-11-14 23:00", freq="h")
            if "wind_gusts_10m" in variables:
                return pd.DataFrame({"time": t, "rafaga_kmh": 30.0})
            return pd.DataFrame({"time": t, "precipitacion_mm": 0.0, "nieve_cm": 0.5})

    now = datetime(2026, 11, 15, 12, 0)
    kw = {"model": "m", "clim_start": date(2024, 1, 1), "now_local": now, "alto": 90}
    (p,) = pronostico_72h(Flat(), [_pt()], **kw)  # type: ignore[arg-type]
    # forecast 72 h sum (36 cm) and max (30 km/h) equal every climatology value: mid-rank 50
    assert (p.nieve.valor, p.nieve.percentil) == (36.0, 50)
    assert (p.rafaga.valor, p.rafaga.percentil) == (30.0, 50)
    t = pd.date_range("2025-01-01", "2025-01-31 23:00", freq="h")
    g = pd.Series(50.0, index=range(len(t)))
    g[24 * 10 + 5] = 100.0  # one gust on Jan 11
    clim = climatologia_rafagas(pd.DataFrame({"time": t, "rafaga_kmh": g}))
    assert int((clim["DJF"] == 100.0).sum()) == 3  # windows ending Jan 11, 12, 13


def _p(nombre: str, nieve: str | None, rafaga: str | None, cm: float) -> Pronostico72:
    return Pronostico72(
        nombre, nombre, "2026-11-18 12:00",
        Medida(cm, 95 if nieve == "alto" else 40, nieve, desde=2021),
        Medida(80.0, 95 if rafaga == "alto" else 40, rafaga, desde=2021),
    )  # fmt: skip


def test_banner_only_when_both_high_and_higher_point_shown() -> None:
    both, one = _p("CH-27", "alto", "alto", 12.0), _p("Jama", "alto", "normal", 5.0)
    assert banner(both)
    assert not banner(one)
    assert not banner(_p("x", "normal", "alto", 1.0))
    assert elegir([one, both]) is both
    html = pagina._pronostico([one, both], NOW)
    assert "Se pronostican nieve y viento fuerte en Jama" in html
    assert "Punto: CH-27" in html
    assert "esta época desde 2021" in html
    assert "Se pronostican" not in pagina._pronostico([one], NOW)
    assert "Esto no es un pronóstico de cierre." in html
    assert "Alto = dentro del 10 % más alto para esta época, según el mismo modelo." in html


# ------------------------------------------------------------------ página
def test_page_escapes_and_has_required_text() -> None:
    evil = "<script>alert(1)</script>"
    snaps = [ar(NOW), cl(NOW, evil)]
    a, c = actual(serie(snaps, "AR"), NOW), actual(serie(snaps, "CL"), NOW)
    datos = pagina.Datos(
        now=NOW, ar=a, cl=c, bloques={"AR": bloques(serie(snaps, "AR"), NOW)},
        por_mes_anio=[(1, 2, 1), (2, 0, 0)], por_anio=[(2016, 3)],
        duraciones={"n": 3, "mediana": 2, "min": 0, "max": 9, "total": 5}, pronostico=[],
        url_telegram='https://t.me/x"><script>', url_plan_flotas="",
    )  # fmt: skip
    html = pagina.index(datos)
    assert "<script>" not in html
    assert "Content-Security-Policy" in html
    assert "ABIERTO" in html
    assert "RESTRINGIDO" in html
    assert "Resolución: 1 h" in html
    assert pagina.NOTA_PRENSA in html
    assert "n = 3" in html
    assert html.count("Recibí los avisos por Telegram") == 2  # under the status and in the footer
    assert "Anotate" not in html  # no link configured → no button
    assert "Por año: 2016 3" in html
    assert "probabilidad" not in html.lower()
    t = pagina.traccion(NOW, 1234, NOW, None, None)
    assert "1.234" in t
    assert "— <span" in t
    assert "todavía sin dato" in t
    t2 = pagina.traccion(
        NOW, 3, NOW, 0, "2026-11-15",
        serie_suscriptores=[("2026-11-14", 1), ("2026-11-15", 3)], canal_desde="2026-11-14",
        url_telegram="https://t.me/x", url_plan_flotas="https://forms.gle/y",
    )  # fmt: skip
    assert "Contamos desde el 14/11/2026" in t2
    assert "actualizado a mano el 15/11/2026" in t2
    assert t2.count('class="mini"') == 2
    assert "14/11 → 15/11" in t2
    assert "Recibí los avisos por Telegram" in t2
    assert "plan de empresas" in t2
    assert "todavía sin dato" not in t2

import json
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import httpx
import numpy as np
import pandas as pd
import pytest
import respx

from corredor.jama_al_dia import cierres, pagina
from corredor.jama_al_dia.estado import actual, bloques, estado_ar, estado_cl, horas, serie
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


def cl(ts: datetime, trans: str = "TRÁNSITO SIN RESTRICCIÓN", **extra: object) -> JamaEstado:
    rec = {"TRANSITABILIDAD": trans, "FECHA": 1794212069000, "HORA": 28800000, **extra}
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
    e = estado_cl(cl(NOW))
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
    assert "Chile: CERRADO" in msg
    assert "Argentina: ABIERTO" in msg
    assert PIE in msg
    assert url in msg
    assert "MOP Chile" in msg
    assert "parte 2026-11-09 08:00" in msg
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
    assert "resumen" in msgs[0]


def test_test_post(tmp_path: Path, tg: respx.MockRouter) -> None:
    a, c = _actuales()
    notificar(TelegramAPI(TOKEN, CHAT), a, c, tmp_path / "t.json", NOW, url="", prueba=True)
    (msg,) = _sent(tg)
    assert "prueba" in msg
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
    meses = dict(cierres.por_mes(out, date(2026, 11, 15)))
    assert meses["2024-06"] == 1
    assert meses["2024-07"] == 1
    assert meses["2016-01"] == 0
    assert list(meses)[-1] == "2026-11"
    d = cierres.duraciones(out)
    assert d == {"n": 1, "mediana": 3, "min": 3, "max": 3, "total": 2}


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


def test_snow_zero_has_no_percentile() -> None:
    now = datetime(2026, 11, 15, 12, 0)
    kw = {"model": "m", "clim_start": date(2024, 1, 1), "now_local": now, "alto": 90}
    (p,) = pronostico_72h(FakeClient(snow=0.0), [_pt()], **kw)  # type: ignore[arg-type]
    assert p.nieve == Medida(0.0, None, "normal", desde=2024)
    html = pagina._pronostico([p], NOW)
    assert "Nieve: sin nieve pronosticada" in html
    assert html.count("más que el") == 1  # only the gusts line


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


# ------------------------------------------------------------------ página
def test_page_escapes_and_has_required_text() -> None:
    evil = "<script>alert(1)</script>"
    snaps = [ar(NOW), cl(NOW, evil)]
    a, c = actual(serie(snaps, "AR"), NOW), actual(serie(snaps, "CL"), NOW)
    datos = pagina.Datos(
        now=NOW, ar=a, cl=c, bloques={"AR": bloques(serie(snaps, "AR"), NOW)},
        por_mes=[("2016-01", 2), ("2016-02", 0)],
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
    assert "Seguir en Telegram" in html
    assert "Plan Flotas" not in html  # no link configured → no button
    assert "probabilidad" not in html.lower()
    t = pagina.traccion(NOW, 1234, NOW, None, None)
    assert "1.234" in t
    assert "sin dato" in t

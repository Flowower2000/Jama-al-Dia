"""Telegram channel: post only when the combined AR/CL state changes, plus a daily summary.

The bot token goes in the API URL path, so it never reaches a log: httpx request logging
is silenced and errors are re-raised with only the method and HTTP status. The last posted
state lives in a small JSON file on the `data-snapshots` branch.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

import httpx

from corredor.jama_al_dia.estado import VIEJO, Actual, EstadoLado, cuando, desde_txt, local

logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)

API = "https://api.telegram.org"
PIE = "Fuente: Pasos Fronterizos (AR) · MOP (CL). No es un canal oficial."
ICONO = {"abierto": "🟢", "cerrado": "🔴", "restringido": "🟠"}
AVISO_OMITIDO = "telegram: sin secrets"  # pragma: allowlist secret


class TelegramError(RuntimeError):
    pass


class TelegramAPI:
    def __init__(self, token: str, chat_id: str, client: httpx.Client | None = None) -> None:
        self._token = token
        self.chat_id = chat_id
        self._client = client or httpx.Client(timeout=20.0)

    def _call(self, method: str, payload: dict[str, object]) -> object:
        try:
            r = self._client.post(f"{API}/bot{self._token}/{method}", json=payload)
        except httpx.HTTPError as exc:
            raise TelegramError(f"telegram {method}: {type(exc).__name__}") from None
        try:
            data = r.json()
        except ValueError:
            data = {}
        if r.status_code != 200 or not isinstance(data, dict) or not data.get("ok"):
            desc = data.get("description", "") if isinstance(data, dict) else ""
            raise TelegramError(f"telegram {method}: HTTP {r.status_code} {str(desc)[:120]}")
        return data.get("result")

    def send_message(self, text: str) -> None:
        self._call(
            "sendMessage",
            {"chat_id": self.chat_id, "text": text, "disable_web_page_preview": True},
        )

    def member_count(self) -> int:
        n = self._call("getChatMemberCount", {"chat_id": self.chat_id})
        if not isinstance(n, int):
            raise TelegramError("telegram getChatMemberCount: respuesta inesperada")
        return n

    def close(self) -> None:
        self._client.close()


@dataclass
class Publicado:
    clave: str | None = None
    publicado_at: str | None = None
    resumen_fecha: str | None = None
    suscriptores: int | None = None
    suscriptores_at: str | None = None
    suscriptores_dia: dict[str, int] | None = None  # local date → last count of that day

    @classmethod
    def load(cls, path: Path) -> Publicado:
        text = path.read_text(encoding="utf-8").strip() if path.exists() else ""
        if not text:
            return cls()
        data = json.loads(text)
        return cls(**{k: data.get(k) for k in cls.__dataclass_fields__})

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=1) + "\n", "utf-8")


def _lado_clave(a: Actual, avisar_horario: bool) -> str | None:
    e = a.ultimo
    if e is None or e.estado is None or a.viejo:
        return None  # stale data never changes the posted state
    if e.estado == "cerrado" and e.por_horario and not avisar_horario:
        return None  # nightly schedule closure: keep the previous value (no post either way)
    return e.estado


def clave(ar: Actual, cl: Actual, previa: str | None, avisar_horario: bool) -> str | None:
    """Combined state key; a side without data keeps its previous value (no post on outages)."""
    prev = dict(p.split("=", 1) for p in previa.split(";")) if previa else {}
    partes = {
        "AR": _lado_clave(ar, avisar_horario) or prev.get("AR"),
        "CL": _lado_clave(cl, avisar_horario) or prev.get("CL"),
    }
    if not any(partes.values()):
        return None
    return ";".join(f"{k}={v or 'sin_dato'}" for k, v in partes.items())


def _cambio_real(previa: str | None, nueva: str) -> bool:
    """A side going from one known state to another (sin_dato → known is just filling in)."""
    if previa is None:
        return False
    prev = dict(p.split("=", 1) for p in previa.split(";"))
    new = dict(p.split("=", 1) for p in nueva.split(";"))
    return any(
        prev.get(k, "sin_dato") != "sin_dato" and v != "sin_dato" and prev.get(k) != v
        for k, v in new.items()
    )


def _linea(nombre: str, a: Actual, now: datetime) -> str:
    """'🟢 Jama — Argentina ABIERTO desde las 14:46', '🟡 Chile: sin parte nuevo desde …'."""
    e: EstadoLado | None = a.ultimo
    if e is None or e.estado is None:
        return f"⚪ {nombre} sin dato"
    t = e.oficial_dt
    if a.parte_viejo and t is not None and now - e.fetched_at <= VIEJO:
        return f"🟡 {nombre} sin parte nuevo desde el {t:%d/%m} (último: {e.nombre_estado})"
    if a.viejo:
        return (
            f"🟡 {nombre} sin dato reciente "
            f"(último: {e.nombre_estado}, {cuando(e.fetched_at, now)})"
        )
    if e.clase == "horario":
        return f"⚪ {nombre} fuera de horario" + (f", abre a las {e.abre}" if e.abre else "")
    txt = f"{ICONO.get(e.clase or '', '⚪')} {nombre} {e.nombre_estado.upper()}"
    if a.desde is not None:
        txt += f" {desde_txt(a, now)}"
    return txt


def mensaje(ar: Actual, cl: Actual, now: datetime, url: str, *, prueba: bool = False) -> str:
    """At most 4 lines: Argentina, Chile, source, link."""
    primera = _linea("Jama — Argentina", ar, now)
    if prueba:
        primera = f"[Prueba] {primera}"
    partes = [primera, _linea("Chile:", cl, now), PIE]
    if url:
        partes.append(url)
    return "\n".join(partes)


def notificar(
    api: TelegramAPI | None,
    ar: Actual,
    cl: Actual,
    estado_path: Path,
    now: datetime,
    *,
    url: str,
    hora_resumen: int = 8,
    avisar_horario: bool = False,
    prueba: bool = False,
) -> list[str]:
    """Post what is due and update the state file; returns what was done (for the log)."""
    if api is None:
        log.info(AVISO_OMITIDO)
        return [AVISO_OMITIDO]
    pub = Publicado.load(estado_path)
    hechos: list[str] = []
    try:
        _publicar(api, pub, hechos, ar, cl, now, url, hora_resumen, avisar_horario, prueba)
    finally:
        pub.save(estado_path)  # whatever was posted is recorded, even if a later call fails
    return hechos


def _publicar(
    api: TelegramAPI,
    pub: Publicado,
    hechos: list[str],
    ar: Actual,
    cl: Actual,
    now: datetime,
    url: str,
    hora_resumen: int,
    avisar_horario: bool,
    prueba: bool,
) -> None:
    loc = local(now)
    nueva = clave(ar, cl, pub.clave, avisar_horario)
    if prueba:
        api.send_message(mensaje(ar, cl, now, url, prueba=True))
        hechos.append("prueba")
    if nueva is not None and nueva != pub.clave:
        if _cambio_real(pub.clave, nueva):
            api.send_message(mensaje(ar, cl, now, url))
            hechos.append("cambio")
        else:
            hechos.append("estado inicial guardado")
        pub.clave, pub.publicado_at = nueva, now.isoformat()
    hoy = loc.date().isoformat()
    if loc.hour == hora_resumen and pub.resumen_fecha != hoy:
        if "cambio" not in hechos:  # same text: the change post doubles as the summary
            api.send_message(mensaje(ar, cl, now, url))
        pub.resumen_fecha = hoy
        hechos.append("resumen")
    try:
        pub.suscriptores, pub.suscriptores_at = api.member_count(), now.isoformat()
        pub.suscriptores_dia = {**(pub.suscriptores_dia or {}), hoy: pub.suscriptores}
        hechos.append("suscriptores")
    except TelegramError as exc:
        hechos.append(str(exc))

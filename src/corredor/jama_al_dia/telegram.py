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

from corredor.jama_al_dia.estado import Actual, EstadoLado, horas, local

logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)

API = "https://api.telegram.org"
PIE = "Fuente: partes oficiales de Argentina y Chile. No es un canal oficial."
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

    @classmethod
    def load(cls, path: Path) -> Publicado:
        if not path.exists():
            return cls()
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(**{k: data.get(k) for k in cls.__dataclass_fields__})

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(self), ensure_ascii=False, indent=1) + "\n", "utf-8")


def _lado_clave(a: Actual, avisar_horario: bool) -> str | None:
    e = a.ultimo
    if e is None or e.estado is None:
        return None
    if e.estado == "cerrado" and e.por_horario and not avisar_horario:
        return "abierto"
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


def _linea(nombre: str, a: Actual, now: datetime) -> str:
    e: EstadoLado | None = a.ultimo
    if e is None or e.estado is None:
        return f"{nombre}: sin dato"
    txt = e.estado.upper() + (" (fuera de horario)" if e.por_horario else "")
    if a.desde is not None:
        h = horas(a.desde, now)
        txt += f", desde hace {'al menos ' if a.desde_al_menos else ''}{h} h"
    oficial = f" — parte {e.hora_oficial}" if e.hora_oficial else ""
    viejo = " (dato viejo)" if a.viejo else ""
    return f"{nombre}: {txt}{viejo}\n  {e.fuente}{oficial}"


def mensaje(titulo: str, ar: Actual, cl: Actual, now: datetime, url: str) -> str:
    partes = [
        titulo,
        _linea("🇦🇷 Argentina", ar, now),
        _linea("🇨🇱 Chile", cl, now),
        "Resolución: 1 h (consultamos cada hora).",
    ]
    if url:
        partes.append(url)
    partes.append(PIE)
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
    hechos = []
    loc = local(now)
    nueva = clave(ar, cl, pub.clave, avisar_horario)
    if prueba:
        api.send_message(mensaje("Paso de Jama — mensaje de prueba", ar, cl, now, url))
        hechos.append("prueba")
    if nueva is not None and nueva != pub.clave:
        if pub.clave is not None:
            api.send_message(mensaje("Paso de Jama — cambió el estado", ar, cl, now, url))
            hechos.append("cambio")
        else:
            hechos.append("estado inicial guardado")
        pub.clave, pub.publicado_at = nueva, now.isoformat()
    hoy = loc.date().isoformat()
    if loc.hour == hora_resumen and pub.resumen_fecha != hoy:
        api.send_message(mensaje("Paso de Jama — resumen de las 8", ar, cl, now, url))
        pub.resumen_fecha = hoy
        hechos.append("resumen")
    try:
        pub.suscriptores, pub.suscriptores_at = api.member_count(), now.isoformat()
        hechos.append("suscriptores")
    except TelegramError as exc:
        hechos.append(str(exc))
    pub.save(estado_path)
    return hechos

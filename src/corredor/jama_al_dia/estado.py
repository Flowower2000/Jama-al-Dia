"""Official Paso de Jama status per side, normalized from the raw snapshots.

AR = argentina.gob.ar (`estado_prioridad`, `estado_vialidad`), CL = MOP Chile
(`TRANSITABILIDAD`, `HABILITADO`). Only allowlisted fields are read (see sources/jama.py);
an unknown value never becomes "abierto".
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, time, timedelta
from typing import Any, Literal

from corredor.models import JamaEstado
from corredor.tablero.bundle import LOCAL_OFFSET, jama_records

Lado = Literal["AR", "CL"]
Estado = Literal["abierto", "cerrado", "restringido"]
FUENTE_LADO: dict[str, Lado] = {"argentina_gob_ar": "AR", "mop_cl": "CL"}
NOMBRE_FUENTE: dict[Lado, str] = {
    "AR": "argentina.gob.ar (Pasos fronterizos)",
    "CL": "MOP Chile (Unidad de Pasos Fronterizos)",
}
# Until 2026-11-15 snapshots were taken every 3 h: a state is carried that long, never more.
MAX_HUECO = timedelta(hours=3)
VIEJO = timedelta(hours=3)
_HORARIO = re.compile(r"^\s*(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})\s*$")


@dataclass(frozen=True)
class EstadoLado:
    lado: Lado
    fetched_at: datetime
    estado: Estado | None
    por_horario: bool = False
    hora_oficial: str | None = None
    horario: str | None = None
    detalle: tuple[str, ...] = ()
    error: str | None = None

    @property
    def fuente(self) -> str:
        return NOMBRE_FUENTE[self.lado]


def local(ts: datetime) -> datetime:
    """Argentina local time (naive), Jujuy is UTC-3 all year."""
    return (ts.astimezone(UTC) + LOCAL_OFFSET).replace(tzinfo=None)


def _up(v: object) -> str:
    return str(v).strip().upper() if v is not None else ""


def _fuera_de_horario(horario: str, cuando: datetime) -> bool:
    m = _HORARIO.match(horario)
    if not m:
        return False
    h1, m1, h2, m2 = (int(x) for x in m.groups())
    if not (h1 < 24 and h2 < 24 and m1 < 60 and m2 < 60):
        return False
    t, a, b = cuando.time(), time(h1, m1), time(h2, m2)
    return not (a <= t < b) if a <= b else (b <= t < a)


def estado_ar(snap: JamaEstado) -> EstadoLado:
    recs = jama_records(snap)
    if snap.error or not recs:
        return EstadoLado("AR", snap.fetched_at, None, error=snap.error or "sin registros")
    r = recs[0]
    prioridad, vialidad = _up(r.get("estado_prioridad")), _up(r.get("estado_vialidad"))
    horario = str(r["fecha_schema"]) if r.get("fecha_schema") else None
    oficial = str(r["fecha_hora_consulta"])[:16] if r.get("fecha_hora_consulta") else None
    estado: Estado | None = None
    por_horario = False
    closed = ("CERRAD", "INHABILITAD", "CORTAD", "INTRANSITABLE", "SUSPENDID")
    road_ok = not vialidad or vialidad.startswith("HABILITAD")
    if any(w in vialidad for w in closed):
        estado = "cerrado"
    elif prioridad == "CERRADO":
        estado = "cerrado"
        por_horario = road_ok and bool(
            horario and _fuera_de_horario(horario, local(snap.fetched_at))
        )
    elif not road_ok:
        estado = "restringido"
    elif prioridad == "ABIERTO":
        estado = "abierto"
    detalle = tuple(
        f"{k}: {v}"
        for k, v in (("Estado", r.get("estado_prioridad")), ("Vialidad", r.get("estado_vialidad")))
        if v
    )
    return EstadoLado(
        "AR", snap.fetched_at, estado, por_horario, oficial, horario, detalle,
        None if estado else "estado desconocido",
    )  # fmt: skip


def estado_cl(snap: JamaEstado) -> EstadoLado:
    recs = jama_records(snap)
    if snap.error or not recs:
        return EstadoLado("CL", snap.fetched_at, None, error=snap.error or "sin registros")
    r = recs[0]
    trans, habil = _up(r.get("TRANSITABILIDAD")), _up(r.get("HABILITADO"))
    estado: Estado | None = None
    if habil in {"NO", "FALSE", "0"} or any(
        w in trans for w in ("CERRAD", "SUSPENDID", "NO HABILITAD", "INTRANSITABLE")
    ):
        estado = "cerrado"
    elif "SIN RESTRICCI" in trans:
        estado = "abierto"
    elif trans:
        estado = "restringido"
    oficial = None
    if r.get("FECHA"):
        oficial = f"{r['FECHA']} {r['HORA']}" if r.get("HORA") else str(r["FECHA"])
    horario = f"{r['ADESDE']}-{r['AHASTA']}" if r.get("ADESDE") and r.get("AHASTA") else None
    detalle = tuple(
        f"{label}: {r[k]}"
        for k, label in (
            ("TRANSITABILIDAD", "Tránsito"),
            ("RESTRICCIONES", "Restricciones"),
            ("CADENAS", "Cadenas"),
            ("ESTADOCALZADA", "Calzada"),
        )
        if r.get(k)
    )
    return EstadoLado(
        "CL", snap.fetched_at, estado, False, oficial, horario, detalle,
        None if estado else "estado desconocido",
    )  # fmt: skip


def serie(snaps: Sequence[JamaEstado], lado: Lado) -> list[EstadoLado]:
    """Every snapshot of one side, oldest first (failed ones keep estado=None)."""
    parse = estado_ar if lado == "AR" else estado_cl
    return [
        parse(s)
        for s in sorted(snaps, key=lambda s: s.fetched_at)
        if FUENTE_LADO.get(s.fuente) == lado
    ]


@dataclass(frozen=True)
class Actual:
    ultimo: EstadoLado | None  # last snapshot with a known state
    desde: datetime | None  # first snapshot of the current run of that state
    desde_al_menos: bool  # the run starts at the first snapshot we have
    viejo: bool  # last known state older than VIEJO
    ultimo_intento: EstadoLado | None


def actual(s: Sequence[EstadoLado], now: datetime) -> Actual:
    validos = [e for e in s if e.estado is not None]
    if not validos:
        return Actual(None, None, False, True, s[-1] if s else None)
    last = validos[-1]
    i = len(validos) - 1
    while (
        i > 0
        and validos[i - 1].estado == last.estado
        and (validos[i].fetched_at - validos[i - 1].fetched_at <= MAX_HUECO + timedelta(minutes=30))
    ):
        i -= 1
    return Actual(last, validos[i].fetched_at, i == 0, now - last.fetched_at > VIEJO, s[-1])


def horas(desde: datetime, now: datetime) -> int:
    """Whole hours (snapshot resolution: 1 h)."""
    return max(0, int((now - desde).total_seconds() // 3600))


def bloques(s: Sequence[EstadoLado], now: datetime, dias: int = 7) -> list[dict[str, Any]]:
    """One row per local day (oldest first), 24 hourly cells: abierto/cerrado/restringido/None.

    A cell takes the last known state at the end of that hour if it is at most MAX_HUECO
    old; otherwise it is None ("sin dato").
    """
    validos = [e for e in s if e.estado is not None]
    hoy = local(now).replace(hour=0, minute=0, second=0, microsecond=0)
    ahora_local = local(now)
    out = []
    j = 0
    ultimo: EstadoLado | None = None
    for d in range(dias - 1, -1, -1):
        dia = hoy - timedelta(days=d)
        celdas: list[str | None] = []
        for h in range(24):
            fin = dia + timedelta(hours=h + 1)
            while j < len(validos) and local(validos[j].fetched_at) < fin:
                ultimo = validos[j]
                j += 1
            inicio = fin - timedelta(hours=1)
            if inicio > ahora_local:
                celdas.append("futuro")
            elif ultimo is not None and fin - local(ultimo.fetched_at) <= MAX_HUECO + timedelta(
                hours=1
            ):
                celdas.append(ultimo.estado)
            else:
                celdas.append(None)
        out.append({"fecha": dia.date().isoformat(), "celdas": celdas})
    return out

"""Paso de Jama closures from the catalog (events at `rn52_paso_jama`), for the public page.

`exportar` reads the pipeline tables and writes `assets/jama/cierres.json` (metadata only:
dates, cause, side, closure type, outlet count). Duration is shown only where the end is
known: the event's last day has a reopening article (`reapertura`).
"""

from __future__ import annotations

import statistics
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import date
from typing import Any

import pandas as pd

from corredor.extraction.patterns import is_reopening

PUNTO = "rn52_paso_jama"
DESDE = date(2016, 1, 1)


def _d(v: Any) -> date | None:
    if v is None or (isinstance(v, float) and pd.isna(v)) or v is pd.NaT:
        return None
    return pd.Timestamp(v).date()


def exportar(eventos: pd.DataFrame, articulos: pd.DataFrame) -> list[dict[str, Any]]:
    by_url: dict[str, tuple[date | None, str]] = {
        str(r["url"]): (_d(r["fecha"]), f"{r['titular'] or ''}. {r['bajada'] or ''}")
        for r in articulos.to_dict("records")
    }
    out = []
    jama = eventos[(eventos["punto_id"] == PUNTO) & (eventos["tipo_corte"] != "precaucion")]
    rows: list[dict[Any, Any]] = jama.sort_values("fecha_inicio").to_dict("records")
    for e in rows:
        inicio = _d(e["fecha_inicio"]) or _d(e["fecha"])
        fin = _d(e["fecha_fin"])
        if inicio is None:
            continue
        urls = [str(u) for u in e["fuentes"]] if e["fuentes"] is not None else []
        reapertura = fin is not None and any(
            f == fin and is_reopening(t) for f, t in (by_url.get(u, (None, "")) for u in urls)
        )
        out.append(
            {
                "fecha_inicio": inicio.isoformat(),
                "fecha_fin": fin.isoformat() if fin else None,
                "reapertura": bool(reapertura),
                "causa": e["causa"],
                "lado": e["lado"],
                "tipo_corte": e["tipo_corte"],
                "n_medios": int(e["n_medios"]),
            }
        )
    return out


def por_mes(cierres: Sequence[Mapping[str, Any]], hasta: date) -> list[tuple[str, int]]:
    cuenta = Counter(str(c["fecha_inicio"])[:7] for c in cierres)
    meses, y, m = [], DESDE.year, DESDE.month
    while (y, m) <= (hasta.year, hasta.month):
        k = f"{y:04d}-{m:02d}"
        meses.append((k, cuenta.get(k, 0)))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return meses


def duraciones(cierres: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Days from first article to the reopening article (publication dates), known ends only."""
    dias = [
        (date.fromisoformat(c["fecha_fin"]) - date.fromisoformat(c["fecha_inicio"])).days
        for c in cierres
        if c.get("reapertura") and c.get("fecha_fin")
    ]
    if not dias:
        return {"n": 0, "mediana": None, "min": None, "max": None, "total": len(cierres)}
    return {
        "n": len(dias),
        "mediana": statistics.median(dias),
        "min": min(dias),
        "max": max(dias),
        "total": len(cierres),
    }

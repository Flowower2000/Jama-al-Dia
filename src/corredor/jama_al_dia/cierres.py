"""Paso de Jama closures from the catalog (events at `rn52_paso_jama`), for the public page.

`exportar` reads the pipeline tables and writes `assets/jama/cierres.json` (metadata only:
dates, cause, side, closure type, confidence, outlet count, first/reopening URLs). The page
counts only `total`/`parcial` closures without `confianza=baja` (`contables`). Duration is
shown only where the end is known (the event's last day has a reopening article,
`reapertura`); administrative closures (COVID etc.) are listed apart, not in the median.
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
        reabre = [
            u
            for u in urls
            if fin is not None
            and by_url.get(u, (None, ""))[0] == fin
            and is_reopening(by_url[u][1])
        ]
        notas = str(e.get("notas") or "")
        out.append(
            {
                "fecha_inicio": inicio.isoformat(),
                "fecha_fin": fin.isoformat() if fin else None,
                "reapertura": bool(reabre),
                "causa": e["causa"],
                "lado": e["lado"],
                "tipo_corte": e["tipo_corte"],
                "n_medios": int(e["n_medios"]),
                "confianza": e.get("confianza"),
                "administrativo": "administrativo" in notas,
                "url_inicio": urls[0] if urls else None,
                "url_reapertura": reabre[0] if reabre else None,
            }
        )
    return out


def contables(cierres: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    """Total or partial closures, without low-confidence events."""
    return [
        c
        for c in cierres
        if c.get("tipo_corte") in {"total", "parcial"} and c.get("confianza") != "baja"
    ]


def por_mes(cierres: Sequence[Mapping[str, Any]], hasta: date) -> list[tuple[str, int, int]]:
    """(AAAA-MM, nieve, otras causas) per month from DESDE, counting `contables` only."""
    nieve = Counter(str(c["fecha_inicio"])[:7] for c in contables(cierres) if c["causa"] == "nieve")
    otros = Counter(str(c["fecha_inicio"])[:7] for c in contables(cierres) if c["causa"] != "nieve")
    meses, y, m = [], DESDE.year, DESDE.month
    while (y, m) <= (hasta.year, hasta.month):
        k = f"{y:04d}-{m:02d}"
        meses.append((k, nieve.get(k, 0), otros.get(k, 0)))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return meses


def duraciones(cierres: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Days from first article to the reopening article (publication dates), known ends only,
    on `contables`; administrative closures are returned apart and left out of the median."""
    base = contables(cierres)

    def dias(c: Mapping[str, Any]) -> int:
        return (date.fromisoformat(c["fecha_fin"]) - date.fromisoformat(c["fecha_inicio"])).days

    conocidos = [c for c in base if c.get("reapertura") and c.get("fecha_fin")]
    adm = [
        {"fecha_inicio": c["fecha_inicio"], "dias": dias(c)}
        for c in conocidos
        if c.get("administrativo")
    ]
    ds = [dias(c) for c in conocidos if not c.get("administrativo")]
    out: dict[str, Any] = {"total": len(base), "administrativos": adm}
    if not ds:
        return {**out, "n": 0, "mediana": None, "min": None, "max": None}
    return {**out, "n": len(ds), "mediana": statistics.median(ds), "min": min(ds), "max": max(ds)}


def mas_largos(cierres: Sequence[Mapping[str, Any]], n: int = 5) -> list[Mapping[str, Any]]:
    conocidos = [c for c in contables(cierres) if c.get("reapertura") and c.get("fecha_fin")]
    return sorted(
        conocidos,
        key=lambda c: date.fromisoformat(c["fecha_fin"]) - date.fromisoformat(c["fecha_inicio"]),
        reverse=True,
    )[:n]

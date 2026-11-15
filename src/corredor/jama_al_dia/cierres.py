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
                "url_inicio": next(
                    (u for u in urls if by_url.get(u, (None, ""))[0] == inicio),
                    urls[0] if urls else None,
                ),
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


def por_mes_del_anio(cierres: Sequence[Mapping[str, Any]]) -> list[tuple[int, int, int]]:
    """(month 1–12, nieve, otras causas) summed over every year, `contables` only."""
    out = []
    base = contables(cierres)
    for m in range(1, 13):
        delmes = [c for c in base if int(str(c["fecha_inicio"])[5:7]) == m]
        nieve = sum(1 for c in delmes if c["causa"] == "nieve")
        out.append((m, nieve, len(delmes) - nieve))
    return out


def por_anio(cierres: Sequence[Mapping[str, Any]], hasta: date) -> list[tuple[int, int]]:
    cuenta = Counter(int(str(c["fecha_inicio"])[:4]) for c in contables(cierres))
    return [(y, cuenta.get(y, 0)) for y in range(DESDE.year, hasta.year + 1)]


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

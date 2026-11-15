"""72 h snowfall and wind gusts at Jama and CH-27, each as a percentile of THE SAME forecast
model's climatology (Historical Forecast API). Descriptive only: not a validated threshold
and not a closure forecast."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Protocol

import numpy as np
import pandas as pd

from corredor.calibration.thresholds import percentile_of, season
from corredor.models import CriticalPoint
from corredor.tablero.forecast import Climatologia, _motivo, features_at
from corredor.weather.features import _regular_hourly
from corredor.weather.openmeteo import GUST_VARIABLES, HOURLY_VARIABLES

HORAS = 72
NIEVE = "nieve_72h_cm"
RAFAGA = "rafaga_kmh"


class Client(Protocol):
    def forecast(
        self, point: CriticalPoint, hours: int, variables: Mapping[str, str] = ...
    ) -> pd.DataFrame: ...

    def historical_forecast(
        self,
        point: CriticalPoint,
        start: date,
        end: date,
        model: str,
        variables: Mapping[str, str] = ...,
    ) -> pd.DataFrame: ...


@dataclass(frozen=True)
class Medida:
    valor: float | None
    percentil: float | None
    nivel: str | None  # "alto" | "normal" | None (sin dato)
    error: str | None = None


@dataclass(frozen=True)
class Pronostico72:
    punto_id: str
    nombre: str
    hasta: str | None
    nieve: Medida
    rafaga: Medida


def _nivel(valor: float | None, pct: float | None, alto: float, need_positive: bool) -> Medida:
    v = None if valor is None or np.isnan(valor) else round(float(valor), 1)
    p = None if pct is None else round(pct)
    if v is None or p is None:
        return Medida(v, p, None, "faltan horas de pronóstico o climatología")
    es_alto = p >= alto and (v > 0 or not need_positive)
    return Medida(v, p, "alto" if es_alto else "normal")


def climatologia_rafagas(hourly: pd.DataFrame) -> dict[str, np.ndarray]:
    """Per season: sorted daily values of the max gust over the 72 h ending at 23:00."""
    reg = _regular_hourly(hourly[["time", RAFAGA]])
    if reg.empty:
        return {}
    mx = reg[RAFAGA].rolling(HORAS, min_periods=HORAS).max()
    daily = mx[pd.DatetimeIndex(mx.index).hour == 23].dropna()
    out: dict[str, list[float]] = {}
    for ts, v in daily.items():
        out.setdefault(season(pd.Timestamp(str(ts)).month), []).append(float(v))
    return {k: np.sort(np.array(v)) for k, v in out.items()}


def _pct(clim: Mapping[str, np.ndarray], value: float, when: datetime) -> float | None:
    arr = clim.get(season(when.month))
    if arr is None or arr.size == 0 or np.isnan(value):
        return None
    return float(percentile_of(arr, np.array([value]))[0])


def pronostico_72h(
    client: Client,
    points: Sequence[CriticalPoint],
    *,
    model: str,
    clim_start: date,
    now_local: datetime,
    alto: float,
) -> list[Pronostico72]:
    from corredor.http import FetchError
    from corredor.weather.openmeteo import CallBudgetExceeded, OpenMeteoError

    errors = (FetchError, OpenMeteoError, CallBudgetExceeded, OSError, ValueError, KeyError)
    base = pd.Timestamp(now_local).floor("h")
    t = base + timedelta(hours=HORAS)
    clim_end = now_local.date() - timedelta(days=1)
    out = []
    for p in points:
        try:
            hourly = client.forecast(p, HORAS, HOURLY_VARIABLES)
            v = features_at(hourly, [t])[0][NIEVE]
            clim = Climatologia.from_hourly(
                client.historical_forecast(p, clim_start, clim_end, model, HOURLY_VARIABLES)
            )
            nieve = _nivel(v, clim.percentil(NIEVE, v, t.to_pydatetime()), alto, True)
        except errors as exc:
            nieve = Medida(None, None, None, _motivo(exc))
        try:
            g = client.forecast(p, HORAS, GUST_VARIABLES)
            win = g[(g["time"] > base) & (g["time"] <= t)][RAFAGA]
            gv = float(win.max()) if len(win) == HORAS and win.notna().all() else float("nan")
            gclim = climatologia_rafagas(
                client.historical_forecast(p, clim_start, clim_end, model, GUST_VARIABLES)
            )
            rafaga = _nivel(gv, _pct(gclim, gv, t.to_pydatetime()), alto, False)
        except errors as exc:
            rafaga = Medida(None, None, None, _motivo(exc))
        out.append(Pronostico72(p.id, p.nombre, t.strftime("%Y-%m-%d %H:%M"), nieve, rafaga))
    return out

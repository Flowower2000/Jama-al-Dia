"""Static HTML for "Jama al Día" (GitHub Pages): index.html and traccion/index.html.

No JavaScript. Every value goes through `html.escape`; the only inline CSS is the <style>
block, allowed by its sha256 hash in a Content-Security-Policy meta tag.
"""

from __future__ import annotations

import base64
import hashlib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any

from corredor.jama_al_dia.estado import Actual, horas, local
from corredor.jama_al_dia.pronostico import Medida, Pronostico72

ESTADO_TXT = {"abierto": "ABIERTO", "cerrado": "CERRADO", "restringido": "RESTRINGIDO"}
NOTA_PRENSA = "según prensa local; puede faltar algún cierre"
CSS = (Path(__file__).parent / "estilo.css").read_text(encoding="utf-8").strip()


def _sha(text: str) -> str:
    return "'sha256-" + base64.b64encode(hashlib.sha256(text.encode()).digest()).decode() + "'"


def csp() -> str:
    return (
        f"default-src 'none'; style-src {_sha(CSS)}; img-src 'self'; base-uri 'none'; "
        "form-action 'none'"
    )


def _doc(title: str, body: str) -> str:
    return (
        '<!doctype html><html lang="es-AR"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<meta http-equiv="Content-Security-Policy" content="{csp()}">'
        '<meta name="referrer" content="no-referrer">'
        f"<title>{escape(title)}</title><style>{CSS}</style></head><body><main>{body}</main>"
        "</body></html>\n"
    )


@dataclass
class Datos:
    now: datetime
    ar: Actual
    cl: Actual
    bloques: Mapping[str, list[dict[str, Any]]]
    por_mes: Sequence[tuple[str, int]]
    duraciones: Mapping[str, Any]
    pronostico: Sequence[Pronostico72]
    url_telegram: str = ""
    url_plan_flotas: str = ""
    catalogo_generado: str | None = None
    alto: float = 90
    extra: dict[str, Any] = field(default_factory=dict)


def _hhmm(ts: datetime) -> str:
    return local(ts).strftime("%d/%m %H:%M")


def _lado(nombre: str, a: Actual, now: datetime) -> str:
    e = a.ultimo
    if e is None or e.estado is None:
        motivo = a.ultimo_intento.error if a.ultimo_intento else "todavía no hay consultas"
        return (
            f'<div class="lado"><h3>{escape(nombre)}</h3><div class="big">SIN DATO</div>'
            f"<p>{escape(str(motivo))}</p></div>"
        )
    big = ESTADO_TXT[e.estado]
    rows = []
    if e.por_horario:
        rows.append(f"fuera de horario ({escape(e.horario or '')})")
    if a.desde is not None:
        h = horas(a.desde, now)
        rows.append(f"desde hace {'al menos ' if a.desde_al_menos else ''}{h} h")
    if e.hora_oficial:
        rows.append(f"parte oficial: {escape(e.hora_oficial)}")
    rows.append(f"consultado: {_hhmm(e.fetched_at)}")
    if a.viejo:
        rows.append(
            f"<strong>dato viejo: última consulta hace {horas(e.fetched_at, now)} h</strong>"
        )
    rows.append(escape(e.fuente))
    ps = "".join(f"<p>{r}</p>" for r in rows)
    return (
        f'<div class="lado {e.estado}"><h3>{escape(nombre)}</h3><div class="big">{big}</div>'
        f"{ps}</div>"
    )


def _dias(nombre: str, filas: Sequence[Mapping[str, Any]]) -> str:
    out = [f'<h3>{escape(nombre)}</h3><div class="dias">']
    for f in filas:
        d = str(f["fecha"])
        cells = "".join(
            f'<div class="c {escape(str(c))}"></div>' if c else '<div class="c"></div>'
            for c in f["celdas"]
        )
        out.append(f'<div class="dia"><span>{escape(d[8:10])}/{escape(d[5:7])}</span>{cells}</div>')
    out.append("</div>")
    return "".join(out)


def _grafico(por_mes: Sequence[tuple[str, int]]) -> str:
    if not por_mes:
        return "<p>Sin datos del catálogo.</p>"
    w, h, top, left = 640, 230, 12, 34
    bw = (w - left) / len(por_mes)
    mx = max((n for _, n in por_mes), default=0) or 1
    sc = (h - top - 30) / mx
    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Cierres de Jama por mes">']
    for k in range(0, mx + 1, max(1, mx // 3)):
        y = h - 30 - k * sc
        parts.append(f'<line class="lin" x1="{left}" x2="{w}" y1="{y:.1f}" y2="{y:.1f}"/>')
        parts.append(f'<text class="eje" x="0" y="{y + 6:.1f}">{k}</text>')
    for i, (mes, n) in enumerate(por_mes):
        x = left + i * bw
        if n:
            parts.append(
                f'<rect class="bar" x="{x:.1f}" y="{h - 30 - n * sc:.1f}" '
                f'width="{max(bw - 1, 1):.1f}" height="{n * sc:.1f}">'
                f"<title>{escape(mes)}: {n}</title></rect>"
            )
        if mes.endswith("-01") and int(mes[:4]) % 2 == 0:
            parts.append(f'<text class="eje" x="{x:.1f}" y="{h - 6}">{escape(mes[:4])}</text>')
    parts.append("</svg>")
    return "".join(parts)


def _duracion(d: Mapping[str, Any]) -> str:
    if not d.get("n"):
        return "<p>Ningún cierre del catálogo tiene fecha de reapertura conocida.</p>"
    med = d["mediana"]
    med_txt = f"{med:g}"
    return (
        f'<p><span class="num">{escape(med_txt)} días</span> de mediana</p>'
        f"<p>Rango: {d['min']} a {d['max']} días · n = {d['n']} cierres con reapertura conocida "
        f"(de {d['total']} cierres en el catálogo).</p>"
        '<p class="nota">Días entre la primera nota del cierre y la nota de reapertura (fechas de '
        "publicación). Solo cierres con una nota de reapertura en el catálogo; "
        f"{escape(NOTA_PRENSA)}.</p>"
    )


def _medida(titulo: str, m: Medida, unidad: str) -> str:
    if m.nivel is None or m.valor is None or m.percentil is None:
        motivo = escape(m.error or "no disponible")
        return f"<p><strong>{escape(titulo)}:</strong> sin dato ({motivo})</p>"
    return (
        f'<p><strong>{escape(titulo)}:</strong> <span class="{m.nivel}">{m.nivel.upper()}</span>'
        f"<br>{m.valor:g} {unidad} · percentil {m.percentil:g}</p>"
    )


def _pronostico(ps: Sequence[Pronostico72], alto: float) -> str:
    cards = []
    for p in ps:
        hasta = f'<p class="nota">próximas 72 h, hasta {escape(p.hasta)}</p>' if p.hasta else ""
        cards.append(
            f'<div class="np"><h3>{escape(p.nombre)}</h3>'
            + _medida("Nieve acumulada", p.nieve, "cm")
            + _medida("Ráfaga máxima", p.rafaga, "km/h")
            + hasta
            + "</div>"
        )
    return (
        f'<div class="nieve">{"".join(cards)}</div>'
        '<p class="nota">Percentil frente a la climatología del mismo modelo de pronóstico '
        "(Open-Meteo, pronósticos archivados desde 2022, misma estación del año). "
        f'"Alto" = percentil {alto:g} o más. Es descriptivo: no es un umbral validado. '
        "<strong>No es un pronóstico de cierre.</strong></p>"
    )


def index(d: Datos) -> str:
    botones = []
    if d.url_telegram:
        botones.append(
            f'<a class="btn" href="{escape(d.url_telegram)}" rel="noopener">Seguir en Telegram</a>'
        )
    if d.url_plan_flotas:
        botones.append(
            f'<a class="btn flotas" href="{escape(d.url_plan_flotas)}" rel="noopener">'
            "Plan Flotas — anotate</a>"
        )
    total = sum(n for _, n in d.por_mes)
    body = [
        "<header><h1>Jama al Día</h1>",
        '<p class="sub">Paso de Jama (RN 52 · CH-27). '
        f"Actualizado {_hhmm(d.now)} (hora argentina).</p>"
        "</header>",
        '<section><h2>Estado ahora</h2><div class="lados">',
        _lado("Argentina", d.ar, d.now),
        _lado("Chile", d.cl, d.now),
        '</div><p class="nota">Resolución: 1 h (consultamos los partes oficiales cada hora). '
        "Argentina marca el paso CERRADO fuera de su horario de atención.</p></section>",
    ]
    if botones:
        body.append(f'<section class="botones">{"".join(botones)}</section>')
    ley = (
        '<div class="ley"><span class="abierto">abierto</span><span class="cerrado">cerrado</span>'
        '<span class="restringido">restringido</span><span>sin dato</span></div>'
    )
    body += [
        "<section><h2>Últimos 7 días</h2>",
        _dias("Argentina", d.bloques.get("AR", [])),
        _dias("Chile", d.bloques.get("CL", [])),
        ley,
        '<p class="nota">Cada bloque = 1 hora (00 a 23). Hasta el 15/11 consultábamos cada 3 h: '
        "un estado se repite como máximo 3 h; si no, queda gris.</p></section>",
        "<section><h2>Cierres de Jama por mes, 2016–2026</h2>",
        _grafico(d.por_mes),
        f'<p class="nota">{total} cierres en el catálogo; {escape(NOTA_PRENSA)}.'
        + (f" Catálogo del {escape(d.catalogo_generado)}." if d.catalogo_generado else "")
        + "</p></section>",
        "<section><h2>Cuánto duran los cierres</h2>",
        _duracion(d.duraciones),
        "</section>",
        "<section><h2>Pronóstico de nieve y viento en Jama (72 h)</h2>",
        _pronostico(d.pronostico, d.alto),
        "</section>",
        "<footer><p>Fuente: partes oficiales de Argentina (argentina.gob.ar) y Chile (MOP). "
        "<strong>No es un canal oficial.</strong> Ante la duda, consultá a Gendarmería o "
        "Vialidad antes de viajar.</p><p>Cierres históricos: catálogo armado con prensa local de "
        "Jujuy (solo metadatos). Pronóstico: Open-Meteo (CC BY 4.0).</p>"
        '<p><a href="traccion/">Tracción</a> · '
        '<a href="https://github.com/emiliano-f/corredor-quebrada-puna">Código</a></p></footer>',
    ]
    return _doc("Jama al Día — estado del Paso de Jama", "".join(body))


def traccion(
    now: datetime,
    suscriptores: int | None,
    suscriptores_at: datetime | None,
    waitlist: int | None,
    waitlist_at: str | None,
) -> str:
    def card(titulo: str, n: int | None, cuando: str | None, origen: str) -> str:
        num = f"{n:,}".replace(",", ".") if n is not None else "sin dato"
        return (
            f'<section><h2>{escape(titulo)}</h2><p class="num">{escape(num)}</p>'
            f'<p class="nota">{escape(origen)}'
            + (f" · actualizado {escape(cuando)}" if cuando else "")
            + "</p></section>"
        )

    body = (
        "<header><h1>Tracción — Jama al Día</h1>"
        f'<p class="sub">Página generada {_hhmm(now)} (hora argentina).</p></header>'
        + card(
            "Suscriptores del canal de Telegram",
            suscriptores,
            _hhmm(suscriptores_at) if suscriptores_at else None,
            "Telegram Bot API (getChatMemberCount), cada hora",
        )
        + card("Inscriptos waitlist Plan Flotas", waitlist, waitlist_at, "carga manual")
        + '<footer><p><a href="../">Volver a Jama al Día</a></p></footer>'
    )
    return _doc("Tracción — Jama al Día", body)


def escribir(salida: Path, index_html: str, traccion_html: str) -> None:
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "index.html").write_text(index_html, encoding="utf-8")
    (salida / "traccion").mkdir(exist_ok=True)
    (salida / "traccion" / "index.html").write_text(traccion_html, encoding="utf-8")
    (salida / ".nojekyll").write_text("", encoding="utf-8")

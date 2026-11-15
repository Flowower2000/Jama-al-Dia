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

from corredor.jama_al_dia.estado import Actual, cuando, datos_de, horas
from corredor.jama_al_dia.pronostico import Medida, Pronostico72, banner, elegir

ESTADO_TXT = {"abierto": "ABIERTO", "cerrado": "CERRADO", "restringido": "RESTRINGIDO"}
MESES = ("Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic")
RELOJ = (
    '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="none" '
    'stroke="currentColor" stroke-width="2"/><path d="M12 6v6l4 2" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
)
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
    por_mes_anio: Sequence[tuple[int, int, int]]  # (mes 1–12, nieve, otros)
    por_anio: Sequence[tuple[int, int]]
    duraciones: Mapping[str, Any]
    pronostico: Sequence[Pronostico72]
    url_telegram: str = ""
    url_plan_flotas: str = ""
    catalogo_generado: str | None = None
    alto: float = 90
    extra: dict[str, Any] = field(default_factory=dict)


def _dias_txt(n: int) -> str:
    return f"{n} día" if n == 1 else f"{n} días"


def _fecha(iso: str) -> str:
    return f"{iso[8:10]}/{iso[5:7]}/{iso[:4]}" if len(iso) >= 10 else iso


def _ultimo_dato(a: Actual, now: datetime) -> str:
    e = a.ultimo
    if e is None:
        return "Último dato: sin datos"
    t = e.oficial_dt
    if a.parte_viejo and t is not None:
        return f"Último dato: {e.nombre_estado}, parte oficial del {t:%d/%m}"
    return f"Último dato: {e.nombre_estado}, {cuando(e.fetched_at, now)}"


def _lado(nombre: str, a: Actual, now: datetime) -> str:
    e = a.ultimo
    if e is None or e.estado is None:
        motivo = a.ultimo_intento.error if a.ultimo_intento else "todavía no hay consultas"
        return (
            f'<div class="lado"><h3>{escape(nombre)}</h3><div class="big">SIN DATO</div>'
            f"<p>{escape(str(motivo))}</p></div>"
        )
    rows = []
    if a.viejo:
        clase, big = "viejo", '<div class="big chico">Estado no confirmado</div>'
        rows.append(escape(_ultimo_dato(a, now)))
    elif e.clase == "horario":
        clase = "horario"
        big = f'<div class="big chico">{RELOJ}Cerrado por horario</div>'
        if e.abre:
            rows.append(f"Abre a las {escape(e.abre)}")
    else:
        clase, big = e.clase or "", f'<div class="big">{ESTADO_TXT[e.estado]}</div>'
        if a.desde is not None:
            h = horas(a.desde, now)
            rows.append(f"desde hace {'al menos ' if a.desde_al_menos else ''}{h} h")
    t = e.oficial_dt
    if t is not None:
        rows.append(
            f"Parte oficial del {t:%d/%m}" if a.parte_viejo else f"Parte oficial: {cuando(t, now)}"
        )
    rows.append(f"Consultado: {cuando(e.fetched_at, now)}")
    rows.append(escape(e.fuente))
    ps = "".join(f"<p>{r}</p>" for r in rows)
    return f'<div class="lado {clase}"><h3>{escape(nombre)}</h3>{big}{ps}</div>'


def _dias(nombre: str, filas: Sequence[Mapping[str, Any]]) -> str:
    ticks = "".join(f"<span>{h if h % 6 == 0 else ''}</span>" for h in range(24))
    out = [
        f'<h3>{escape(nombre)}</h3><div class="dias">'
        f'<div class="dia ticks"><span></span>{ticks}</div>'
    ]
    for f in filas:
        d = str(f["fecha"])
        cells = "".join(
            f'<div class="c {escape(str(c))}"></div>' if c else '<div class="c"></div>'
            for c in f["celdas"]
        )
        out.append(f'<div class="dia"><span>{escape(d[8:10])}/{escape(d[5:7])}</span>{cells}</div>')
    out.append("</div>")
    return "".join(out)


def _grafico(por_mes: Sequence[tuple[int, int, int]]) -> str:
    if not por_mes:
        return "<p>Sin datos del catálogo.</p>"
    w, h, left = 640, 240, 4
    bw = (w - left) / 12
    mx = max((a + b for _, a, b in por_mes), default=0) or 1
    sc = (h - 60) / mx
    parts = [
        f'<svg class="graf" viewBox="0 0 {w} {h}" role="img" aria-label="Cierres por mes del año">'
    ]
    for m, nieve, otros in por_mes:
        x = left + (m - 1) * bw
        base = float(h - 26)
        for cls, n in (("bar nieve", nieve), ("bar otros", otros)):
            if n:
                parts.append(
                    f'<rect class="{cls}" x="{x + 4:.1f}" y="{base - n * sc:.1f}" '
                    f'width="{bw - 8:.1f}" height="{n * sc:.1f}"/>'
                )
                base -= n * sc
        cx = x + bw / 2
        parts.append(
            f'<text class="val" x="{cx:.1f}" y="{base - 6:.1f}" text-anchor="middle">'
            f"{nieve + otros}</text>"
        )
        parts.append(
            f'<text class="eje" x="{cx:.1f}" y="{h - 6}" text-anchor="middle">{MESES[m - 1]}</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


def _duracion(d: Mapping[str, Any]) -> str:
    if not d.get("n"):
        return "<p>Ningún cierre del catálogo tiene fecha de reapertura conocida.</p>"
    med = d["mediana"]
    med_txt = f"{med:g}".replace(".", ",")
    unidad = "día" if med == 1 else "días"
    rango_u = "día" if d["max"] == 1 else "días"
    adm = d.get("administrativos") or []
    adm_txt = ""
    if adm:
        lista = ", ".join(
            f"{escape(_fecha(str(a['fecha_inicio'])))} ({_dias_txt(int(a['dias']))})" for a in adm
        )
        adm_txt = (
            "<p>Cierres administrativos (no meteorológicos, p. ej. sanitarios), fuera de la "
            f"mediana: {len(adm)} — {lista}.</p>"
        )
    return (
        f'<p><span class="num">{escape(med_txt)} {unidad}</span> de mediana</p>'
        f"<p>Rango: {d['min']} a {d['max']} {rango_u} · n = {d['n']} cierres con reapertura "
        f"conocida (de {d['total']} cierres en el catálogo).</p>"
        + adm_txt
        + '<p class="nota">Días entre la primera nota del cierre y la nota de reapertura (fechas '
        "de publicación). Solo cierres con una nota de reapertura en el catálogo; "
        f"{escape(NOTA_PRENSA)}.</p>"
    )


def _num(v: float) -> str:
    return f"{v:g}".replace(".", ",")


def _nieve_txt(m: Medida) -> str:
    if m.nivel is None or m.valor is None:
        return f"Nieve: sin dato ({escape(m.error or 'no disponible')})"
    if m.percentil is None:
        return "Nieve: no se espera"
    hab = "más que lo habitual para la época" if m.nivel == "alto" else "normal para la época"
    return f"Nieve: {_num(m.valor)} cm, {hab}"


def _viento_txt(m: Medida) -> str:
    if m.nivel is None or m.valor is None:
        return f"Viento: sin dato ({escape(m.error or 'no disponible')})"
    hab = "más fuerte que lo habitual" if m.nivel == "alto" else "normal para la época"
    return f"Viento: {hab} (ráfagas de hasta {_num(m.valor)} km/h)"


def _detalle(m: Medida, que: str, unidad: str) -> str:
    if m.valor is None:
        return f"{que}: sin dato"
    if m.percentil is None:
        return f"{que}: 0 {unidad}"
    desde = f" desde {m.desde}" if m.desde else ""
    return (
        f"{que}: {_num(m.valor)} {unidad} · {m.nivel} (más que el {m.percentil:g} % de lo que "
        f"este modelo pronosticó para esta época{desde})"
    )


def _pronostico(ps: Sequence[Pronostico72], now: datetime, alto: float = 90) -> str:
    p = elegir(ps)
    if p is None:
        motivos = {m.error for x in ps for m in (x.nieve, x.rafaga) if m.error}
        body = f"<p>Sin dato ({escape('; '.join(sorted(motivos)) or 'no disponible')}).</p>"
        como = ""
    else:
        body = f"<p>{_nieve_txt(p.nieve)}</p><p>{_viento_txt(p.rafaga)}</p>"
        if banner(p):
            body += (
                '<p class="banner"><strong>Se pronostican nieve y viento fuerte en Jama en las '
                "próximas 72 h.</strong></p>"
            )
        otros = ", ".join(x.nombre for x in ps if x is not p)
        como = (
            "<details><summary>Cómo se calcula</summary>"
            f"<p>Punto: {escape(p.nombre)}"
            + (f" (el de valores más altos; también calculamos {escape(otros)})" if otros else "")
            + ".</p>"
            f"<p>{_detalle(p.nieve, 'Nieve (suma de 72 h)', 'cm')}</p>"
            f"<p>{_detalle(p.rafaga, 'Ráfagas (máximo de 72 h)', 'km/h')}</p>"
            f"<p>&quot;Más que lo habitual&quot; = percentil {alto:g} o más de la climatología del "
            "mismo modelo de pronóstico (Open-Meteo, misma celda y misma época del año).</p>"
            "</details>"
        )
    return (
        f'<div class="prono">{body}</div>'
        '<p class="nota">Esto no es un pronóstico de cierre. Compara el pronóstico con lo '
        "habitual para esta época según el mismo modelo (Open-Meteo). &quot;Alto&quot; quiere "
        "decir dentro del 10 % más alto; no es un umbral probado con cierres reales. El cierre "
        "lo deciden las autoridades de Chile y Argentina: consultá siempre el estado oficial.</p>"
        + como
        + '<p class="nota">Pronóstico y climatología: Open-Meteo (CC BY 4.0). '
        f"Actualizado {cuando(now, now)}.</p>"
    )


def _ctas(d: Datos) -> str:
    out = []
    if d.url_telegram:
        out.append(
            f'<a class="cta tg" href="{escape(d.url_telegram)}" rel="noopener">'
            "Recibí los avisos por Telegram</a>"
        )
    if d.url_plan_flotas:
        out.append(
            f'<a class="cta flota" href="{escape(d.url_plan_flotas)}" rel="noopener">'
            "¿Tenés una flota? Anotate para el plan de empresas</a>"
        )
    return f'<div class="ctas">{"".join(out)}</div>' if out else ""


def index(d: Datos) -> str:
    total = sum(a + b for _, a, b in d.por_mes_anio)
    nieve_total = sum(a for _, a, _b in d.por_mes_anio)
    dd = datos_de(d.ar, d.cl)
    if dd is None:
        datos_txt = "Sin datos de los partes oficiales"
    else:
        c = cuando(dd, d.now)
        datos_txt = f"Datos de las {c[4:]}" if c.startswith("hoy ") else f"Datos del {c}"
    anios = " · ".join(f"{y} {n}" for y, n in d.por_anio)
    ley = (
        '<div class="ley"><span class="abierto">abierto</span><span class="cerrado">cerrado</span>'
        '<span class="horario">fuera de horario</span>'
        '<span class="restringido">restringido</span><span>gris = sin dato</span></div>'
    )
    body = [
        "<header><h1>Jama al Día</h1>",
        f'<p class="sub">Paso de Jama (RN 52 · CH-27). {escape(datos_txt)} (hora argentina).</p>'
        "</header>",
        '<section><h2>Estado ahora</h2><div class="lados">',
        _lado("Argentina", d.ar, d.now),
        _lado("Chile", d.cl, d.now),
        '</div><p class="nota">Resolución: 1 h (consultamos los partes oficiales cada hora).</p>'
        "</section>",
        _ctas(d),
        "<section><h2>Últimos 7 días</h2>",
        _dias("Argentina", d.bloques.get("AR", [])),
        _dias("Chile", d.bloques.get("CL", [])),
        ley,
        "</section>",
        "<section><h2>Cierres por mes del año</h2>",
        _grafico(d.por_mes_anio),
        '<div class="ley"><span class="nieve">nieve</span><span class="otros">otras causas</span>'
        "</div>"
        f'<p class="nota">n = {total} cierres totales o parciales 2016–2026 ({nieve_total} por '
        f"nieve), sin los de confianza baja; {escape(NOTA_PRENSA)}.</p>"
        f'<p class="nota">Por año: {escape(anios)}.'
        + (f" Catálogo del {escape(_fecha(d.catalogo_generado))}." if d.catalogo_generado else "")
        + "</p></section>",
        "<section><h2>Cuánto duran los cierres</h2>",
        _duracion(d.duraciones),
        "</section>",
        "<section><h2>Pronóstico para Jama — próximas 72 h</h2>",
        _pronostico(d.pronostico, d.now, d.alto),
        "</section>",
        "<footer>",
        _ctas(d),
        "<p>Fuente: partes oficiales de Argentina (argentina.gob.ar) y Chile (MOP). "
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
    def card(titulo: str, n: int | None, act: str | None, origen: str) -> str:
        num = f"{n:,}".replace(",", ".") if n is not None else "sin dato"
        return (
            f'<section><h2>{escape(titulo)}</h2><p class="num">{escape(num)}</p>'
            f'<p class="nota">{escape(origen)}'
            + (f" · actualizado {escape(act)}" if act else "")
            + "</p></section>"
        )

    body = (
        "<header><h1>Tracción — Jama al Día</h1>"
        f'<p class="sub">Página generada {cuando(now, now)} (hora argentina).</p></header>'
        + card(
            "Suscriptores del canal de Telegram",
            suscriptores,
            cuando(suscriptores_at, now) if suscriptores_at else None,
            "Telegram Bot API (getChatMemberCount), cada hora",
        )
        + card(
            "Inscriptos waitlist Plan Flotas",
            waitlist,
            _fecha(waitlist_at) if waitlist_at else None,
            "carga manual",
        )
        + '<footer><p><a href="../">Volver a Jama al Día</a></p></footer>'
    )
    return _doc("Tracción — Jama al Día", body)


def escribir(salida: Path, index_html: str, traccion_html: str) -> None:
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "index.html").write_text(index_html, encoding="utf-8")
    (salida / "traccion").mkdir(exist_ok=True)
    (salida / "traccion" / "index.html").write_text(traccion_html, encoding="utf-8")
    (salida / ".nojekyll").write_text("", encoding="utf-8")

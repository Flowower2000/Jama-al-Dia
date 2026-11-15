# Cómo leer el tablero

El tablero funciona sin conexión: todo lo que muestra viene adentro del archivo, generado
con `make tablero` a partir de las tablas del proyecto. Arriba y al pie dice de qué fecha
y hora son los datos y el pronóstico.

## Mapa

- Cada círculo es un punto crítico de la RN 9 o la RN 52. Tocalo (o tocá su nombre en la
  lista) para abrir su ficha.
- Rojo = alerta, verde = sin alerta, gris = umbral pendiente o sin datos de pronóstico.
- Mientras no haya umbrales elegidos, todos los puntos se ven grises y dicen "Umbral
  pendiente de definición": el tablero nunca usa un umbral por defecto.
- La línea punteada es el Tren Solar; los cuadrados son estaciones y salares de litio.
- "Usar mi ubicación" muestra el punto crítico más cercano en línea recta. La ubicación
  no sale del teléfono.

## Ficha de punto

- Riesgo para hoy, las próximas 24 h y las próximas 72 h. Cada ventana suma la lluvia o
  la nieve pronosticadas (más las de los días anteriores) igual que en la calibración.
- Cada valor del pronóstico va con su percentil: qué tan raro es para ese punto y esa
  estación según la historia del MISMO modelo de pronóstico. p95 = solo el 5 % de los días
  de esa estación tuvieron más.
- Si el umbral elegido está en mm o cm, se muestra pero dice "No comparable (modelo
  distinto)": los mm del pronóstico no se comparan con los mm de ERA5.
- Abajo están los cortes históricos de ese punto, con el medio y el enlace a la nota.
- También dice si el punto comparte la celda de clima ERA5 con otros (misma serie).

## Historial

- Todos los eventos del catálogo, con filtros por ruta, causa, año y punto.
- La tabla por año separa eventos con al menos una fuente estable (archivo desde 2016) de
  los que vienen solo de medios nuevos.

## Paso de Jama

- La última captura de cada fuente oficial (Chile y Argentina) con su hora, y las capturas
  de los últimos 7 días. Si la última tiene más de 6 horas, el tablero lo avisa.

## Jama al Día (página pública)

https://emiliano-f.github.io/corredor-quebrada-puna/ — se rearma cada hora.

- **Estado ahora:** ABIERTO / CERRADO / RESTRINGIDO por lado, según el parte oficial de cada
  país (argentina.gob.ar y MOP Chile). "Desde hace X h" cuenta desde la primera consulta con ese
  estado; la resolución es 1 h ("al menos" si arranca en la primera consulta que tenemos).
  Fuera de su horario Argentina marca el paso cerrado: se muestra "Cerrado por horario" (gris,
  con reloj, "Abre a las HH:MM"), no en rojo (rojo = cierre real). Si la última consulta de un
  lado tiene más de 2 h, la tarjeta se pone ámbar con "Estado no confirmado" y el último dato
  ("Último dato: Cerrado por horario, hoy 03:43"). Si la consulta es reciente pero el parte
  oficial de la fuente (p. ej. FECHA/HORA del MOP) tiene más de 24 h, sigue ámbar con "Sin parte
  nuevo", "Último parte oficial (09/11 08:00): Abierto" y "Chile no actualiza este parte desde el
  09/11. Consultá el estado oficial antes de cruzar." (otra fuente chilena: issue #44). El encabezado dice "Datos de
  las HH:MM" con la hora del dato más viejo de los dos lados. Fechas: "hoy", "ayer" o "dd/mm".
- **Avisos:** debajo del estado (y en el pie), "Recibí los avisos por Telegram" y "¿Tenés una
  flota? Anotate para el plan de empresas" (enlaces de `jama_al_dia` en `config.yaml`; sin
  enlace, no se muestran).
- **Últimos 7 días:** un bloque por hora y por lado (marcas 0/6/12/18); gris = sin dato; gris
  oscuro = fuera de horario.
- **Cierres por mes del año y duración:** del catálogo de prensa local (eventos en
  `rn52_paso_jama` con corte total o parcial, sin los de confianza baja): 12 barras (ene–dic,
  total 2016–2026, nieve y otras causas apiladas, con n) y una línea "Por año"; puede faltar
  algún cierre. La duración usa solo cierres con una nota de reapertura, en días de publicación:
  mediana y percentil 75 ("La mitad de los cierres duró… 3 de cada 4…"), sin rango (el máximo
  encadena varios cierres por el dedup, issue #42); los cierres administrativos (sanitarios,
  etc.) quedan fuera: "No incluye 1 cierre administrativo (enero 2022)." Cada bloque dice su base ("Sobre 67 cierres de Jama en
  el catálogo, 2016–2026"). No hay probabilidad de reapertura.
- **/traccion:** "Contamos desde el …" (`jama_al_dia.canal_desde`), suscriptores del canal
  (getChatMemberCount, cada hora) e inscriptos de la waitlist (carga manual, con su fecha), cada
  uno con una serie de un valor por día; sin dato se ve "— todavía sin dato". Mismos botones que
  la portada.
- **Pronóstico para Jama — próximas 72 h:** nieve = SUMA de las próximas 72 h frente a las
  sumas de 72 h de la climatología; ráfagas = MÁXIMO de las próximas 72 h frente a los máximos
  de 72 h. Mismo modelo de pronóstico, misma celda y misma estación del año (Historical
  Forecast API, desde `clima.pronostico_historico_desde` = 2021-01-01). Se calcula para Jama y
  la CH-27 y se muestra el punto con valores más altos (nieve primero). "alto" desde el
  percentil `jama_al_dia.percentil_alto` (90); nieve 0 → "sin nieve pronosticada", sin
  percentil. El aviso "Se pronostican nieve y viento fuerte" aparece solo si las dos son "alto".
  Es descriptivo, no un umbral probado con cierres. No es un pronóstico de cierre.
- **Telegram:** publica solo cuando cambia el estado combinado (sin los cierres nocturnos por
  horario de Argentina, salvo `avisar_cierre_por_horario: true`, y nunca con datos de más de
  2 h) y un resumen a las 08:00. Cada mensaje tiene hasta 4 líneas: Argentina
  ("🟢 Jama — Argentina ABIERTO desde las 14:46"; 🔴 cerrado, 🟠 restringido, ⚪ fuera de
  horario), Chile ("🟡 Chile: sin parte nuevo desde el 09/11 (último: Abierto)" mientras el
  parte siga viejo), "Fuente: Pasos Fronterizos (AR) · MOP (CL). No es un canal oficial." y el
  link a la página.

## Qué NO significa una alerta

- No significa que la ruta esté cortada ni que se vaya a cortar: indica lluvia o nieve
  inusual para ese lugar y estación.
- Sin alerta no significa ruta segura. Consultá siempre las fuentes oficiales.

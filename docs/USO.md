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
  Argentina marca el paso CERRADO fuera de su horario de atención: se muestra "fuera de horario".
- **Últimos 7 días:** un bloque por hora y por lado; gris = sin dato.
- **Cierres por mes y duración:** del catálogo de prensa local (eventos en `rn52_paso_jama`,
  sin avisos de precaución); puede faltar algún cierre. La duración usa solo cierres con una
  nota de reapertura, en días de publicación. No hay probabilidad de reapertura.
- **Nieve y viento 72 h:** nieve acumulada y ráfaga máxima pronosticadas en Jama y en la
  CH-27, cada una con su percentil frente a la climatología del mismo modelo de pronóstico
  (pronósticos archivados, misma estación del año); "alto" desde el percentil
  `jama_al_dia.percentil_alto` (90). Es descriptivo, no un umbral validado. No es un pronóstico
  de cierre.
- **Telegram:** publica solo cuando cambia el estado combinado (sin los cierres nocturnos por
  horario de Argentina, salvo `avisar_cierre_por_horario: true`) y un resumen a las 08:00.
  No es un canal oficial.

## Qué NO significa una alerta

- No significa que la ruta esté cortada ni que se vaya a cortar: indica lluvia o nieve
  inusual para ese lugar y estación.
- Sin alerta no significa ruta segura. Consultá siempre las fuentes oficiales.

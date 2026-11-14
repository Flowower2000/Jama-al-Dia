# Validación de umbrales

> Generado: 2026-11-14 23:30 UTC · versión `0.1.0.dev0` · commit `64883b2` · SCHEMA_VERSION 3 · fuentes `b3dab32ad1adf821`

Causas meteorológicas: aluvión y crecida contra lluvia, nieve contra nieve. Una regla por causa, igual para todos los puntos; ajuste 2016–2022, prueba 2023→hoy. Acierto = evento con alarma ese día o el anterior; falsa alarma = día con alarma sin evento ese día o el siguiente. Los mm de ERA5 no son lluvia local (ver docs/DATOS.md): por eso cada variable va también como percentil de su celda en la misma estación. Cada sección trae también la variante con aluvión y crecida juntos como una sola causa "lluvia". Junto a cada número va n = días-evento (punto, fecha) del período en que se basa; en prueba, n < 10 se marca "muestra chica". Vos elegís la regla final.

Fuentes estables (archivo desde ≤ 2016-01-01): elsubmarino, eltribunojujuy, jujuyaldia, jujuyalmomento, todojujuy.

## Todas las fuentes

Eventos con punto crítico usados: aluvión 65, crecida 65 (lluvia 130), nieve 61.

### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 40 | 10.8 | 2.9 | 75 |
| aluvion | `lluvia_48h_mm` | 40 | 26.3 | 7.1 | 85 |
| aluvion | `lluvia_72h_mm` | 40 | 34.3 | 12.1 | 75 |
| aluvion | `lluvia_7d_mm` | 40 | 63.2 | 34.1 | 65 |
| aluvion | `lluvia_max_horaria_24h_mm` | 40 | 1.9 | 0.7 | 80 |
| aluvion | `lluvia_max_horaria_72h_mm` | 40 | 3.1 | 1.5 | 77 |
| crecida | `lluvia_24h_mm` | 55 | 11.5 | 2.4 | 78 |
| crecida | `lluvia_48h_mm` | 55 | 20.4 | 6.3 | 75 |
| crecida | `lluvia_72h_mm` | 55 | 27.3 | 10.9 | 76 |
| crecida | `lluvia_7d_mm` | 55 | 54.8 | 31.6 | 63 |
| crecida | `lluvia_max_horaria_24h_mm` | 55 | 1.7 | 0.6 | 71 |
| crecida | `lluvia_max_horaria_72h_mm` | 55 | 2.9 | 1.3 | 73 |
| nieve | `nieve_24h_cm` | 35 | 0.0 | 0.0 | 48 |
| nieve | `nieve_72h_cm` | 35 | 0.4 | 0.0 | 91 |
| nieve | `nieve_7d_cm` | 35 | 0.4 | 0.0 | 85 |

### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 3.8 mm | 36 (n=48) | 12 (n=48) | 8558 (n=48) | 12 (n=17) | 5 (n=17) | 4516 (n=17) |
| aluvion | `lluvia_24h_mm` | 7.1 mm | 34 (n=48) | 14 (n=48) | 5215 (n=48) | 7 (n=17) | 10 (n=17) | 2660 (n=17) |
| aluvion | `lluvia_24h_mm` | 12 mm | 27 (n=48) | 21 (n=48) | 2762 (n=48) | 3 (n=17) | 14 (n=17) | 1341 (n=17) |
| aluvion | `lluvia_24h_mm` | 23.9 mm | 15 (n=48) | 33 (n=48) | 801 (n=48) | 0 (n=17) | 17 (n=17) | 393 (n=17) |
| aluvion | `lluvia_48h_mm` | 9.9 mm | 36 (n=48) | 12 (n=48) | 7647 (n=48) | 8 (n=17) | 9 (n=17) | 4042 (n=17) |
| aluvion | `lluvia_48h_mm` | 17.2 mm | 30 (n=48) | 18 (n=48) | 4429 (n=48) | 4 (n=17) | 13 (n=17) | 2203 (n=17) |
| aluvion | `lluvia_48h_mm` | 27.2 mm | 22 (n=48) | 26 (n=48) | 2208 (n=48) | 0 (n=17) | 17 (n=17) | 1045 (n=17) |
| aluvion | `lluvia_48h_mm` | 38.8 mm | 11 (n=48) | 37 (n=48) | 1068 (n=48) | 0 (n=17) | 17 (n=17) | 453 (n=17) |
| aluvion | `lluvia_72h_mm` | 10 mm | 36 (n=48) | 12 (n=48) | 10461 (n=48) | 10 (n=17) | 7 (n=17) | 5609 (n=17) |
| aluvion | `lluvia_72h_mm` | 23.5 mm | 30 (n=48) | 18 (n=48) | 5096 (n=48) | 5 (n=17) | 12 (n=17) | 2544 (n=17) |
| aluvion | `lluvia_72h_mm` | 34.3 mm | 20 (n=48) | 28 (n=48) | 2949 (n=48) | 2 (n=17) | 15 (n=17) | 1388 (n=17) |
| aluvion | `lluvia_72h_mm` | 44.8 mm | 11 (n=48) | 37 (n=48) | 1760 (n=48) | 1 (n=17) | 16 (n=17) | 796 (n=17) |
| aluvion | `lluvia_7d_mm` | 27.6 mm | 36 (n=48) | 12 (n=48) | 10181 (n=48) | 9 (n=17) | 8 (n=17) | 5581 (n=17) |
| aluvion | `lluvia_7d_mm` | 36.6 mm | 31 (n=48) | 17 (n=48) | 8244 (n=48) | 8 (n=17) | 9 (n=17) | 4298 (n=17) |
| aluvion | `lluvia_7d_mm` | 63.2 mm | 21 (n=48) | 27 (n=48) | 4141 (n=48) | 4 (n=17) | 13 (n=17) | 2009 (n=17) |
| aluvion | `lluvia_7d_mm` | 94.1 mm | 10 (n=48) | 38 (n=48) | 1825 (n=48) | 2 (n=17) | 15 (n=17) | 773 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm` | 0.7 mm | 37 (n=48) | 11 (n=48) | 10020 (n=48) | 12 (n=17) | 5 (n=17) | 5137 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm` | 1.1 mm | 36 (n=48) | 12 (n=48) | 7047 (n=48) | 12 (n=17) | 5 (n=17) | 3563 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm` | 1.9 mm | 31 (n=48) | 17 (n=48) | 3623 (n=48) | 9 (n=17) | 8 (n=17) | 1811 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm` | 3.9 mm | 16 (n=48) | 32 (n=48) | 941 (n=48) | 1 (n=17) | 16 (n=17) | 449 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm` | 1.4 mm | 36 (n=48) | 12 (n=48) | 10000 (n=48) | 12 (n=17) | 5 (n=17) | 5297 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm` | 2 mm | 33 (n=48) | 15 (n=48) | 7093 (n=48) | 11 (n=17) | 6 (n=17) | 3577 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm` | 3.1 mm | 20 (n=48) | 28 (n=48) | 3662 (n=48) | 3 (n=17) | 14 (n=17) | 1769 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm` | 5 mm | 11 (n=48) | 37 (n=48) | 1411 (n=48) | 2 (n=17) | 15 (n=17) | 652 (n=17) |
| crecida | `lluvia_24h_mm` | 0.7 mm | 49 (n=56) | 7 (n=56) | 14760 (n=56) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 8334 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 3.4 mm | 42 (n=56) | 14 (n=56) | 9093 (n=56) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 4862 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 11.9 mm | 30 (n=56) | 26 (n=56) | 2785 (n=56) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1367 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 17.9 mm | 19 (n=56) | 37 (n=56) | 1411 (n=56) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 695 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 2.3 mm | 50 (n=56) | 6 (n=56) | 14712 (n=56) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 8015 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 6 mm | 43 (n=56) | 13 (n=56) | 10437 (n=56) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 5694 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 23 mm | 28 (n=56) | 28 (n=56) | 2937 (n=56) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1411 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 38.5 mm | 20 (n=56) | 36 (n=56) | 1090 (n=56) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 459 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 4.3 mm | 47 (n=56) | 9 (n=56) | 14541 (n=56) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 8029 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 12.6 mm | 40 (n=56) | 16 (n=56) | 9039 (n=56) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 4842 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 28 mm | 31 (n=56) | 25 (n=56) | 3940 (n=56) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1985 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 53.5 mm | 14 (n=56) | 42 (n=56) | 1117 (n=56) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 464 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 7.4 mm | 51 (n=56) | 5 (n=56) | 17435 (n=56) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 9579 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 30.2 mm | 41 (n=56) | 15 (n=56) | 9579 (n=56) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 5199 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 55.9 mm | 29 (n=56) | 27 (n=56) | 5026 (n=56) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2462 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 97.9 mm | 14 (n=56) | 42 (n=56) | 1590 (n=56) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 678 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 0.3 mm | 47 (n=56) | 9 (n=56) | 14865 (n=56) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 7775 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 0.8 mm | 40 (n=56) | 16 (n=56) | 9172 (n=56) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 4717 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 1.8 mm | 32 (n=56) | 24 (n=56) | 3935 (n=56) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 1942 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 2.7 mm | 19 (n=56) | 37 (n=56) | 1998 (n=56) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 966 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 0.5 mm | 50 (n=56) | 6 (n=56) | 17200 (n=56) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 8829 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 1.3 mm | 40 (n=56) | 16 (n=56) | 10614 (n=56) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 5595 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 3 mm | 30 (n=56) | 26 (n=56) | 3903 (n=56) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1922 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 4.6 mm | 15 (n=56) | 41 (n=56) | 1679 (n=56) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 828 (n=9 muestra chica) |
| nieve | `nieve_24h_cm` | 0.1 cm | 18 (n=35) | 17 (n=35) | 261 (n=35) | 11 (n=26) | 15 (n=26) | 109 (n=26) |
| nieve | `nieve_24h_cm` | 0.2 cm | 16 (n=35) | 19 (n=35) | 223 (n=35) | 10 (n=26) | 16 (n=26) | 97 (n=26) |
| nieve | `nieve_24h_cm` | 0.6 cm | 9 (n=35) | 26 (n=35) | 135 (n=35) | 5 (n=26) | 21 (n=26) | 54 (n=26) |
| nieve | `nieve_24h_cm` | 1.7 cm | 4 (n=35) | 31 (n=35) | 41 (n=35) | 3 (n=26) | 23 (n=26) | 16 (n=26) |
| nieve | `nieve_72h_cm` | 0.1 cm | 22 (n=35) | 13 (n=35) | 626 (n=35) | 13 (n=26) | 13 (n=26) | 234 (n=26) |
| nieve | `nieve_72h_cm` | 0.4 cm | 18 (n=35) | 17 (n=35) | 418 (n=35) | 9 (n=26) | 17 (n=26) | 176 (n=26) |
| nieve | `nieve_72h_cm` | 0.9 cm | 12 (n=35) | 23 (n=35) | 292 (n=35) | 7 (n=26) | 19 (n=26) | 104 (n=26) |
| nieve | `nieve_72h_cm` | 2.2 cm | 9 (n=35) | 26 (n=35) | 97 (n=35) | 3 (n=26) | 23 (n=26) | 40 (n=26) |
| nieve | `nieve_7d_cm` | 0.1 cm | 24 (n=35) | 11 (n=35) | 1278 (n=35) | 14 (n=26) | 12 (n=26) | 468 (n=26) |
| nieve | `nieve_7d_cm` | 0.4 cm | 20 (n=35) | 15 (n=35) | 876 (n=35) | 9 (n=26) | 17 (n=26) | 369 (n=26) |
| nieve | `nieve_7d_cm` | 1.5 cm | 12 (n=35) | 23 (n=35) | 413 (n=35) | 4 (n=26) | 22 (n=26) | 146 (n=26) |
| nieve | `nieve_7d_cm` | 2.9 cm | 7 (n=35) | 28 (n=35) | 188 (n=35) | 1 (n=26) | 25 (n=26) | 70 (n=26) |

### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm_pct` | p80 | 31 (n=48) | 17 (n=48) | 5781 (n=48) | 13 (n=17) | 4 (n=17) | 3337 (n=17) |
| aluvion | `lluvia_24h_mm_pct` | p90 | 21 (n=48) | 27 (n=48) | 3045 (n=48) | 8 (n=17) | 9 (n=17) | 1709 (n=17) |
| aluvion | `lluvia_24h_mm_pct` | p95 | 13 (n=48) | 35 (n=48) | 1587 (n=48) | 4 (n=17) | 13 (n=17) | 907 (n=17) |
| aluvion | `lluvia_24h_mm_pct` | p98 | 6 (n=48) | 42 (n=48) | 666 (n=48) | 1 (n=17) | 16 (n=17) | 385 (n=17) |
| aluvion | `lluvia_24h_mm_pct` | p99 | 3 (n=48) | 45 (n=48) | 311 (n=48) | 0 (n=17) | 17 (n=17) | 171 (n=17) |
| aluvion | `lluvia_48h_mm_pct` | p80 | 27 (n=48) | 21 (n=48) | 6059 (n=48) | 8 (n=17) | 9 (n=17) | 3339 (n=17) |
| aluvion | `lluvia_48h_mm_pct` | p90 | 12 (n=48) | 36 (n=48) | 3140 (n=48) | 7 (n=17) | 10 (n=17) | 1743 (n=17) |
| aluvion | `lluvia_48h_mm_pct` | p95 | 9 (n=48) | 39 (n=48) | 1625 (n=48) | 3 (n=17) | 14 (n=17) | 902 (n=17) |
| aluvion | `lluvia_48h_mm_pct` | p98 | 5 (n=48) | 43 (n=48) | 665 (n=48) | 2 (n=17) | 15 (n=17) | 329 (n=17) |
| aluvion | `lluvia_48h_mm_pct` | p99 | 2 (n=48) | 46 (n=48) | 309 (n=48) | 0 (n=17) | 17 (n=17) | 162 (n=17) |
| aluvion | `lluvia_72h_mm_pct` | p80 | 17 (n=48) | 31 (n=48) | 6157 (n=48) | 10 (n=17) | 7 (n=17) | 3340 (n=17) |
| aluvion | `lluvia_72h_mm_pct` | p90 | 10 (n=48) | 38 (n=48) | 3216 (n=48) | 8 (n=17) | 9 (n=17) | 1760 (n=17) |
| aluvion | `lluvia_72h_mm_pct` | p95 | 6 (n=48) | 42 (n=48) | 1648 (n=48) | 4 (n=17) | 13 (n=17) | 872 (n=17) |
| aluvion | `lluvia_72h_mm_pct` | p98 | 4 (n=48) | 44 (n=48) | 665 (n=48) | 1 (n=17) | 16 (n=17) | 293 (n=17) |
| aluvion | `lluvia_72h_mm_pct` | p99 | 2 (n=48) | 46 (n=48) | 315 (n=48) | 0 (n=17) | 17 (n=17) | 133 (n=17) |
| aluvion | `lluvia_7d_mm_pct` | p80 | 16 (n=48) | 32 (n=48) | 6431 (n=48) | 12 (n=17) | 5 (n=17) | 3533 (n=17) |
| aluvion | `lluvia_7d_mm_pct` | p90 | 9 (n=48) | 39 (n=48) | 3288 (n=48) | 10 (n=17) | 7 (n=17) | 1752 (n=17) |
| aluvion | `lluvia_7d_mm_pct` | p95 | 6 (n=48) | 42 (n=48) | 1651 (n=48) | 2 (n=17) | 15 (n=17) | 823 (n=17) |
| aluvion | `lluvia_7d_mm_pct` | p98 | 4 (n=48) | 44 (n=48) | 658 (n=48) | 2 (n=17) | 15 (n=17) | 295 (n=17) |
| aluvion | `lluvia_7d_mm_pct` | p99 | 3 (n=48) | 45 (n=48) | 305 (n=48) | 1 (n=17) | 16 (n=17) | 138 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p80 | 31 (n=48) | 17 (n=48) | 5777 (n=48) | 14 (n=17) | 3 (n=17) | 3222 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p90 | 20 (n=48) | 28 (n=48) | 3011 (n=48) | 9 (n=17) | 8 (n=17) | 1618 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p95 | 7 (n=48) | 41 (n=48) | 1587 (n=48) | 4 (n=17) | 13 (n=17) | 868 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p98 | 5 (n=48) | 43 (n=48) | 652 (n=48) | 2 (n=17) | 15 (n=17) | 311 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p99 | 1 (n=48) | 47 (n=48) | 317 (n=48) | 0 (n=17) | 17 (n=17) | 149 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p80 | 14 (n=48) | 34 (n=48) | 6085 (n=48) | 11 (n=17) | 6 (n=17) | 3194 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p90 | 7 (n=48) | 41 (n=48) | 3197 (n=48) | 7 (n=17) | 10 (n=17) | 1729 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p95 | 6 (n=48) | 42 (n=48) | 1618 (n=48) | 4 (n=17) | 13 (n=17) | 792 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p98 | 1 (n=48) | 47 (n=48) | 653 (n=48) | 2 (n=17) | 15 (n=17) | 289 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p99 | 1 (n=48) | 47 (n=48) | 305 (n=48) | 1 (n=17) | 16 (n=17) | 157 (n=17) |
| crecida | `lluvia_24h_mm_pct` | p80 | 32 (n=56) | 24 (n=56) | 5775 (n=56) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 3349 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p90 | 16 (n=56) | 40 (n=56) | 3052 (n=56) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1715 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p95 | 7 (n=56) | 49 (n=56) | 1593 (n=56) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 911 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p98 | 4 (n=56) | 52 (n=56) | 668 (n=56) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 386 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p99 | 2 (n=56) | 54 (n=56) | 312 (n=56) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 171 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p80 | 34 (n=56) | 22 (n=56) | 6052 (n=56) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3347 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p90 | 17 (n=56) | 39 (n=56) | 3139 (n=56) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1749 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p95 | 8 (n=56) | 48 (n=56) | 1629 (n=56) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 904 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p98 | 4 (n=56) | 52 (n=56) | 667 (n=56) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 330 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p99 | 3 (n=56) | 53 (n=56) | 308 (n=56) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 162 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p80 | 24 (n=56) | 32 (n=56) | 6147 (n=56) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3352 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p90 | 15 (n=56) | 41 (n=56) | 3213 (n=56) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1770 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p95 | 9 (n=56) | 47 (n=56) | 1644 (n=56) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 876 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p98 | 3 (n=56) | 53 (n=56) | 666 (n=56) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 294 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p99 | 3 (n=56) | 53 (n=56) | 313 (n=56) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 133 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p80 | 19 (n=56) | 37 (n=56) | 6427 (n=56) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 3552 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p90 | 10 (n=56) | 46 (n=56) | 3287 (n=56) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1764 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p95 | 5 (n=56) | 51 (n=56) | 1651 (n=56) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 825 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p98 | 4 (n=56) | 52 (n=56) | 656 (n=56) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 298 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p99 | 2 (n=56) | 54 (n=56) | 305 (n=56) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 140 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p80 | 27 (n=56) | 29 (n=56) | 5781 (n=56) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3232 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p90 | 13 (n=56) | 43 (n=56) | 3017 (n=56) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1627 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p95 | 5 (n=56) | 51 (n=56) | 1588 (n=56) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 873 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p98 | 4 (n=56) | 52 (n=56) | 653 (n=56) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 313 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p99 | 2 (n=56) | 54 (n=56) | 316 (n=56) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 149 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p80 | 20 (n=56) | 36 (n=56) | 6074 (n=56) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3208 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p90 | 8 (n=56) | 48 (n=56) | 3194 (n=56) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1737 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p95 | 7 (n=56) | 49 (n=56) | 1615 (n=56) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 795 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p98 | 4 (n=56) | 52 (n=56) | 648 (n=56) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 291 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p99 | 4 (n=56) | 52 (n=56) | 300 (n=56) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 158 (n=9 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p80 | 18 (n=35) | 17 (n=35) | 314 (n=35) | 13 (n=26) | 13 (n=26) | 138 (n=26) |
| nieve | `nieve_24h_cm_pct` | p90 | 17 (n=35) | 18 (n=35) | 289 (n=35) | 13 (n=26) | 13 (n=26) | 129 (n=26) |
| nieve | `nieve_24h_cm_pct` | p95 | 15 (n=35) | 20 (n=35) | 257 (n=35) | 13 (n=26) | 13 (n=26) | 110 (n=26) |
| nieve | `nieve_24h_cm_pct` | p98 | 7 (n=35) | 28 (n=35) | 182 (n=35) | 6 (n=26) | 20 (n=26) | 69 (n=26) |
| nieve | `nieve_24h_cm_pct` | p99 | 4 (n=35) | 31 (n=35) | 115 (n=35) | 5 (n=26) | 21 (n=26) | 39 (n=26) |
| nieve | `nieve_72h_cm_pct` | p80 | 23 (n=35) | 12 (n=35) | 686 (n=35) | 14 (n=26) | 12 (n=26) | 274 (n=26) |
| nieve | `nieve_72h_cm_pct` | p90 | 19 (n=35) | 16 (n=35) | 594 (n=35) | 12 (n=26) | 14 (n=26) | 235 (n=26) |
| nieve | `nieve_72h_cm_pct` | p95 | 14 (n=35) | 21 (n=35) | 444 (n=35) | 9 (n=26) | 17 (n=26) | 169 (n=26) |
| nieve | `nieve_72h_cm_pct` | p98 | 6 (n=35) | 29 (n=35) | 263 (n=35) | 5 (n=26) | 21 (n=26) | 82 (n=26) |
| nieve | `nieve_72h_cm_pct` | p99 | 3 (n=35) | 32 (n=35) | 163 (n=35) | 3 (n=26) | 23 (n=26) | 48 (n=26) |
| nieve | `nieve_7d_cm_pct` | p80 | 22 (n=35) | 13 (n=35) | 1251 (n=35) | 13 (n=26) | 13 (n=26) | 489 (n=26) |
| nieve | `nieve_7d_cm_pct` | p90 | 13 (n=35) | 22 (n=35) | 963 (n=35) | 10 (n=26) | 16 (n=26) | 358 (n=26) |
| nieve | `nieve_7d_cm_pct` | p95 | 8 (n=35) | 27 (n=35) | 656 (n=35) | 7 (n=26) | 19 (n=26) | 210 (n=26) |
| nieve | `nieve_7d_cm_pct` | p98 | 3 (n=35) | 32 (n=35) | 358 (n=35) | 4 (n=26) | 22 (n=26) | 98 (n=26) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=35) | 34 (n=35) | 181 (n=35) | 2 (n=26) | 24 (n=26) | 66 (n=26) |

### Variante: aluvión + crecida = lluvia

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 95 | 10.8 | 2.0 | 78 |
| lluvia | `lluvia_48h_mm` | 95 | 23.6 | 5.2 | 80 |
| lluvia | `lluvia_72h_mm` | 95 | 29.6 | 9.0 | 76 |
| lluvia | `lluvia_7d_mm` | 95 | 56.9 | 26.0 | 64 |
| lluvia | `lluvia_max_horaria_24h_mm` | 95 | 1.8 | 0.5 | 74 |
| lluvia | `lluvia_max_horaria_72h_mm` | 95 | 2.9 | 1.2 | 74 |
| nieve | `nieve_24h_cm` | 35 | 0.0 | 0.0 | 48 |
| nieve | `nieve_72h_cm` | 35 | 0.4 | 0.0 | 91 |
| nieve | `nieve_7d_cm` | 35 | 0.4 | 0.0 | 85 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 2.2 mm | 84 (n=104) | 20 (n=104) | 10992 (n=104) | 19 (n=26) | 7 (n=26) | 5960 (n=26) |
| lluvia | `lluvia_24h_mm` | 4.5 mm | 75 (n=104) | 29 (n=104) | 7591 (n=104) | 16 (n=26) | 10 (n=26) | 4043 (n=26) |
| lluvia | `lluvia_24h_mm` | 11.9 mm | 57 (n=104) | 47 (n=104) | 2749 (n=104) | 5 (n=26) | 21 (n=26) | 1364 (n=26) |
| lluvia | `lluvia_24h_mm` | 20.5 mm | 34 (n=104) | 70 (n=104) | 1071 (n=104) | 1 (n=26) | 25 (n=26) | 543 (n=26) |
| lluvia | `lluvia_48h_mm` | 2.7 mm | 85 (n=104) | 19 (n=104) | 14028 (n=104) | 22 (n=26) | 4 (n=26) | 7687 (n=26) |
| lluvia | `lluvia_48h_mm` | 10.5 mm | 76 (n=104) | 28 (n=104) | 7217 (n=104) | 12 (n=26) | 14 (n=26) | 3832 (n=26) |
| lluvia | `lluvia_48h_mm` | 24.1 mm | 49 (n=104) | 55 (n=104) | 2669 (n=104) | 2 (n=26) | 24 (n=26) | 1304 (n=26) |
| lluvia | `lluvia_48h_mm` | 38.8 mm | 31 (n=104) | 73 (n=104) | 1046 (n=104) | 1 (n=26) | 25 (n=26) | 452 (n=26) |
| lluvia | `lluvia_72h_mm` | 4.7 mm | 84 (n=104) | 20 (n=104) | 14079 (n=104) | 21 (n=26) | 5 (n=26) | 7810 (n=26) |
| lluvia | `lluvia_72h_mm` | 17 mm | 75 (n=104) | 29 (n=104) | 7078 (n=104) | 10 (n=26) | 16 (n=26) | 3711 (n=26) |
| lluvia | `lluvia_72h_mm` | 30.1 mm | 53 (n=104) | 51 (n=104) | 3512 (n=104) | 4 (n=26) | 22 (n=26) | 1737 (n=26) |
| lluvia | `lluvia_72h_mm` | 52.1 mm | 27 (n=104) | 77 (n=104) | 1198 (n=104) | 2 (n=26) | 24 (n=26) | 512 (n=26) |
| lluvia | `lluvia_7d_mm` | 7.9 mm | 89 (n=104) | 15 (n=104) | 17008 (n=104) | 22 (n=26) | 4 (n=26) | 9379 (n=26) |
| lluvia | `lluvia_7d_mm` | 33.5 mm | 72 (n=104) | 32 (n=104) | 8801 (n=104) | 12 (n=26) | 14 (n=26) | 4710 (n=26) |
| lluvia | `lluvia_7d_mm` | 59.1 mm | 51 (n=104) | 53 (n=104) | 4571 (n=104) | 7 (n=26) | 19 (n=26) | 2246 (n=26) |
| lluvia | `lluvia_7d_mm` | 95.8 mm | 25 (n=104) | 79 (n=104) | 1707 (n=104) | 3 (n=26) | 23 (n=26) | 710 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm` | 0.5 mm | 82 (n=104) | 22 (n=104) | 12066 (n=104) | 23 (n=26) | 3 (n=26) | 6142 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm` | 0.9 mm | 73 (n=104) | 31 (n=104) | 8351 (n=104) | 18 (n=26) | 8 (n=26) | 4343 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm` | 1.9 mm | 60 (n=104) | 44 (n=104) | 3579 (n=104) | 14 (n=26) | 12 (n=26) | 1806 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm` | 3.7 mm | 32 (n=104) | 72 (n=104) | 1025 (n=104) | 2 (n=26) | 24 (n=26) | 522 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm` | 0.7 mm | 85 (n=104) | 19 (n=104) | 14898 (n=104) | 21 (n=26) | 5 (n=26) | 7805 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm` | 1.8 mm | 70 (n=104) | 34 (n=104) | 7926 (n=104) | 18 (n=26) | 8 (n=26) | 4085 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm` | 3 mm | 50 (n=104) | 54 (n=104) | 3870 (n=104) | 5 (n=26) | 21 (n=26) | 1918 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm` | 4.7 mm | 26 (n=104) | 78 (n=104) | 1621 (n=104) | 2 (n=26) | 24 (n=26) | 792 (n=26) |
| nieve | `nieve_24h_cm` | 0.1 cm | 18 (n=35) | 17 (n=35) | 261 (n=35) | 11 (n=26) | 15 (n=26) | 109 (n=26) |
| nieve | `nieve_24h_cm` | 0.2 cm | 16 (n=35) | 19 (n=35) | 223 (n=35) | 10 (n=26) | 16 (n=26) | 97 (n=26) |
| nieve | `nieve_24h_cm` | 0.6 cm | 9 (n=35) | 26 (n=35) | 135 (n=35) | 5 (n=26) | 21 (n=26) | 54 (n=26) |
| nieve | `nieve_24h_cm` | 1.7 cm | 4 (n=35) | 31 (n=35) | 41 (n=35) | 3 (n=26) | 23 (n=26) | 16 (n=26) |
| nieve | `nieve_72h_cm` | 0.1 cm | 22 (n=35) | 13 (n=35) | 626 (n=35) | 13 (n=26) | 13 (n=26) | 234 (n=26) |
| nieve | `nieve_72h_cm` | 0.4 cm | 18 (n=35) | 17 (n=35) | 418 (n=35) | 9 (n=26) | 17 (n=26) | 176 (n=26) |
| nieve | `nieve_72h_cm` | 0.9 cm | 12 (n=35) | 23 (n=35) | 292 (n=35) | 7 (n=26) | 19 (n=26) | 104 (n=26) |
| nieve | `nieve_72h_cm` | 2.2 cm | 9 (n=35) | 26 (n=35) | 97 (n=35) | 3 (n=26) | 23 (n=26) | 40 (n=26) |
| nieve | `nieve_7d_cm` | 0.1 cm | 24 (n=35) | 11 (n=35) | 1278 (n=35) | 14 (n=26) | 12 (n=26) | 468 (n=26) |
| nieve | `nieve_7d_cm` | 0.4 cm | 20 (n=35) | 15 (n=35) | 876 (n=35) | 9 (n=26) | 17 (n=26) | 369 (n=26) |
| nieve | `nieve_7d_cm` | 1.5 cm | 12 (n=35) | 23 (n=35) | 413 (n=35) | 4 (n=26) | 22 (n=26) | 146 (n=26) |
| nieve | `nieve_7d_cm` | 2.9 cm | 7 (n=35) | 28 (n=35) | 188 (n=35) | 1 (n=26) | 25 (n=26) | 70 (n=26) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm_pct` | p80 | 63 (n=104) | 41 (n=104) | 5737 (n=104) | 17 (n=26) | 9 (n=26) | 3331 (n=26) |
| lluvia | `lluvia_24h_mm_pct` | p90 | 37 (n=104) | 67 (n=104) | 3027 (n=104) | 10 (n=26) | 16 (n=26) | 1705 (n=26) |
| lluvia | `lluvia_24h_mm_pct` | p95 | 20 (n=104) | 84 (n=104) | 1578 (n=104) | 5 (n=26) | 21 (n=26) | 906 (n=26) |
| lluvia | `lluvia_24h_mm_pct` | p98 | 10 (n=104) | 94 (n=104) | 662 (n=104) | 1 (n=26) | 25 (n=26) | 385 (n=26) |
| lluvia | `lluvia_24h_mm_pct` | p99 | 5 (n=104) | 99 (n=104) | 309 (n=104) | 0 (n=26) | 26 (n=26) | 171 (n=26) |
| lluvia | `lluvia_48h_mm_pct` | p80 | 61 (n=104) | 43 (n=104) | 6016 (n=104) | 11 (n=26) | 15 (n=26) | 3333 (n=26) |
| lluvia | `lluvia_48h_mm_pct` | p90 | 29 (n=104) | 75 (n=104) | 3120 (n=104) | 9 (n=26) | 17 (n=26) | 1739 (n=26) |
| lluvia | `lluvia_48h_mm_pct` | p95 | 17 (n=104) | 87 (n=104) | 1616 (n=104) | 5 (n=26) | 21 (n=26) | 900 (n=26) |
| lluvia | `lluvia_48h_mm_pct` | p98 | 9 (n=104) | 95 (n=104) | 661 (n=104) | 3 (n=26) | 23 (n=26) | 328 (n=26) |
| lluvia | `lluvia_48h_mm_pct` | p99 | 5 (n=104) | 99 (n=104) | 306 (n=104) | 0 (n=26) | 26 (n=26) | 162 (n=26) |
| lluvia | `lluvia_72h_mm_pct` | p80 | 41 (n=104) | 63 (n=104) | 6120 (n=104) | 13 (n=26) | 13 (n=26) | 3335 (n=26) |
| lluvia | `lluvia_72h_mm_pct` | p90 | 25 (n=104) | 79 (n=104) | 3196 (n=104) | 10 (n=26) | 16 (n=26) | 1757 (n=26) |
| lluvia | `lluvia_72h_mm_pct` | p95 | 15 (n=104) | 89 (n=104) | 1636 (n=104) | 5 (n=26) | 21 (n=26) | 870 (n=26) |
| lluvia | `lluvia_72h_mm_pct` | p98 | 7 (n=104) | 97 (n=104) | 660 (n=104) | 1 (n=26) | 25 (n=26) | 293 (n=26) |
| lluvia | `lluvia_72h_mm_pct` | p99 | 5 (n=104) | 99 (n=104) | 311 (n=104) | 0 (n=26) | 26 (n=26) | 133 (n=26) |
| lluvia | `lluvia_7d_mm_pct` | p80 | 35 (n=104) | 69 (n=104) | 6399 (n=104) | 14 (n=26) | 12 (n=26) | 3529 (n=26) |
| lluvia | `lluvia_7d_mm_pct` | p90 | 19 (n=104) | 85 (n=104) | 3274 (n=104) | 12 (n=26) | 14 (n=26) | 1748 (n=26) |
| lluvia | `lluvia_7d_mm_pct` | p95 | 11 (n=104) | 93 (n=104) | 1643 (n=104) | 3 (n=26) | 23 (n=26) | 821 (n=26) |
| lluvia | `lluvia_7d_mm_pct` | p98 | 8 (n=104) | 96 (n=104) | 652 (n=104) | 2 (n=26) | 24 (n=26) | 295 (n=26) |
| lluvia | `lluvia_7d_mm_pct` | p99 | 5 (n=104) | 99 (n=104) | 303 (n=104) | 1 (n=26) | 25 (n=26) | 138 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p80 | 58 (n=104) | 46 (n=104) | 5740 (n=104) | 21 (n=26) | 5 (n=26) | 3214 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p90 | 33 (n=104) | 71 (n=104) | 2995 (n=104) | 11 (n=26) | 15 (n=26) | 1615 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p95 | 12 (n=104) | 92 (n=104) | 1580 (n=104) | 4 (n=26) | 22 (n=26) | 868 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p98 | 9 (n=104) | 95 (n=104) | 648 (n=104) | 2 (n=26) | 24 (n=26) | 311 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p99 | 3 (n=104) | 101 (n=104) | 315 (n=104) | 0 (n=26) | 26 (n=26) | 149 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p80 | 34 (n=104) | 70 (n=104) | 6051 (n=104) | 14 (n=26) | 12 (n=26) | 3190 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p90 | 15 (n=104) | 89 (n=104) | 3184 (n=104) | 8 (n=26) | 18 (n=26) | 1727 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p95 | 13 (n=104) | 91 (n=104) | 1607 (n=104) | 5 (n=26) | 21 (n=26) | 790 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p98 | 5 (n=104) | 99 (n=104) | 647 (n=104) | 2 (n=26) | 24 (n=26) | 289 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p99 | 5 (n=104) | 99 (n=104) | 299 (n=104) | 1 (n=26) | 25 (n=26) | 157 (n=26) |
| nieve | `nieve_24h_cm_pct` | p80 | 18 (n=35) | 17 (n=35) | 314 (n=35) | 13 (n=26) | 13 (n=26) | 138 (n=26) |
| nieve | `nieve_24h_cm_pct` | p90 | 17 (n=35) | 18 (n=35) | 289 (n=35) | 13 (n=26) | 13 (n=26) | 129 (n=26) |
| nieve | `nieve_24h_cm_pct` | p95 | 15 (n=35) | 20 (n=35) | 257 (n=35) | 13 (n=26) | 13 (n=26) | 110 (n=26) |
| nieve | `nieve_24h_cm_pct` | p98 | 7 (n=35) | 28 (n=35) | 182 (n=35) | 6 (n=26) | 20 (n=26) | 69 (n=26) |
| nieve | `nieve_24h_cm_pct` | p99 | 4 (n=35) | 31 (n=35) | 115 (n=35) | 5 (n=26) | 21 (n=26) | 39 (n=26) |
| nieve | `nieve_72h_cm_pct` | p80 | 23 (n=35) | 12 (n=35) | 686 (n=35) | 14 (n=26) | 12 (n=26) | 274 (n=26) |
| nieve | `nieve_72h_cm_pct` | p90 | 19 (n=35) | 16 (n=35) | 594 (n=35) | 12 (n=26) | 14 (n=26) | 235 (n=26) |
| nieve | `nieve_72h_cm_pct` | p95 | 14 (n=35) | 21 (n=35) | 444 (n=35) | 9 (n=26) | 17 (n=26) | 169 (n=26) |
| nieve | `nieve_72h_cm_pct` | p98 | 6 (n=35) | 29 (n=35) | 263 (n=35) | 5 (n=26) | 21 (n=26) | 82 (n=26) |
| nieve | `nieve_72h_cm_pct` | p99 | 3 (n=35) | 32 (n=35) | 163 (n=35) | 3 (n=26) | 23 (n=26) | 48 (n=26) |
| nieve | `nieve_7d_cm_pct` | p80 | 22 (n=35) | 13 (n=35) | 1251 (n=35) | 13 (n=26) | 13 (n=26) | 489 (n=26) |
| nieve | `nieve_7d_cm_pct` | p90 | 13 (n=35) | 22 (n=35) | 963 (n=35) | 10 (n=26) | 16 (n=26) | 358 (n=26) |
| nieve | `nieve_7d_cm_pct` | p95 | 8 (n=35) | 27 (n=35) | 656 (n=35) | 7 (n=26) | 19 (n=26) | 210 (n=26) |
| nieve | `nieve_7d_cm_pct` | p98 | 3 (n=35) | 32 (n=35) | 358 (n=35) | 4 (n=26) | 22 (n=26) | 98 (n=26) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=35) | 34 (n=35) | 181 (n=35) | 2 (n=26) | 24 (n=26) | 66 (n=26) |

## Solo fuentes estables

Eventos con punto crítico usados: aluvión 62, crecida 64 (lluvia 126), nieve 57.

### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 39 | 10.8 | 2.9 | 75 |
| aluvion | `lluvia_48h_mm` | 39 | 27.2 | 7.1 | 85 |
| aluvion | `lluvia_72h_mm` | 39 | 34.6 | 12.1 | 76 |
| aluvion | `lluvia_7d_mm` | 39 | 65.0 | 34.1 | 66 |
| aluvion | `lluvia_max_horaria_24h_mm` | 39 | 1.8 | 0.7 | 80 |
| aluvion | `lluvia_max_horaria_72h_mm` | 39 | 3.3 | 1.5 | 76 |
| crecida | `lluvia_24h_mm` | 54 | 11.6 | 2.4 | 79 |
| crecida | `lluvia_48h_mm` | 54 | 21.6 | 6.3 | 75 |
| crecida | `lluvia_72h_mm` | 54 | 27.6 | 10.9 | 77 |
| crecida | `lluvia_7d_mm` | 54 | 55.9 | 31.6 | 64 |
| crecida | `lluvia_max_horaria_24h_mm` | 54 | 1.8 | 0.6 | 71 |
| crecida | `lluvia_max_horaria_72h_mm` | 54 | 3.0 | 1.3 | 73 |
| nieve | `nieve_24h_cm` | 33 | 0.0 | 0.0 | 48 |
| nieve | `nieve_72h_cm` | 33 | 0.4 | 0.0 | 92 |
| nieve | `nieve_7d_cm` | 33 | 0.8 | 0.0 | 86 |

### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 3.7 mm | 35 (n=46) | 11 (n=46) | 8695 (n=46) | 11 (n=16) | 5 (n=16) | 4588 (n=16) |
| aluvion | `lluvia_24h_mm` | 6.9 mm | 33 (n=46) | 13 (n=46) | 5353 (n=46) | 7 (n=16) | 9 (n=16) | 2753 (n=16) |
| aluvion | `lluvia_24h_mm` | 12.1 mm | 25 (n=46) | 21 (n=46) | 2733 (n=46) | 3 (n=16) | 13 (n=16) | 1328 (n=16) |
| aluvion | `lluvia_24h_mm` | 24.4 mm | 14 (n=46) | 32 (n=46) | 762 (n=46) | 0 (n=16) | 16 (n=16) | 376 (n=16) |
| aluvion | `lluvia_48h_mm` | 9.8 mm | 35 (n=46) | 11 (n=46) | 7710 (n=46) | 7 (n=16) | 9 (n=16) | 4078 (n=16) |
| aluvion | `lluvia_48h_mm` | 17 mm | 29 (n=46) | 17 (n=46) | 4503 (n=46) | 4 (n=16) | 12 (n=16) | 2230 (n=16) |
| aluvion | `lluvia_48h_mm` | 27.5 mm | 21 (n=46) | 25 (n=46) | 2167 (n=46) | 0 (n=16) | 16 (n=16) | 1026 (n=16) |
| aluvion | `lluvia_48h_mm` | 38.9 mm | 11 (n=46) | 35 (n=46) | 1066 (n=46) | 0 (n=16) | 16 (n=16) | 453 (n=16) |
| aluvion | `lluvia_72h_mm` | 9.6 mm | 35 (n=46) | 11 (n=46) | 10696 (n=46) | 9 (n=16) | 7 (n=16) | 5745 (n=16) |
| aluvion | `lluvia_72h_mm` | 23.7 mm | 29 (n=46) | 17 (n=46) | 5031 (n=46) | 5 (n=16) | 11 (n=16) | 2506 (n=16) |
| aluvion | `lluvia_72h_mm` | 34.6 mm | 20 (n=46) | 26 (n=46) | 2878 (n=46) | 2 (n=16) | 14 (n=16) | 1367 (n=16) |
| aluvion | `lluvia_72h_mm` | 45.5 mm | 11 (n=46) | 35 (n=46) | 1706 (n=46) | 1 (n=16) | 15 (n=16) | 760 (n=16) |
| aluvion | `lluvia_7d_mm` | 27.4 mm | 35 (n=46) | 11 (n=46) | 10234 (n=46) | 8 (n=16) | 8 (n=16) | 5628 (n=16) |
| aluvion | `lluvia_7d_mm` | 36.6 mm | 30 (n=46) | 16 (n=46) | 8245 (n=46) | 7 (n=16) | 9 (n=16) | 4300 (n=16) |
| aluvion | `lluvia_7d_mm` | 65 mm | 21 (n=46) | 25 (n=46) | 3976 (n=46) | 4 (n=16) | 12 (n=16) | 1887 (n=16) |
| aluvion | `lluvia_7d_mm` | 94.6 mm | 10 (n=46) | 36 (n=46) | 1793 (n=46) | 2 (n=16) | 14 (n=16) | 758 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm` | 0.6 mm | 36 (n=46) | 10 (n=46) | 10998 (n=46) | 12 (n=16) | 4 (n=16) | 5578 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm` | 1.1 mm | 35 (n=46) | 11 (n=46) | 7049 (n=46) | 11 (n=16) | 5 (n=16) | 3564 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm` | 1.9 mm | 30 (n=46) | 16 (n=46) | 3625 (n=46) | 8 (n=16) | 8 (n=16) | 1812 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm` | 3.9 mm | 16 (n=46) | 30 (n=46) | 941 (n=46) | 1 (n=16) | 15 (n=16) | 449 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm` | 1.4 mm | 35 (n=46) | 11 (n=46) | 10002 (n=46) | 11 (n=16) | 5 (n=16) | 5299 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm` | 2 mm | 32 (n=46) | 14 (n=46) | 7095 (n=46) | 10 (n=16) | 6 (n=16) | 3579 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm` | 3.3 mm | 20 (n=46) | 26 (n=46) | 3238 (n=46) | 3 (n=16) | 13 (n=16) | 1598 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm` | 5 mm | 11 (n=46) | 35 (n=46) | 1411 (n=46) | 2 (n=16) | 14 (n=16) | 652 (n=16) |
| crecida | `lluvia_24h_mm` | 0.7 mm | 48 (n=55) | 7 (n=55) | 14762 (n=55) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 8334 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 3.6 mm | 41 (n=55) | 14 (n=55) | 8822 (n=55) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 4681 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 12.4 mm | 29 (n=55) | 26 (n=55) | 2626 (n=55) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1274 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 18.3 mm | 16 (n=55) | 39 (n=55) | 1366 (n=55) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 660 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 2.3 mm | 49 (n=55) | 6 (n=55) | 14714 (n=55) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 8015 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 6.6 mm | 42 (n=55) | 13 (n=55) | 9927 (n=55) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 5392 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 23.2 mm | 28 (n=55) | 27 (n=55) | 2877 (n=55) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1390 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 39 mm | 20 (n=55) | 35 (n=55) | 1052 (n=55) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 451 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 4.2 mm | 46 (n=55) | 9 (n=55) | 14642 (n=55) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 8096 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 13.2 mm | 40 (n=55) | 15 (n=55) | 8745 (n=55) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 4643 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 28.8 mm | 30 (n=55) | 25 (n=55) | 3794 (n=55) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1902 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 53.5 mm | 14 (n=55) | 41 (n=55) | 1117 (n=55) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 464 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 7.5 mm | 50 (n=55) | 5 (n=55) | 17350 (n=55) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 9520 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 33.4 mm | 41 (n=55) | 14 (n=55) | 8878 (n=55) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 4737 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 56.9 mm | 29 (n=55) | 26 (n=55) | 4878 (n=55) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2410 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 98.2 mm | 14 (n=55) | 41 (n=55) | 1573 (n=55) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 668 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 0.3 mm | 46 (n=55) | 9 (n=55) | 14867 (n=55) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 7775 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 0.8 mm | 39 (n=55) | 16 (n=55) | 9173 (n=55) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 4717 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 1.9 mm | 29 (n=55) | 26 (n=55) | 3623 (n=55) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 1815 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 2.7 mm | 19 (n=55) | 36 (n=55) | 1998 (n=55) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 966 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 0.5 mm | 49 (n=55) | 6 (n=55) | 17202 (n=55) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 8829 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 1.3 mm | 40 (n=55) | 15 (n=55) | 10614 (n=55) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 5595 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 3 mm | 30 (n=55) | 25 (n=55) | 3903 (n=55) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1922 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 4.6 mm | 15 (n=55) | 40 (n=55) | 1679 (n=55) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 828 (n=9 muestra chica) |
| nieve | `nieve_24h_cm` | 0.1 cm | 18 (n=33) | 15 (n=33) | 261 (n=33) | 10 (n=24) | 14 (n=24) | 110 (n=24) |
| nieve | `nieve_24h_cm` | 0.2 cm | 16 (n=33) | 17 (n=33) | 223 (n=33) | 9 (n=24) | 15 (n=24) | 98 (n=24) |
| nieve | `nieve_24h_cm` | 0.6 cm | 9 (n=33) | 24 (n=33) | 135 (n=33) | 4 (n=24) | 20 (n=24) | 55 (n=24) |
| nieve | `nieve_24h_cm` | 1.7 cm | 4 (n=33) | 29 (n=33) | 41 (n=33) | 3 (n=24) | 21 (n=24) | 16 (n=24) |
| nieve | `nieve_72h_cm` | 0.1 cm | 22 (n=33) | 11 (n=33) | 626 (n=33) | 12 (n=24) | 12 (n=24) | 235 (n=24) |
| nieve | `nieve_72h_cm` | 0.4 cm | 18 (n=33) | 15 (n=33) | 418 (n=33) | 8 (n=24) | 16 (n=24) | 177 (n=24) |
| nieve | `nieve_72h_cm` | 0.9 cm | 12 (n=33) | 21 (n=33) | 292 (n=33) | 6 (n=24) | 18 (n=24) | 105 (n=24) |
| nieve | `nieve_72h_cm` | 2.2 cm | 9 (n=33) | 24 (n=33) | 97 (n=33) | 3 (n=24) | 21 (n=24) | 40 (n=24) |
| nieve | `nieve_7d_cm` | 0.1 cm | 24 (n=33) | 9 (n=33) | 1278 (n=33) | 12 (n=24) | 12 (n=24) | 471 (n=24) |
| nieve | `nieve_7d_cm` | 0.4 cm | 20 (n=33) | 13 (n=33) | 876 (n=33) | 8 (n=24) | 16 (n=24) | 370 (n=24) |
| nieve | `nieve_7d_cm` | 1.5 cm | 12 (n=33) | 21 (n=33) | 413 (n=33) | 4 (n=24) | 20 (n=24) | 146 (n=24) |
| nieve | `nieve_7d_cm` | 2.9 cm | 7 (n=33) | 26 (n=33) | 188 (n=33) | 1 (n=24) | 23 (n=24) | 70 (n=24) |

### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm_pct` | p80 | 30 (n=46) | 16 (n=46) | 5782 (n=46) | 12 (n=16) | 4 (n=16) | 3338 (n=16) |
| aluvion | `lluvia_24h_mm_pct` | p90 | 21 (n=46) | 25 (n=46) | 3045 (n=46) | 7 (n=16) | 9 (n=16) | 1710 (n=16) |
| aluvion | `lluvia_24h_mm_pct` | p95 | 13 (n=46) | 33 (n=46) | 1587 (n=46) | 4 (n=16) | 12 (n=16) | 907 (n=16) |
| aluvion | `lluvia_24h_mm_pct` | p98 | 6 (n=46) | 40 (n=46) | 666 (n=46) | 1 (n=16) | 15 (n=16) | 385 (n=16) |
| aluvion | `lluvia_24h_mm_pct` | p99 | 3 (n=46) | 43 (n=46) | 311 (n=46) | 0 (n=16) | 16 (n=16) | 171 (n=16) |
| aluvion | `lluvia_48h_mm_pct` | p80 | 26 (n=46) | 20 (n=46) | 6060 (n=46) | 8 (n=16) | 8 (n=16) | 3339 (n=16) |
| aluvion | `lluvia_48h_mm_pct` | p90 | 12 (n=46) | 34 (n=46) | 3140 (n=46) | 7 (n=16) | 9 (n=16) | 1743 (n=16) |
| aluvion | `lluvia_48h_mm_pct` | p95 | 9 (n=46) | 37 (n=46) | 1625 (n=46) | 3 (n=16) | 13 (n=16) | 902 (n=16) |
| aluvion | `lluvia_48h_mm_pct` | p98 | 5 (n=46) | 41 (n=46) | 665 (n=46) | 2 (n=16) | 14 (n=16) | 329 (n=16) |
| aluvion | `lluvia_48h_mm_pct` | p99 | 2 (n=46) | 44 (n=46) | 309 (n=46) | 0 (n=16) | 16 (n=16) | 162 (n=16) |
| aluvion | `lluvia_72h_mm_pct` | p80 | 17 (n=46) | 29 (n=46) | 6157 (n=46) | 9 (n=16) | 7 (n=16) | 3341 (n=16) |
| aluvion | `lluvia_72h_mm_pct` | p90 | 10 (n=46) | 36 (n=46) | 3216 (n=46) | 8 (n=16) | 8 (n=16) | 1760 (n=16) |
| aluvion | `lluvia_72h_mm_pct` | p95 | 6 (n=46) | 40 (n=46) | 1648 (n=46) | 4 (n=16) | 12 (n=16) | 872 (n=16) |
| aluvion | `lluvia_72h_mm_pct` | p98 | 4 (n=46) | 42 (n=46) | 665 (n=46) | 1 (n=16) | 15 (n=16) | 293 (n=16) |
| aluvion | `lluvia_72h_mm_pct` | p99 | 2 (n=46) | 44 (n=46) | 315 (n=46) | 0 (n=16) | 16 (n=16) | 133 (n=16) |
| aluvion | `lluvia_7d_mm_pct` | p80 | 16 (n=46) | 30 (n=46) | 6431 (n=46) | 11 (n=16) | 5 (n=16) | 3535 (n=16) |
| aluvion | `lluvia_7d_mm_pct` | p90 | 9 (n=46) | 37 (n=46) | 3288 (n=46) | 9 (n=16) | 7 (n=16) | 1754 (n=16) |
| aluvion | `lluvia_7d_mm_pct` | p95 | 6 (n=46) | 40 (n=46) | 1651 (n=46) | 2 (n=16) | 14 (n=16) | 823 (n=16) |
| aluvion | `lluvia_7d_mm_pct` | p98 | 4 (n=46) | 42 (n=46) | 658 (n=46) | 2 (n=16) | 14 (n=16) | 295 (n=16) |
| aluvion | `lluvia_7d_mm_pct` | p99 | 3 (n=46) | 43 (n=46) | 305 (n=46) | 1 (n=16) | 15 (n=16) | 138 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p80 | 30 (n=46) | 16 (n=46) | 5779 (n=46) | 13 (n=16) | 3 (n=16) | 3223 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p90 | 19 (n=46) | 27 (n=46) | 3012 (n=46) | 8 (n=16) | 8 (n=16) | 1619 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p95 | 7 (n=46) | 39 (n=46) | 1587 (n=46) | 4 (n=16) | 12 (n=16) | 868 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p98 | 5 (n=46) | 41 (n=46) | 652 (n=46) | 2 (n=16) | 14 (n=16) | 311 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p99 | 1 (n=46) | 45 (n=46) | 317 (n=46) | 0 (n=16) | 16 (n=16) | 149 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p80 | 14 (n=46) | 32 (n=46) | 6085 (n=46) | 10 (n=16) | 6 (n=16) | 3195 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p90 | 7 (n=46) | 39 (n=46) | 3197 (n=46) | 7 (n=16) | 9 (n=16) | 1729 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p95 | 6 (n=46) | 40 (n=46) | 1618 (n=46) | 4 (n=16) | 12 (n=16) | 792 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p98 | 1 (n=46) | 45 (n=46) | 653 (n=46) | 2 (n=16) | 14 (n=16) | 289 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p99 | 1 (n=46) | 45 (n=46) | 305 (n=46) | 1 (n=16) | 15 (n=16) | 157 (n=16) |
| crecida | `lluvia_24h_mm_pct` | p80 | 32 (n=55) | 23 (n=55) | 5775 (n=55) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 3349 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p90 | 16 (n=55) | 39 (n=55) | 3052 (n=55) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1715 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p95 | 7 (n=55) | 48 (n=55) | 1593 (n=55) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 911 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p98 | 4 (n=55) | 51 (n=55) | 668 (n=55) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 386 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p99 | 2 (n=55) | 53 (n=55) | 312 (n=55) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 171 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p80 | 34 (n=55) | 21 (n=55) | 6052 (n=55) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3347 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p90 | 17 (n=55) | 38 (n=55) | 3139 (n=55) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1749 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p95 | 8 (n=55) | 47 (n=55) | 1629 (n=55) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 904 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p98 | 4 (n=55) | 51 (n=55) | 667 (n=55) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 330 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p99 | 3 (n=55) | 52 (n=55) | 308 (n=55) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 162 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p80 | 24 (n=55) | 31 (n=55) | 6147 (n=55) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3352 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p90 | 15 (n=55) | 40 (n=55) | 3213 (n=55) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1770 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p95 | 9 (n=55) | 46 (n=55) | 1644 (n=55) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 876 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p98 | 3 (n=55) | 52 (n=55) | 666 (n=55) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 294 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p99 | 3 (n=55) | 52 (n=55) | 313 (n=55) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 133 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p80 | 19 (n=55) | 36 (n=55) | 6427 (n=55) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 3552 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p90 | 10 (n=55) | 45 (n=55) | 3287 (n=55) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1764 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p95 | 5 (n=55) | 50 (n=55) | 1651 (n=55) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 825 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p98 | 4 (n=55) | 51 (n=55) | 656 (n=55) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 298 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p99 | 2 (n=55) | 53 (n=55) | 305 (n=55) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 140 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p80 | 27 (n=55) | 28 (n=55) | 5781 (n=55) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3232 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p90 | 13 (n=55) | 42 (n=55) | 3017 (n=55) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1627 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p95 | 5 (n=55) | 50 (n=55) | 1588 (n=55) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 873 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p98 | 4 (n=55) | 51 (n=55) | 653 (n=55) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 313 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p99 | 2 (n=55) | 53 (n=55) | 316 (n=55) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 149 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p80 | 20 (n=55) | 35 (n=55) | 6074 (n=55) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3208 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p90 | 8 (n=55) | 47 (n=55) | 3194 (n=55) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1737 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p95 | 7 (n=55) | 48 (n=55) | 1615 (n=55) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 795 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p98 | 4 (n=55) | 51 (n=55) | 648 (n=55) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 291 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p99 | 4 (n=55) | 51 (n=55) | 300 (n=55) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 158 (n=9 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p80 | 18 (n=33) | 15 (n=33) | 314 (n=33) | 12 (n=24) | 12 (n=24) | 139 (n=24) |
| nieve | `nieve_24h_cm_pct` | p90 | 17 (n=33) | 16 (n=33) | 289 (n=33) | 12 (n=24) | 12 (n=24) | 130 (n=24) |
| nieve | `nieve_24h_cm_pct` | p95 | 15 (n=33) | 18 (n=33) | 257 (n=33) | 12 (n=24) | 12 (n=24) | 111 (n=24) |
| nieve | `nieve_24h_cm_pct` | p98 | 7 (n=33) | 26 (n=33) | 182 (n=33) | 5 (n=24) | 19 (n=24) | 70 (n=24) |
| nieve | `nieve_24h_cm_pct` | p99 | 4 (n=33) | 29 (n=33) | 115 (n=33) | 5 (n=24) | 19 (n=24) | 39 (n=24) |
| nieve | `nieve_72h_cm_pct` | p80 | 23 (n=33) | 10 (n=33) | 686 (n=33) | 13 (n=24) | 11 (n=24) | 275 (n=24) |
| nieve | `nieve_72h_cm_pct` | p90 | 19 (n=33) | 14 (n=33) | 594 (n=33) | 11 (n=24) | 13 (n=24) | 236 (n=24) |
| nieve | `nieve_72h_cm_pct` | p95 | 14 (n=33) | 19 (n=33) | 444 (n=33) | 8 (n=24) | 16 (n=24) | 170 (n=24) |
| nieve | `nieve_72h_cm_pct` | p98 | 6 (n=33) | 27 (n=33) | 263 (n=33) | 5 (n=24) | 19 (n=24) | 82 (n=24) |
| nieve | `nieve_72h_cm_pct` | p99 | 3 (n=33) | 30 (n=33) | 163 (n=33) | 3 (n=24) | 21 (n=24) | 48 (n=24) |
| nieve | `nieve_7d_cm_pct` | p80 | 22 (n=33) | 11 (n=33) | 1251 (n=33) | 11 (n=24) | 13 (n=24) | 492 (n=24) |
| nieve | `nieve_7d_cm_pct` | p90 | 13 (n=33) | 20 (n=33) | 963 (n=33) | 8 (n=24) | 16 (n=24) | 361 (n=24) |
| nieve | `nieve_7d_cm_pct` | p95 | 8 (n=33) | 25 (n=33) | 656 (n=33) | 6 (n=24) | 18 (n=24) | 212 (n=24) |
| nieve | `nieve_7d_cm_pct` | p98 | 3 (n=33) | 30 (n=33) | 358 (n=33) | 3 (n=24) | 21 (n=24) | 100 (n=24) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=33) | 32 (n=33) | 181 (n=33) | 2 (n=24) | 22 (n=24) | 66 (n=24) |

### Variante: aluvión + crecida = lluvia

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 93 | 11.5 | 2.0 | 78 |
| lluvia | `lluvia_48h_mm` | 93 | 23.8 | 5.2 | 80 |
| lluvia | `lluvia_72h_mm` | 93 | 30.1 | 9.0 | 76 |
| lluvia | `lluvia_7d_mm` | 93 | 61.3 | 26.0 | 65 |
| lluvia | `lluvia_max_horaria_24h_mm` | 93 | 1.8 | 0.5 | 74 |
| lluvia | `lluvia_max_horaria_72h_mm` | 93 | 3.0 | 1.2 | 74 |
| nieve | `nieve_24h_cm` | 33 | 0.0 | 0.0 | 48 |
| nieve | `nieve_72h_cm` | 33 | 0.4 | 0.0 | 92 |
| nieve | `nieve_7d_cm` | 33 | 0.8 | 0.0 | 86 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 2.2 mm | 82 (n=101) | 19 (n=101) | 10996 (n=101) | 18 (n=25) | 7 (n=25) | 5961 (n=25) |
| lluvia | `lluvia_24h_mm` | 4.5 mm | 74 (n=101) | 27 (n=101) | 7593 (n=101) | 15 (n=25) | 10 (n=25) | 4044 (n=25) |
| lluvia | `lluvia_24h_mm` | 12.1 mm | 54 (n=101) | 47 (n=101) | 2691 (n=101) | 5 (n=25) | 20 (n=25) | 1325 (n=25) |
| lluvia | `lluvia_24h_mm` | 21.6 mm | 32 (n=101) | 69 (n=101) | 967 (n=101) | 1 (n=25) | 24 (n=25) | 488 (n=25) |
| lluvia | `lluvia_48h_mm` | 2.7 mm | 83 (n=101) | 18 (n=101) | 14031 (n=101) | 21 (n=25) | 4 (n=25) | 7689 (n=25) |
| lluvia | `lluvia_48h_mm` | 10.5 mm | 75 (n=101) | 26 (n=101) | 7219 (n=101) | 11 (n=25) | 14 (n=25) | 3833 (n=25) |
| lluvia | `lluvia_48h_mm` | 24.7 mm | 49 (n=101) | 52 (n=101) | 2569 (n=101) | 1 (n=25) | 24 (n=25) | 1256 (n=25) |
| lluvia | `lluvia_48h_mm` | 39 mm | 30 (n=101) | 71 (n=101) | 1038 (n=101) | 1 (n=25) | 24 (n=25) | 451 (n=25) |
| lluvia | `lluvia_72h_mm` | 4.7 mm | 82 (n=101) | 19 (n=101) | 14082 (n=101) | 20 (n=25) | 5 (n=25) | 7812 (n=25) |
| lluvia | `lluvia_72h_mm` | 19 mm | 70 (n=101) | 31 (n=101) | 6365 (n=101) | 9 (n=25) | 16 (n=25) | 3315 (n=25) |
| lluvia | `lluvia_72h_mm` | 33.9 mm | 49 (n=101) | 52 (n=101) | 2962 (n=101) | 4 (n=25) | 21 (n=25) | 1411 (n=25) |
| lluvia | `lluvia_72h_mm` | 52.5 mm | 26 (n=101) | 75 (n=101) | 1179 (n=101) | 2 (n=25) | 23 (n=25) | 502 (n=25) |
| lluvia | `lluvia_7d_mm` | 8 mm | 86 (n=101) | 15 (n=101) | 16948 (n=101) | 21 (n=25) | 4 (n=25) | 9357 (n=25) |
| lluvia | `lluvia_7d_mm` | 33.6 mm | 71 (n=101) | 30 (n=101) | 8787 (n=101) | 11 (n=25) | 14 (n=25) | 4700 (n=25) |
| lluvia | `lluvia_7d_mm` | 63.2 mm | 48 (n=101) | 53 (n=101) | 4094 (n=101) | 6 (n=25) | 19 (n=25) | 2005 (n=25) |
| lluvia | `lluvia_7d_mm` | 96 mm | 24 (n=101) | 77 (n=101) | 1696 (n=101) | 3 (n=25) | 22 (n=25) | 705 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm` | 0.5 mm | 80 (n=101) | 21 (n=101) | 12070 (n=101) | 22 (n=25) | 3 (n=25) | 6143 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm` | 0.9 mm | 72 (n=101) | 29 (n=101) | 8353 (n=101) | 17 (n=25) | 8 (n=25) | 4344 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm` | 1.9 mm | 59 (n=101) | 42 (n=101) | 3581 (n=101) | 13 (n=25) | 12 (n=25) | 1807 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm` | 3.9 mm | 31 (n=101) | 70 (n=101) | 925 (n=101) | 1 (n=25) | 24 (n=25) | 449 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm` | 0.7 mm | 83 (n=101) | 18 (n=101) | 14901 (n=101) | 20 (n=25) | 5 (n=25) | 7807 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm` | 1.9 mm | 69 (n=101) | 32 (n=101) | 7476 (n=101) | 16 (n=25) | 9 (n=25) | 3853 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm` | 3.1 mm | 49 (n=101) | 52 (n=101) | 3613 (n=101) | 5 (n=25) | 20 (n=25) | 1766 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm` | 4.8 mm | 24 (n=101) | 77 (n=101) | 1530 (n=101) | 2 (n=25) | 23 (n=25) | 748 (n=25) |
| nieve | `nieve_24h_cm` | 0.1 cm | 18 (n=33) | 15 (n=33) | 261 (n=33) | 10 (n=24) | 14 (n=24) | 110 (n=24) |
| nieve | `nieve_24h_cm` | 0.2 cm | 16 (n=33) | 17 (n=33) | 223 (n=33) | 9 (n=24) | 15 (n=24) | 98 (n=24) |
| nieve | `nieve_24h_cm` | 0.6 cm | 9 (n=33) | 24 (n=33) | 135 (n=33) | 4 (n=24) | 20 (n=24) | 55 (n=24) |
| nieve | `nieve_24h_cm` | 1.7 cm | 4 (n=33) | 29 (n=33) | 41 (n=33) | 3 (n=24) | 21 (n=24) | 16 (n=24) |
| nieve | `nieve_72h_cm` | 0.1 cm | 22 (n=33) | 11 (n=33) | 626 (n=33) | 12 (n=24) | 12 (n=24) | 235 (n=24) |
| nieve | `nieve_72h_cm` | 0.4 cm | 18 (n=33) | 15 (n=33) | 418 (n=33) | 8 (n=24) | 16 (n=24) | 177 (n=24) |
| nieve | `nieve_72h_cm` | 0.9 cm | 12 (n=33) | 21 (n=33) | 292 (n=33) | 6 (n=24) | 18 (n=24) | 105 (n=24) |
| nieve | `nieve_72h_cm` | 2.2 cm | 9 (n=33) | 24 (n=33) | 97 (n=33) | 3 (n=24) | 21 (n=24) | 40 (n=24) |
| nieve | `nieve_7d_cm` | 0.1 cm | 24 (n=33) | 9 (n=33) | 1278 (n=33) | 12 (n=24) | 12 (n=24) | 471 (n=24) |
| nieve | `nieve_7d_cm` | 0.4 cm | 20 (n=33) | 13 (n=33) | 876 (n=33) | 8 (n=24) | 16 (n=24) | 370 (n=24) |
| nieve | `nieve_7d_cm` | 1.5 cm | 12 (n=33) | 21 (n=33) | 413 (n=33) | 4 (n=24) | 20 (n=24) | 146 (n=24) |
| nieve | `nieve_7d_cm` | 2.9 cm | 7 (n=33) | 26 (n=33) | 188 (n=33) | 1 (n=24) | 23 (n=24) | 70 (n=24) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm_pct` | p80 | 62 (n=101) | 39 (n=101) | 5738 (n=101) | 16 (n=25) | 9 (n=25) | 3332 (n=25) |
| lluvia | `lluvia_24h_mm_pct` | p90 | 37 (n=101) | 64 (n=101) | 3027 (n=101) | 9 (n=25) | 16 (n=25) | 1706 (n=25) |
| lluvia | `lluvia_24h_mm_pct` | p95 | 20 (n=101) | 81 (n=101) | 1578 (n=101) | 5 (n=25) | 20 (n=25) | 906 (n=25) |
| lluvia | `lluvia_24h_mm_pct` | p98 | 10 (n=101) | 91 (n=101) | 662 (n=101) | 1 (n=25) | 24 (n=25) | 385 (n=25) |
| lluvia | `lluvia_24h_mm_pct` | p99 | 5 (n=101) | 96 (n=101) | 309 (n=101) | 0 (n=25) | 25 (n=25) | 171 (n=25) |
| lluvia | `lluvia_48h_mm_pct` | p80 | 60 (n=101) | 41 (n=101) | 6017 (n=101) | 11 (n=25) | 14 (n=25) | 3333 (n=25) |
| lluvia | `lluvia_48h_mm_pct` | p90 | 29 (n=101) | 72 (n=101) | 3120 (n=101) | 9 (n=25) | 16 (n=25) | 1739 (n=25) |
| lluvia | `lluvia_48h_mm_pct` | p95 | 17 (n=101) | 84 (n=101) | 1616 (n=101) | 5 (n=25) | 20 (n=25) | 900 (n=25) |
| lluvia | `lluvia_48h_mm_pct` | p98 | 9 (n=101) | 92 (n=101) | 661 (n=101) | 3 (n=25) | 22 (n=25) | 328 (n=25) |
| lluvia | `lluvia_48h_mm_pct` | p99 | 5 (n=101) | 96 (n=101) | 306 (n=101) | 0 (n=25) | 25 (n=25) | 162 (n=25) |
| lluvia | `lluvia_72h_mm_pct` | p80 | 41 (n=101) | 60 (n=101) | 6120 (n=101) | 12 (n=25) | 13 (n=25) | 3336 (n=25) |
| lluvia | `lluvia_72h_mm_pct` | p90 | 25 (n=101) | 76 (n=101) | 3196 (n=101) | 10 (n=25) | 15 (n=25) | 1757 (n=25) |
| lluvia | `lluvia_72h_mm_pct` | p95 | 15 (n=101) | 86 (n=101) | 1636 (n=101) | 5 (n=25) | 20 (n=25) | 870 (n=25) |
| lluvia | `lluvia_72h_mm_pct` | p98 | 7 (n=101) | 94 (n=101) | 660 (n=101) | 1 (n=25) | 24 (n=25) | 293 (n=25) |
| lluvia | `lluvia_72h_mm_pct` | p99 | 5 (n=101) | 96 (n=101) | 311 (n=101) | 0 (n=25) | 25 (n=25) | 133 (n=25) |
| lluvia | `lluvia_7d_mm_pct` | p80 | 35 (n=101) | 66 (n=101) | 6399 (n=101) | 13 (n=25) | 12 (n=25) | 3531 (n=25) |
| lluvia | `lluvia_7d_mm_pct` | p90 | 19 (n=101) | 82 (n=101) | 3274 (n=101) | 11 (n=25) | 14 (n=25) | 1750 (n=25) |
| lluvia | `lluvia_7d_mm_pct` | p95 | 11 (n=101) | 90 (n=101) | 1643 (n=101) | 3 (n=25) | 22 (n=25) | 821 (n=25) |
| lluvia | `lluvia_7d_mm_pct` | p98 | 8 (n=101) | 93 (n=101) | 652 (n=101) | 2 (n=25) | 23 (n=25) | 295 (n=25) |
| lluvia | `lluvia_7d_mm_pct` | p99 | 5 (n=101) | 96 (n=101) | 303 (n=101) | 1 (n=25) | 24 (n=25) | 138 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p80 | 57 (n=101) | 44 (n=101) | 5742 (n=101) | 20 (n=25) | 5 (n=25) | 3215 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p90 | 32 (n=101) | 69 (n=101) | 2996 (n=101) | 10 (n=25) | 15 (n=25) | 1616 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p95 | 12 (n=101) | 89 (n=101) | 1580 (n=101) | 4 (n=25) | 21 (n=25) | 868 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p98 | 9 (n=101) | 92 (n=101) | 648 (n=101) | 2 (n=25) | 23 (n=25) | 311 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p99 | 3 (n=101) | 98 (n=101) | 315 (n=101) | 0 (n=25) | 25 (n=25) | 149 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p80 | 34 (n=101) | 67 (n=101) | 6051 (n=101) | 13 (n=25) | 12 (n=25) | 3191 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p90 | 15 (n=101) | 86 (n=101) | 3184 (n=101) | 8 (n=25) | 17 (n=25) | 1727 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p95 | 13 (n=101) | 88 (n=101) | 1607 (n=101) | 5 (n=25) | 20 (n=25) | 790 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p98 | 5 (n=101) | 96 (n=101) | 647 (n=101) | 2 (n=25) | 23 (n=25) | 289 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p99 | 5 (n=101) | 96 (n=101) | 299 (n=101) | 1 (n=25) | 24 (n=25) | 157 (n=25) |
| nieve | `nieve_24h_cm_pct` | p80 | 18 (n=33) | 15 (n=33) | 314 (n=33) | 12 (n=24) | 12 (n=24) | 139 (n=24) |
| nieve | `nieve_24h_cm_pct` | p90 | 17 (n=33) | 16 (n=33) | 289 (n=33) | 12 (n=24) | 12 (n=24) | 130 (n=24) |
| nieve | `nieve_24h_cm_pct` | p95 | 15 (n=33) | 18 (n=33) | 257 (n=33) | 12 (n=24) | 12 (n=24) | 111 (n=24) |
| nieve | `nieve_24h_cm_pct` | p98 | 7 (n=33) | 26 (n=33) | 182 (n=33) | 5 (n=24) | 19 (n=24) | 70 (n=24) |
| nieve | `nieve_24h_cm_pct` | p99 | 4 (n=33) | 29 (n=33) | 115 (n=33) | 5 (n=24) | 19 (n=24) | 39 (n=24) |
| nieve | `nieve_72h_cm_pct` | p80 | 23 (n=33) | 10 (n=33) | 686 (n=33) | 13 (n=24) | 11 (n=24) | 275 (n=24) |
| nieve | `nieve_72h_cm_pct` | p90 | 19 (n=33) | 14 (n=33) | 594 (n=33) | 11 (n=24) | 13 (n=24) | 236 (n=24) |
| nieve | `nieve_72h_cm_pct` | p95 | 14 (n=33) | 19 (n=33) | 444 (n=33) | 8 (n=24) | 16 (n=24) | 170 (n=24) |
| nieve | `nieve_72h_cm_pct` | p98 | 6 (n=33) | 27 (n=33) | 263 (n=33) | 5 (n=24) | 19 (n=24) | 82 (n=24) |
| nieve | `nieve_72h_cm_pct` | p99 | 3 (n=33) | 30 (n=33) | 163 (n=33) | 3 (n=24) | 21 (n=24) | 48 (n=24) |
| nieve | `nieve_7d_cm_pct` | p80 | 22 (n=33) | 11 (n=33) | 1251 (n=33) | 11 (n=24) | 13 (n=24) | 492 (n=24) |
| nieve | `nieve_7d_cm_pct` | p90 | 13 (n=33) | 20 (n=33) | 963 (n=33) | 8 (n=24) | 16 (n=24) | 361 (n=24) |
| nieve | `nieve_7d_cm_pct` | p95 | 8 (n=33) | 25 (n=33) | 656 (n=33) | 6 (n=24) | 18 (n=24) | 212 (n=24) |
| nieve | `nieve_7d_cm_pct` | p98 | 3 (n=33) | 30 (n=33) | 358 (n=33) | 3 (n=24) | 21 (n=24) | 100 (n=24) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=33) | 32 (n=33) | 181 (n=33) | 2 (n=24) | 22 (n=24) | 66 (n=24) |

## Todas las fuentes: nieve en Paso de Jama por lado

Eventos de nieve en `rn52_paso_jama`: 57 (AR 1, ambos 9, CL 42, lado desconocido 5, que quedan fuera de esta sección).

Falta el clima de `ch27_alto`: CL y combinado quedan sin datos.

### Nieve AR o ambos (clima de rn52_paso_jama)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 5 | 0.0 | 0.0 | 48 |
| nieve | `nieve_72h_cm` | 5 | 0.1 | 0.0 | 91 |
| nieve | `nieve_7d_cm` | 5 | 0.1 | 0.0 | 83 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 1 (n=5) | 4 (n=5) | 142 (n=5) | 3 (n=5 muestra chica) | 2 (n=5 muestra chica) | 79 (n=5 muestra chica) |
| nieve | `nieve_72h_cm` | 0.1 cm | 3 (n=5) | 2 (n=5) | 304 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 155 (n=5 muestra chica) |
| nieve | `nieve_72h_cm` | 0.2 cm | 1 (n=5) | 4 (n=5) | 275 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 148 (n=5 muestra chica) |
| nieve | `nieve_7d_cm` | 0.1 cm | 3 (n=5) | 2 (n=5) | 552 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 283 (n=5 muestra chica) |
| nieve | `nieve_7d_cm` | 0.2 cm | 1 (n=5) | 4 (n=5) | 505 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 274 (n=5 muestra chica) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 1 (n=5) | 4 (n=5) | 168 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 91 (n=5 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p90 | 1 (n=5) | 4 (n=5) | 141 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 82 (n=5 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p95 | 1 (n=5) | 4 (n=5) | 106 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 63 (n=5 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=5) | 5 (n=5) | 53 (n=5) | 3 (n=5 muestra chica) | 2 (n=5 muestra chica) | 32 (n=5 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=5) | 5 (n=5) | 24 (n=5) | 3 (n=5 muestra chica) | 2 (n=5 muestra chica) | 19 (n=5 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p80 | 3 (n=5) | 2 (n=5) | 307 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 152 (n=5 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p90 | 3 (n=5) | 2 (n=5) | 221 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 114 (n=5 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=5) | 5 (n=5) | 126 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 76 (n=5 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=5) | 5 (n=5) | 52 (n=5) | 2 (n=5 muestra chica) | 3 (n=5 muestra chica) | 31 (n=5 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=5) | 5 (n=5) | 26 (n=5) | 1 (n=5 muestra chica) | 4 (n=5 muestra chica) | 17 (n=5 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p80 | 3 (n=5) | 2 (n=5) | 437 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 219 (n=5 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=5) | 5 (n=5) | 262 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 149 (n=5 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=5) | 5 (n=5) | 129 (n=5) | 3 (n=5 muestra chica) | 2 (n=5 muestra chica) | 89 (n=5 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=5) | 5 (n=5) | 53 (n=5) | 1 (n=5 muestra chica) | 4 (n=5 muestra chica) | 40 (n=5 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=5) | 5 (n=5) | 27 (n=5) | 1 (n=5 muestra chica) | 4 (n=5 muestra chica) | 27 (n=5 muestra chica) |

### Nieve CL (clima de ch27_alto)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0 | — | — | — |
| nieve | `nieve_72h_cm` | 0 | — | — | — |
| nieve | `nieve_7d_cm` | 0 | — | — | — |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

Sin candidatos (no hay eventos de esta causa con punto en el período de ajuste).

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 0 (n=28) | 28 (n=28) | 0 (n=28) | 0 (n=14) | 14 (n=14) | 0 (n=14) |
| nieve | `nieve_24h_cm_pct` | p90 | 0 (n=28) | 28 (n=28) | 0 (n=28) | 0 (n=14) | 14 (n=14) | 0 (n=14) |
| nieve | `nieve_24h_cm_pct` | p95 | 0 (n=28) | 28 (n=28) | 0 (n=28) | 0 (n=14) | 14 (n=14) | 0 (n=14) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=28) | 28 (n=28) | 0 (n=28) | 0 (n=14) | 14 (n=14) | 0 (n=14) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=28) | 28 (n=28) | 0 (n=28) | 0 (n=14) | 14 (n=14) | 0 (n=14) |
| nieve | `nieve_72h_cm_pct` | p80 | 0 (n=28) | 28 (n=28) | 0 (n=28) | 0 (n=14) | 14 (n=14) | 0 (n=14) |
| nieve | `nieve_72h_cm_pct` | p90 | 0 (n=28) | 28 (n=28) | 0 (n=28) | 0 (n=14) | 14 (n=14) | 0 (n=14) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=28) | 28 (n=28) | 0 (n=28) | 0 (n=14) | 14 (n=14) | 0 (n=14) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=28) | 28 (n=28) | 0 (n=28) | 0 (n=14) | 14 (n=14) | 0 (n=14) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=28) | 28 (n=28) | 0 (n=28) | 0 (n=14) | 14 (n=14) | 0 (n=14) |
| nieve | `nieve_7d_cm_pct` | p80 | 0 (n=28) | 28 (n=28) | 0 (n=28) | 0 (n=14) | 14 (n=14) | 0 (n=14) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=28) | 28 (n=28) | 0 (n=28) | 0 (n=14) | 14 (n=14) | 0 (n=14) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=28) | 28 (n=28) | 0 (n=28) | 0 (n=14) | 14 (n=14) | 0 (n=14) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=28) | 28 (n=28) | 0 (n=28) | 0 (n=14) | 14 (n=14) | 0 (n=14) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=28) | 28 (n=28) | 0 (n=28) | 0 (n=14) | 14 (n=14) | 0 (n=14) |

### Nieve combinado (AR + ambos + CL)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 5 | 0.0 | 0.0 | 48 |
| nieve | `nieve_72h_cm` | 5 | 0.1 | 0.0 | 91 |
| nieve | `nieve_7d_cm` | 5 | 0.1 | 0.0 | 83 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 1 (n=33) | 32 (n=33) | 142 (n=33) | 3 (n=19) | 16 (n=19) | 79 (n=19) |
| nieve | `nieve_72h_cm` | 0.1 cm | 3 (n=33) | 30 (n=33) | 304 (n=33) | 4 (n=19) | 15 (n=19) | 155 (n=19) |
| nieve | `nieve_72h_cm` | 0.2 cm | 1 (n=33) | 32 (n=33) | 275 (n=33) | 4 (n=19) | 15 (n=19) | 148 (n=19) |
| nieve | `nieve_7d_cm` | 0.1 cm | 3 (n=33) | 30 (n=33) | 552 (n=33) | 4 (n=19) | 15 (n=19) | 283 (n=19) |
| nieve | `nieve_7d_cm` | 0.2 cm | 1 (n=33) | 32 (n=33) | 505 (n=33) | 4 (n=19) | 15 (n=19) | 274 (n=19) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 1 (n=33) | 32 (n=33) | 168 (n=33) | 4 (n=19) | 15 (n=19) | 91 (n=19) |
| nieve | `nieve_24h_cm_pct` | p90 | 1 (n=33) | 32 (n=33) | 141 (n=33) | 4 (n=19) | 15 (n=19) | 82 (n=19) |
| nieve | `nieve_24h_cm_pct` | p95 | 1 (n=33) | 32 (n=33) | 106 (n=33) | 4 (n=19) | 15 (n=19) | 63 (n=19) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=33) | 33 (n=33) | 53 (n=33) | 3 (n=19) | 16 (n=19) | 32 (n=19) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=33) | 33 (n=33) | 24 (n=33) | 3 (n=19) | 16 (n=19) | 19 (n=19) |
| nieve | `nieve_72h_cm_pct` | p80 | 3 (n=33) | 30 (n=33) | 307 (n=33) | 4 (n=19) | 15 (n=19) | 152 (n=19) |
| nieve | `nieve_72h_cm_pct` | p90 | 3 (n=33) | 30 (n=33) | 221 (n=33) | 4 (n=19) | 15 (n=19) | 114 (n=19) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=33) | 33 (n=33) | 126 (n=33) | 4 (n=19) | 15 (n=19) | 76 (n=19) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=33) | 33 (n=33) | 52 (n=33) | 2 (n=19) | 17 (n=19) | 31 (n=19) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=33) | 33 (n=33) | 26 (n=33) | 1 (n=19) | 18 (n=19) | 17 (n=19) |
| nieve | `nieve_7d_cm_pct` | p80 | 3 (n=33) | 30 (n=33) | 437 (n=33) | 4 (n=19) | 15 (n=19) | 219 (n=19) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=33) | 33 (n=33) | 262 (n=33) | 4 (n=19) | 15 (n=19) | 149 (n=19) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=33) | 33 (n=33) | 129 (n=33) | 3 (n=19) | 16 (n=19) | 89 (n=19) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=33) | 33 (n=33) | 53 (n=33) | 1 (n=19) | 18 (n=19) | 40 (n=19) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=33) | 33 (n=33) | 27 (n=33) | 1 (n=19) | 18 (n=19) | 27 (n=19) |


## Solo fuentes estables: nieve en Paso de Jama por lado

Eventos de nieve en `rn52_paso_jama`: 54 (AR 1, ambos 9, CL 40, lado desconocido 4, que quedan fuera de esta sección).

Falta el clima de `ch27_alto`: CL y combinado quedan sin datos.

### Nieve AR o ambos (clima de rn52_paso_jama)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 5 | 0.0 | 0.0 | 48 |
| nieve | `nieve_72h_cm` | 5 | 0.1 | 0.0 | 91 |
| nieve | `nieve_7d_cm` | 5 | 0.1 | 0.0 | 83 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 1 (n=5) | 4 (n=5) | 142 (n=5) | 3 (n=5 muestra chica) | 2 (n=5 muestra chica) | 79 (n=5 muestra chica) |
| nieve | `nieve_72h_cm` | 0.1 cm | 3 (n=5) | 2 (n=5) | 304 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 155 (n=5 muestra chica) |
| nieve | `nieve_72h_cm` | 0.2 cm | 1 (n=5) | 4 (n=5) | 275 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 148 (n=5 muestra chica) |
| nieve | `nieve_7d_cm` | 0.1 cm | 3 (n=5) | 2 (n=5) | 552 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 283 (n=5 muestra chica) |
| nieve | `nieve_7d_cm` | 0.2 cm | 1 (n=5) | 4 (n=5) | 505 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 274 (n=5 muestra chica) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 1 (n=5) | 4 (n=5) | 168 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 91 (n=5 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p90 | 1 (n=5) | 4 (n=5) | 141 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 82 (n=5 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p95 | 1 (n=5) | 4 (n=5) | 106 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 63 (n=5 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=5) | 5 (n=5) | 53 (n=5) | 3 (n=5 muestra chica) | 2 (n=5 muestra chica) | 32 (n=5 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=5) | 5 (n=5) | 24 (n=5) | 3 (n=5 muestra chica) | 2 (n=5 muestra chica) | 19 (n=5 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p80 | 3 (n=5) | 2 (n=5) | 307 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 152 (n=5 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p90 | 3 (n=5) | 2 (n=5) | 221 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 114 (n=5 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=5) | 5 (n=5) | 126 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 76 (n=5 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=5) | 5 (n=5) | 52 (n=5) | 2 (n=5 muestra chica) | 3 (n=5 muestra chica) | 31 (n=5 muestra chica) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=5) | 5 (n=5) | 26 (n=5) | 1 (n=5 muestra chica) | 4 (n=5 muestra chica) | 17 (n=5 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p80 | 3 (n=5) | 2 (n=5) | 437 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 219 (n=5 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=5) | 5 (n=5) | 262 (n=5) | 4 (n=5 muestra chica) | 1 (n=5 muestra chica) | 149 (n=5 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=5) | 5 (n=5) | 129 (n=5) | 3 (n=5 muestra chica) | 2 (n=5 muestra chica) | 89 (n=5 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=5) | 5 (n=5) | 53 (n=5) | 1 (n=5 muestra chica) | 4 (n=5 muestra chica) | 40 (n=5 muestra chica) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=5) | 5 (n=5) | 27 (n=5) | 1 (n=5 muestra chica) | 4 (n=5 muestra chica) | 27 (n=5 muestra chica) |

### Nieve CL (clima de ch27_alto)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0 | — | — | — |
| nieve | `nieve_72h_cm` | 0 | — | — | — |
| nieve | `nieve_7d_cm` | 0 | — | — | — |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

Sin candidatos (no hay eventos de esta causa con punto en el período de ajuste).

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 0 (n=27) | 27 (n=27) | 0 (n=27) | 0 (n=13) | 13 (n=13) | 0 (n=13) |
| nieve | `nieve_24h_cm_pct` | p90 | 0 (n=27) | 27 (n=27) | 0 (n=27) | 0 (n=13) | 13 (n=13) | 0 (n=13) |
| nieve | `nieve_24h_cm_pct` | p95 | 0 (n=27) | 27 (n=27) | 0 (n=27) | 0 (n=13) | 13 (n=13) | 0 (n=13) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=27) | 27 (n=27) | 0 (n=27) | 0 (n=13) | 13 (n=13) | 0 (n=13) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=27) | 27 (n=27) | 0 (n=27) | 0 (n=13) | 13 (n=13) | 0 (n=13) |
| nieve | `nieve_72h_cm_pct` | p80 | 0 (n=27) | 27 (n=27) | 0 (n=27) | 0 (n=13) | 13 (n=13) | 0 (n=13) |
| nieve | `nieve_72h_cm_pct` | p90 | 0 (n=27) | 27 (n=27) | 0 (n=27) | 0 (n=13) | 13 (n=13) | 0 (n=13) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=27) | 27 (n=27) | 0 (n=27) | 0 (n=13) | 13 (n=13) | 0 (n=13) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=27) | 27 (n=27) | 0 (n=27) | 0 (n=13) | 13 (n=13) | 0 (n=13) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=27) | 27 (n=27) | 0 (n=27) | 0 (n=13) | 13 (n=13) | 0 (n=13) |
| nieve | `nieve_7d_cm_pct` | p80 | 0 (n=27) | 27 (n=27) | 0 (n=27) | 0 (n=13) | 13 (n=13) | 0 (n=13) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=27) | 27 (n=27) | 0 (n=27) | 0 (n=13) | 13 (n=13) | 0 (n=13) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=27) | 27 (n=27) | 0 (n=27) | 0 (n=13) | 13 (n=13) | 0 (n=13) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=27) | 27 (n=27) | 0 (n=27) | 0 (n=13) | 13 (n=13) | 0 (n=13) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=27) | 27 (n=27) | 0 (n=27) | 0 (n=13) | 13 (n=13) | 0 (n=13) |

### Nieve combinado (AR + ambos + CL)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 5 | 0.0 | 0.0 | 48 |
| nieve | `nieve_72h_cm` | 5 | 0.1 | 0.0 | 91 |
| nieve | `nieve_7d_cm` | 5 | 0.1 | 0.0 | 83 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 1 (n=32) | 31 (n=32) | 142 (n=32) | 3 (n=18) | 15 (n=18) | 79 (n=18) |
| nieve | `nieve_72h_cm` | 0.1 cm | 3 (n=32) | 29 (n=32) | 304 (n=32) | 4 (n=18) | 14 (n=18) | 155 (n=18) |
| nieve | `nieve_72h_cm` | 0.2 cm | 1 (n=32) | 31 (n=32) | 275 (n=32) | 4 (n=18) | 14 (n=18) | 148 (n=18) |
| nieve | `nieve_7d_cm` | 0.1 cm | 3 (n=32) | 29 (n=32) | 552 (n=32) | 4 (n=18) | 14 (n=18) | 283 (n=18) |
| nieve | `nieve_7d_cm` | 0.2 cm | 1 (n=32) | 31 (n=32) | 505 (n=32) | 4 (n=18) | 14 (n=18) | 274 (n=18) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 1 (n=32) | 31 (n=32) | 168 (n=32) | 4 (n=18) | 14 (n=18) | 91 (n=18) |
| nieve | `nieve_24h_cm_pct` | p90 | 1 (n=32) | 31 (n=32) | 141 (n=32) | 4 (n=18) | 14 (n=18) | 82 (n=18) |
| nieve | `nieve_24h_cm_pct` | p95 | 1 (n=32) | 31 (n=32) | 106 (n=32) | 4 (n=18) | 14 (n=18) | 63 (n=18) |
| nieve | `nieve_24h_cm_pct` | p98 | 0 (n=32) | 32 (n=32) | 53 (n=32) | 3 (n=18) | 15 (n=18) | 32 (n=18) |
| nieve | `nieve_24h_cm_pct` | p99 | 0 (n=32) | 32 (n=32) | 24 (n=32) | 3 (n=18) | 15 (n=18) | 19 (n=18) |
| nieve | `nieve_72h_cm_pct` | p80 | 3 (n=32) | 29 (n=32) | 307 (n=32) | 4 (n=18) | 14 (n=18) | 152 (n=18) |
| nieve | `nieve_72h_cm_pct` | p90 | 3 (n=32) | 29 (n=32) | 221 (n=32) | 4 (n=18) | 14 (n=18) | 114 (n=18) |
| nieve | `nieve_72h_cm_pct` | p95 | 0 (n=32) | 32 (n=32) | 126 (n=32) | 4 (n=18) | 14 (n=18) | 76 (n=18) |
| nieve | `nieve_72h_cm_pct` | p98 | 0 (n=32) | 32 (n=32) | 52 (n=32) | 2 (n=18) | 16 (n=18) | 31 (n=18) |
| nieve | `nieve_72h_cm_pct` | p99 | 0 (n=32) | 32 (n=32) | 26 (n=32) | 1 (n=18) | 17 (n=18) | 17 (n=18) |
| nieve | `nieve_7d_cm_pct` | p80 | 3 (n=32) | 29 (n=32) | 437 (n=32) | 4 (n=18) | 14 (n=18) | 219 (n=18) |
| nieve | `nieve_7d_cm_pct` | p90 | 0 (n=32) | 32 (n=32) | 262 (n=32) | 4 (n=18) | 14 (n=18) | 149 (n=18) |
| nieve | `nieve_7d_cm_pct` | p95 | 0 (n=32) | 32 (n=32) | 129 (n=32) | 3 (n=18) | 15 (n=18) | 89 (n=18) |
| nieve | `nieve_7d_cm_pct` | p98 | 0 (n=32) | 32 (n=32) | 53 (n=32) | 1 (n=18) | 17 (n=18) | 40 (n=18) |
| nieve | `nieve_7d_cm_pct` | p99 | 0 (n=32) | 32 (n=32) | 27 (n=32) | 1 (n=18) | 17 (n=18) | 27 (n=18) |

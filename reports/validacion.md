# Validación de umbrales

> Generado: 2026-11-15 15:10 UTC · versión `0.1.0.dev0` · commit `36b5484` · SCHEMA_VERSION 3 · fuentes `b3dab32ad1adf821`

Causas meteorológicas: aluvión y crecida contra lluvia, nieve contra nieve. Una regla por causa, igual para todos los puntos; ajuste 2016–2022, prueba 2023→hoy. Acierto = evento con alarma ese día o el anterior; falsa alarma = día con alarma sin evento ese día o el siguiente. Los mm de ERA5 no son lluvia local (ver docs/DATOS.md): por eso cada variable va también como percentil de su celda en la misma estación. Cada sección trae también la variante con aluvión y crecida juntos como una sola causa "lluvia". Junto a cada número va n = días-evento (punto, fecha) del período en que se basa; en prueba, n < 10 se marca "muestra chica". Vos elegís la regla final.

Fuentes estables (archivo desde ≤ 2016-01-01): elsubmarino, eltribunojujuy, jujuyaldia, jujuyalmomento, todojujuy.

## Todas las fuentes

Eventos con punto crítico usados: aluvión 65, crecida 67 (lluvia 132), nieve 64.

### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 48 | 10.4 | 3.1 | 74 |
| aluvion | `lluvia_48h_mm` | 48 | 27.5 | 7.6 | 84 |
| aluvion | `lluvia_72h_mm` | 48 | 36.8 | 13.1 | 75 |
| aluvion | `lluvia_7d_mm` | 48 | 62.8 | 36.9 | 63 |
| aluvion | `lluvia_max_horaria_24h_mm` | 48 | 1.8 | 0.7 | 80 |
| aluvion | `lluvia_max_horaria_72h_mm` | 48 | 3.4 | 1.5 | 77 |
| crecida | `lluvia_24h_mm` | 58 | 11.1 | 2.4 | 78 |
| crecida | `lluvia_48h_mm` | 58 | 19.6 | 6.2 | 75 |
| crecida | `lluvia_72h_mm` | 58 | 27.3 | 10.9 | 75 |
| crecida | `lluvia_7d_mm` | 58 | 54.3 | 32.0 | 62 |
| crecida | `lluvia_max_horaria_24h_mm` | 58 | 1.6 | 0.6 | 71 |
| crecida | `lluvia_max_horaria_72h_mm` | 58 | 2.8 | 1.3 | 72 |
| nieve | `nieve_24h_cm` | 37 | 0.0 | 0.0 | 48 |
| nieve | `nieve_72h_cm` | 37 | 0.1 | 0.0 | 89 |
| nieve | `nieve_7d_cm` | 37 | 0.4 | 0.0 | 83 |

### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 3.2 mm | 42 (n=48) | 6 (n=48) | 11618 (n=48) | 14 (n=17) | 3 (n=17) | 6288 (n=17) |
| aluvion | `lluvia_24h_mm` | 6.7 mm | 40 (n=48) | 8 (n=48) | 6980 (n=48) | 9 (n=17) | 8 (n=17) | 3619 (n=17) |
| aluvion | `lluvia_24h_mm` | 12 mm | 33 (n=48) | 15 (n=48) | 3596 (n=48) | 4 (n=17) | 13 (n=17) | 1752 (n=17) |
| aluvion | `lluvia_24h_mm` | 26 mm | 20 (n=48) | 28 (n=48) | 922 (n=48) | 1 (n=17) | 16 (n=17) | 431 (n=17) |
| aluvion | `lluvia_48h_mm` | 9.6 mm | 42 (n=48) | 6 (n=48) | 9919 (n=48) | 9 (n=17) | 8 (n=17) | 5224 (n=17) |
| aluvion | `lluvia_48h_mm` | 17.8 mm | 36 (n=48) | 12 (n=48) | 5490 (n=48) | 4 (n=17) | 13 (n=17) | 2718 (n=17) |
| aluvion | `lluvia_48h_mm` | 28.1 mm | 26 (n=48) | 22 (n=48) | 2788 (n=48) | 1 (n=17) | 16 (n=17) | 1295 (n=17) |
| aluvion | `lluvia_48h_mm` | 38.7 mm | 14 (n=48) | 34 (n=48) | 1450 (n=48) | 1 (n=17) | 16 (n=17) | 613 (n=17) |
| aluvion | `lluvia_72h_mm` | 8.7 mm | 43 (n=48) | 5 (n=48) | 14087 (n=48) | 12 (n=17) | 5 (n=17) | 7674 (n=17) |
| aluvion | `lluvia_72h_mm` | 24.2 mm | 35 (n=48) | 13 (n=48) | 6287 (n=48) | 6 (n=17) | 11 (n=17) | 3190 (n=17) |
| aluvion | `lluvia_72h_mm` | 38.9 mm | 24 (n=48) | 24 (n=48) | 3086 (n=48) | 2 (n=17) | 15 (n=17) | 1418 (n=17) |
| aluvion | `lluvia_72h_mm` | 45.5 mm | 13 (n=48) | 35 (n=48) | 2280 (n=48) | 2 (n=17) | 15 (n=17) | 1006 (n=17) |
| aluvion | `lluvia_7d_mm` | 27.3 mm | 43 (n=48) | 5 (n=48) | 13044 (n=48) | 10 (n=17) | 7 (n=17) | 7181 (n=17) |
| aluvion | `lluvia_7d_mm` | 38.3 mm | 38 (n=48) | 10 (n=48) | 10133 (n=48) | 9 (n=17) | 8 (n=17) | 5254 (n=17) |
| aluvion | `lluvia_7d_mm` | 62.8 mm | 25 (n=48) | 23 (n=48) | 5489 (n=48) | 5 (n=17) | 12 (n=17) | 2691 (n=17) |
| aluvion | `lluvia_7d_mm` | 94.1 mm | 12 (n=48) | 36 (n=48) | 2408 (n=48) | 3 (n=17) | 14 (n=17) | 986 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm` | 0.6 mm | 43 (n=48) | 5 (n=48) | 13484 (n=48) | 14 (n=17) | 3 (n=17) | 6888 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm` | 1 mm | 42 (n=48) | 6 (n=48) | 9483 (n=48) | 13 (n=17) | 4 (n=17) | 4832 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm` | 1.9 mm | 37 (n=48) | 11 (n=48) | 4516 (n=48) | 10 (n=17) | 7 (n=17) | 2236 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm` | 4.4 mm | 16 (n=48) | 32 (n=48) | 970 (n=48) | 2 (n=17) | 15 (n=17) | 455 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm` | 1.3 mm | 43 (n=48) | 5 (n=48) | 13197 (n=48) | 13 (n=17) | 4 (n=17) | 6983 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm` | 2.1 mm | 36 (n=48) | 12 (n=48) | 8365 (n=48) | 10 (n=17) | 7 (n=17) | 4285 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm` | 3.5 mm | 24 (n=48) | 24 (n=48) | 3867 (n=48) | 4 (n=17) | 13 (n=17) | 1924 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm` | 5.3 mm | 13 (n=48) | 35 (n=48) | 1622 (n=48) | 2 (n=17) | 15 (n=17) | 801 (n=17) |
| crecida | `lluvia_24h_mm` | 0.8 mm | 51 (n=58) | 7 (n=58) | 17836 (n=58) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 10111 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 3.5 mm | 43 (n=58) | 15 (n=58) | 11189 (n=58) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 5978 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 11.9 mm | 31 (n=58) | 27 (n=58) | 3635 (n=58) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1783 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 18.6 mm | 17 (n=58) | 41 (n=58) | 1776 (n=58) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 867 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 2.4 mm | 51 (n=58) | 7 (n=58) | 18110 (n=58) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 9942 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 6.4 mm | 44 (n=58) | 14 (n=58) | 12677 (n=58) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 6905 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 23 mm | 29 (n=58) | 29 (n=58) | 3856 (n=58) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1862 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 37.2 mm | 21 (n=58) | 37 (n=58) | 1621 (n=58) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 690 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 4.4 mm | 49 (n=58) | 9 (n=58) | 18063 (n=58) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 10030 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 13 mm | 42 (n=58) | 16 (n=58) | 11225 (n=58) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 5960 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 28 mm | 32 (n=58) | 26 (n=58) | 5146 (n=58) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2612 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 53.5 mm | 14 (n=58) | 44 (n=58) | 1524 (n=58) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 622 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 7.4 mm | 53 (n=58) | 5 (n=58) | 21960 (n=58) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 12084 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 27.5 mm | 43 (n=58) | 15 (n=58) | 12976 (n=58) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 7148 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 55.9 mm | 30 (n=58) | 28 (n=58) | 6577 (n=58) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 3237 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 98.5 mm | 15 (n=58) | 43 (n=58) | 2096 (n=58) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 841 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 0.3 mm | 49 (n=58) | 9 (n=58) | 18328 (n=58) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 9630 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 0.8 mm | 42 (n=58) | 16 (n=58) | 11249 (n=58) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 5806 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 1.8 mm | 34 (n=58) | 24 (n=58) | 4895 (n=58) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 2407 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 2.7 mm | 20 (n=58) | 38 (n=58) | 2577 (n=58) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1233 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 0.6 mm | 50 (n=58) | 8 (n=58) | 19855 (n=58) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 10288 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 1.3 mm | 42 (n=58) | 16 (n=58) | 13197 (n=58) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 6994 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 3 mm | 31 (n=58) | 27 (n=58) | 5072 (n=58) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2485 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 4.7 mm | 15 (n=58) | 43 (n=58) | 2180 (n=58) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 1067 (n=9 muestra chica) |
| nieve | `nieve_24h_cm` | 0.1 cm | 18 (n=37) | 19 (n=37) | 562 (n=37) | 11 (n=27) | 16 (n=27) | 256 (n=27) |
| nieve | `nieve_24h_cm` | 0.2 cm | 16 (n=37) | 21 (n=37) | 491 (n=37) | 10 (n=27) | 17 (n=27) | 233 (n=27) |
| nieve | `nieve_24h_cm` | 0.6 cm | 9 (n=37) | 28 (n=37) | 315 (n=37) | 5 (n=27) | 22 (n=27) | 142 (n=27) |
| nieve | `nieve_24h_cm` | 1.7 cm | 4 (n=37) | 33 (n=37) | 131 (n=37) | 3 (n=27) | 24 (n=27) | 64 (n=27) |
| nieve | `nieve_72h_cm` | 0.1 cm | 22 (n=37) | 15 (n=37) | 1212 (n=37) | 13 (n=27) | 14 (n=27) | 513 (n=27) |
| nieve | `nieve_72h_cm` | 0.4 cm | 18 (n=37) | 19 (n=37) | 866 (n=37) | 9 (n=27) | 18 (n=27) | 397 (n=27) |
| nieve | `nieve_72h_cm` | 0.9 cm | 12 (n=37) | 25 (n=37) | 631 (n=37) | 7 (n=27) | 20 (n=27) | 274 (n=27) |
| nieve | `nieve_72h_cm` | 2.2 cm | 9 (n=37) | 28 (n=37) | 299 (n=37) | 3 (n=27) | 24 (n=27) | 147 (n=27) |
| nieve | `nieve_7d_cm` | 0.1 cm | 24 (n=37) | 13 (n=37) | 2308 (n=37) | 14 (n=27) | 13 (n=27) | 974 (n=27) |
| nieve | `nieve_7d_cm` | 0.4 cm | 20 (n=37) | 17 (n=37) | 1689 (n=37) | 9 (n=27) | 18 (n=27) | 781 (n=27) |
| nieve | `nieve_7d_cm` | 1.5 cm | 12 (n=37) | 25 (n=37) | 921 (n=37) | 4 (n=27) | 23 (n=27) | 416 (n=27) |
| nieve | `nieve_7d_cm` | 2.9 cm | 7 (n=37) | 30 (n=37) | 530 (n=37) | 1 (n=27) | 26 (n=27) | 254 (n=27) |

### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm_pct` | p80 | 37 (n=48) | 11 (n=48) | 7116 (n=48) | 14 (n=17) | 3 (n=17) | 4103 (n=17) |
| aluvion | `lluvia_24h_mm_pct` | p90 | 27 (n=48) | 21 (n=48) | 3759 (n=48) | 9 (n=17) | 8 (n=17) | 2121 (n=17) |
| aluvion | `lluvia_24h_mm_pct` | p95 | 15 (n=48) | 33 (n=48) | 1969 (n=48) | 5 (n=17) | 12 (n=17) | 1133 (n=17) |
| aluvion | `lluvia_24h_mm_pct` | p98 | 6 (n=48) | 42 (n=48) | 822 (n=48) | 1 (n=17) | 16 (n=17) | 467 (n=17) |
| aluvion | `lluvia_24h_mm_pct` | p99 | 3 (n=48) | 45 (n=48) | 384 (n=48) | 0 (n=17) | 17 (n=17) | 213 (n=17) |
| aluvion | `lluvia_48h_mm_pct` | p80 | 32 (n=48) | 16 (n=48) | 7457 (n=48) | 9 (n=17) | 8 (n=17) | 4131 (n=17) |
| aluvion | `lluvia_48h_mm_pct` | p90 | 13 (n=48) | 35 (n=48) | 3897 (n=48) | 8 (n=17) | 9 (n=17) | 2167 (n=17) |
| aluvion | `lluvia_48h_mm_pct` | p95 | 10 (n=48) | 38 (n=48) | 2007 (n=48) | 3 (n=17) | 14 (n=17) | 1116 (n=17) |
| aluvion | `lluvia_48h_mm_pct` | p98 | 6 (n=48) | 42 (n=48) | 819 (n=48) | 2 (n=17) | 15 (n=17) | 420 (n=17) |
| aluvion | `lluvia_48h_mm_pct` | p99 | 2 (n=48) | 46 (n=48) | 381 (n=48) | 0 (n=17) | 17 (n=17) | 210 (n=17) |
| aluvion | `lluvia_72h_mm_pct` | p80 | 20 (n=48) | 28 (n=48) | 7605 (n=48) | 11 (n=17) | 6 (n=17) | 4139 (n=17) |
| aluvion | `lluvia_72h_mm_pct` | p90 | 12 (n=48) | 36 (n=48) | 3977 (n=48) | 8 (n=17) | 9 (n=17) | 2192 (n=17) |
| aluvion | `lluvia_72h_mm_pct` | p95 | 7 (n=48) | 41 (n=48) | 2032 (n=48) | 4 (n=17) | 13 (n=17) | 1080 (n=17) |
| aluvion | `lluvia_72h_mm_pct` | p98 | 4 (n=48) | 44 (n=48) | 821 (n=48) | 1 (n=17) | 16 (n=17) | 373 (n=17) |
| aluvion | `lluvia_72h_mm_pct` | p99 | 2 (n=48) | 46 (n=48) | 388 (n=48) | 0 (n=17) | 17 (n=17) | 158 (n=17) |
| aluvion | `lluvia_7d_mm_pct` | p80 | 18 (n=48) | 30 (n=48) | 7958 (n=48) | 13 (n=17) | 4 (n=17) | 4387 (n=17) |
| aluvion | `lluvia_7d_mm_pct` | p90 | 10 (n=48) | 38 (n=48) | 4049 (n=48) | 11 (n=17) | 6 (n=17) | 2166 (n=17) |
| aluvion | `lluvia_7d_mm_pct` | p95 | 7 (n=48) | 41 (n=48) | 2027 (n=48) | 3 (n=17) | 14 (n=17) | 1023 (n=17) |
| aluvion | `lluvia_7d_mm_pct` | p98 | 5 (n=48) | 43 (n=48) | 810 (n=48) | 2 (n=17) | 15 (n=17) | 334 (n=17) |
| aluvion | `lluvia_7d_mm_pct` | p99 | 3 (n=48) | 45 (n=48) | 377 (n=48) | 1 (n=17) | 16 (n=17) | 155 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p80 | 37 (n=48) | 11 (n=48) | 7132 (n=48) | 15 (n=17) | 2 (n=17) | 3948 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p90 | 25 (n=48) | 23 (n=48) | 3720 (n=48) | 10 (n=17) | 7 (n=17) | 2027 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p95 | 10 (n=48) | 38 (n=48) | 1969 (n=48) | 4 (n=17) | 13 (n=17) | 1085 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p98 | 8 (n=48) | 40 (n=48) | 805 (n=48) | 2 (n=17) | 15 (n=17) | 393 (n=17) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p99 | 2 (n=48) | 46 (n=48) | 387 (n=48) | 0 (n=17) | 17 (n=17) | 174 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p80 | 18 (n=48) | 30 (n=48) | 7503 (n=48) | 12 (n=17) | 5 (n=17) | 3983 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p90 | 11 (n=48) | 37 (n=48) | 3955 (n=48) | 7 (n=17) | 10 (n=17) | 2153 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p95 | 9 (n=48) | 39 (n=48) | 1991 (n=48) | 4 (n=17) | 13 (n=17) | 979 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p98 | 1 (n=48) | 47 (n=48) | 786 (n=48) | 2 (n=17) | 15 (n=17) | 336 (n=17) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p99 | 1 (n=48) | 47 (n=48) | 380 (n=48) | 1 (n=17) | 16 (n=17) | 182 (n=17) |
| crecida | `lluvia_24h_mm_pct` | p80 | 34 (n=58) | 24 (n=58) | 7114 (n=58) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 4116 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p90 | 17 (n=58) | 41 (n=58) | 3771 (n=58) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2128 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p95 | 7 (n=58) | 51 (n=58) | 1977 (n=58) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1138 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p98 | 4 (n=58) | 54 (n=58) | 824 (n=58) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 468 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p99 | 2 (n=58) | 56 (n=58) | 385 (n=58) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 213 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p80 | 35 (n=58) | 23 (n=58) | 7456 (n=58) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 4141 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p90 | 17 (n=58) | 41 (n=58) | 3897 (n=58) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2174 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p95 | 8 (n=58) | 50 (n=58) | 2012 (n=58) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1118 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p98 | 4 (n=58) | 54 (n=58) | 822 (n=58) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 421 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p99 | 3 (n=58) | 55 (n=58) | 380 (n=58) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 210 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p80 | 24 (n=58) | 34 (n=58) | 7599 (n=58) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 4153 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p90 | 15 (n=58) | 43 (n=58) | 3977 (n=58) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2202 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p95 | 9 (n=58) | 49 (n=58) | 2029 (n=58) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1084 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p98 | 3 (n=58) | 55 (n=58) | 822 (n=58) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 374 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p99 | 3 (n=58) | 55 (n=58) | 386 (n=58) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 158 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p80 | 20 (n=58) | 38 (n=58) | 7956 (n=58) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 4408 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p90 | 10 (n=58) | 48 (n=58) | 4050 (n=58) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2180 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p95 | 5 (n=58) | 53 (n=58) | 2029 (n=58) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1027 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p98 | 4 (n=58) | 54 (n=58) | 810 (n=58) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 337 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p99 | 2 (n=58) | 56 (n=58) | 377 (n=58) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 157 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p80 | 29 (n=58) | 29 (n=58) | 7141 (n=58) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3959 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p90 | 14 (n=58) | 44 (n=58) | 3730 (n=58) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2037 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p95 | 5 (n=58) | 53 (n=58) | 1973 (n=58) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 1090 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p98 | 4 (n=58) | 54 (n=58) | 809 (n=58) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 395 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p99 | 2 (n=58) | 56 (n=58) | 387 (n=58) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 174 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p80 | 21 (n=58) | 37 (n=58) | 7497 (n=58) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3999 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p90 | 8 (n=58) | 50 (n=58) | 3958 (n=58) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 2161 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p95 | 7 (n=58) | 51 (n=58) | 1992 (n=58) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 982 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p98 | 4 (n=58) | 54 (n=58) | 781 (n=58) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 338 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p99 | 4 (n=58) | 54 (n=58) | 375 (n=58) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 183 (n=9 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p80 | 18 (n=37) | 19 (n=37) | 616 (n=37) | 13 (n=27) | 14 (n=27) | 295 (n=27) |
| nieve | `nieve_24h_cm_pct` | p90 | 17 (n=37) | 20 (n=37) | 528 (n=37) | 13 (n=27) | 14 (n=27) | 266 (n=27) |
| nieve | `nieve_24h_cm_pct` | p95 | 15 (n=37) | 22 (n=37) | 411 (n=37) | 13 (n=27) | 14 (n=27) | 212 (n=27) |
| nieve | `nieve_24h_cm_pct` | p98 | 7 (n=37) | 30 (n=37) | 259 (n=37) | 6 (n=27) | 21 (n=27) | 120 (n=27) |
| nieve | `nieve_24h_cm_pct` | p99 | 4 (n=37) | 33 (n=37) | 157 (n=37) | 5 (n=27) | 22 (n=27) | 66 (n=27) |
| nieve | `nieve_72h_cm_pct` | p80 | 23 (n=37) | 14 (n=37) | 1191 (n=37) | 14 (n=27) | 13 (n=27) | 544 (n=27) |
| nieve | `nieve_72h_cm_pct` | p90 | 19 (n=37) | 18 (n=37) | 908 (n=37) | 12 (n=27) | 15 (n=27) | 436 (n=27) |
| nieve | `nieve_72h_cm_pct` | p95 | 14 (n=37) | 23 (n=37) | 631 (n=37) | 9 (n=27) | 18 (n=27) | 305 (n=27) |
| nieve | `nieve_72h_cm_pct` | p98 | 6 (n=37) | 31 (n=37) | 356 (n=37) | 5 (n=27) | 22 (n=27) | 131 (n=27) |
| nieve | `nieve_72h_cm_pct` | p99 | 3 (n=37) | 34 (n=37) | 217 (n=37) | 3 (n=27) | 24 (n=27) | 79 (n=27) |
| nieve | `nieve_7d_cm_pct` | p80 | 22 (n=37) | 15 (n=37) | 1895 (n=37) | 13 (n=27) | 14 (n=27) | 873 (n=27) |
| nieve | `nieve_7d_cm_pct` | p90 | 13 (n=37) | 24 (n=37) | 1351 (n=37) | 10 (n=27) | 17 (n=27) | 632 (n=27) |
| nieve | `nieve_7d_cm_pct` | p95 | 8 (n=37) | 29 (n=37) | 883 (n=37) | 7 (n=27) | 20 (n=27) | 331 (n=27) |
| nieve | `nieve_7d_cm_pct` | p98 | 3 (n=37) | 34 (n=37) | 476 (n=37) | 4 (n=27) | 23 (n=27) | 131 (n=27) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=37) | 36 (n=37) | 235 (n=37) | 2 (n=27) | 25 (n=27) | 78 (n=27) |

### Variante: aluvión + crecida = lluvia

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 106 | 10.7 | 2.0 | 75 |
| lluvia | `lluvia_48h_mm` | 106 | 23.9 | 5.3 | 80 |
| lluvia | `lluvia_72h_mm` | 106 | 31.2 | 9.3 | 75 |
| lluvia | `lluvia_7d_mm` | 106 | 56.7 | 27.3 | 63 |
| lluvia | `lluvia_max_horaria_24h_mm` | 106 | 1.7 | 0.5 | 72 |
| lluvia | `lluvia_max_horaria_72h_mm` | 106 | 3.0 | 1.2 | 74 |
| nieve | `nieve_24h_cm` | 37 | 0.0 | 0.0 | 48 |
| nieve | `nieve_72h_cm` | 37 | 0.1 | 0.0 | 89 |
| nieve | `nieve_7d_cm` | 37 | 0.4 | 0.0 | 83 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 2.2 mm | 92 (n=106) | 14 (n=106) | 13653 (n=106) | 20 (n=26) | 6 (n=26) | 7447 (n=26) |
| lluvia | `lluvia_24h_mm` | 4.5 mm | 83 (n=106) | 23 (n=106) | 9526 (n=106) | 17 (n=26) | 9 (n=26) | 5063 (n=26) |
| lluvia | `lluvia_24h_mm` | 11.9 mm | 64 (n=106) | 42 (n=106) | 3593 (n=106) | 6 (n=26) | 20 (n=26) | 1779 (n=26) |
| lluvia | `lluvia_24h_mm` | 24.1 mm | 35 (n=106) | 71 (n=106) | 1064 (n=106) | 2 (n=26) | 24 (n=26) | 520 (n=26) |
| lluvia | `lluvia_48h_mm` | 2.7 mm | 93 (n=106) | 13 (n=106) | 17439 (n=106) | 23 (n=26) | 3 (n=26) | 9637 (n=26) |
| lluvia | `lluvia_48h_mm` | 11.1 mm | 82 (n=106) | 24 (n=106) | 8770 (n=106) | 12 (n=26) | 14 (n=26) | 4599 (n=26) |
| lluvia | `lluvia_48h_mm` | 25.2 mm | 55 (n=106) | 51 (n=106) | 3288 (n=106) | 2 (n=26) | 24 (n=26) | 1601 (n=26) |
| lluvia | `lluvia_48h_mm` | 38.7 mm | 34 (n=106) | 72 (n=106) | 1428 (n=106) | 2 (n=26) | 24 (n=26) | 612 (n=26) |
| lluvia | `lluvia_72h_mm` | 4.7 mm | 93 (n=106) | 13 (n=106) | 17647 (n=106) | 22 (n=26) | 4 (n=26) | 9801 (n=26) |
| lluvia | `lluvia_72h_mm` | 20.9 mm | 77 (n=106) | 29 (n=106) | 7448 (n=106) | 11 (n=26) | 15 (n=26) | 3831 (n=26) |
| lluvia | `lluvia_72h_mm` | 33.9 mm | 55 (n=106) | 51 (n=106) | 3903 (n=106) | 5 (n=26) | 21 (n=26) | 1862 (n=26) |
| lluvia | `lluvia_72h_mm` | 51.8 mm | 29 (n=106) | 77 (n=106) | 1663 (n=106) | 2 (n=26) | 24 (n=26) | 701 (n=26) |
| lluvia | `lluvia_7d_mm` | 8.1 mm | 98 (n=106) | 8 (n=106) | 21270 (n=106) | 23 (n=26) | 3 (n=26) | 11773 (n=26) |
| lluvia | `lluvia_7d_mm` | 33.6 mm | 80 (n=106) | 26 (n=106) | 11198 (n=106) | 13 (n=26) | 13 (n=26) | 6037 (n=26) |
| lluvia | `lluvia_7d_mm` | 59.1 mm | 56 (n=106) | 50 (n=106) | 5995 (n=106) | 8 (n=26) | 18 (n=26) | 2967 (n=26) |
| lluvia | `lluvia_7d_mm` | 96 mm | 27 (n=106) | 79 (n=106) | 2261 (n=106) | 4 (n=26) | 22 (n=26) | 899 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm` | 0.4 mm | 93 (n=106) | 13 (n=106) | 16350 (n=106) | 24 (n=26) | 2 (n=26) | 8443 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm` | 0.9 mm | 81 (n=106) | 25 (n=106) | 10228 (n=106) | 19 (n=26) | 7 (n=26) | 5329 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm` | 1.9 mm | 68 (n=106) | 38 (n=106) | 4470 (n=106) | 15 (n=26) | 11 (n=26) | 2231 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm` | 3.9 mm | 37 (n=106) | 69 (n=106) | 1230 (n=106) | 2 (n=26) | 24 (n=26) | 591 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm` | 0.7 mm | 94 (n=106) | 12 (n=106) | 18474 (n=106) | 22 (n=26) | 4 (n=26) | 9719 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm` | 1.9 mm | 79 (n=106) | 27 (n=106) | 9377 (n=106) | 18 (n=26) | 8 (n=26) | 4792 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm` | 3.1 mm | 55 (n=106) | 51 (n=106) | 4732 (n=106) | 6 (n=26) | 20 (n=26) | 2306 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm` | 5.1 mm | 28 (n=106) | 78 (n=106) | 1764 (n=106) | 2 (n=26) | 24 (n=26) | 863 (n=26) |
| nieve | `nieve_24h_cm` | 0.1 cm | 18 (n=37) | 19 (n=37) | 562 (n=37) | 11 (n=27) | 16 (n=27) | 256 (n=27) |
| nieve | `nieve_24h_cm` | 0.2 cm | 16 (n=37) | 21 (n=37) | 491 (n=37) | 10 (n=27) | 17 (n=27) | 233 (n=27) |
| nieve | `nieve_24h_cm` | 0.6 cm | 9 (n=37) | 28 (n=37) | 315 (n=37) | 5 (n=27) | 22 (n=27) | 142 (n=27) |
| nieve | `nieve_24h_cm` | 1.7 cm | 4 (n=37) | 33 (n=37) | 131 (n=37) | 3 (n=27) | 24 (n=27) | 64 (n=27) |
| nieve | `nieve_72h_cm` | 0.1 cm | 22 (n=37) | 15 (n=37) | 1212 (n=37) | 13 (n=27) | 14 (n=27) | 513 (n=27) |
| nieve | `nieve_72h_cm` | 0.4 cm | 18 (n=37) | 19 (n=37) | 866 (n=37) | 9 (n=27) | 18 (n=27) | 397 (n=27) |
| nieve | `nieve_72h_cm` | 0.9 cm | 12 (n=37) | 25 (n=37) | 631 (n=37) | 7 (n=27) | 20 (n=27) | 274 (n=27) |
| nieve | `nieve_72h_cm` | 2.2 cm | 9 (n=37) | 28 (n=37) | 299 (n=37) | 3 (n=27) | 24 (n=27) | 147 (n=27) |
| nieve | `nieve_7d_cm` | 0.1 cm | 24 (n=37) | 13 (n=37) | 2308 (n=37) | 14 (n=27) | 13 (n=27) | 974 (n=27) |
| nieve | `nieve_7d_cm` | 0.4 cm | 20 (n=37) | 17 (n=37) | 1689 (n=37) | 9 (n=27) | 18 (n=27) | 781 (n=27) |
| nieve | `nieve_7d_cm` | 1.5 cm | 12 (n=37) | 25 (n=37) | 921 (n=37) | 4 (n=27) | 23 (n=27) | 416 (n=27) |
| nieve | `nieve_7d_cm` | 2.9 cm | 7 (n=37) | 30 (n=37) | 530 (n=37) | 1 (n=27) | 26 (n=27) | 254 (n=27) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm_pct` | p80 | 71 (n=106) | 35 (n=106) | 7070 (n=106) | 18 (n=26) | 8 (n=26) | 4097 (n=26) |
| lluvia | `lluvia_24h_mm_pct` | p90 | 44 (n=106) | 62 (n=106) | 3740 (n=106) | 11 (n=26) | 15 (n=26) | 2117 (n=26) |
| lluvia | `lluvia_24h_mm_pct` | p95 | 22 (n=106) | 84 (n=106) | 1960 (n=106) | 6 (n=26) | 20 (n=26) | 1132 (n=26) |
| lluvia | `lluvia_24h_mm_pct` | p98 | 10 (n=106) | 96 (n=106) | 818 (n=106) | 1 (n=26) | 25 (n=26) | 467 (n=26) |
| lluvia | `lluvia_24h_mm_pct` | p99 | 5 (n=106) | 101 (n=106) | 382 (n=106) | 0 (n=26) | 26 (n=26) | 213 (n=26) |
| lluvia | `lluvia_48h_mm_pct` | p80 | 67 (n=106) | 39 (n=106) | 7413 (n=106) | 12 (n=26) | 14 (n=26) | 4125 (n=26) |
| lluvia | `lluvia_48h_mm_pct` | p90 | 30 (n=106) | 76 (n=106) | 3877 (n=106) | 10 (n=26) | 16 (n=26) | 2163 (n=26) |
| lluvia | `lluvia_48h_mm_pct` | p95 | 18 (n=106) | 88 (n=106) | 1998 (n=106) | 5 (n=26) | 21 (n=26) | 1114 (n=26) |
| lluvia | `lluvia_48h_mm_pct` | p98 | 10 (n=106) | 96 (n=106) | 815 (n=106) | 3 (n=26) | 23 (n=26) | 419 (n=26) |
| lluvia | `lluvia_48h_mm_pct` | p99 | 5 (n=106) | 101 (n=106) | 378 (n=106) | 0 (n=26) | 26 (n=26) | 210 (n=26) |
| lluvia | `lluvia_72h_mm_pct` | p80 | 44 (n=106) | 62 (n=106) | 7568 (n=106) | 14 (n=26) | 12 (n=26) | 4134 (n=26) |
| lluvia | `lluvia_72h_mm_pct` | p90 | 27 (n=106) | 79 (n=106) | 3957 (n=106) | 10 (n=26) | 16 (n=26) | 2189 (n=26) |
| lluvia | `lluvia_72h_mm_pct` | p95 | 16 (n=106) | 90 (n=106) | 2020 (n=106) | 5 (n=26) | 21 (n=26) | 1078 (n=26) |
| lluvia | `lluvia_72h_mm_pct` | p98 | 7 (n=106) | 99 (n=106) | 816 (n=106) | 1 (n=26) | 25 (n=26) | 373 (n=26) |
| lluvia | `lluvia_72h_mm_pct` | p99 | 5 (n=106) | 101 (n=106) | 384 (n=106) | 0 (n=26) | 26 (n=26) | 158 (n=26) |
| lluvia | `lluvia_7d_mm_pct` | p80 | 38 (n=106) | 68 (n=106) | 7925 (n=106) | 15 (n=26) | 11 (n=26) | 4383 (n=26) |
| lluvia | `lluvia_7d_mm_pct` | p90 | 20 (n=106) | 86 (n=106) | 4035 (n=106) | 13 (n=26) | 13 (n=26) | 2162 (n=26) |
| lluvia | `lluvia_7d_mm_pct` | p95 | 12 (n=106) | 94 (n=106) | 2019 (n=106) | 4 (n=26) | 22 (n=26) | 1021 (n=26) |
| lluvia | `lluvia_7d_mm_pct` | p98 | 9 (n=106) | 97 (n=106) | 804 (n=106) | 2 (n=26) | 24 (n=26) | 334 (n=26) |
| lluvia | `lluvia_7d_mm_pct` | p99 | 5 (n=106) | 101 (n=106) | 375 (n=106) | 1 (n=26) | 25 (n=26) | 155 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p80 | 66 (n=106) | 40 (n=106) | 7093 (n=106) | 22 (n=26) | 4 (n=26) | 3940 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p90 | 39 (n=106) | 67 (n=106) | 3703 (n=106) | 12 (n=26) | 14 (n=26) | 2024 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p95 | 15 (n=106) | 91 (n=106) | 1962 (n=106) | 4 (n=26) | 22 (n=26) | 1085 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p98 | 12 (n=106) | 94 (n=106) | 801 (n=106) | 2 (n=26) | 24 (n=26) | 393 (n=26) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p99 | 4 (n=106) | 102 (n=106) | 385 (n=106) | 0 (n=26) | 26 (n=26) | 174 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p80 | 39 (n=106) | 67 (n=106) | 7468 (n=106) | 15 (n=26) | 11 (n=26) | 3979 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p90 | 19 (n=106) | 87 (n=106) | 3942 (n=106) | 8 (n=26) | 18 (n=26) | 2151 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p95 | 16 (n=106) | 90 (n=106) | 1980 (n=106) | 5 (n=26) | 21 (n=26) | 977 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p98 | 5 (n=106) | 101 (n=106) | 780 (n=106) | 2 (n=26) | 24 (n=26) | 336 (n=26) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p99 | 5 (n=106) | 101 (n=106) | 374 (n=106) | 1 (n=26) | 25 (n=26) | 182 (n=26) |
| nieve | `nieve_24h_cm_pct` | p80 | 18 (n=37) | 19 (n=37) | 616 (n=37) | 13 (n=27) | 14 (n=27) | 295 (n=27) |
| nieve | `nieve_24h_cm_pct` | p90 | 17 (n=37) | 20 (n=37) | 528 (n=37) | 13 (n=27) | 14 (n=27) | 266 (n=27) |
| nieve | `nieve_24h_cm_pct` | p95 | 15 (n=37) | 22 (n=37) | 411 (n=37) | 13 (n=27) | 14 (n=27) | 212 (n=27) |
| nieve | `nieve_24h_cm_pct` | p98 | 7 (n=37) | 30 (n=37) | 259 (n=37) | 6 (n=27) | 21 (n=27) | 120 (n=27) |
| nieve | `nieve_24h_cm_pct` | p99 | 4 (n=37) | 33 (n=37) | 157 (n=37) | 5 (n=27) | 22 (n=27) | 66 (n=27) |
| nieve | `nieve_72h_cm_pct` | p80 | 23 (n=37) | 14 (n=37) | 1191 (n=37) | 14 (n=27) | 13 (n=27) | 544 (n=27) |
| nieve | `nieve_72h_cm_pct` | p90 | 19 (n=37) | 18 (n=37) | 908 (n=37) | 12 (n=27) | 15 (n=27) | 436 (n=27) |
| nieve | `nieve_72h_cm_pct` | p95 | 14 (n=37) | 23 (n=37) | 631 (n=37) | 9 (n=27) | 18 (n=27) | 305 (n=27) |
| nieve | `nieve_72h_cm_pct` | p98 | 6 (n=37) | 31 (n=37) | 356 (n=37) | 5 (n=27) | 22 (n=27) | 131 (n=27) |
| nieve | `nieve_72h_cm_pct` | p99 | 3 (n=37) | 34 (n=37) | 217 (n=37) | 3 (n=27) | 24 (n=27) | 79 (n=27) |
| nieve | `nieve_7d_cm_pct` | p80 | 22 (n=37) | 15 (n=37) | 1895 (n=37) | 13 (n=27) | 14 (n=27) | 873 (n=27) |
| nieve | `nieve_7d_cm_pct` | p90 | 13 (n=37) | 24 (n=37) | 1351 (n=37) | 10 (n=27) | 17 (n=27) | 632 (n=27) |
| nieve | `nieve_7d_cm_pct` | p95 | 8 (n=37) | 29 (n=37) | 883 (n=37) | 7 (n=27) | 20 (n=27) | 331 (n=27) |
| nieve | `nieve_7d_cm_pct` | p98 | 3 (n=37) | 34 (n=37) | 476 (n=37) | 4 (n=27) | 23 (n=27) | 131 (n=27) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=37) | 36 (n=37) | 235 (n=37) | 2 (n=27) | 25 (n=27) | 78 (n=27) |

## Solo fuentes estables

Eventos con punto crítico usados: aluvión 62, crecida 66 (lluvia 128), nieve 60.

### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 46 | 10.8 | 3.1 | 74 |
| aluvion | `lluvia_48h_mm` | 46 | 28.1 | 7.6 | 84 |
| aluvion | `lluvia_72h_mm` | 46 | 36.8 | 13.1 | 75 |
| aluvion | `lluvia_7d_mm` | 46 | 62.8 | 36.9 | 63 |
| aluvion | `lluvia_max_horaria_24h_mm` | 46 | 1.8 | 0.7 | 80 |
| aluvion | `lluvia_max_horaria_72h_mm` | 46 | 3.4 | 1.5 | 77 |
| crecida | `lluvia_24h_mm` | 57 | 11.5 | 2.4 | 78 |
| crecida | `lluvia_48h_mm` | 57 | 20.4 | 6.2 | 76 |
| crecida | `lluvia_72h_mm` | 57 | 27.3 | 10.9 | 75 |
| crecida | `lluvia_7d_mm` | 57 | 54.8 | 32.0 | 63 |
| crecida | `lluvia_max_horaria_24h_mm` | 57 | 1.7 | 0.6 | 71 |
| crecida | `lluvia_max_horaria_72h_mm` | 57 | 2.9 | 1.3 | 73 |
| nieve | `nieve_24h_cm` | 35 | 0.0 | 0.0 | 48 |
| nieve | `nieve_72h_cm` | 35 | 0.4 | 0.0 | 91 |
| nieve | `nieve_7d_cm` | 35 | 0.4 | 0.0 | 85 |

### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm` | 3.2 mm | 40 (n=46) | 6 (n=46) | 11621 (n=46) | 13 (n=16) | 3 (n=16) | 6289 (n=16) |
| aluvion | `lluvia_24h_mm` | 6.5 mm | 38 (n=46) | 8 (n=46) | 7199 (n=46) | 8 (n=16) | 8 (n=16) | 3738 (n=16) |
| aluvion | `lluvia_24h_mm` | 12.1 mm | 30 (n=46) | 16 (n=46) | 3560 (n=46) | 4 (n=16) | 12 (n=16) | 1735 (n=16) |
| aluvion | `lluvia_24h_mm` | 26 mm | 19 (n=46) | 27 (n=46) | 923 (n=46) | 1 (n=16) | 15 (n=16) | 431 (n=16) |
| aluvion | `lluvia_48h_mm` | 9.4 mm | 40 (n=46) | 6 (n=46) | 10078 (n=46) | 9 (n=16) | 7 (n=16) | 5312 (n=16) |
| aluvion | `lluvia_48h_mm` | 17.5 mm | 34 (n=46) | 12 (n=46) | 5588 (n=46) | 4 (n=16) | 12 (n=16) | 2784 (n=16) |
| aluvion | `lluvia_48h_mm` | 29.6 mm | 24 (n=46) | 22 (n=46) | 2490 (n=46) | 1 (n=16) | 15 (n=16) | 1164 (n=16) |
| aluvion | `lluvia_48h_mm` | 38.8 mm | 13 (n=46) | 33 (n=46) | 1450 (n=46) | 1 (n=16) | 15 (n=16) | 613 (n=16) |
| aluvion | `lluvia_72h_mm` | 7.8 mm | 41 (n=46) | 5 (n=46) | 14744 (n=46) | 11 (n=16) | 5 (n=16) | 8124 (n=16) |
| aluvion | `lluvia_72h_mm` | 24.7 mm | 34 (n=46) | 12 (n=46) | 6133 (n=46) | 6 (n=16) | 10 (n=16) | 3110 (n=16) |
| aluvion | `lluvia_72h_mm` | 38.9 mm | 23 (n=46) | 23 (n=46) | 3088 (n=46) | 2 (n=16) | 14 (n=16) | 1418 (n=16) |
| aluvion | `lluvia_72h_mm` | 44.1 mm | 12 (n=46) | 34 (n=46) | 2411 (n=46) | 2 (n=16) | 14 (n=16) | 1075 (n=16) |
| aluvion | `lluvia_7d_mm` | 27 mm | 41 (n=46) | 5 (n=46) | 13140 (n=46) | 9 (n=16) | 7 (n=16) | 7218 (n=16) |
| aluvion | `lluvia_7d_mm` | 37.2 mm | 36 (n=46) | 10 (n=46) | 10416 (n=46) | 8 (n=16) | 8 (n=16) | 5411 (n=16) |
| aluvion | `lluvia_7d_mm` | 62.8 mm | 24 (n=46) | 22 (n=46) | 5491 (n=46) | 5 (n=16) | 11 (n=16) | 2691 (n=16) |
| aluvion | `lluvia_7d_mm` | 92.5 mm | 12 (n=46) | 34 (n=46) | 2492 (n=46) | 3 (n=16) | 13 (n=16) | 1041 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm` | 0.6 mm | 41 (n=46) | 5 (n=46) | 13487 (n=46) | 13 (n=16) | 3 (n=16) | 6889 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm` | 1 mm | 40 (n=46) | 6 (n=46) | 9486 (n=46) | 12 (n=16) | 4 (n=16) | 4833 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm` | 1.9 mm | 35 (n=46) | 11 (n=46) | 4519 (n=46) | 9 (n=16) | 7 (n=16) | 2237 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm` | 4.5 mm | 15 (n=46) | 31 (n=46) | 940 (n=46) | 2 (n=16) | 14 (n=16) | 432 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm` | 1.1 mm | 41 (n=46) | 5 (n=46) | 14831 (n=46) | 13 (n=16) | 3 (n=16) | 7817 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm` | 2 mm | 38 (n=46) | 8 (n=46) | 8915 (n=46) | 11 (n=16) | 5 (n=16) | 4478 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm` | 3.5 mm | 23 (n=46) | 23 (n=46) | 3869 (n=46) | 4 (n=16) | 12 (n=16) | 1924 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm` | 5.3 mm | 12 (n=46) | 34 (n=46) | 1624 (n=46) | 2 (n=16) | 14 (n=16) | 801 (n=16) |
| crecida | `lluvia_24h_mm` | 0.8 mm | 50 (n=57) | 7 (n=57) | 17838 (n=57) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 10111 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 3.8 mm | 42 (n=57) | 15 (n=57) | 10693 (n=57) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 5658 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 12.4 mm | 30 (n=57) | 27 (n=57) | 3437 (n=57) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1664 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm` | 19 mm | 17 (n=57) | 40 (n=57) | 1706 (n=57) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 841 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 2.3 mm | 51 (n=57) | 6 (n=57) | 18276 (n=57) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 10053 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 6.9 mm | 43 (n=57) | 14 (n=57) | 12163 (n=57) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 6569 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 23.2 mm | 29 (n=57) | 28 (n=57) | 3779 (n=57) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1837 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm` | 38 mm | 21 (n=57) | 36 (n=57) | 1532 (n=57) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 637 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 4.3 mm | 48 (n=57) | 9 (n=57) | 18206 (n=57) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 10086 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 14.3 mm | 41 (n=57) | 16 (n=57) | 10428 (n=57) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 5549 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 28.8 mm | 31 (n=57) | 26 (n=57) | 4966 (n=57) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2497 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm` | 53.5 mm | 14 (n=57) | 43 (n=57) | 1524 (n=57) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 622 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 7.6 mm | 52 (n=57) | 5 (n=57) | 21774 (n=57) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 11971 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 31.3 mm | 42 (n=57) | 15 (n=57) | 11889 (n=57) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 6457 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 56.9 mm | 30 (n=57) | 27 (n=57) | 6390 (n=57) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 3168 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm` | 98.7 mm | 15 (n=57) | 42 (n=57) | 2085 (n=57) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 829 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 0.3 mm | 48 (n=57) | 9 (n=57) | 18330 (n=57) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 9630 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 0.8 mm | 41 (n=57) | 16 (n=57) | 11250 (n=57) | 6 (n=9 muestra chica) | 3 (n=9 muestra chica) | 5806 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 1.9 mm | 31 (n=57) | 26 (n=57) | 4522 (n=57) | 5 (n=9 muestra chica) | 4 (n=9 muestra chica) | 2241 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm` | 2.7 mm | 20 (n=57) | 37 (n=57) | 2577 (n=57) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1233 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 0.6 mm | 49 (n=57) | 8 (n=57) | 19856 (n=57) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 10288 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 1.3 mm | 42 (n=57) | 15 (n=57) | 13197 (n=57) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 6994 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 3 mm | 31 (n=57) | 26 (n=57) | 5072 (n=57) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2485 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm` | 4.7 mm | 15 (n=57) | 42 (n=57) | 2180 (n=57) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 1067 (n=9 muestra chica) |
| nieve | `nieve_24h_cm` | 0.1 cm | 18 (n=35) | 17 (n=35) | 562 (n=35) | 10 (n=25) | 15 (n=25) | 257 (n=25) |
| nieve | `nieve_24h_cm` | 0.2 cm | 16 (n=35) | 19 (n=35) | 491 (n=35) | 9 (n=25) | 16 (n=25) | 234 (n=25) |
| nieve | `nieve_24h_cm` | 0.6 cm | 9 (n=35) | 26 (n=35) | 315 (n=35) | 4 (n=25) | 21 (n=25) | 143 (n=25) |
| nieve | `nieve_24h_cm` | 1.7 cm | 4 (n=35) | 31 (n=35) | 131 (n=35) | 3 (n=25) | 22 (n=25) | 64 (n=25) |
| nieve | `nieve_72h_cm` | 0.1 cm | 22 (n=35) | 13 (n=35) | 1212 (n=35) | 12 (n=25) | 13 (n=25) | 514 (n=25) |
| nieve | `nieve_72h_cm` | 0.4 cm | 18 (n=35) | 17 (n=35) | 866 (n=35) | 8 (n=25) | 17 (n=25) | 398 (n=25) |
| nieve | `nieve_72h_cm` | 0.9 cm | 12 (n=35) | 23 (n=35) | 631 (n=35) | 6 (n=25) | 19 (n=25) | 275 (n=25) |
| nieve | `nieve_72h_cm` | 2.2 cm | 9 (n=35) | 26 (n=35) | 299 (n=35) | 3 (n=25) | 22 (n=25) | 147 (n=25) |
| nieve | `nieve_7d_cm` | 0.1 cm | 24 (n=35) | 11 (n=35) | 2308 (n=35) | 12 (n=25) | 13 (n=25) | 977 (n=25) |
| nieve | `nieve_7d_cm` | 0.4 cm | 20 (n=35) | 15 (n=35) | 1689 (n=35) | 8 (n=25) | 17 (n=25) | 782 (n=25) |
| nieve | `nieve_7d_cm` | 1.5 cm | 12 (n=35) | 23 (n=35) | 921 (n=35) | 4 (n=25) | 21 (n=25) | 416 (n=25) |
| nieve | `nieve_7d_cm` | 2.9 cm | 7 (n=35) | 28 (n=35) | 530 (n=35) | 1 (n=25) | 24 (n=25) | 254 (n=25) |

### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| aluvion | `lluvia_24h_mm_pct` | p80 | 35 (n=46) | 11 (n=46) | 7118 (n=46) | 13 (n=16) | 3 (n=16) | 4104 (n=16) |
| aluvion | `lluvia_24h_mm_pct` | p90 | 26 (n=46) | 20 (n=46) | 3760 (n=46) | 8 (n=16) | 8 (n=16) | 2122 (n=16) |
| aluvion | `lluvia_24h_mm_pct` | p95 | 15 (n=46) | 31 (n=46) | 1969 (n=46) | 5 (n=16) | 11 (n=16) | 1133 (n=16) |
| aluvion | `lluvia_24h_mm_pct` | p98 | 6 (n=46) | 40 (n=46) | 822 (n=46) | 1 (n=16) | 15 (n=16) | 467 (n=16) |
| aluvion | `lluvia_24h_mm_pct` | p99 | 3 (n=46) | 43 (n=46) | 384 (n=46) | 0 (n=16) | 16 (n=16) | 213 (n=16) |
| aluvion | `lluvia_48h_mm_pct` | p80 | 30 (n=46) | 16 (n=46) | 7459 (n=46) | 9 (n=16) | 7 (n=16) | 4131 (n=16) |
| aluvion | `lluvia_48h_mm_pct` | p90 | 12 (n=46) | 34 (n=46) | 3898 (n=46) | 8 (n=16) | 8 (n=16) | 2167 (n=16) |
| aluvion | `lluvia_48h_mm_pct` | p95 | 9 (n=46) | 37 (n=46) | 2008 (n=46) | 3 (n=16) | 13 (n=16) | 1116 (n=16) |
| aluvion | `lluvia_48h_mm_pct` | p98 | 5 (n=46) | 41 (n=46) | 820 (n=46) | 2 (n=16) | 14 (n=16) | 420 (n=16) |
| aluvion | `lluvia_48h_mm_pct` | p99 | 2 (n=46) | 44 (n=46) | 381 (n=46) | 0 (n=16) | 16 (n=16) | 210 (n=16) |
| aluvion | `lluvia_72h_mm_pct` | p80 | 19 (n=46) | 27 (n=46) | 7607 (n=46) | 10 (n=16) | 6 (n=16) | 4140 (n=16) |
| aluvion | `lluvia_72h_mm_pct` | p90 | 11 (n=46) | 35 (n=46) | 3979 (n=46) | 8 (n=16) | 8 (n=16) | 2192 (n=16) |
| aluvion | `lluvia_72h_mm_pct` | p95 | 6 (n=46) | 40 (n=46) | 2033 (n=46) | 4 (n=16) | 12 (n=16) | 1080 (n=16) |
| aluvion | `lluvia_72h_mm_pct` | p98 | 4 (n=46) | 42 (n=46) | 821 (n=46) | 1 (n=16) | 15 (n=16) | 373 (n=16) |
| aluvion | `lluvia_72h_mm_pct` | p99 | 2 (n=46) | 44 (n=46) | 388 (n=46) | 0 (n=16) | 16 (n=16) | 158 (n=16) |
| aluvion | `lluvia_7d_mm_pct` | p80 | 17 (n=46) | 29 (n=46) | 7960 (n=46) | 12 (n=16) | 4 (n=16) | 4389 (n=16) |
| aluvion | `lluvia_7d_mm_pct` | p90 | 9 (n=46) | 37 (n=46) | 4051 (n=46) | 10 (n=16) | 6 (n=16) | 2168 (n=16) |
| aluvion | `lluvia_7d_mm_pct` | p95 | 6 (n=46) | 40 (n=46) | 2029 (n=46) | 3 (n=16) | 13 (n=16) | 1023 (n=16) |
| aluvion | `lluvia_7d_mm_pct` | p98 | 4 (n=46) | 42 (n=46) | 812 (n=46) | 2 (n=16) | 14 (n=16) | 334 (n=16) |
| aluvion | `lluvia_7d_mm_pct` | p99 | 3 (n=46) | 43 (n=46) | 377 (n=46) | 1 (n=16) | 15 (n=16) | 155 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p80 | 35 (n=46) | 11 (n=46) | 7135 (n=46) | 14 (n=16) | 2 (n=16) | 3949 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p90 | 23 (n=46) | 23 (n=46) | 3722 (n=46) | 9 (n=16) | 7 (n=16) | 2028 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p95 | 10 (n=46) | 36 (n=46) | 1969 (n=46) | 4 (n=16) | 12 (n=16) | 1085 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p98 | 8 (n=46) | 38 (n=46) | 805 (n=46) | 2 (n=16) | 14 (n=16) | 393 (n=16) |
| aluvion | `lluvia_max_horaria_24h_mm_pct` | p99 | 2 (n=46) | 44 (n=46) | 387 (n=46) | 0 (n=16) | 16 (n=16) | 174 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p80 | 17 (n=46) | 29 (n=46) | 7505 (n=46) | 11 (n=16) | 5 (n=16) | 3984 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p90 | 10 (n=46) | 36 (n=46) | 3957 (n=46) | 7 (n=16) | 9 (n=16) | 2153 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p95 | 9 (n=46) | 37 (n=46) | 1991 (n=46) | 4 (n=16) | 12 (n=16) | 979 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p98 | 1 (n=46) | 45 (n=46) | 786 (n=46) | 2 (n=16) | 14 (n=16) | 336 (n=16) |
| aluvion | `lluvia_max_horaria_72h_mm_pct` | p99 | 1 (n=46) | 45 (n=46) | 380 (n=46) | 1 (n=16) | 15 (n=16) | 182 (n=16) |
| crecida | `lluvia_24h_mm_pct` | p80 | 34 (n=57) | 23 (n=57) | 7114 (n=57) | 4 (n=9 muestra chica) | 5 (n=9 muestra chica) | 4116 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p90 | 17 (n=57) | 40 (n=57) | 3771 (n=57) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2128 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p95 | 7 (n=57) | 50 (n=57) | 1977 (n=57) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1138 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p98 | 4 (n=57) | 53 (n=57) | 824 (n=57) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 468 (n=9 muestra chica) |
| crecida | `lluvia_24h_mm_pct` | p99 | 2 (n=57) | 55 (n=57) | 385 (n=57) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 213 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p80 | 35 (n=57) | 22 (n=57) | 7456 (n=57) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 4141 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p90 | 17 (n=57) | 40 (n=57) | 3897 (n=57) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2174 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p95 | 8 (n=57) | 49 (n=57) | 2012 (n=57) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 1118 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p98 | 4 (n=57) | 53 (n=57) | 822 (n=57) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 421 (n=9 muestra chica) |
| crecida | `lluvia_48h_mm_pct` | p99 | 3 (n=57) | 54 (n=57) | 380 (n=57) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 210 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p80 | 24 (n=57) | 33 (n=57) | 7599 (n=57) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 4153 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p90 | 15 (n=57) | 42 (n=57) | 3977 (n=57) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2202 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p95 | 9 (n=57) | 48 (n=57) | 2029 (n=57) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1084 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p98 | 3 (n=57) | 54 (n=57) | 822 (n=57) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 374 (n=9 muestra chica) |
| crecida | `lluvia_72h_mm_pct` | p99 | 3 (n=57) | 54 (n=57) | 386 (n=57) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 158 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p80 | 20 (n=57) | 37 (n=57) | 7956 (n=57) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 4408 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p90 | 10 (n=57) | 47 (n=57) | 4050 (n=57) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2180 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p95 | 5 (n=57) | 52 (n=57) | 2029 (n=57) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 1027 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p98 | 4 (n=57) | 53 (n=57) | 810 (n=57) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 337 (n=9 muestra chica) |
| crecida | `lluvia_7d_mm_pct` | p99 | 2 (n=57) | 55 (n=57) | 377 (n=57) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 157 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p80 | 29 (n=57) | 28 (n=57) | 7141 (n=57) | 7 (n=9 muestra chica) | 2 (n=9 muestra chica) | 3959 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p90 | 14 (n=57) | 43 (n=57) | 3730 (n=57) | 2 (n=9 muestra chica) | 7 (n=9 muestra chica) | 2037 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p95 | 5 (n=57) | 52 (n=57) | 1973 (n=57) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 1090 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p98 | 4 (n=57) | 53 (n=57) | 809 (n=57) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 395 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_24h_mm_pct` | p99 | 2 (n=57) | 55 (n=57) | 387 (n=57) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 174 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p80 | 21 (n=57) | 36 (n=57) | 7497 (n=57) | 3 (n=9 muestra chica) | 6 (n=9 muestra chica) | 3999 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p90 | 8 (n=57) | 49 (n=57) | 3958 (n=57) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 2161 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p95 | 7 (n=57) | 50 (n=57) | 1992 (n=57) | 1 (n=9 muestra chica) | 8 (n=9 muestra chica) | 982 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p98 | 4 (n=57) | 53 (n=57) | 781 (n=57) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 338 (n=9 muestra chica) |
| crecida | `lluvia_max_horaria_72h_mm_pct` | p99 | 4 (n=57) | 53 (n=57) | 375 (n=57) | 0 (n=9 muestra chica) | 9 (n=9 muestra chica) | 183 (n=9 muestra chica) |
| nieve | `nieve_24h_cm_pct` | p80 | 18 (n=35) | 17 (n=35) | 616 (n=35) | 12 (n=25) | 13 (n=25) | 296 (n=25) |
| nieve | `nieve_24h_cm_pct` | p90 | 17 (n=35) | 18 (n=35) | 528 (n=35) | 12 (n=25) | 13 (n=25) | 267 (n=25) |
| nieve | `nieve_24h_cm_pct` | p95 | 15 (n=35) | 20 (n=35) | 411 (n=35) | 12 (n=25) | 13 (n=25) | 213 (n=25) |
| nieve | `nieve_24h_cm_pct` | p98 | 7 (n=35) | 28 (n=35) | 259 (n=35) | 5 (n=25) | 20 (n=25) | 121 (n=25) |
| nieve | `nieve_24h_cm_pct` | p99 | 4 (n=35) | 31 (n=35) | 157 (n=35) | 5 (n=25) | 20 (n=25) | 66 (n=25) |
| nieve | `nieve_72h_cm_pct` | p80 | 23 (n=35) | 12 (n=35) | 1191 (n=35) | 13 (n=25) | 12 (n=25) | 545 (n=25) |
| nieve | `nieve_72h_cm_pct` | p90 | 19 (n=35) | 16 (n=35) | 908 (n=35) | 11 (n=25) | 14 (n=25) | 437 (n=25) |
| nieve | `nieve_72h_cm_pct` | p95 | 14 (n=35) | 21 (n=35) | 631 (n=35) | 8 (n=25) | 17 (n=25) | 306 (n=25) |
| nieve | `nieve_72h_cm_pct` | p98 | 6 (n=35) | 29 (n=35) | 356 (n=35) | 5 (n=25) | 20 (n=25) | 131 (n=25) |
| nieve | `nieve_72h_cm_pct` | p99 | 3 (n=35) | 32 (n=35) | 217 (n=35) | 3 (n=25) | 22 (n=25) | 79 (n=25) |
| nieve | `nieve_7d_cm_pct` | p80 | 22 (n=35) | 13 (n=35) | 1895 (n=35) | 11 (n=25) | 14 (n=25) | 876 (n=25) |
| nieve | `nieve_7d_cm_pct` | p90 | 13 (n=35) | 22 (n=35) | 1351 (n=35) | 8 (n=25) | 17 (n=25) | 635 (n=25) |
| nieve | `nieve_7d_cm_pct` | p95 | 8 (n=35) | 27 (n=35) | 883 (n=35) | 6 (n=25) | 19 (n=25) | 333 (n=25) |
| nieve | `nieve_7d_cm_pct` | p98 | 3 (n=35) | 32 (n=35) | 476 (n=35) | 3 (n=25) | 22 (n=25) | 133 (n=25) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=35) | 34 (n=35) | 235 (n=35) | 2 (n=25) | 23 (n=25) | 78 (n=25) |

### Variante: aluvión + crecida = lluvia

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 103 | 10.8 | 2.0 | 76 |
| lluvia | `lluvia_48h_mm` | 103 | 24.1 | 5.3 | 80 |
| lluvia | `lluvia_72h_mm` | 103 | 32.3 | 9.3 | 75 |
| lluvia | `lluvia_7d_mm` | 103 | 56.9 | 27.3 | 63 |
| lluvia | `lluvia_max_horaria_24h_mm` | 103 | 1.7 | 0.5 | 72 |
| lluvia | `lluvia_max_horaria_72h_mm` | 103 | 3.0 | 1.2 | 74 |
| nieve | `nieve_24h_cm` | 35 | 0.0 | 0.0 | 48 |
| nieve | `nieve_72h_cm` | 35 | 0.4 | 0.0 | 91 |
| nieve | `nieve_7d_cm` | 35 | 0.4 | 0.0 | 85 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm` | 2.2 mm | 89 (n=103) | 14 (n=103) | 13658 (n=103) | 19 (n=25) | 6 (n=25) | 7448 (n=25) |
| lluvia | `lluvia_24h_mm` | 4.5 mm | 81 (n=103) | 22 (n=103) | 9529 (n=103) | 16 (n=25) | 9 (n=25) | 5064 (n=25) |
| lluvia | `lluvia_24h_mm` | 12.1 mm | 60 (n=103) | 43 (n=103) | 3517 (n=103) | 6 (n=25) | 19 (n=25) | 1732 (n=25) |
| lluvia | `lluvia_24h_mm` | 24.2 mm | 33 (n=103) | 70 (n=103) | 1054 (n=103) | 2 (n=25) | 23 (n=25) | 514 (n=25) |
| lluvia | `lluvia_48h_mm` | 2.6 mm | 90 (n=103) | 13 (n=103) | 17644 (n=103) | 22 (n=25) | 3 (n=25) | 9715 (n=25) |
| lluvia | `lluvia_48h_mm` | 11.3 mm | 80 (n=103) | 23 (n=103) | 8642 (n=103) | 12 (n=25) | 13 (n=25) | 4514 (n=25) |
| lluvia | `lluvia_48h_mm` | 25.4 mm | 54 (n=103) | 49 (n=103) | 3253 (n=103) | 2 (n=25) | 23 (n=25) | 1578 (n=25) |
| lluvia | `lluvia_48h_mm` | 38.7 mm | 33 (n=103) | 70 (n=103) | 1429 (n=103) | 2 (n=25) | 23 (n=25) | 612 (n=25) |
| lluvia | `lluvia_72h_mm` | 4.6 mm | 90 (n=103) | 13 (n=103) | 17782 (n=103) | 21 (n=25) | 4 (n=25) | 9870 (n=25) |
| lluvia | `lluvia_72h_mm` | 20.9 mm | 75 (n=103) | 28 (n=103) | 7451 (n=103) | 10 (n=25) | 15 (n=25) | 3832 (n=25) |
| lluvia | `lluvia_72h_mm` | 34 mm | 52 (n=103) | 51 (n=103) | 3892 (n=103) | 5 (n=25) | 20 (n=25) | 1850 (n=25) |
| lluvia | `lluvia_72h_mm` | 51.5 mm | 28 (n=103) | 75 (n=103) | 1684 (n=103) | 2 (n=25) | 23 (n=25) | 711 (n=25) |
| lluvia | `lluvia_7d_mm` | 8.3 mm | 95 (n=103) | 8 (n=103) | 21121 (n=103) | 22 (n=25) | 3 (n=25) | 11695 (n=25) |
| lluvia | `lluvia_7d_mm` | 33.6 mm | 78 (n=103) | 25 (n=103) | 11202 (n=103) | 12 (n=25) | 13 (n=25) | 6039 (n=25) |
| lluvia | `lluvia_7d_mm` | 61.3 mm | 55 (n=103) | 48 (n=103) | 5662 (n=103) | 7 (n=25) | 18 (n=25) | 2815 (n=25) |
| lluvia | `lluvia_7d_mm` | 95.8 mm | 27 (n=103) | 76 (n=103) | 2275 (n=103) | 4 (n=25) | 21 (n=25) | 905 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm` | 0.4 mm | 90 (n=103) | 13 (n=103) | 16355 (n=103) | 23 (n=25) | 2 (n=25) | 8444 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm` | 0.9 mm | 79 (n=103) | 24 (n=103) | 10231 (n=103) | 18 (n=25) | 7 (n=25) | 5330 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm` | 1.9 mm | 66 (n=103) | 37 (n=103) | 4473 (n=103) | 14 (n=25) | 11 (n=25) | 2232 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm` | 3.9 mm | 36 (n=103) | 67 (n=103) | 1231 (n=103) | 2 (n=25) | 23 (n=25) | 591 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm` | 0.7 mm | 91 (n=103) | 12 (n=103) | 18479 (n=103) | 21 (n=25) | 4 (n=25) | 9721 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm` | 1.9 mm | 77 (n=103) | 26 (n=103) | 9381 (n=103) | 17 (n=25) | 8 (n=25) | 4794 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm` | 3.1 mm | 54 (n=103) | 49 (n=103) | 4734 (n=103) | 6 (n=25) | 19 (n=25) | 2306 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm` | 5.1 mm | 27 (n=103) | 76 (n=103) | 1766 (n=103) | 2 (n=25) | 23 (n=25) | 863 (n=25) |
| nieve | `nieve_24h_cm` | 0.1 cm | 18 (n=35) | 17 (n=35) | 562 (n=35) | 10 (n=25) | 15 (n=25) | 257 (n=25) |
| nieve | `nieve_24h_cm` | 0.2 cm | 16 (n=35) | 19 (n=35) | 491 (n=35) | 9 (n=25) | 16 (n=25) | 234 (n=25) |
| nieve | `nieve_24h_cm` | 0.6 cm | 9 (n=35) | 26 (n=35) | 315 (n=35) | 4 (n=25) | 21 (n=25) | 143 (n=25) |
| nieve | `nieve_24h_cm` | 1.7 cm | 4 (n=35) | 31 (n=35) | 131 (n=35) | 3 (n=25) | 22 (n=25) | 64 (n=25) |
| nieve | `nieve_72h_cm` | 0.1 cm | 22 (n=35) | 13 (n=35) | 1212 (n=35) | 12 (n=25) | 13 (n=25) | 514 (n=25) |
| nieve | `nieve_72h_cm` | 0.4 cm | 18 (n=35) | 17 (n=35) | 866 (n=35) | 8 (n=25) | 17 (n=25) | 398 (n=25) |
| nieve | `nieve_72h_cm` | 0.9 cm | 12 (n=35) | 23 (n=35) | 631 (n=35) | 6 (n=25) | 19 (n=25) | 275 (n=25) |
| nieve | `nieve_72h_cm` | 2.2 cm | 9 (n=35) | 26 (n=35) | 299 (n=35) | 3 (n=25) | 22 (n=25) | 147 (n=25) |
| nieve | `nieve_7d_cm` | 0.1 cm | 24 (n=35) | 11 (n=35) | 2308 (n=35) | 12 (n=25) | 13 (n=25) | 977 (n=25) |
| nieve | `nieve_7d_cm` | 0.4 cm | 20 (n=35) | 15 (n=35) | 1689 (n=35) | 8 (n=25) | 17 (n=25) | 782 (n=25) |
| nieve | `nieve_7d_cm` | 1.5 cm | 12 (n=35) | 23 (n=35) | 921 (n=35) | 4 (n=25) | 21 (n=25) | 416 (n=25) |
| nieve | `nieve_7d_cm` | 2.9 cm | 7 (n=35) | 28 (n=35) | 530 (n=35) | 1 (n=25) | 24 (n=25) | 254 (n=25) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| lluvia | `lluvia_24h_mm_pct` | p80 | 69 (n=103) | 34 (n=103) | 7072 (n=103) | 17 (n=25) | 8 (n=25) | 4098 (n=25) |
| lluvia | `lluvia_24h_mm_pct` | p90 | 43 (n=103) | 60 (n=103) | 3741 (n=103) | 10 (n=25) | 15 (n=25) | 2118 (n=25) |
| lluvia | `lluvia_24h_mm_pct` | p95 | 22 (n=103) | 81 (n=103) | 1960 (n=103) | 6 (n=25) | 19 (n=25) | 1132 (n=25) |
| lluvia | `lluvia_24h_mm_pct` | p98 | 10 (n=103) | 93 (n=103) | 818 (n=103) | 1 (n=25) | 24 (n=25) | 467 (n=25) |
| lluvia | `lluvia_24h_mm_pct` | p99 | 5 (n=103) | 98 (n=103) | 382 (n=103) | 0 (n=25) | 25 (n=25) | 213 (n=25) |
| lluvia | `lluvia_48h_mm_pct` | p80 | 65 (n=103) | 38 (n=103) | 7415 (n=103) | 12 (n=25) | 13 (n=25) | 4125 (n=25) |
| lluvia | `lluvia_48h_mm_pct` | p90 | 29 (n=103) | 74 (n=103) | 3878 (n=103) | 10 (n=25) | 15 (n=25) | 2163 (n=25) |
| lluvia | `lluvia_48h_mm_pct` | p95 | 17 (n=103) | 86 (n=103) | 1999 (n=103) | 5 (n=25) | 20 (n=25) | 1114 (n=25) |
| lluvia | `lluvia_48h_mm_pct` | p98 | 9 (n=103) | 94 (n=103) | 816 (n=103) | 3 (n=25) | 22 (n=25) | 419 (n=25) |
| lluvia | `lluvia_48h_mm_pct` | p99 | 5 (n=103) | 98 (n=103) | 378 (n=103) | 0 (n=25) | 25 (n=25) | 210 (n=25) |
| lluvia | `lluvia_72h_mm_pct` | p80 | 43 (n=103) | 60 (n=103) | 7570 (n=103) | 13 (n=25) | 12 (n=25) | 4135 (n=25) |
| lluvia | `lluvia_72h_mm_pct` | p90 | 26 (n=103) | 77 (n=103) | 3959 (n=103) | 10 (n=25) | 15 (n=25) | 2189 (n=25) |
| lluvia | `lluvia_72h_mm_pct` | p95 | 15 (n=103) | 88 (n=103) | 2021 (n=103) | 5 (n=25) | 20 (n=25) | 1078 (n=25) |
| lluvia | `lluvia_72h_mm_pct` | p98 | 7 (n=103) | 96 (n=103) | 816 (n=103) | 1 (n=25) | 24 (n=25) | 373 (n=25) |
| lluvia | `lluvia_72h_mm_pct` | p99 | 5 (n=103) | 98 (n=103) | 384 (n=103) | 0 (n=25) | 25 (n=25) | 158 (n=25) |
| lluvia | `lluvia_7d_mm_pct` | p80 | 37 (n=103) | 66 (n=103) | 7927 (n=103) | 14 (n=25) | 11 (n=25) | 4385 (n=25) |
| lluvia | `lluvia_7d_mm_pct` | p90 | 19 (n=103) | 84 (n=103) | 4037 (n=103) | 12 (n=25) | 13 (n=25) | 2164 (n=25) |
| lluvia | `lluvia_7d_mm_pct` | p95 | 11 (n=103) | 92 (n=103) | 2021 (n=103) | 4 (n=25) | 21 (n=25) | 1021 (n=25) |
| lluvia | `lluvia_7d_mm_pct` | p98 | 8 (n=103) | 95 (n=103) | 806 (n=103) | 2 (n=25) | 23 (n=25) | 334 (n=25) |
| lluvia | `lluvia_7d_mm_pct` | p99 | 5 (n=103) | 98 (n=103) | 375 (n=103) | 1 (n=25) | 24 (n=25) | 155 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p80 | 64 (n=103) | 39 (n=103) | 7096 (n=103) | 21 (n=25) | 4 (n=25) | 3941 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p90 | 37 (n=103) | 66 (n=103) | 3705 (n=103) | 11 (n=25) | 14 (n=25) | 2025 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p95 | 15 (n=103) | 88 (n=103) | 1962 (n=103) | 4 (n=25) | 21 (n=25) | 1085 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p98 | 12 (n=103) | 91 (n=103) | 801 (n=103) | 2 (n=25) | 23 (n=25) | 393 (n=25) |
| lluvia | `lluvia_max_horaria_24h_mm_pct` | p99 | 4 (n=103) | 99 (n=103) | 385 (n=103) | 0 (n=25) | 25 (n=25) | 174 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p80 | 38 (n=103) | 65 (n=103) | 7470 (n=103) | 14 (n=25) | 11 (n=25) | 3980 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p90 | 18 (n=103) | 85 (n=103) | 3944 (n=103) | 8 (n=25) | 17 (n=25) | 2151 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p95 | 16 (n=103) | 87 (n=103) | 1980 (n=103) | 5 (n=25) | 20 (n=25) | 977 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p98 | 5 (n=103) | 98 (n=103) | 780 (n=103) | 2 (n=25) | 23 (n=25) | 336 (n=25) |
| lluvia | `lluvia_max_horaria_72h_mm_pct` | p99 | 5 (n=103) | 98 (n=103) | 374 (n=103) | 1 (n=25) | 24 (n=25) | 182 (n=25) |
| nieve | `nieve_24h_cm_pct` | p80 | 18 (n=35) | 17 (n=35) | 616 (n=35) | 12 (n=25) | 13 (n=25) | 296 (n=25) |
| nieve | `nieve_24h_cm_pct` | p90 | 17 (n=35) | 18 (n=35) | 528 (n=35) | 12 (n=25) | 13 (n=25) | 267 (n=25) |
| nieve | `nieve_24h_cm_pct` | p95 | 15 (n=35) | 20 (n=35) | 411 (n=35) | 12 (n=25) | 13 (n=25) | 213 (n=25) |
| nieve | `nieve_24h_cm_pct` | p98 | 7 (n=35) | 28 (n=35) | 259 (n=35) | 5 (n=25) | 20 (n=25) | 121 (n=25) |
| nieve | `nieve_24h_cm_pct` | p99 | 4 (n=35) | 31 (n=35) | 157 (n=35) | 5 (n=25) | 20 (n=25) | 66 (n=25) |
| nieve | `nieve_72h_cm_pct` | p80 | 23 (n=35) | 12 (n=35) | 1191 (n=35) | 13 (n=25) | 12 (n=25) | 545 (n=25) |
| nieve | `nieve_72h_cm_pct` | p90 | 19 (n=35) | 16 (n=35) | 908 (n=35) | 11 (n=25) | 14 (n=25) | 437 (n=25) |
| nieve | `nieve_72h_cm_pct` | p95 | 14 (n=35) | 21 (n=35) | 631 (n=35) | 8 (n=25) | 17 (n=25) | 306 (n=25) |
| nieve | `nieve_72h_cm_pct` | p98 | 6 (n=35) | 29 (n=35) | 356 (n=35) | 5 (n=25) | 20 (n=25) | 131 (n=25) |
| nieve | `nieve_72h_cm_pct` | p99 | 3 (n=35) | 32 (n=35) | 217 (n=35) | 3 (n=25) | 22 (n=25) | 79 (n=25) |
| nieve | `nieve_7d_cm_pct` | p80 | 22 (n=35) | 13 (n=35) | 1895 (n=35) | 11 (n=25) | 14 (n=25) | 876 (n=25) |
| nieve | `nieve_7d_cm_pct` | p90 | 13 (n=35) | 22 (n=35) | 1351 (n=35) | 8 (n=25) | 17 (n=25) | 635 (n=25) |
| nieve | `nieve_7d_cm_pct` | p95 | 8 (n=35) | 27 (n=35) | 883 (n=35) | 6 (n=25) | 19 (n=25) | 333 (n=25) |
| nieve | `nieve_7d_cm_pct` | p98 | 3 (n=35) | 32 (n=35) | 476 (n=35) | 3 (n=25) | 22 (n=25) | 133 (n=25) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=35) | 34 (n=35) | 235 (n=35) | 2 (n=25) | 23 (n=25) | 78 (n=25) |

## Todas las fuentes: nieve en Paso de Jama por lado

Eventos de nieve en `rn52_paso_jama`: 60 (AR 1, ambos 9, CL 43, lado desconocido 7, que quedan fuera de esta sección).

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
| nieve | `nieve_24h_cm` | 29 | 0.4 | 0.0 | 92 |
| nieve | `nieve_72h_cm` | 29 | 2.2 | 0.0 | 91 |
| nieve | `nieve_7d_cm` | 29 | 4.8 | 0.0 | 91 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 21 (n=29) | 8 (n=29) | 228 (n=29) | 9 (n=14) | 5 (n=14) | 118 (n=14) |
| nieve | `nieve_24h_cm` | 0.4 cm | 20 (n=29) | 9 (n=29) | 153 (n=29) | 7 (n=14) | 7 (n=14) | 86 (n=14) |
| nieve | `nieve_24h_cm` | 1.2 cm | 12 (n=29) | 17 (n=29) | 85 (n=29) | 5 (n=14) | 9 (n=14) | 54 (n=14) |
| nieve | `nieve_24h_cm` | 3.8 cm | 5 (n=29) | 24 (n=29) | 38 (n=29) | 0 (n=14) | 14 (n=14) | 20 (n=14) |
| nieve | `nieve_72h_cm` | 0.4 cm | 22 (n=29) | 7 (n=29) | 336 (n=29) | 7 (n=14) | 7 (n=14) | 178 (n=14) |
| nieve | `nieve_72h_cm` | 1 cm | 18 (n=29) | 11 (n=29) | 236 (n=29) | 6 (n=14) | 8 (n=14) | 135 (n=14) |
| nieve | `nieve_72h_cm` | 3.6 cm | 13 (n=29) | 16 (n=29) | 109 (n=29) | 0 (n=14) | 14 (n=14) | 66 (n=14) |
| nieve | `nieve_72h_cm` | 5.8 cm | 8 (n=29) | 21 (n=29) | 78 (n=29) | 0 (n=14) | 14 (n=14) | 44 (n=14) |
| nieve | `nieve_7d_cm` | 0.6 cm | 22 (n=29) | 7 (n=29) | 543 (n=29) | 7 (n=14) | 7 (n=14) | 292 (n=14) |
| nieve | `nieve_7d_cm` | 1.3 cm | 18 (n=29) | 11 (n=29) | 417 (n=29) | 6 (n=14) | 8 (n=14) | 235 (n=14) |
| nieve | `nieve_7d_cm` | 5.2 cm | 13 (n=29) | 16 (n=29) | 199 (n=29) | 0 (n=14) | 14 (n=14) | 113 (n=14) |
| nieve | `nieve_7d_cm` | 10.6 cm | 6 (n=29) | 23 (n=29) | 96 (n=29) | 0 (n=14) | 14 (n=14) | 51 (n=14) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 22 (n=29) | 7 (n=29) | 222 (n=29) | 9 (n=14) | 5 (n=14) | 123 (n=14) |
| nieve | `nieve_24h_cm_pct` | p90 | 20 (n=29) | 9 (n=29) | 164 (n=29) | 9 (n=14) | 5 (n=14) | 103 (n=14) |
| nieve | `nieve_24h_cm_pct` | p95 | 15 (n=29) | 14 (n=29) | 88 (n=29) | 8 (n=14) | 6 (n=14) | 70 (n=14) |
| nieve | `nieve_24h_cm_pct` | p98 | 8 (n=29) | 21 (n=29) | 42 (n=29) | 5 (n=14) | 9 (n=14) | 35 (n=14) |
| nieve | `nieve_24h_cm_pct` | p99 | 3 (n=29) | 26 (n=29) | 20 (n=29) | 2 (n=14) | 12 (n=14) | 20 (n=14) |
| nieve | `nieve_72h_cm_pct` | p80 | 23 (n=29) | 6 (n=29) | 360 (n=29) | 9 (n=14) | 5 (n=14) | 204 (n=14) |
| nieve | `nieve_72h_cm_pct` | p90 | 17 (n=29) | 12 (n=29) | 191 (n=29) | 7 (n=14) | 7 (n=14) | 140 (n=14) |
| nieve | `nieve_72h_cm_pct` | p95 | 12 (n=29) | 17 (n=29) | 106 (n=29) | 6 (n=14) | 8 (n=14) | 98 (n=14) |
| nieve | `nieve_72h_cm_pct` | p98 | 4 (n=29) | 25 (n=29) | 45 (n=29) | 2 (n=14) | 12 (n=14) | 34 (n=14) |
| nieve | `nieve_72h_cm_pct` | p99 | 1 (n=29) | 28 (n=29) | 24 (n=29) | 1 (n=14) | 13 (n=14) | 20 (n=14) |
| nieve | `nieve_7d_cm_pct` | p80 | 18 (n=29) | 11 (n=29) | 411 (n=29) | 7 (n=14) | 7 (n=14) | 267 (n=14) |
| nieve | `nieve_7d_cm_pct` | p90 | 15 (n=29) | 14 (n=29) | 225 (n=29) | 5 (n=14) | 9 (n=14) | 198 (n=14) |
| nieve | `nieve_7d_cm_pct` | p95 | 9 (n=29) | 20 (n=29) | 116 (n=29) | 2 (n=14) | 12 (n=14) | 91 (n=14) |
| nieve | `nieve_7d_cm_pct` | p98 | 1 (n=29) | 28 (n=29) | 52 (n=29) | 0 (n=14) | 14 (n=14) | 19 (n=14) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=29) | 28 (n=29) | 22 (n=29) | 0 (n=14) | 14 (n=14) | 12 (n=14) |

### Nieve combinado (AR + ambos + CL)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 34 | 0.2 | 0.0 | 91 |
| nieve | `nieve_72h_cm` | 34 | 1.2 | 0.0 | 91 |
| nieve | `nieve_7d_cm` | 34 | 2.6 | 0.0 | 84 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 22 (n=34) | 12 (n=34) | 370 (n=34) | 12 (n=19) | 7 (n=19) | 197 (n=19) |
| nieve | `nieve_24h_cm` | 0.3 cm | 20 (n=34) | 14 (n=34) | 268 (n=34) | 9 (n=19) | 10 (n=19) | 145 (n=19) |
| nieve | `nieve_24h_cm` | 1.2 cm | 12 (n=34) | 22 (n=34) | 126 (n=34) | 7 (n=19) | 12 (n=19) | 77 (n=19) |
| nieve | `nieve_24h_cm` | 3.3 cm | 5 (n=34) | 29 (n=34) | 51 (n=34) | 3 (n=19) | 16 (n=19) | 33 (n=19) |
| nieve | `nieve_72h_cm` | 0.2 cm | 24 (n=34) | 10 (n=34) | 677 (n=34) | 13 (n=19) | 6 (n=19) | 360 (n=19) |
| nieve | `nieve_72h_cm` | 0.6 cm | 20 (n=34) | 14 (n=34) | 484 (n=34) | 10 (n=19) | 9 (n=19) | 252 (n=19) |
| nieve | `nieve_72h_cm` | 2.7 cm | 15 (n=34) | 19 (n=34) | 182 (n=34) | 5 (n=19) | 14 (n=19) | 115 (n=19) |
| nieve | `nieve_72h_cm` | 5.4 cm | 8 (n=34) | 26 (n=34) | 96 (n=34) | 1 (n=19) | 18 (n=19) | 58 (n=19) |
| nieve | `nieve_7d_cm` | 0.3 cm | 24 (n=34) | 10 (n=34) | 1077 (n=34) | 10 (n=19) | 9 (n=19) | 570 (n=19) |
| nieve | `nieve_7d_cm` | 0.8 cm | 22 (n=34) | 12 (n=34) | 829 (n=34) | 10 (n=19) | 9 (n=19) | 442 (n=19) |
| nieve | `nieve_7d_cm` | 4.9 cm | 14 (n=34) | 20 (n=34) | 261 (n=34) | 1 (n=19) | 18 (n=19) | 162 (n=19) |
| nieve | `nieve_7d_cm` | 10.5 cm | 7 (n=34) | 27 (n=34) | 117 (n=34) | 1 (n=19) | 18 (n=19) | 63 (n=19) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 23 (n=34) | 11 (n=34) | 390 (n=34) | 13 (n=19) | 6 (n=19) | 214 (n=19) |
| nieve | `nieve_24h_cm_pct` | p90 | 21 (n=34) | 13 (n=34) | 305 (n=34) | 13 (n=19) | 6 (n=19) | 185 (n=19) |
| nieve | `nieve_24h_cm_pct` | p95 | 16 (n=34) | 18 (n=34) | 194 (n=34) | 12 (n=19) | 7 (n=19) | 133 (n=19) |
| nieve | `nieve_24h_cm_pct` | p98 | 8 (n=34) | 26 (n=34) | 95 (n=34) | 8 (n=19) | 11 (n=19) | 67 (n=19) |
| nieve | `nieve_24h_cm_pct` | p99 | 3 (n=34) | 31 (n=34) | 44 (n=34) | 5 (n=19) | 14 (n=19) | 39 (n=19) |
| nieve | `nieve_72h_cm_pct` | p80 | 26 (n=34) | 8 (n=34) | 667 (n=34) | 13 (n=19) | 6 (n=19) | 356 (n=19) |
| nieve | `nieve_72h_cm_pct` | p90 | 20 (n=34) | 14 (n=34) | 412 (n=34) | 11 (n=19) | 8 (n=19) | 254 (n=19) |
| nieve | `nieve_72h_cm_pct` | p95 | 12 (n=34) | 22 (n=34) | 232 (n=34) | 10 (n=19) | 9 (n=19) | 174 (n=19) |
| nieve | `nieve_72h_cm_pct` | p98 | 4 (n=34) | 30 (n=34) | 97 (n=34) | 4 (n=19) | 15 (n=19) | 65 (n=19) |
| nieve | `nieve_72h_cm_pct` | p99 | 1 (n=34) | 33 (n=34) | 50 (n=34) | 2 (n=19) | 17 (n=19) | 37 (n=19) |
| nieve | `nieve_7d_cm_pct` | p80 | 21 (n=34) | 13 (n=34) | 848 (n=34) | 11 (n=19) | 8 (n=19) | 486 (n=19) |
| nieve | `nieve_7d_cm_pct` | p90 | 15 (n=34) | 19 (n=34) | 487 (n=34) | 9 (n=19) | 10 (n=19) | 347 (n=19) |
| nieve | `nieve_7d_cm_pct` | p95 | 9 (n=34) | 25 (n=34) | 245 (n=34) | 5 (n=19) | 14 (n=19) | 180 (n=19) |
| nieve | `nieve_7d_cm_pct` | p98 | 1 (n=34) | 33 (n=34) | 105 (n=34) | 1 (n=19) | 18 (n=19) | 59 (n=19) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=34) | 33 (n=34) | 49 (n=34) | 1 (n=19) | 18 (n=19) | 39 (n=19) |


## Solo fuentes estables: nieve en Paso de Jama por lado

Eventos de nieve en `rn52_paso_jama`: 57 (AR 1, ambos 9, CL 41, lado desconocido 6, que quedan fuera de esta sección).

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
| nieve | `nieve_24h_cm` | 28 | 0.6 | 0.0 | 93 |
| nieve | `nieve_72h_cm` | 28 | 2.5 | 0.0 | 92 |
| nieve | `nieve_7d_cm` | 28 | 4.9 | 0.0 | 91 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 21 (n=28) | 7 (n=28) | 228 (n=28) | 8 (n=13) | 5 (n=13) | 119 (n=13) |
| nieve | `nieve_24h_cm` | 0.4 cm | 20 (n=28) | 8 (n=28) | 153 (n=28) | 6 (n=13) | 7 (n=13) | 87 (n=13) |
| nieve | `nieve_24h_cm` | 1.2 cm | 12 (n=28) | 16 (n=28) | 85 (n=28) | 4 (n=13) | 9 (n=13) | 55 (n=13) |
| nieve | `nieve_24h_cm` | 3.8 cm | 5 (n=28) | 23 (n=28) | 38 (n=28) | 0 (n=13) | 13 (n=13) | 20 (n=13) |
| nieve | `nieve_72h_cm` | 0.4 cm | 22 (n=28) | 6 (n=28) | 336 (n=28) | 6 (n=13) | 7 (n=13) | 179 (n=13) |
| nieve | `nieve_72h_cm` | 1 cm | 18 (n=28) | 10 (n=28) | 236 (n=28) | 5 (n=13) | 8 (n=13) | 136 (n=13) |
| nieve | `nieve_72h_cm` | 3.6 cm | 13 (n=28) | 15 (n=28) | 109 (n=28) | 0 (n=13) | 13 (n=13) | 66 (n=13) |
| nieve | `nieve_72h_cm` | 5.8 cm | 8 (n=28) | 20 (n=28) | 78 (n=28) | 0 (n=13) | 13 (n=13) | 44 (n=13) |
| nieve | `nieve_7d_cm` | 0.6 cm | 22 (n=28) | 6 (n=28) | 543 (n=28) | 6 (n=13) | 7 (n=13) | 293 (n=13) |
| nieve | `nieve_7d_cm` | 1.3 cm | 18 (n=28) | 10 (n=28) | 417 (n=28) | 5 (n=13) | 8 (n=13) | 236 (n=13) |
| nieve | `nieve_7d_cm` | 5.2 cm | 13 (n=28) | 15 (n=28) | 199 (n=28) | 0 (n=13) | 13 (n=13) | 113 (n=13) |
| nieve | `nieve_7d_cm` | 10.6 cm | 6 (n=28) | 22 (n=28) | 96 (n=28) | 0 (n=13) | 13 (n=13) | 51 (n=13) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 22 (n=28) | 6 (n=28) | 222 (n=28) | 8 (n=13) | 5 (n=13) | 124 (n=13) |
| nieve | `nieve_24h_cm_pct` | p90 | 20 (n=28) | 8 (n=28) | 164 (n=28) | 8 (n=13) | 5 (n=13) | 104 (n=13) |
| nieve | `nieve_24h_cm_pct` | p95 | 15 (n=28) | 13 (n=28) | 88 (n=28) | 7 (n=13) | 6 (n=13) | 71 (n=13) |
| nieve | `nieve_24h_cm_pct` | p98 | 8 (n=28) | 20 (n=28) | 42 (n=28) | 4 (n=13) | 9 (n=13) | 36 (n=13) |
| nieve | `nieve_24h_cm_pct` | p99 | 3 (n=28) | 25 (n=28) | 20 (n=28) | 2 (n=13) | 11 (n=13) | 20 (n=13) |
| nieve | `nieve_72h_cm_pct` | p80 | 23 (n=28) | 5 (n=28) | 360 (n=28) | 8 (n=13) | 5 (n=13) | 205 (n=13) |
| nieve | `nieve_72h_cm_pct` | p90 | 17 (n=28) | 11 (n=28) | 191 (n=28) | 6 (n=13) | 7 (n=13) | 141 (n=13) |
| nieve | `nieve_72h_cm_pct` | p95 | 12 (n=28) | 16 (n=28) | 106 (n=28) | 5 (n=13) | 8 (n=13) | 99 (n=13) |
| nieve | `nieve_72h_cm_pct` | p98 | 4 (n=28) | 24 (n=28) | 45 (n=28) | 2 (n=13) | 11 (n=13) | 34 (n=13) |
| nieve | `nieve_72h_cm_pct` | p99 | 1 (n=28) | 27 (n=28) | 24 (n=28) | 1 (n=13) | 12 (n=13) | 20 (n=13) |
| nieve | `nieve_7d_cm_pct` | p80 | 18 (n=28) | 10 (n=28) | 411 (n=28) | 6 (n=13) | 7 (n=13) | 268 (n=13) |
| nieve | `nieve_7d_cm_pct` | p90 | 15 (n=28) | 13 (n=28) | 225 (n=28) | 5 (n=13) | 8 (n=13) | 198 (n=13) |
| nieve | `nieve_7d_cm_pct` | p95 | 9 (n=28) | 19 (n=28) | 116 (n=28) | 2 (n=13) | 11 (n=13) | 91 (n=13) |
| nieve | `nieve_7d_cm_pct` | p98 | 1 (n=28) | 27 (n=28) | 52 (n=28) | 0 (n=13) | 13 (n=13) | 19 (n=13) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=28) | 27 (n=28) | 22 (n=28) | 0 (n=13) | 13 (n=13) | 12 (n=13) |

### Nieve combinado (AR + ambos + CL)

#### Variables en días con y sin evento (ajuste)

| causa | variable | días con evento | mediana con evento | mediana sin evento | percentil mediano con evento |
|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 33 | 0.2 | 0.0 | 92 |
| nieve | `nieve_72h_cm` | 33 | 1.3 | 0.0 | 91 |
| nieve | `nieve_7d_cm` | 33 | 3.1 | 0.0 | 84 |

#### Candidatos en unidades absolutas (mm / cm de ERA5)

| causa | variable | umbral | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm` | 0.1 cm | 22 (n=33) | 11 (n=33) | 370 (n=33) | 11 (n=18) | 7 (n=18) | 198 (n=18) |
| nieve | `nieve_24h_cm` | 0.3 cm | 20 (n=33) | 13 (n=33) | 268 (n=33) | 8 (n=18) | 10 (n=18) | 146 (n=18) |
| nieve | `nieve_24h_cm` | 1.2 cm | 12 (n=33) | 21 (n=33) | 126 (n=33) | 6 (n=18) | 12 (n=18) | 78 (n=18) |
| nieve | `nieve_24h_cm` | 3.3 cm | 5 (n=33) | 28 (n=33) | 51 (n=33) | 2 (n=18) | 16 (n=18) | 34 (n=18) |
| nieve | `nieve_72h_cm` | 0.2 cm | 24 (n=33) | 9 (n=33) | 677 (n=33) | 12 (n=18) | 6 (n=18) | 361 (n=18) |
| nieve | `nieve_72h_cm` | 0.6 cm | 20 (n=33) | 13 (n=33) | 484 (n=33) | 9 (n=18) | 9 (n=18) | 253 (n=18) |
| nieve | `nieve_72h_cm` | 2.7 cm | 15 (n=33) | 18 (n=33) | 182 (n=33) | 4 (n=18) | 14 (n=18) | 116 (n=18) |
| nieve | `nieve_72h_cm` | 5.4 cm | 8 (n=33) | 25 (n=33) | 96 (n=33) | 1 (n=18) | 17 (n=18) | 58 (n=18) |
| nieve | `nieve_7d_cm` | 0.3 cm | 24 (n=33) | 9 (n=33) | 1077 (n=33) | 9 (n=18) | 9 (n=18) | 571 (n=18) |
| nieve | `nieve_7d_cm` | 0.8 cm | 22 (n=33) | 11 (n=33) | 829 (n=33) | 9 (n=18) | 9 (n=18) | 443 (n=18) |
| nieve | `nieve_7d_cm` | 4.9 cm | 14 (n=33) | 19 (n=33) | 261 (n=33) | 1 (n=18) | 17 (n=18) | 162 (n=18) |
| nieve | `nieve_7d_cm` | 10.5 cm | 7 (n=33) | 26 (n=33) | 117 (n=33) | 1 (n=18) | 17 (n=18) | 63 (n=18) |

#### Candidatos en percentil por celda (climatología 2016–2022, misma estación)

| causa | variable | percentil | train aciertos | train fallos | train falsas alarmas | test aciertos | test fallos | test falsas alarmas |
|---|---|---|---|---|---|---|---|---|
| nieve | `nieve_24h_cm_pct` | p80 | 23 (n=33) | 10 (n=33) | 390 (n=33) | 12 (n=18) | 6 (n=18) | 215 (n=18) |
| nieve | `nieve_24h_cm_pct` | p90 | 21 (n=33) | 12 (n=33) | 305 (n=33) | 12 (n=18) | 6 (n=18) | 186 (n=18) |
| nieve | `nieve_24h_cm_pct` | p95 | 16 (n=33) | 17 (n=33) | 194 (n=33) | 11 (n=18) | 7 (n=18) | 134 (n=18) |
| nieve | `nieve_24h_cm_pct` | p98 | 8 (n=33) | 25 (n=33) | 95 (n=33) | 7 (n=18) | 11 (n=18) | 68 (n=18) |
| nieve | `nieve_24h_cm_pct` | p99 | 3 (n=33) | 30 (n=33) | 44 (n=33) | 5 (n=18) | 13 (n=18) | 39 (n=18) |
| nieve | `nieve_72h_cm_pct` | p80 | 26 (n=33) | 7 (n=33) | 667 (n=33) | 12 (n=18) | 6 (n=18) | 357 (n=18) |
| nieve | `nieve_72h_cm_pct` | p90 | 20 (n=33) | 13 (n=33) | 412 (n=33) | 10 (n=18) | 8 (n=18) | 255 (n=18) |
| nieve | `nieve_72h_cm_pct` | p95 | 12 (n=33) | 21 (n=33) | 232 (n=33) | 9 (n=18) | 9 (n=18) | 175 (n=18) |
| nieve | `nieve_72h_cm_pct` | p98 | 4 (n=33) | 29 (n=33) | 97 (n=33) | 4 (n=18) | 14 (n=18) | 65 (n=18) |
| nieve | `nieve_72h_cm_pct` | p99 | 1 (n=33) | 32 (n=33) | 50 (n=33) | 2 (n=18) | 16 (n=18) | 37 (n=18) |
| nieve | `nieve_7d_cm_pct` | p80 | 21 (n=33) | 12 (n=33) | 848 (n=33) | 10 (n=18) | 8 (n=18) | 487 (n=18) |
| nieve | `nieve_7d_cm_pct` | p90 | 15 (n=33) | 18 (n=33) | 487 (n=33) | 9 (n=18) | 9 (n=18) | 347 (n=18) |
| nieve | `nieve_7d_cm_pct` | p95 | 9 (n=33) | 24 (n=33) | 245 (n=33) | 5 (n=18) | 13 (n=18) | 180 (n=18) |
| nieve | `nieve_7d_cm_pct` | p98 | 1 (n=33) | 32 (n=33) | 105 (n=33) | 1 (n=18) | 17 (n=18) | 59 (n=18) |
| nieve | `nieve_7d_cm_pct` | p99 | 1 (n=33) | 32 (n=33) | 49 (n=33) | 1 (n=18) | 17 (n=18) | 39 (n=18) |

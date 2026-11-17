# Landing de "Jama al Día"

Página de presentación del proyecto para la hackathon: estática, sin build, sin recursos
externos (ni fuentes, ni CDN, ni imágenes remotas) y con una Content-Security-Policy estricta.

| Archivo | Qué es |
|---|---|
| `public/index.html` | La página (texto en español de Argentina). |
| `public/app.js` | Menú móvil, sombra del encabezado y aparición al hacer scroll. La página se lee igual sin JavaScript. |
| `public/styles.css` | **Generado** por Tailwind CSS a partir de `src/input.css`. Se commitea; no editar a mano. |
| `src/input.css`, `tailwind.config.js` | Fuente de los estilos y la paleta (no se publican). |

Solo `public/` se publica.

## Verla

```bash
python3 -m http.server 8000 --directory landing/public
```

Y abrir http://localhost:8000/.

## Regenerar `styles.css`

Después de cambiar clases en `public/index.html`, `public/app.js` o `src/input.css`, con el
[CLI independiente de Tailwind CSS](https://tailwindcss.com/blog/standalone-cli) v3.4 (no
necesita Node):

```bash
cd landing
tailwindcss -c tailwind.config.js -i src/input.css -o public/styles.css --minify
```

## Desplegar en Vercel

`vercel.json`, en la raíz del repo, ya deja todo configurado: sin framework, sin install, un
build que no hace nada (el CSS ya está compilado) y `landing/public` como directorio de salida.
También agrega los encabezados de seguridad (CSP, `nosniff`, `no-referrer`) y URLs sin `.html`.

1. En Vercel: **Add New → Project** e importar este repo.
2. Dejar **Root Directory** en la raíz (`./`) y no tocar los comandos: los toma de `vercel.json`.
3. **Deploy**.

Si se cambian estilos, regenerar `public/styles.css` y commitearlo: Vercel no compila Tailwind.

## Contenido

Secciones: Hero, El problema y la solución, Beneficios, Características técnicas, Casos de uso
y Sumate (alertas y contacto).

- **Cifras fijas.** "67 cierres desde 2016", "51 por nieve" y "55 solo del lado chileno"
  salen de `assets/jama/cierres.json` (cierres totales o parciales sin confianza baja, el
  mismo criterio de la página de estado). "15 puntos críticos" sale de `assets/geo/puntos.geojson`.
  Si cambia el catálogo, hay que actualizarlas a mano.
- **Mapa.** El SVG del Hero se generó una vez con las trazas de `assets/geo/rutas.geojson`, el
  Tren Solar de `assets/geo/ferrocarril.geojson` y los puntos de `assets/geo/puntos.geojson`
  (proyección equirectangular, una de cada 12 coordenadas de ruta). No muestra riesgo.
- **Casos de uso.** Las tres citas (Roberto Gómez, Marcela Apaza, Lucas Fernández) las
  aportó el equipo; no salen del pipeline.
- **Enlaces.** El canal, la página de estado y el formulario del plan de flotas son los de
  `jama_al_dia` en `config.yaml`.

La página no muestra datos en vivo; ningún workflow de GitHub la publica (ver Vercel arriba).

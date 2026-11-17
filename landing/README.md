# Landing de "Jama al Día"

Página de presentación del proyecto: estática, sin recursos externos (ni fuentes, ni CDN, ni
imágenes remotas) y con una Content-Security-Policy estricta.

| Archivo | Qué es |
|---|---|
| `index.html` | La página (texto en español de Argentina). |
| `app.js` | Menú móvil, sombra del encabezado y aparición al hacer scroll. La página se lee igual sin JavaScript. |
| `styles.css` | **Generado** por Tailwind CSS a partir de `src/input.css`. No editar a mano. |
| `src/input.css`, `tailwind.config.js` | Fuente de los estilos y la paleta. |

## Verla

```bash
python3 -m http.server 8000 --directory landing
```

Y abrir http://localhost:8000/.

## Regenerar `styles.css`

Después de cambiar clases en `index.html`, `app.js` o `src/input.css`, con el
[CLI independiente de Tailwind CSS](https://tailwindcss.com/blog/standalone-cli) v3.4 (no
necesita Node):

```bash
cd landing
tailwindcss -c tailwind.config.js -i src/input.css -o styles.css --minify
```

## Contenido

Secciones: Hero, El problema y la solución, Beneficios, Características técnicas, Testimonios,
Próximos pasos y Sumate (alertas y contacto).

- **Cifras fijas.** "67 cierres desde 2016", "51 por nieve" y "55 solo del lado chileno"
  salen de `assets/jama/cierres.json` (cierres totales o parciales sin confianza baja, el
  mismo criterio de la página de estado). "15 puntos críticos" sale de `assets/geo/puntos.geojson`.
  Si cambia el catálogo, hay que actualizarlas a mano.
- **Mapa.** El SVG del Hero se generó una vez con las trazas de `assets/geo/rutas.geojson`, el
  Tren Solar de `assets/geo/ferrocarril.geojson` y los puntos de `assets/geo/puntos.geojson`
  (proyección equirectangular, una de cada 12 coordenadas de ruta). No muestra riesgo.
- **Testimonios.** Son ejemplos ilustrativos y están rotulados como tales: reemplazarlos por
  citas reales, con permiso, antes de presentarlos como testimonios.
- **Enlaces.** El canal, la página de estado y el formulario del plan de flotas son los de
  `jama_al_dia` en `config.yaml`.

La página no muestra datos en vivo y todavía no la publica ningún workflow.

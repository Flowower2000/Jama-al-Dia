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

Los enlaces (canal, página de estado, formulario del plan de flotas) son los de `jama_al_dia`
en `config.yaml`. La página no muestra datos en vivo: el aviso de Telegram del encabezado es un
ejemplo del formato y está rotulado como tal. Todavía no la publica ningún workflow.

// Landing de "Jama al Día": menú móvil, sombra del encabezado y aparición al hacer scroll.
(() => {
  "use strict";
  document.documentElement.classList.add("js");

  const boton = document.getElementById("menu-boton");
  const menu = document.getElementById("menu-movil");
  const cerrarMenu = () => {
    menu.classList.add("hidden");
    boton.setAttribute("aria-expanded", "false");
  };
  boton.addEventListener("click", () => {
    const abierto = boton.getAttribute("aria-expanded") === "true";
    menu.classList.toggle("hidden", abierto);
    boton.setAttribute("aria-expanded", String(!abierto));
  });
  menu.addEventListener("click", (e) => {
    if (e.target.closest("a")) cerrarMenu();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") cerrarMenu();
  });

  const encabezado = document.getElementById("encabezado");
  const alScroll = () => encabezado.classList.toggle("shadow-lg", window.scrollY > 8);
  window.addEventListener("scroll", alScroll, { passive: true });
  alScroll();

  const bloques = document.querySelectorAll(".aparecer");
  if ("IntersectionObserver" in window) {
    const obs = new IntersectionObserver(
      (entradas) => {
        for (const e of entradas) {
          if (e.isIntersecting) {
            e.target.classList.add("visible");
            obs.unobserve(e.target);
          }
        }
      },
      { rootMargin: "0px 0px -10% 0px" },
    );
    bloques.forEach((b) => obs.observe(b));
  } else {
    bloques.forEach((b) => b.classList.add("visible"));
  }
})();

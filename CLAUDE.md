# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es este repositorio

Este es el repositorio especial de perfil de GitHub de **JAPEREZ-L001** (un repo cuyo nombre coincide exactamente con el nombre de usuario). GitHub renderiza su `README.md` directamente en la página de perfil del usuario: https://github.com/JAPEREZ-L001

No es una aplicación de software: no hay build, lint, tests ni dependencias que instalar. El contenido completo son dos archivos:

- `README.md` — el perfil que se muestra en GitHub.
- `assets/profile-banner.svg` — banner SVG hecho a mano que se referencia desde el README.

## Estructura del README

El README está organizado en secciones delimitadas por comentarios HTML y encabezados `##`/`###`, en este orden:

1. **Hero/banner** — imagen `assets/profile-banner.svg` + typing SVG animado (readme-typing-svg.demolab.com).
2. **Sobre mí** — bullets de estado actual (estudios, stack, intereses).
3. **🛠️ Stack** — badges de shields.io agrupados por categoría (Lenguajes, Frontend & UI, Backend/datos/formularios, IA/ML, Bases de datos, Testing, Herramientas y entornos).
4. **Estado actual** — tabla con datos básicos (nombre, rol, formación, stack principal), seguida de widgets de estadísticas dinámicas (github-readme-stats, komarev visit counter, streak stats, trophy, activity graph), todos apuntando a `username=JAPEREZ-L001`.
5. **🔥 Proyectos Destacados** — pins de repos vía github-readme-stats `/api/pin`, con enlaces a `github.com/JAPEREZ-L001/<repo>`.
6. **Frase personal** y **Contacto**.

La estética (adoptada en 2026-10 a partir de la paleta real de Computer Science Hub —
`Computer-Sciencie-Hub/computer-science-hub-wiki`, página "Diseño Visual") es "premium dark con
glow sutil": fondo casi negro, acento emerald dominante, tipografía Montserrat, sin pixel-art ni
framing de terminal/videojuego. Todo el contenido va en español salvo los nombres de
tecnologías/badges.

## Paleta de colores

Tomada de la paleta *real* de CSH (la que efectivamente ve el visitante en `cshdevs.org`, no solo
los tokens OKLCH declarados — ahí el acento dominante real es emerald, no el teal del token
`--accent`):

| Rol | Hex | Uso en este repo |
|---|---|---|
| Fondo | `#0d0d0d` | `bg_color`/`background` de todos los widgets dinámicos y banner |
| Fondo hero | `#050505` | Variante más oscura para el glow del banner |
| Texto | `#f8f8f8` | `text_color`/`point` de widgets, texto principal del banner |
| Texto secundario | `#8f8f8f` | Texto atenuado (labels, `sideLabels`, `dates`) |
| Acento primario | `#34d399` (emerald-400) | `title_color`/`color`/`ring`/`fire`, texto del rol en el banner |
| Acento secundario | `#00c6c9` (teal, token oficial de CSH) | `icon_color`/`line`, divisor del banner |
| Acento cálido | `#f6922e` | Toques puntuales (ej. el acento interior de la marca geométrica del banner) |
| Borde | `#161616` | Bordes sutiles donde no se usa `hide_border` |

## Convenciones al editar

- **Idioma**: todo el texto visible del README va en español (es el idioma del resto del contenido); los nombres de tecnologías, badges y URLs se mantienen en inglés/formato original.
- **No eliminar información**: este README tiene historial de reorganizaciones que accidentalmente borraron contenido (badges, secciones de stats, la frase personal). Al reorganizar, mover/recolorear es válido; borrar un dato existente (badge, bullet, proyecto, contacto) no lo es salvo pedido explícito.
- **Badges de stack**: usar el formato shields.io `for-the-badge` ya establecido, con los colores de marca nativos de cada tecnología (esos no se recolorean con la paleta del perfil).
- **Widgets dinámicos**: todos los servicios de terceros (github-readme-stats, streak-stats, trophy, activity-graph, komarev) están fijados a `username=JAPEREZ-L001` — si se agregan nuevos, usar la paleta de la tabla de arriba.
- **SVG del banner**: `assets/profile-banner.svg` usa un gradiente de fondo casi negro, un glow radial emerald con `feGaussianBlur`, y una marca geométrica propia (no es el isotipo de CSH, que es la marca distintiva de esa organización). Mantener el `viewBox="0 0 1200 280"` si se regenera. El `font-family` apunta a `'Montserrat', 'Segoe UI', sans-serif`: GitHub sanitiza SVGs embebidos y no carga fuentes externas, así que el texto cae al fallback del sistema — es una limitación conocida, no un bug.
- Al añadir un nuevo repo destacado en "Proyectos Destacados", seguir el patrón existente: pin de github-readme-stats + badges de stack + lista de sub-repos (producción/testing/wiki) si aplica.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es este repositorio

Este es el repositorio especial de perfil de GitHub de **JAPEREZ-L001** (un repo cuyo nombre coincide exactamente con el nombre de usuario). GitHub renderiza su `README.md` directamente en la página de perfil del usuario: https://github.com/JAPEREZ-L001

## Cómo está construido el perfil (desde 2026-10)

El perfil es una copia exacta de un diseño hecho en Claude Design ("Perfil GitHub JL"). Como GitHub no permite CSS en los README, el diseño se renderiza a imágenes:

- `scripts/render_profile.py` — **fuente de verdad**. Contiene todos los datos del perfil (experiencia, proyectos, stack, organizaciones, contacto) y el HTML/CSS del diseño. Lo renderiza con Chromium headless (Playwright), captura cada sección como PNG en `assets/readme/` y **regenera `README.md`**.
- `assets/readme/*.png` — imágenes generadas (a 2x). No editarlas a mano.
- `README.md` — generado. No editarlo a mano: cualquier cambio se pierde en la siguiente ejecución.

Para cambiar algo: edita los datos o el HTML en el script y ejecútalo:

```bash
pip install playwright && python -m playwright install chromium
npm install --prefix scripts @fontsource/jetbrains-mono @fontsource/space-grotesk @fontsource/silkscreen
python scripts/render_profile.py
```

(`FONTS_DIR` y `CHROME_PATH` permiten apuntar a otras rutas de fuentes o de Chromium.)

## Detalles del README que no hay que romper

- Las piezas que deben ser enlaces se capturan por separado: navegación (`nav-*`, enlazan a anclas `<a id>`), badges de contacto (`badge-*`), celdas de organizaciones (`org-*`) y enlaces del pie (`link-*`). Sus anchos se escriben en porcentaje del ancho de diseño (774 px) para que escalen igual que las secciones completas.
- Todas las imágenes llevan `align="top"`: evita el hueco de ~6 px que deja la línea de texto bajo una imagen en línea. No usar `align="left"`/`"right"`: GitHub les añade 20 px de padding.
- `nav-spacer` empuja los badges al borde derecho de la fila de navegación.
- Los espacios entre secciones van dentro de las propias imágenes (padding de 48 px), así que no hay que añadir `<br>` extra ni párrafos.
- El script fija alturas enteras y separa los bloques antes de capturar para que ninguna imagen arrastre una fila de píxeles del bloque vecino.

## Estilo y contenido

- Estética: terminal oscura sobre el fondo de GitHub dark (`#0d1117`), superficie `#161b22`, bordes `#30363d`/`#21262d`, texto `#e6edf3`/`#c9d1d9`, atenuado `#8b949e`, un solo acento verde fósforo `#7ee787`. Tipografías: JetBrains Mono (cuerpo), Space Grotesk (títulos), Silkscreen (monograma "JL").
- El contenido sigue el CV de Josué (experiencia, formación, stack por categorías). Las estadísticas de GitHub (471 contribuciones, lenguajes) son una foto estática: hay que actualizarlas a mano en el script.
- Todo el texto visible va en español; nombres de tecnologías en su forma original.
- No eliminar información (experiencia, proyectos, contacto, organizaciones) salvo pedido explícito.

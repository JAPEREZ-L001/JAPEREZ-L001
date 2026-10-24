"""Renderiza el perfil (diseño de Claude Design) a imágenes PNG y regenera README.md.

GitHub no permite CSS en los README, así que cada sección del diseño se captura
como imagen con un Chromium headless y el README las apila. Las piezas que deben
ser enlaces (navegación, badges de contacto, organizaciones) se capturan por
separado para poder envolverlas en <a>.

Uso:
    pip install playwright
    npm install --prefix scripts @fontsource/jetbrains-mono @fontsource/space-grotesk @fontsource/silkscreen
    python scripts/render_profile.py

Para cambiar contenido, edita los datos de abajo y vuelve a ejecutar.
"""

import json
import os
import pathlib

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "readme"
FONTS = pathlib.Path(os.environ.get("FONTS_DIR", ROOT / "scripts" / "node_modules" / "@fontsource"))
CHROME = os.environ.get("CHROME_PATH")  # opcional

W = 774  # ancho del área de contenido del diseño (880 - márgenes del marco)
ACC = "#7ee787"

GITHUB = "https://github.com/JAPEREZ-L001"
EMAIL = "japereze25@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/josu%C3%A9-adona%C3%AD-p%C3%A9rez-l%C3%B3pez-6666193a8"

HIGHLIGHTS = [
    ("2022", "construyendo software en gobierno, educación, salud y startup"),
    ("6", "roles de desarrollo y soporte técnico"),
    ("7", "hallazgos de seguridad en una auditoría RLS de 8 tablas"),
]

JOBS = [
    ("feb 2026 – hoy", "Desarrollador Full Stack", "Haiku",
     "Gestión segura de credenciales de proveedores de IA con Supabase Vault y RPC. Auditoría RLS con corrección de una vulnerabilidad crítica. Migración del frontend a un esquema normalizado y 12 PRs entre frontend y backend.",
     ["TypeScript", "Supabase", "Zod", "RLS"], True),
    ("jun 2026 – hoy", "Soporte Técnico Nivel 1", "HES · DoctorSV",
     "Soporte a médicos y usuarios de la plataforma de telemedicina. Más de 630 tickets en dos meses con 95% de resolución. Creé Atajos N1, un bookmarklet en JavaScript que automatiza el llenado de tickets.",
     ["ServiceDesk Plus", "Jira", "JavaScript"], True),
    ("2025", "Desarrollador / Soporte TIC", "Universidad Don Bosco",
     "Desarrollé Computer Science Hub. Automaticé el aprovisionamiento de estaciones con Python y PowerShell y realicé auditorías de red LAN.",
     ["Python", "PowerShell", "Nmap", "Wireshark"], False),
    ("2024", "Desarrollador", "Tribunal Supremo Electoral",
     "Mantenimiento del sistema de inventario de kits electorales durante el proceso presidencial y legislativo, en sistemas de alta criticidad.",
     ["C#", "WinForms", "SQL Server"], False),
    ("2023", "Desarrollador Full Stack", "MINDEL",
     "Mantenimiento del Sistema de Gestión de Adquisiciones en producción, apoyo en auditoría de logs y automatización de respaldos y despliegues.",
     ["Visual Basic", "SQL Server", "DevExpress", "PowerShell"], False),
    ("2022", "Desarrollador", "Colegio El Espíritu Santo",
     "Sistema de Gestión de Notas y Sistema de Expedientes de la clínica escolar.",
     ["PHP", "MySQL", "C#", "WPF"], False),
]

PROJECTS = [
    ("ShiftSyncMega", "en desarrollo · meta nov 2026",
     "Herramienta para consultar los horarios de turnos de un equipo con 5 sedes. Lee una Google Sheet sin modificarla y filtra por sede y rol.",
     ["PRD · PMBOK", "Google Sheets", "Google Stitch", "ADRs"]),
    ("Computer Science Hub", "fundador",
     "Plataforma web de la primera comunidad estudiantil de Ciencias de la Computación de la Universidad Don Bosco, que fundé y organizo.",
     ["React", "TypeScript", "Supabase", "Vercel"]),
]

GROUPS = [
    ("Principales", ["React", "TypeScript", "JavaScript", "C#", ".NET", "Node.js", "PostgreSQL", "SQL Server", "Supabase", "Git"], True),
    ("Adicionales", ["Python", "PHP", "Visual Basic", "Express", "Tailwind CSS", "DevExpress", "WPF/XAML", "MySQL", "PowerShell", "Zod", "Vite", "Vercel", "Java", "HTML/CSS", "Bootstrap", "Bash"], False),
    ("Seguridad", ["Row Level Security", "Supabase Vault", "Auditoría de accesos", "Nmap", "Wireshark"], False),
    ("Linux", ["Ubuntu", "Parrot OS", "Arch Linux"], False),
    ("Calidad", ["TestSprite", "Pruebas de regresión"], False),
    ("Soporte y gestión", ["ServiceDesk Plus", "Jira Service Mgmt", "PMBOK", "ADRs"], False),
]

LANGS = [
    ("TypeScript", "37.62%", ACC), ("C#", "33.91%", "#c9d1d9"), ("HTML", "24.42%", "#6e7681"),
    ("CSS", "3.22%", "#484f58"), ("PL/pgSQL", "0.81%", "#30363d"), ("JavaScript", "0.02%", "#21262d"),
]

ORGS = [
    ("Farsight", "Proyectos propios con alcance de producto real.", "https://github.com/software-insight"),
    ("DoctorSV", "Plataforma de salud y telemedicina.", "https://github.com/doctor-sv"),
    ("Computer Science Hub", "Comunidad de Ing. en Ciencias de la Computación de la UDB: acompañamiento académico entre pares, organización estudiantil y proyección profesional.", "https://github.com/Computer-Sciencie-Hub"),
    ("Universidad Don Bosco", "Proyectos y trabajos de cátedra de la etapa universitaria.", "https://github.com/udb-sv"),
    ("Colegio El Espíritu Santo", "Proyectos de la etapa de Técnico Vocacional en Desarrollo de Software.", "https://github.com/cees-sv"),
    ("Delirios Creativos", "Experimentos, prototipos y delirios sin utilidad declarada.", "https://github.com/delirios-creativos"),
]

NAV = [("sobre-mí", "sobre-mi"), ("experiencia", "experiencia"), ("proyectos", "proyectos"), ("stack", "stack"), ("orgs", "orgs")]
BADGES = [("GITHUB", GITHUB), ("EMAIL", f"mailto:{EMAIL}"), ("LINKEDIN", LINKEDIN)]

MONO = "'JetBrains Mono', ui-monospace, monospace"
GROT = "'Space Grotesk', sans-serif"
PIX = "'Silkscreen', monospace"


def tag(t):
    return f'<span style="font-size:10.5px;padding:3px 8px;border:1px solid #30363d;color:#8b949e">{t}</span>'


def head(num, title, path):
    return f'''<div style="display:flex;align-items:baseline;gap:14px;padding-bottom:12px;border-bottom:1px solid #21262d">
<span style="font-size:12px;color:{ACC}">{num}</span>
<h2 style="margin:0;font-family:{GROT};font-weight:700;font-size:24px;color:#f0f6fc">{title}</h2>
<span style="flex:1"></span><span style="font-size:11px;color:#8b949e">{path}</span></div>'''


def section(slice_id, num, title, path, body, pad_top=48):
    return f'''<div data-slice="{slice_id}" style="width:{W}px;padding-top:{pad_top}px;display:flex;flex-direction:column;gap:18px">
{head(num, title, path)}{body}</div>'''


def badge(text, extra=""):
    return f'''<span style="display:inline-flex;align-items:center;gap:8px;height:28px;padding:0 12px;box-sizing:border-box;background:#161b22;border:1px solid #30363d;font-size:10.5px;font-weight:700;letter-spacing:0.1em;color:#c9d1d9{extra}"><span style="width:8px;height:8px;background:{ACC}"></span>{text}</span>'''


def build_html():
    css = "\n".join(
        f"@font-face{{font-family:'{fam}';font-weight:{wt};src:url('file://{FONTS}/{pkg}/files/{pkg}-{sub}-{wt}-normal.woff2') format('woff2');{rng}}}"
        for fam, pkg in [("JetBrains Mono", "jetbrains-mono"), ("Space Grotesk", "space-grotesk"), ("Silkscreen", "silkscreen")]
        for wt in ([400, 500, 700] if pkg == "jetbrains-mono" else [500, 700] if pkg == "space-grotesk" else [400])
        for sub, rng in [("latin", ""), ("latin-ext", "")]
    )

    banner = f'''<div data-slice="banner" style="width:{W}px;padding-bottom:48px">
<div style="border:1px solid #30363d;border-radius:10px;background:#0b0f14;overflow:hidden">
<div style="display:flex;align-items:center;gap:8px;padding:10px 16px;border-bottom:1px solid #21262d;background:#0d1117">
<span style="width:10px;height:10px;border-radius:50%;background:#30363d"></span><span style="width:10px;height:10px;border-radius:50%;background:#30363d"></span><span style="width:10px;height:10px;border-radius:50%;background:#30363d"></span>
<span style="margin-left:12px;font-size:11px;color:#8b949e">shaddy@github: ~</span></div>
<div style="padding:44px 40px 40px;display:flex;align-items:center;gap:36px;background-image:radial-gradient(#1c232c 1px,transparent 1px);background-size:18px 18px">
<div style="width:128px;height:128px;flex-shrink:0;border:2px solid {ACC};border-radius:6px;display:flex;align-items:center;justify-content:center;background:#0d1117;box-sizing:border-box">
<span style="font-family:{PIX};font-size:60px;line-height:1;color:{ACC}">JL</span></div>
<div style="display:flex;flex-direction:column;gap:10px;min-width:0">
<div style="display:flex;flex-wrap:wrap;gap:10px;font-size:12px;letter-spacing:0.14em;color:{ACC}"><span>DESARROLLADOR FULL STACK</span><span style="color:#8b949e">·</span><span>CIBERSEGURIDAD</span></div>
<h1 style="margin:0;font-family:{GROT};font-weight:700;font-size:40px;line-height:1.05;letter-spacing:-0.02em;color:#f0f6fc">Josué Adonaí Pérez López</h1>
<div style="margin-top:6px;font-size:13px;line-height:1.6;color:#8b949e">$ cat stack.txt <span style="color:{ACC}">→</span> <span style="color:#e6edf3">React · TypeScript · C#/.NET · PostgreSQL · SQL Server</span><span style="display:inline-block;width:8px;height:15px;margin-left:6px;vertical-align:-2px;background:{ACC}"></span></div>
</div></div>
<div style="display:flex;justify-content:space-between;padding:10px 16px;border-top:1px solid #21262d;font-size:11px;color:#8b949e"><span>San Salvador, El Salvador</span><span>construyendo software desde 2022</span></div>
</div></div>'''

    nav_items = "".join(
        f'<span data-slice="nav-{a}" style="display:inline-flex;align-items:center;height:28px;padding-right:{0 if i == len(NAV) - 1 else 16}px;font-size:12px;color:#8b949e;white-space:nowrap"><span style="color:{ACC}">#</span>&nbsp;{t}</span>'
        for i, (t, a) in enumerate(NAV)
    )
    badge_items = "".join(
        f'<span data-slice="badge-{t.lower()}" style="display:inline-flex;padding-left:{0 if i == 0 else 6}px">{badge(t)}</span>'
        for i, (t, _) in enumerate(BADGES)
    )
    nav = f'<div style="width:{W}px;display:flex;align-items:center"><div style="display:flex">{nav_items}</div><span data-slice="nav-spacer" style="flex:1;height:28px"></span><div style="display:flex">{badge_items}</div></div>'

    hl = "".join(
        f'''<div style="padding:22px 22px 20px;display:flex;flex-direction:column;gap:6px;border-right:1px solid #21262d"><span style="font-family:{GROT};font-weight:700;font-size:32px;line-height:1;color:{ACC}">{n}</span><span style="font-size:11.5px;line-height:1.5;color:#c9d1d9">{t}</span></div>'''
        for n, t in HIGHLIGHTS
    )
    highlights = f'''<div data-slice="highlights" style="width:{W}px;padding-top:48px"><div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border:1px solid #30363d;border-radius:8px;background:#0d1117">{hl}</div></div>'''

    S = '<span style="color:' + ACC + '">$</span>'
    M = lambda t: f'<span style="color:#8b949e">{t}</span>'
    term = (f'''<div style="background:#161b22;border:1px solid #30363d;border-radius:8px;padding:22px 24px;font-size:13px;line-height:1.75;white-space:pre;color:#c9d1d9">{S} whoami
<span style="color:#f0f6fc">Josué "Shaddy" Pérez López</span> {M("— Desarrollador Full Stack · Ciberseguridad")}

{S} cat perfil.md
Construyo y mantengo aplicaciones web y sistemas institucionales
desde 2022: frontend, backend y base de datos.
Mi diferenciador es la ciberseguridad: diseño con control de acceso
y manejo seguro de credenciales desde el inicio, no como un añadido.

{S} cat formacion.log
<span style="color:{ACC}">[✓]</span> 2022–2024  Bachillerato Técnico Vocacional en Desarrollo de Software
{M("[~]")} 2024–2026  Técnico Superior Universitario en Ciberseguridad · ESIT
{M("[~]")} 2025–2029  Ingeniería en Ciencias de la Computación · UDB

{S} ls ./ahora
haiku/  {M("full stack")}    doctorsv/  {M("soporte N1")}    shiftsyncmega/  {M("en desarrollo")}</div>''')
    sobre = section("sobre-mi", "01", "Sobre mí", "~/whoami", term)

    jobs = "".join(
        f'''<div style="display:grid;grid-template-columns:132px 20px minmax(0,1fr);gap:14px;padding:4px 0 22px">
<span style="padding-top:3px;font-size:11px;color:#8b949e">{date}</span>
<div style="display:flex;flex-direction:column;align-items:center;gap:6px"><span style="width:10px;height:10px;margin-top:5px;flex-shrink:0;border:2px solid {ACC if cur else '#484f58'};background:{ACC if cur else '#0d1117'}"></span><span style="flex:1;width:1px;background:#21262d"></span></div>
<div style="display:flex;flex-direction:column;gap:6px">
<div style="display:flex;flex-wrap:wrap;align-items:baseline;gap:8px"><span style="font-family:{GROT};font-weight:700;font-size:16px;color:#f0f6fc">{role}</span><span style="font-size:12px;color:{ACC}">@ {org}</span></div>
<span style="font-family:{GROT};font-size:13.5px;line-height:1.55;color:#c9d1d9">{d}</span>
<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:2px">{"".join(tag(t) for t in tags)}</div>
</div></div>'''
        for date, role, org, d, tags, cur in JOBS
    )
    exp = section("experiencia", "02", "Experiencia", "~/git log --oneline", f'<div style="display:flex;flex-direction:column">{jobs}</div>')

    projs = "".join(
        f'''<div style="background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:20px 22px;display:flex;flex-direction:column;gap:12px">
<div style="display:flex;justify-content:space-between;align-items:baseline;gap:10px"><span style="font-size:14px;font-weight:700;color:{ACC}">{n}</span><span style="font-size:10.5px;color:#8b949e">{s}</span></div>
<span style="font-family:{GROT};font-size:13.5px;line-height:1.55;color:#c9d1d9">{d}</span>
<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:auto">{"".join(tag(t) for t in tags)}</div></div>'''
        for n, s, d, tags in PROJECTS
    )
    proy = section("proyectos", "03", "Proyectos destacados", "~/pinned", f'<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px">{projs}</div>')

    rows = "".join(
        f'''<div style="display:grid;grid-template-columns:150px minmax(0,1fr);gap:16px;align-items:start">
<span style="padding-top:6px;font-size:11px;letter-spacing:0.08em;text-transform:uppercase;color:#8b949e">{label}</span>
<div style="display:flex;flex-wrap:wrap;gap:6px">{"".join(f'<span style="display:inline-flex;align-items:center;gap:7px;height:26px;padding:0 10px;box-sizing:border-box;background:#161b22;border:1px solid {ACC if main else "#30363d"};font-size:10.5px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:#c9d1d9"><span style="width:6px;height:6px;background:{ACC}"></span>{i}</span>' for i in items)}</div></div>'''
        for label, items, main in GROUPS
    )
    stack = section("stack", "04", "Stack", "~/stack", f'<div style="display:flex;flex-direction:column;gap:14px">{rows}</div>')

    bar = "".join(f'<span style="width:{p};background:{c}"></span>' for _, p, c in LANGS)
    legend = "".join(
        f'<div style="display:flex;align-items:center;gap:8px;font-size:11.5px"><span style="width:8px;height:8px;border-radius:50%;background:{c};box-shadow:0 0 0 1px #484f58"></span><span style="color:#c9d1d9">{n}</span><span style="color:#8b949e">{p}</span></div>'
        for n, p, c in LANGS
    )
    stats_body = f'''<div style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.5fr);gap:14px">
<div style="background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:20px 22px;display:flex;flex-direction:column;justify-content:center;gap:8px">
<span style="font-family:{GROT};font-weight:700;font-size:40px;line-height:1;color:#f0f6fc">471</span><span style="font-size:12px;color:#c9d1d9">contribuciones totales</span><span style="font-size:10.5px;color:#8b949e">12 may 2024 – hoy</span></div>
<div style="background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:20px 22px;display:flex;flex-direction:column;gap:16px">
<span style="font-size:13px;font-weight:700;color:{ACC}">Lenguajes más usados</span>
<div style="display:flex;height:8px;border-radius:4px;overflow:hidden;background:#21262d">{bar}</div>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px 16px">{legend}</div></div></div>
<div style="background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:18px 22px 14px;display:flex;flex-direction:column;gap:10px">
<div style="display:flex;justify-content:space-between;font-size:11.5px"><span style="font-weight:700;color:{ACC}">Actividad · últimos 30 días</span><span style="color:#8b949e">vista previa · se genera en vivo</span></div>
<svg width="100%" height="110" viewBox="0 0 760 110" preserveAspectRatio="none" aria-hidden="true" style="display:block">
<line x1="0" y1="28" x2="760" y2="28" stroke="#161b22" stroke-width="1"/><line x1="0" y1="56" x2="760" y2="56" stroke="#161b22" stroke-width="1"/><line x1="0" y1="84" x2="760" y2="84" stroke="#161b22" stroke-width="1"/>
<polyline fill="none" stroke="{ACC}" stroke-width="2" stroke-linejoin="round" points="0,102 26,96 52,102 78,86 104,92 130,102 156,78 182,90 208,102 234,96 260,70 286,84 312,102 338,92 364,64 390,80 416,96 442,102 468,88 494,56 520,74 546,92 572,102 598,88 624,68 650,82 676,52 702,66 728,58 760,44"/></svg></div>'''
    stats = section("stats", "05", "Actividad en GitHub", "~/stats --live", stats_body)

    orgs_head = section("orgs", "06", "Organizaciones", "~/orgs",
                        '<p style="margin:0;font-size:13px;line-height:1.6;color:#8b949e">El trabajo vive repartido por organización según su contexto, no suelto en mi cuenta personal.</p>')
    orgs_head = orgs_head.replace('gap:18px">', 'gap:18px;padding-bottom:18px">', 1)
    cells = "".join(
        f'''<div data-slice="org-{i}" style="padding:18px 20px;box-sizing:border-box;border-right:1px solid #30363d;border-bottom:1px solid #30363d;{'border-left:1px solid #30363d;' if i % 2 == 0 else ''}{'border-top:1px solid #30363d;' if i < 2 else ''}display:flex;flex-direction:column;gap:8px">
<span style="font-size:13px;font-weight:700;color:{ACC}">{n} <span style="color:#8b949e;font-weight:400">↗</span></span>
<span style="font-family:{GROT};font-size:13.5px;line-height:1.5;color:#c9d1d9">{d}</span></div>'''
        for i, (n, d, _) in enumerate(ORGS)
    )
    orgs = f'<div style="width:{W}px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr))">{cells}</div>'

    foot_a = f'''<div data-slice="frase" style="width:{W}px;padding-top:48px"><div style="display:flex;flex-direction:column;align-items:center;gap:22px;padding:36px 0 22px;border-top:1px solid #21262d">
<span style="font-family:{PIX};font-size:12px;letter-spacing:0.12em;color:#8b949e">FRASE PERSONAL</span>
<p style="margin:0;font-size:22px;color:#f0f6fc"><span style="color:{ACC}">//</span> Si te funciona no lo arruines.</p></div></div>'''
    links = [("email", EMAIL), ("sep1", "/"), ("github", "@JAPEREZ-L001"), ("sep2", "/"), ("linkedin", "linkedin")]
    foot_links = '<div style="display:flex;justify-content:center">' + "".join(
        f'<span data-slice="link-{k}" style="display:inline-flex;padding-right:{0 if k == "linkedin" else 20}px;font-size:12px;line-height:18px;color:{"#30363d" if k.startswith("sep") else "#c9d1d9"};white-space:nowrap">{t}</span>'
        for k, t in links
    ) + "</div>"
    foot_b = f'''<div data-slice="firma" style="width:{W}px;padding:22px 0 8px;display:flex;justify-content:center"><span style="font-family:{PIX};font-size:14px;color:{ACC}">JL_</span></div>'''

    body = "\n".join([banner, nav, highlights, sobre, exp, proy, stack, stats, orgs_head, orgs, foot_a, foot_links, foot_b])
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{css}
body{{margin:0;background:#0d1117;color:#e6edf3;font-family:{MONO};-webkit-font-smoothing:antialiased}}
#root{{width:{W}px;padding:0 0 0 0}}</style></head><body><div id="root">{body}</div></body></html>'''


def render():
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*.png"):
        f.unlink()
    html = ROOT / "scripts" / ".render.html"
    html.write_text(build_html(), encoding="utf-8")
    sizes = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME) if CHROME else p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": 1000}, device_scale_factor=2)
        page.goto(html.as_uri())
        page.evaluate("document.fonts.ready")
        loaded = page.evaluate("[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight)")
        print("fuentes cargadas:", sorted(set(loaded)))
        # Alturas enteras y separación entre bloques: así ninguna captura arrastra
        # una fila de píxeles del bloque vecino (bordes fantasma en las uniones).
        page.evaluate(f"""() => {{
            for (const el of document.querySelectorAll('[data-slice]')) {{
                const r = el.getBoundingClientRect();
                el.style.boxSizing = 'border-box';
                el.style.height = Math.ceil(r.height) + 'px';
                if (Math.round(r.width) === {W}) el.style.marginBottom = '40px';
            }}
            document.querySelectorAll('[data-slice^="org-"]').forEach(el => el.parentElement.style.marginBottom = '40px');
            document.querySelectorAll('[data-slice^="link-"]').forEach(el => el.parentElement.style.marginBottom = '40px');
            document.querySelectorAll('[data-slice^="nav-"]').forEach(el => el.parentElement.parentElement.style.marginBottom = '40px');
        }}""")
        for el in page.query_selector_all("[data-slice]"):
            name = el.get_attribute("data-slice")
            box = el.bounding_box()
            el.screenshot(path=str(OUT / f"{name}.png"))
            sizes[name] = {"w": box["width"], "h": box["height"]}
        page.screenshot(path=str(ROOT / "scripts" / ".preview.png"), full_page=True)
        browser.close()
    html.unlink()
    return sizes


def pct(w):
    return f"{w / W * 100:.3f}%"


def img(name, alt, sizes, width=None):
    # align="top" evita el hueco de ~6px que deja la línea de texto bajo cada imagen
    # en línea, sin convertirla en flotante (GitHub añade 20px a las flotantes).
    w = width or pct(sizes[name]["w"])
    return f'<img src="assets/readme/{name}.png" alt="{alt}" width="{w}" align="top">'


def build_readme(sizes):
    nav = "".join(f'<a href="#{a}">{img("nav-" + a, t, sizes)}</a>' for t, a in NAV)
    # El espaciador empuja los badges al borde derecho; se recorta un poco para
    # que el redondeo nunca haga saltar la fila.
    spacer_w = f'{max(sizes["nav-spacer"]["w"] / W * 100 - 0.15, 0):.3f}%'
    nav += img("nav-spacer", "", sizes, spacer_w)
    badges = "".join(f'<a href="{url}">{img("badge-" + t.lower(), t.title(), sizes)}</a>' for t, url in BADGES)
    org_rows = []
    for i in range(0, len(ORGS), 2):
        pair = "".join(f'<a href="{ORGS[j][2]}">{img(f"org-{j}", f"{ORGS[j][0]}: {ORGS[j][1]}", sizes, "50%")}</a>' for j in (i, i + 1))
        org_rows.append(pair)
    links = {
        "email": f"mailto:{EMAIL}", "github": GITHUB, "linkedin": LINKEDIN,
    }
    foot = "".join(
        (f'<a href="{links[k]}">{img("link-" + k, alt, sizes)}</a>' if k in links else img("link-" + k, alt, sizes))
        for k, alt in [("email", EMAIL), ("sep1", "/"), ("github", "@JAPEREZ-L001"), ("sep2", "/"), ("linkedin", "LinkedIn")]
    )
    full = lambda n, alt: img(n, alt, sizes, "100%")
    parts = [
        "<!-- Generado por scripts/render_profile.py a partir del diseño del perfil. No editar a mano: edita el script y vuelve a ejecutarlo. -->",
        "",
        "<div>",
        full("banner", "Josué Adonaí Pérez López — Desarrollador Full Stack · Ciberseguridad. Stack: React, TypeScript, C#/.NET, PostgreSQL, SQL Server. San Salvador, El Salvador."),
        f"{nav}{badges}",
        full("highlights", "Desde 2022 construyendo software en gobierno, educación, salud y startup · 6 roles de desarrollo y soporte técnico · 7 hallazgos de seguridad en una auditoría RLS de 8 tablas"),
        '<a id="sobre-mi"></a>' + full("sobre-mi", "Sobre mí: Desarrollador Full Stack con experiencia desde 2022 y la ciberseguridad como diferenciador. Formación: Bachillerato Técnico Vocacional en Desarrollo de Software (2022–2024), Técnico Superior Universitario en Ciberseguridad en ESIT (2024–2026), Ingeniería en Ciencias de la Computación en la UDB (2025–2029)."),
        '<a id="experiencia"></a>' + full("experiencia", "Experiencia: " + "; ".join(f"{r} en {o} ({d})" for d, r, o, *_ in JOBS)),
        '<a id="proyectos"></a>' + full("proyectos", "Proyectos destacados: " + "; ".join(f"{n} — {d}" for n, _, d, _ in PROJECTS)),
        '<a id="stack"></a>' + full("stack", "Stack: " + "; ".join(f"{l}: {', '.join(i)}" for l, i, _ in GROUPS)),
        full("stats", "Actividad en GitHub: 471 contribuciones totales. Lenguajes más usados: " + ", ".join(f"{n} {p}" for n, p, _ in LANGS)),
        '<a id="orgs"></a>' + full("orgs", "Organizaciones: el trabajo vive repartido por organización según su contexto, no suelto en mi cuenta personal."),
        "<br>".join(org_rows),
        full("frase", "Frase personal: Si te funciona no lo arruines."),
        "</div>",
        "",
        f'<div align="center">{foot}</div>',
        "",
        f'<div align="center">{img("firma", "JL", sizes, "100%")}</div>',
        "",
    ]
    # Separa las piezas de bloque con <br> para que se apilen sin márgenes de párrafo.
    body = parts[:3] + ["<br>\n".join(parts[3:14])] + parts[14:]
    (ROOT / "README.md").write_text("\n".join(body), encoding="utf-8")


if __name__ == "__main__":
    s = render()
    (ROOT / "scripts" / ".sizes.json").write_text(json.dumps(s, indent=1))
    build_readme(s)
    print("listo:", len(s), "imágenes")

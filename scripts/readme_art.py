"""Generates the animated README art. Run from the repo root: python scripts/readme_art.py"""
# ruff: noqa: E501  (SVG markup lines are kept whole to stay readable)

import sys
from pathlib import Path

BG = "#0B0A12"
EDGE = "#251E45"
V2 = "#5B4BC4"
V3 = "#8B7CF6"
ACC = "#E9E5FF"
WHITE = "#F4F2FF"
MUTED = "#A9A3C9"
DIM = "#6E6890"
FAINT = "#4A4466"

MONO = "'JetBrains Mono','SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

SECTIONS = [
    "idea",
    "architecture",
    "quick start",
    "workflow",
    "where to code",
    "ai layer",
    "checks",
    "repo map",
    "agent rules",
    "commands",
    "teamwork",
    "faq",
]

MONO_CHAR = 7.2

TAGLINE = "Repository template for AI projects"
TYPE_START, TYPE_STEP, HOLD_UNTIL, ERASE_STEP, CYCLE = 0.4, 0.09, 7.5, 0.035, 10.0

NAV = [
    (1, "Идея"),
    (2, "Как устроено"),
    (3, "Быстрый старт"),
    (4, "Как вести проект"),
    (5, "Куда писать код"),
    (6, "ИИ-часть"),
    (7, "Проверки"),
    (12, "Вопросы"),
]

SERVICES = [
    ("frontend", "Vite + React", "screens only"),
    ("backend", "FastAPI", "data + rules"),
    ("ml", "FastAPI", "prompts · RAG · agents"),
    ("model", "Anthropic API", "key lives in ml"),
]

STEPS = [
    ("input", "docs/input/"),
    ("brief", "docs/BRIEF.md"),
    ("approve", "you sign off"),
    ("tasks", "one at a time"),
    ("review", "V1 · V2, 1–5"),
]

TASK_LOOP = ["steps", "code", "make check", "PROGRESS.md", "commit T&lt;n&gt;"]


def svg(width: int, height: int, title: str, style: str, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{title}">\n'
        f"<title>{title}</title>\n<style>\n{style}\n{REDUCED}\n</style>\n{body}\n</svg>\n"
    )


def frame(width: int, height: int) -> str:
    return (
        f'<rect width="{width}" height="{height}" rx="14" fill="{BG}"/>\n'
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="14" '
        f'fill="none" stroke="{EDGE}"/>'
    )


def header() -> str:
    style = f"""
.mono{{font-family:{MONO}}}
.sans{{font-family:{SANS}}}
.dot{{fill:{V3};opacity:.5;animation:wave 3.2s ease-in-out infinite}}
.dot.hot{{fill:{ACC};opacity:1}}
@keyframes wave{{0%,100%{{opacity:.12}}45%{{opacity:1}}}}
.typer{{transform:translateX(56px);animation:type 6s infinite}}
@keyframes type{{0%{{transform:translateX(0)}}10%{{transform:translateX(0);animation-timing-function:steps(7,end)}}35%,100%{{transform:translateX(56px)}}}}
.cursor{{fill:{ACC};animation:blink 1s steps(1) infinite}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.out{{animation:out 6s infinite}}
@keyframes out{{0%,40%{{opacity:0}}45%,92%{{opacity:1}}100%{{opacity:0}}}}"""
    dots = []
    for row in range(8):
        for col in range(9):
            hot = row == col - 1
            delay = (row + col) * 0.11
            dots.append(
                f'<circle class="dot{" hot" if hot else ""}" cx="{520 + col * 17}" '
                f'cy="{40 + row * 20}" r="{3.6 if hot else 2.8}" '
                f'style="animation-delay:{delay:.2f}s"/>'
            )
    body = f"""{frame(680, 250)}
<text class="mono" x="36" y="48" fill="{V3}" font-size="12">~/ai-template</text>
<text class="mono" x="34" y="104" fill="{WHITE}" font-size="44" font-weight="500" letter-spacing="-1">ai-template</text>
<text class="sans" x="36" y="136" fill="{MUTED}" font-size="15">LLM projects, from brief to verified commit.</text>
<g class="mono" font-size="13">
<text x="36" y="200" fill="{V3}">$</text>
<text x="52" y="200" fill="{WHITE}">make up</text>
<g class="typer"><rect x="52" y="186" width="80" height="20" fill="{BG}"/><rect class="cursor" x="53" y="189" width="8" height="14"/></g>
<text class="out" x="36" y="222" fill="{DIM}">ok  frontend → backend → ml → model</text>
</g>
{chr(10).join(dots)}
<text class="mono" x="588" y="228" text-anchor="middle" fill="{FAINT}" font-size="11">attention</text>"""
    return svg(680, 250, "ai-template — LLM projects, from brief to verified commit", style, body)


TOKEN_WIDTHS = [22, 40, 14, 30, 52, 18, 26, 44, 12, 34, 20, 48, 16, 28, 38, 14, 24, 46, 20, 30]


def divider(number: int, label: str) -> str:
    style = f"""
.tok{{fill:{V3};opacity:.6;animation:tok 2.8s ease-in-out infinite}}
.tok.alt{{fill:{V2}}}
@keyframes tok{{0%,100%{{opacity:.18}}30%{{opacity:1}}}}
.label{{font-family:{MONO}}}"""
    tokens, x, i = [], 20, 0
    while True:
        width = TOKEN_WIDTHS[(i + number * 5) % len(TOKEN_WIDTHS)]
        if x + width > 520:
            break
        alt = " alt" if i % 7 == 3 else ""
        tokens.append(
            f'<rect class="tok{alt}" x="{x}" y="13" width="{width}" height="14" rx="3" '
            f'style="animation-delay:{i * 0.09:.2f}s"/>'
        )
        x += width + 5
        i += 1
    body = (
        "\n".join(tokens)
        + f'\n<text class="label" x="540" y="25" fill="{V3}" font-size="12">{number:02d} / {label}</text>'
    )
    return svg(680, 40, f"{number:02d} / {label}", style, body)


def footer() -> str:
    style = f"""
.mono{{font-family:{MONO}}}
.sans{{font-family:{SANS}}}
.dot{{fill:{V3};animation:wave 3.2s ease-in-out infinite}}
@keyframes wave{{0%,100%{{opacity:.12}}45%{{opacity:1}}}}
.eos{{animation:breathe 2.4s ease-in-out infinite}}
@keyframes breathe{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}"""
    dots = []
    for col in range(34):
        fade = 1 - col / 34
        dots.append(
            f'<g opacity="{fade:.2f}"><circle class="dot" cx="{36 + col * 18.6:.1f}" cy="36" '
            f'r="2.4" style="animation-delay:{col * 0.07:.2f}s"/></g>'
        )
    body = f"""{frame(680, 150)}
{chr(10).join(dots)}
<rect class="eos" x="36" y="74" width="72" height="30" rx="6" fill="none" stroke="{ACC}"/>
<text class="mono" x="72" y="94" text-anchor="middle" fill="{ACC}" font-size="14">&lt;eos&gt;</text>
<text class="sans" x="124" y="88" fill="{WHITE}" font-size="14">brief → tasks → verified commits</text>
<text class="mono" x="124" y="108" fill="{DIM}" font-size="12">make check · make smoke · make eval</text>
<text class="mono" x="644" y="108" text-anchor="end" fill="{FAINT}" font-size="11">built for hackathons</text>"""
    return svg(680, 150, "end of sequence: brief → tasks → verified commits", style, body)


def tagline() -> str:
    """Typewriter loop: types the line, holds it, erases it, starts again. Transparent background."""
    n, cell, size = len(TAGLINE), 18, 30
    x0 = (680 - n * cell) / 2
    typed = [TYPE_START + (i + 1) * TYPE_STEP for i in range(n)]
    erased = [HOLD_UNTIL + (n - 1 - i) * ERASE_STEP for i in range(n)]

    def pct(seconds: float) -> str:
        return f"{seconds / CYCLE * 100:.2f}%"

    rules = [
        f".t{{font-family:{MONO};font-weight:700}}",
        f".c{{animation:{CYCLE}s steps(1,end) infinite}}",
        f".caret{{fill:{V3};animation:move {CYCLE}s steps(1,end) infinite}}",
        ".blink{animation:blink 1s steps(1) infinite}",
        "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}",
    ]
    glyphs = []
    for i, ch in enumerate(TAGLINE):
        if ch == " ":
            continue
        rules.append(
            f"@keyframes c{i}{{0%{{opacity:0}}{pct(typed[i])}{{opacity:1}}"
            f"{pct(erased[i])},100%{{opacity:0}}}}"
        )
        glyphs.append(
            f'<text class="t c" x="{x0 + i * cell:.0f}" y="40" font-size="{size}" '
            f'style="animation-name:c{i}">{ch}</text>'
        )
    steps = [f"0%{{transform:translateX({-n * cell}px)}}"]
    steps += [
        f"{pct(t)}{{transform:translateX({(i + 1 - n) * cell}px)}}" for i, t in enumerate(typed)
    ]
    steps += [
        f"{pct(erased[i])}{{transform:translateX({(i - n) * cell}px)}}" for i in reversed(range(n))
    ]
    rules.append("@keyframes move{" + "".join(steps) + "}")

    body = f"""<defs><linearGradient id="ink" gradientUnits="userSpaceOnUse" x1="{x0:.0f}" x2="{x0 + n * cell:.0f}" y1="0" y2="0">
<stop offset="0" stop-color="{V2}"/><stop offset="1" stop-color="{V3}"/>
</linearGradient></defs>
<g fill="url(#ink)">
{chr(10).join(glyphs)}
</g>
<g class="blink"><rect class="caret" x="{x0 + n * cell + 2:.0f}" y="14" width="3" height="32"/></g>"""
    return svg(680, 56, TAGLINE, "\n".join(rules), body)


def nav_button(order: int, number: int, label: str) -> str:
    size, char, pad, height = 13, 7.8, 16, 34
    width = round(pad * 2 + (2 + len(label)) * char + 8)
    style = f"""
.mono{{font-family:{MONO}}}
.edge{{fill:{BG};stroke:{V2};animation:glow 4.8s ease-in-out infinite}}
@keyframes glow{{0%,100%{{stroke:{V2}}}12%{{stroke:{ACC}}}28%{{stroke:{V2}}}}}"""
    body = (
        f'<rect class="edge" x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="{height / 2}" '
        f'style="animation-delay:{order * 0.35:.2f}s"/>\n'
        f'<text class="mono" x="{width / 2}" y="{height / 2 + 4.5}" text-anchor="middle" font-size="{size}">'
        f'<tspan fill="{V3}">{number:02d}</tspan><tspan fill="{WHITE}" dx="8">{label}</tspan></text>'
    )
    return svg(width, height, f"{number:02d} {label}", style, body)


def architecture() -> str:
    style = f"""
.mono{{font-family:{MONO}}}
.sans{{font-family:{SANS}}}
.req{{fill:{V3};animation:req 3.2s linear infinite}}
.res{{fill:{ACC};opacity:0;animation:res 3.2s linear infinite}}
@keyframes req{{0%{{transform:translateX(0);opacity:1}}25%{{transform:translateX(20px);opacity:1}}26%,100%{{opacity:0}}}}
@keyframes res{{0%,50%{{opacity:0;transform:translateX(20px)}}51%{{opacity:1;transform:translateX(20px)}}75%{{opacity:1;transform:translateX(0)}}76%,100%{{opacity:0}}}}
.db{{animation:breathe 3.2s ease-in-out infinite}}
@keyframes breathe{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}"""
    box_w, gap, top, box_h = 128, 32, 44, 78
    parts = [frame(680, 196)]
    for i, (name, tech, role) in enumerate(SERVICES):
        x = 36 + i * (box_w + gap)
        cx = x + box_w / 2
        stroke = V2 if name != "model" else FAINT
        parts.append(
            f'<rect x="{x}" y="{top}" width="{box_w}" height="{box_h}" rx="10" fill="none" stroke="{stroke}"/>\n'
            f'<text class="mono" x="{cx:.0f}" y="{top + 28}" text-anchor="middle" fill="{WHITE}" font-size="14">{name}</text>\n'
            f'<text class="sans" x="{cx:.0f}" y="{top + 48}" text-anchor="middle" fill="{MUTED}" font-size="11">{tech}</text>\n'
            f'<text class="sans" x="{cx:.0f}" y="{top + 64}" text-anchor="middle" fill="{DIM}" font-size="11">{role}</text>'
        )
        if i < len(SERVICES) - 1:
            gx = x + box_w + 6
            y = top + box_h / 2
            parts.append(
                f'<line x1="{x + box_w + 2}" y1="{y}" x2="{x + box_w + gap - 2}" y2="{y}" stroke="{EDGE}"/>\n'
                f'<circle class="req" cx="{gx}" cy="{y - 5}" r="2.6" style="animation-delay:{i * 0.27:.2f}s"/>\n'
                f'<circle class="res" cx="{gx}" cy="{y + 5}" r="2.6" style="animation-delay:{(2 - i) * 0.27:.2f}s"/>'
            )
    backend_cx = 36 + box_w + gap + box_w / 2
    parts.append(
        f'<line x1="{backend_cx}" y1="{top + box_h}" x2="{backend_cx}" y2="{top + box_h + 26}" stroke="{EDGE}" stroke-dasharray="3 3"/>\n'
        f'<rect class="db" x="{backend_cx - 48}" y="{top + box_h + 26}" width="96" height="26" rx="13" fill="none" stroke="{V2}"/>\n'
        f'<text class="mono" x="{backend_cx}" y="{top + box_h + 43}" text-anchor="middle" fill="{MUTED}" font-size="11">Postgres</text>\n'
        f'<text class="mono" x="36" y="28" fill="{V3}" font-size="12">browser → frontend → backend → ml → model</text>\n'
        f'<text class="mono" x="644" y="{top + box_h + 43}" text-anchor="end" fill="{FAINT}" font-size="11">HTTP only · no shared code</text>'
    )
    return svg(
        680, 196, "architecture: frontend → backend → ml → model API", style, "\n".join(parts)
    )


def workflow() -> str:
    style = f"""
.mono{{font-family:{MONO}}}
.sans{{font-family:{SANS}}}
.node{{fill:{BG};stroke:{V2};animation:lit 5s ease-in-out infinite}}
@keyframes lit{{0%,100%{{stroke:{V2}}}12%{{stroke:{ACC}}}24%{{stroke:{V2}}}}}
.step{{animation:step 5s steps(1) infinite;opacity:.35}}
@keyframes step{{0%{{opacity:1}}20%,100%{{opacity:.35}}}}"""
    spacing, y = 130, 70
    parts = [frame(680, 220)]
    for i, (name, hint) in enumerate(STEPS):
        cx = 80 + i * spacing
        if i < len(STEPS) - 1:
            parts.append(
                f'<line x1="{cx + 18}" y1="{y}" x2="{cx + spacing - 18}" y2="{y}" stroke="{EDGE}"/>'
            )
        parts.append(
            f'<circle class="node" cx="{cx}" cy="{y}" r="17" style="animation-delay:{i * 0.6:.1f}s"/>\n'
            f'<text class="mono" x="{cx}" y="{y + 4}" text-anchor="middle" fill="{ACC}" font-size="12">{i + 1}</text>\n'
            f'<text class="mono" x="{cx}" y="{y + 40}" text-anchor="middle" fill="{WHITE}" font-size="13">{name}</text>\n'
            f'<text class="sans" x="{cx}" y="{y + 58}" text-anchor="middle" fill="{MUTED}" font-size="11">{hint}</text>'
        )
    tasks_cx = 80 + 3 * spacing
    parts.append(
        f'<line x1="{tasks_cx}" y1="{y + 66}" x2="{tasks_cx}" y2="{y + 82}" stroke="{EDGE}" stroke-dasharray="3 3"/>\n'
        f'<rect x="36" y="{y + 82}" width="608" height="40" rx="10" fill="none" stroke="{EDGE}"/>\n'
        f'<text class="mono" x="52" y="{y + 107}" fill="{V3}" font-size="12">each task</text>'
    )
    x = 140
    for i, label in enumerate(TASK_LOOP):
        text_len = len(label.replace("&lt;", "<").replace("&gt;", ">"))
        parts.append(
            f'<text class="mono step" x="{x}" y="{y + 107}" fill="{WHITE}" font-size="12" '
            f'style="animation-delay:{i}s">{label}</text>'
        )
        x += text_len * MONO_CHAR
        if i < len(TASK_LOOP) - 1:
            parts.append(
                f'<text class="mono" x="{x + 11}" y="{y + 107}" fill="{DIM}" font-size="12">→</text>'
            )
            x += 34
    parts.append(
        f'<text class="mono" x="36" y="32" fill="{V3}" font-size="12">brief → tasks → verified commits</text>'
    )
    return svg(
        680, 220, "workflow: input → brief → approve → tasks → review", style, "\n".join(parts)
    )


def main(out_dir: str) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    pictures = {
        "header": header,
        "tagline": tagline,
        "architecture": architecture,
        "workflow": workflow,
        "footer": footer,
    }
    for name, draw in pictures.items():
        (out / f"{name}.svg").write_text(draw(), encoding="utf-8")
    for order, (number, label) in enumerate(NAV):
        (out / f"nav-{number:02d}.svg").write_text(
            nav_button(order, number, label), encoding="utf-8"
        )
    for number, label in enumerate(SECTIONS, start=1):
        (out / f"divider-{number:02d}.svg").write_text(divider(number, label), encoding="utf-8")
    print(f"wrote {len(SECTIONS) + len(pictures) + len(NAV)} files to {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "docs/assets/readme")

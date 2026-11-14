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
    "architecture",
    "quick start",
    "workflow",
    "repo map",
    "ai layer",
    "checks",
    "skills",
    "agent rules",
    "commands",
    "teamwork",
    "out of scope",
    "other agents",
]


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


def main(out_dir: str) -> None:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "header.svg").write_text(header(), encoding="utf-8")
    (out / "footer.svg").write_text(footer(), encoding="utf-8")
    for number, label in enumerate(SECTIONS, start=1):
        (out / f"divider-{number:02d}.svg").write_text(divider(number, label), encoding="utf-8")
    print(f"wrote {len(SECTIONS) + 2} files to {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "docs/assets/readme")

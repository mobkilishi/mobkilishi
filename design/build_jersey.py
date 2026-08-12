#!/usr/bin/env python3
"""
City Boy jersey — technical flat generator.

Rebuilds the "City boy jersey 3" sheet as vector art with two revisions:
  1. The halftone dot gradients on the side panels are gone; those panels
     are now flat green.
  2. The collar matches the shirt: white shirt -> white collar,
     black shirt -> black collar.

Emits one SVG/PNG/PDF per colourway, each holding a front view, a back view
and the colour chip block, laid out like the original sheet.
"""

import os
import cairosvg

# ---------------------------------------------------------------- palette ---
RED = "#E8232A"
NAVY = "#2A1B3D"
GREEN = "#3BA94C"
BLUE = "#62C6E8"
WHITE = "#FFFFFF"
BLACK = "#141414"
GREY = "#9B9B9B"
LINE = "#141414"
SEAM = "#8A8A8A"

SW = 3.0      # garment outline
SWT = 2.0     # panel edges

# Each jersey is authored in a 1000 x 1000 box; the left half is drawn
# explicitly and mirrored for the right.
CX = 500

# --------------------------------------------------------------- anatomy ---
NECK = (405, 122)      # neckline / collar seam, left end
SHO = (86, 252)        # outer top corner of the sleeve
CUFF_O = (50, 462)     # outer cuff corner
CUFF_I = (208, 496)    # inner cuff corner
ARMPIT = (232, 452)    # underarm
HEM_X = 200            # side seam at the hem
HEM_Y = 920
VNECK = 268            # depth of the front neckline


def m(x):
    return 2 * CX - x


# Edge fragments shared by the silhouette and the sleeve colour block, so the
# two can never drift apart.
SHOULDER = f"C 370 150, 200 200, {SHO[0]} {SHO[1]}"
SLEEVE_EDGE = f"C 62 320, 50 400, {CUFF_O[0]} {CUFF_O[1]}"
CUFF = f"L {CUFF_I[0]} {CUFF_I[1]}"
UNDERARM = f"C 220 480, 228 466, {ARMPIT[0]} {ARMPIT[1]}"
SIDE_SEAM = f"C 214 590, 204 760, {HEM_X} {HEM_Y}"
RAGLAN = f"C 296 340, 372 210, {NECK[0]} {NECK[1]}"   # underarm -> neck


def body_outline(view):
    """Garment silhouette. `view` is 'front' (V neck) or 'back' (shallow neck)."""
    d = [f"M {NECK[0]} {NECK[1]}", SHOULDER, SLEEVE_EDGE, CUFF, UNDERARM,
         SIDE_SEAM, f"L {m(HEM_X)} {HEM_Y}",
         f"C {m(204)} 760, {m(214)} 590, {m(ARMPIT[0])} {ARMPIT[1]}",
         f"C {m(228)} 466, {m(220)} 480, {m(CUFF_I[0])} {CUFF_I[1]}",
         f"L {m(CUFF_O[0])} {CUFF_O[1]}",
         f"C {m(50)} 400, {m(62)} 320, {m(SHO[0])} {SHO[1]}",
         f"C {m(200)} 200, {m(370)} 150, {m(NECK[0])} {NECK[1]}"]
    if view == "front":
        d += [f"C 562 172, 536 228, {CX} {VNECK}",
              f"C 464 228, 438 172, {NECK[0]} {NECK[1]}"]
    else:
        d += [f"C 552 164, 448 164, {NECK[0]} {NECK[1]}"]
    d.append("Z")
    return " ".join(d)


def sleeve_block():
    """Sleeve + shoulder yoke, bounded inboard by the raglan seam (left half)."""
    return (f"M {NECK[0]} {NECK[1]} {SHOULDER} {SLEEVE_EDGE} {CUFF} "
            f"{UNDERARM} {RAGLAN} Z")


# ---------------------------------------------------------------- panels ---
# Green stripe across the sleeve. Clipped to the sleeve so it stops dead at
# the raglan seam instead of running on over the chest.
GREEN_BAND = ("M 52 342 "
              "C 140 336, 240 328, 330 310 "
              "L 296 380 "
              "C 214 390, 128 398, 48 404 Z")

# Light blue sweep beside the armhole, tapering to a point mid-body.
BLUE_CRESCENT = ("M 252 442 "
                 "C 268 520, 300 620, 352 772 "
                 "C 350 700, 330 560, 308 440 Z")

# The side panel that used to carry the halftone gradient — now flat green.
# Its upper edge tracks the blue crescent, then sweeps in toward the hem.
SIDE_PANEL = ("M 140 434 "
              "L 252 442 "
              "C 268 520, 300 620, 352 772 "
              "C 366 812, 380 866, 390 920 "
              "L 140 920 Z")

# Black wedge at the bottom outer corner of the side panel.
BLACK_WEDGE = ("M 206 764 "
               "C 224 826, 258 884, 296 920 "
               "L 140 920 L 140 764 Z")


def panels(sleeve_clip):
    """One half of the side / shoulder colour blocking."""
    return "\n".join([
        f'<path d="{SIDE_PANEL}" fill="{GREEN}" stroke="{LINE}"'
        f' stroke-width="{SWT}" stroke-linejoin="round"/>',
        f'<path d="{BLACK_WEDGE}" fill="{BLACK}"/>',
        f'<path d="{BLUE_CRESCENT}" fill="{BLUE}" stroke="{LINE}"'
        f' stroke-width="{SWT}" stroke-linejoin="round"/>',
        f'<g clip-path="url(#{sleeve_clip})">'
        f'<path d="{GREEN_BAND}" fill="{GREEN}"/></g>',
    ])


def collar(colorway, view):
    """Polo collar. The fill follows the shirt so the two read as one garment."""
    fill = colorway["collar"]
    out = []
    if view == "front":
        # squared collar points at the shoulders, band running down to the V
        outer = (f"M 376 100 L 392 84 C 440 68, 560 68, 608 84 L 624 100 "
                 f"C 604 168, 554 232, {CX} 306 "
                 f"C 446 232, 396 168, 376 100 Z")
        inner = (f"M {NECK[0]} {NECK[1]} C 448 146, 552 146, {m(NECK[0])} {NECK[1]} "
                 f"C 562 172, 536 228, {CX} {VNECK} "
                 f"C 464 228, 438 172, {NECK[0]} {NECK[1]} Z")
        lens = ("M 416 126 C 452 152, 548 152, 584 126 "
                "C 562 192, 438 192, 416 126 Z")
        stripe = (f"M 396 114 C 416 170, 452 216, {CX} 276 "
                  f"C 548 216, 584 170, 604 114")
        out.append(f'<path d="{lens}" fill="{GREY}"/>')
        out.append(f'<path d="{outer} {inner}" fill="{fill}" fill-rule="evenodd"'
                   f' stroke="{LINE}" stroke-width="{SW}" stroke-linejoin="round"/>')
        out.append(f'<path d="{stripe}" fill="none" stroke="{RED}"'
                   f' stroke-width="10" stroke-linecap="round"/>')
    else:
        band = (f"M 392 110 C 424 82, 576 82, 608 110 "
                f"L {m(NECK[0])} {NECK[1]} C 552 164, 448 164, {NECK[0]} {NECK[1]} Z")
        stripe = "M 400 104 C 432 82, 568 82, 600 104"
        out.append(f'<path d="{band}" fill="{fill}" stroke="{LINE}"'
                   f' stroke-width="{SW}" stroke-linejoin="round"/>')
        out.append(f'<path d="{stripe}" fill="none" stroke="{RED}"'
                   f' stroke-width="11" stroke-linecap="round"/>')
    return "\n".join(out)


# ------------------------------------------------------------- graphics ----
def brand_mark(x, y, s=1.0):
    """Ribbon monogram at centre chest — placeholder for the real mark."""
    d = ("M 0 46 L 20 4 L 44 32 L 68 4 L 88 46 L 70 46 L 60 26 "
         "L 44 50 L 28 26 L 18 46 Z")
    return f'<g transform="translate({x},{y}) scale({s})"><path d="{d}" fill="{GREEN}"/></g>'


def crest(x, y, s=1.0):
    """Simplified club crest — placeholder for the real artwork."""
    return f"""<g transform="translate({x},{y}) scale({s})">
  <path d="M -32 -36 L 32 -36 L 32 10 C 32 36, 13 49, 0 56
           C -13 49, -32 36, -32 10 Z" fill="{RED}" stroke="{BLACK}" stroke-width="3.5"/>
  <path d="M -32 -36 L -32 10 C -32 24, -27 33, -19 41 L -19 -36 Z" fill="{GREEN}"/>
  <path d="M 32 -36 L 32 10 C 32 24, 27 33, 19 41 L 19 -36 Z" fill="{GREEN}"/>
  <rect x="-19" y="-29" width="38" height="16" fill="{WHITE}"/>
  <text x="0" y="-16" font-family="DejaVu Sans" font-size="14" font-weight="bold"
        fill="{RED}" text-anchor="middle">APC</text>
  <path d="M -5 -8 L 5 -8 L 3.5 32 L -3.5 32 Z" fill="{BLACK}"/>
</g>"""


def wordmark(x, y):
    """'City Boy' lockup — placeholder, swap in the real script logo."""
    return f"""<g transform="translate({x},{y})">
  <text x="0" y="0" font-family="DejaVu Serif" font-style="italic"
        font-weight="bold" font-size="40" fill="{BLACK}">City</text>
  <text x="8" y="38" font-family="DejaVu Serif" font-style="italic"
        font-weight="bold" font-size="40" fill="{BLACK}">Boy</text>
</g>"""


def year_number(x, y):
    return (f'<text x="{x}" y="{y}" font-family="DejaVu Sans" font-weight="bold"'
            f' font-size="122" letter-spacing="4" fill="none" stroke="{RED}"'
            f' stroke-width="7" text-anchor="middle">2027</text>')


def make_up_lines():
    """Raglan seams, cuff turn-ups and the hem stitch line."""
    thin = f'fill="none" stroke="{LINE}" stroke-width="1.6"'
    dash = f'fill="none" stroke="{SEAM}" stroke-width="1.8" stroke-dasharray="10 9"'
    return "\n".join([
        f'<path d="M {ARMPIT[0]} {ARMPIT[1]} {RAGLAN}" {thin}/>',
        f'<path d="M {m(ARMPIT[0])} {ARMPIT[1]} C {m(296)} 340, {m(372)} 210,'
        f' {m(NECK[0])} {NECK[1]}" {thin}/>',
        f'<path d="M 66 428 L 218 462" {dash}/>',
        f'<path d="M {m(66)} 428 L {m(218)} 462" {dash}/>',
        f'<path d="M 206 878 L {m(206)} 878" {dash}/>',
    ])


def jersey(colorway, view):
    tag = f"{colorway['id']}-{view}"
    outline = body_outline(view)
    sleeve = sleeve_block()

    yoke = ""
    if colorway["sleeve"] != colorway["body"]:
        yoke = (f'<path d="{sleeve}" fill="{colorway["sleeve"]}"/>'
                f'<g transform="translate({2 * CX},0) scale(-1,1)">'
                f'<path d="{sleeve}" fill="{colorway["sleeve"]}"/></g>')

    art = (wordmark(372, 424) + crest(624, 424) + brand_mark(456, 328)
           if view == "front" else year_number(CX, 408))

    return f"""<g>
  <defs>
    <clipPath id="clip-{tag}"><path d="{outline}"/></clipPath>
    <clipPath id="slv-{tag}"><path d="{sleeve}"/></clipPath>
    <clipPath id="slvm-{tag}">
      <path d="{sleeve}" transform="translate({2 * CX},0) scale(-1,1)"/>
    </clipPath>
  </defs>
  <path d="{outline}" fill="{colorway['body']}"/>
  <g clip-path="url(#clip-{tag})">
    {yoke}
    <g>{panels(f'slv-{tag}')}</g>
    <g transform="translate({2 * CX},0) scale(-1,1)">{panels(f'slv-{tag}')}</g>
    {make_up_lines()}
  </g>
  <path d="{outline}" fill="none" stroke="{LINE}" stroke-width="{SW}"
        stroke-linejoin="round"/>
  {collar(colorway, view)}
  {art}
</g>"""


def swatches(x, y, size=120, gap=28):
    cells = [(RED, 0, 0), (NAVY, 1, 0), (GREEN, 0, 1), (BLUE, 1, 1)]
    out = [f'<rect x="{x + cx * (size + gap)}" y="{y + cy * (size + gap)}"'
           f' width="{size}" height="{size}" fill="{c}"/>' for c, cx, cy in cells]
    out.append(f'<rect x="{x}" y="{y + 2 * (size + gap)}" width="{size}"'
               f' height="{size}" fill="{WHITE}" stroke="{GREY}" stroke-width="2"/>')
    return "\n".join(out)


def sheet(colorway):
    W = H = 2000
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
     viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" fill="{WHITE}"/>
  <g transform="translate(70,60) scale(0.92)">{jersey(colorway, 'front')}</g>
  <g transform="translate(980,1010) scale(0.92)">{jersey(colorway, 'back')}</g>
  {swatches(1500, 190)}
</svg>"""


COLORWAYS = [
    {"id": "white", "body": WHITE, "sleeve": WHITE, "collar": WHITE,
     "name": "City-Boy-jersey-3-white"},
    {"id": "black", "body": WHITE, "sleeve": BLACK, "collar": BLACK,
     "name": "City-Boy-jersey-3-black"},
]

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for cw in COLORWAYS:
        svg = sheet(cw)
        base = os.path.join(here, cw["name"])
        with open(base + ".svg", "w") as fh:
            fh.write(svg)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=base + ".png",
                         output_width=1400)
        cairosvg.svg2pdf(bytestring=svg.encode(), write_to=base + ".pdf")
        print("wrote", base + ".svg")

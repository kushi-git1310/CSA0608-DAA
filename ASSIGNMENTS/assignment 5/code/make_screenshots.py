"""Renders the REAL captured program output (../outputs/*.txt) as terminal-style PNG screenshots."""
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "screenshots")
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 15)
BOLD = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 15)
LH, PADX, PADY, TITLE = 20, 16, 14, 34
PROGS = ["b1_graph_colouring", "trace_demo", "b2_adversarial", "b3_set_cover", "b4_bin_packing"]
PAGE = 42


def render(cmd, lines, path, part, parts):
    w = max(80, max(len(l) for l in lines) + 2)
    W = PADX * 2 + int(FONT.getlength("M") * w) + 0
    H = TITLE + PADY * 2 + LH * (len(lines) + 2)
    im = Image.new("RGB", (W, H), (30, 30, 36))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, TITLE], fill=(58, 58, 66))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([12 + i * 22, 11, 24 + i * 22, 23], fill=c)
    d.text((90, 8), f"S KUSHA LAKSHMI (CSA0608) - Terminal - {cmd}  [{part}/{parts}]", font=FONT, fill=(220, 220, 220))
    y = TITLE + PADY
    d.text((PADX, y), f"$ {cmd}", font=BOLD, fill=(120, 220, 120)); y += LH
    for l in lines:
        col = (230, 230, 230)
        if "PASS" in l or "ALL TESTS PASSED" in l: col = (120, 230, 120)
        if "FAIL" in l or "NOT colourable" in l or "NO colouring" in l: col = (255, 150, 120)
        if l.startswith("=") or l.startswith("-"): col = (130, 170, 255)
        if "BACKTRACK" in l: col = (255, 200, 90)
        d.text((PADX, y), l, font=FONT, fill=col); y += LH
    im.save(path)


for p in PROGS:
    txt = open(os.path.join(HERE, "..", "outputs", p + ".txt")).read().rstrip("\n").split("\n")
    pages = [txt[i:i + PAGE] for i in range(0, len(txt), PAGE)]
    for k, chunk in enumerate(pages, 1):
        path = os.path.join(OUT, f"{p}_{k}.png")
        render(f"python3 {p}.py", chunk, path, k, len(pages))
        print("wrote", os.path.basename(path))

"""Renders each outputs/taskN_output.txt as terminal-style PNG screenshots (screenshots/taskN_partK.png)."""
import glob, os, textwrap
from PIL import Image, ImageDraw, ImageFont

FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 15)
BOLD = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 15)
CW, LH = 9, 20            # char width / line height
COLS, ROWS = 118, 46
BG, FG, ACC, OK, BAD, TITLE = (30, 30, 30), (220, 220, 220), (86, 182, 194), (152, 195, 121), (224, 108, 117), (60, 60, 60)

def wrap(lines):
    out = []
    for ln in lines:
        if len(ln) <= COLS:
            out.append(ln)
        else:
            ind = len(ln) - len(ln.lstrip())
            out += textwrap.wrap(ln, COLS, subsequent_indent=" " * (ind + 4), replace_whitespace=False, drop_whitespace=False)
    return out

def colour(ln):
    if ln.startswith("#") or ln.startswith("==="): return ACC, True
    if any(k in ln for k in ("MATCH", "PASS", "valid MST", "OK", "CORRECT", "MINIMUM", "Minimum", "ALL MATCH")) and "MISMATCH" not in ln: return OK, False
    if any(k in ln for k in ("WRONG", "MISMATCH", "defect", "misleading", "NEGATIVE CYCLE DETECTED", "rejected")): return BAD, False
    return FG, False

def render(cmd, lines, path):
    h = 34 + ROWS * LH + 16
    img = Image.new("RGB", (COLS * CW + 30, h), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width, 30], fill=TITLE)
    for k, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([10 + k * 20, 9, 22 + k * 20, 21], fill=c)
    d.text((90, 7), "Terminal - S KUSHA LAKSHMI (192571074) - CSA0608", font=FONT, fill=(200, 200, 200))
    d.text((15, 36), cmd, font=BOLD, fill=(229, 192, 123))
    y = 36 + LH
    for ln in lines:
        col, b = colour(ln)
        d.text((15, y), ln, font=BOLD if b else FONT, fill=col)
        y += LH
    img.crop((0, 0, img.width, y + 12)).save(path)

os.makedirs("screenshots", exist_ok=True)
for f in glob.glob("screenshots/*.png"): os.remove(f)
for f in sorted(glob.glob("outputs/task*_output.txt")):
    n = os.path.basename(f)[4]
    script = glob.glob(f"task{n}_*.py")[0]
    lines = wrap(open(f, encoding="utf-8").read().rstrip("\n").split("\n"))
    parts = [lines[i:i + ROWS - 1] for i in range(0, len(lines), ROWS - 1)]
    for k, part in enumerate(parts, 1):
        render(f"PS C:\\CSA0608_Assignment4B> python {script}   [screen {k}/{len(parts)}]", part, f"screenshots/task{n}_part{k}.png")
    print(script, len(lines), "lines ->", len(parts), "screenshots")

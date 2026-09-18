"""OG 画像（1200x630）を static/og/ に生成する。ビルドとは独立に手元で実行し、生成物をコミットする。"""
import glob, json, os, re, textwrap
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG = json.load(open(os.path.join(ROOT, "site.json"), encoding="utf-8"))
META_RE = re.compile(r"^<!--\s*meta\s*(\{.*?\})\s*-->", re.S)
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_R = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
OUT = os.path.join(ROOT, "static", "og")
os.makedirs(OUT, exist_ok=True)
W, H = 1200, 630
BG, FG, ACCENT, SUB = (250, 248, 243), (34, 40, 49), (39, 110, 96), (110, 116, 124)


NO_HEAD = set("ー、。）」・ぁぃぅぇぉっゃゅょァィゥェォッャュョ")


def wrap_jp(s, n):
    """n 文字で折り返し、行頭禁則文字は前行に付ける。"""
    lines, cur = [], ""
    for ch in s:
        if len(cur) >= n and ch not in NO_HEAD:
            lines.append(cur)
            cur = ""
        cur += ch
    if cur:
        lines.append(cur)
    return lines


def draw(slug, title, sub):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 18], fill=ACCENT)
    fb = ImageFont.truetype(FONT, 60, index=0)
    fs = ImageFont.truetype(FONT_R, 30, index=0)
    fbrand = ImageFont.truetype(FONT, 34, index=0)
    main = title.split("｜")[0]
    lines = wrap_jp(main, 16)[:3]
    y = 120
    for ln in lines:
        d.text((80, y), ln, font=fb, fill=FG)
        y += 84
    if sub:
        for ln in wrap_jp(sub, 34)[:2]:
            d.text((80, y + 10), ln, font=fs, fill=SUB)
            y += 44
    d.text((80, H - 90), CONFIG["site_name"], font=fbrand, fill=ACCENT)
    d.text((W - 80 - d.textlength("無料・登録不要", font=fs), H - 84), "無料・登録不要", font=fs, fill=SUB)
    img.save(os.path.join(OUT, f"{slug}.png"), optimize=True)


draw("index", CONFIG["site_name"], CONFIG["tagline"])
for p in sorted(glob.glob(os.path.join(ROOT, "tools", "*.html"))):
    meta = json.loads(META_RE.match(open(p, encoding="utf-8").read()).group(1))
    slug = os.path.splitext(os.path.basename(p))[0]
    parts = meta["title"].split("｜")
    draw(slug, parts[0], parts[1] if len(parts) > 1 else "")
for entry in CONFIG["pages"]:
    slug, title, desc = entry[0], entry[1], entry[2]
    if len(entry) > 3 and entry[3].get("hidden"):
        continue
    draw(slug, title, desc[:60])
print("ok", len(os.listdir(OUT)))

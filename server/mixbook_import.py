"""Turn the Mixbook layout of The Hearts of Mauna Kea (server/mixbook-book.json, exported
from the Mixbook share link) into the page list the book reader uses (server/book-pages.json).

Every Mixbook page is rebuilt as HTML: photos and text boxes placed where they sit in
the book, so the text stays sharp at any size. Mixbook's own fonts are swapped for close
matches from Google Fonts. Photos still load from Mixbook for now (their largest size,
1400 px); swap in the original photos later by changing PHOTO_BASE / the src values.

Run:  python3 server/mixbook_import.py && python3 build.py
"""
import json, os, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
book = json.load(open(os.path.join(HERE, "mixbook-book.json")))
AR = book["ar"]            # page width / height (trim). 1 unit = page height.
PT = 576                   # Mixbook font sizes are points; 576 pt = 1 unit

FONTS = {
    "Above the Beyond Serif": "'Cormorant Garamond', Georgia, serif;font-weight:500",
    "Didot New": "'Cormorant Garamond', Georgia, serif",
    "Bentham": "Bentham, Georgia, serif",
    "Bohemia Small Caps": "'Cormorant SC', 'Cormorant Garamond', serif;font-weight:500",
    "May Wilde": "Allura, cursive",
    "Allura": "Allura, cursive",
    "Above the Beyond Script": "Allura, cursive",
    "Futura": "Jost, sans-serif",
    "Avenir Next": "Jost, sans-serif",
}

def pct(v): return f"{v * 100:.3f}%".replace(".000%", "%")

def box(i):
    left = (i["x"] - i["w"] / 2 + AR / 2) / AR
    top = i["y"] - i["h"] / 2 + 0.5
    st = f"left:{pct(left)};top:{pct(top)};width:{pct(i['w'] / AR)};height:{pct(i['h'])}"
    if i.get("rot"): st += f";transform:rotate({i['rot']}deg)"
    if i.get("a") not in (None, 1): st += f";opacity:{i['a']}"
    return st

def crop(fw, fh, iw, ih, ox, oy):
    return (f"width:{pct(iw / fw)};height:{pct(ih / fh)};"
            f"left:{pct(0.5 + (ox - iw / 2) / fw)};top:{pct(0.5 + (oy - ih / 2) / fh)}")

def span_style(attrs):
    a = dict(re.findall(r'([a-z-]+)="([^"]*)"', attrs))
    st = []
    fam = a.get("font-family")
    if fam: st.append("font-family:" + FONTS.get(fam, "'Cormorant Garamond', serif"))
    if a.get("font-size"): st.append(f"font-size:calc({float(a['font-size']):g} * var(--pt))")
    if a.get("color") and a["color"].lower() != "#000000": st.append("color:" + a["color"])
    if a.get("font-style") == "italic": st.append("font-style:italic")
    if a.get("font-weight") not in (None, "400", "normal"): st.append("font-weight:" + a["font-weight"])
    if a.get("line-height"): st.append("line-height:" + a["line-height"])
    if a.get("text-decoration"): st.append("text-decoration:" + a["text-decoration"])
    return ";".join(st)

def text_html(doc):
    out = []
    for p_attrs, inner in re.findall(r"<p([^>]*)>(.*?)</p>", doc, re.S):
        align = dict(re.findall(r'([a-z-]+)="([^"]*)"', p_attrs)).get("text-align", "left")
        spans = re.findall(r"<s([^>]*)>(.*?)</s>", inner, re.S)
        body = "".join(f'<span style="{span_style(a)}">{t}</span>' for a, t in spans if t)
        size = ""
        if spans:
            m = re.search(r'font-size="([^"]+)"', spans[0][0]); lh = re.search(r'line-height="([^"]+)"', spans[0][0])
            size = f"font-size:calc({float(m.group(1)):g} * var(--pt));" if m else ""
            size += f"line-height:{lh.group(1)};" if lh else ""
        out.append(f'<p style="{size}text-align:{align}">{body or "<br>"}</p>')
    return "".join(out)

def plain_text(doc):
    paras = []
    for _, inner in re.findall(r"<p([^>]*)>(.*?)</p>", doc, re.S):
        paras.append(html.unescape(re.sub(r"<[^>]+>", "", inner)).strip())
    return "\n".join(paras).strip()

def render(pg, n):
    parts, imgs, alt_bits = [], [], []
    bg = pg.get("bg") or {}
    fill = bg.get("fill") or "#ffffff"
    if bg.get("img"):
        # background box is 1.36655 x 1.07125, centred on the page
        bw, bh = 1.36655, 1.07125
        frame = {"x": 0, "y": 0, "w": bw, "h": bh}
        parts.append(f'<div class="mb-photo" style="{box(frame)}"><img src="{bg["img"]}" alt="" style="{crop(bw, bh, bg["iw"], bg["ih"], bg["ox"], bg["oy"])}" loading="lazy" decoding="async"></div>')
        imgs.append(bg["img"])
    for i in pg["items"]:
        if i["t"] == "p":
            if not i.get("src"): continue
            st = crop(i["w"], i["h"], i["iw"], i["ih"], i["ox"], i["oy"])
            if i.get("flip"): st += ";transform:scaleX(-1)"
            extra = f";border-radius:{i['br']}px" if i.get("br") else ""
            parts.append(f'<div class="mb-photo" style="{box(i)}{extra}"><img src="{i["src"]}" alt="" style="{st}" decoding="async"></div>')
            imgs.append(i["src"])
        else:
            st = box(i)
            if i.get("fill"): st += f";background:color-mix(in srgb, {i['fill']} {round(i.get('fa', 1) * 100)}%, transparent)"
            parts.append(f'<div class="mb-text" style="{st}">{text_html(i["doc"])}</div>')
            t = plain_text(i["doc"])
            if t: alt_bits.append(t)
    raw = f'<div class="mb-page" style="background:{fill}">{"".join(parts)}</div>'
    return {"raw": raw, "imgs": imgs, "text": page_text(pg)}

def page_text(pg):
    texts = [plain_text(i["doc"]) for i in sorted(pg["items"], key=lambda i: (round(i["y"] - i["h"] / 2, 2), i["x"])) if i["t"] == "t"]
    return "\n\n".join(re.sub(r"\n{2,}", "\n\n", t) for t in texts if t)

pages = {p["pos"]: p for p in book["pages"]}
order = [(-1, "Front cover")] + [(k, f"Page {k}") for k in range(1, 158)] + [(-2, "Back cover")]
out = []
for pos, label in order:
    out.append(render(pages[pos], label))
json.dump({"aspect": AR, "pages": out}, open(os.path.join(HERE, "book-pages.json"), "w"), ensure_ascii=False, separators=(",", ":"))

# Plain text of every page, in order, for review.
lines = [f"# The Hearts of Mauna Kea: text of every page\n"]
for pos, label in order:
    pg = pages[pos]
    texts = [plain_text(i["doc"]) for i in sorted(pg["items"], key=lambda i: (round(i["y"] - i["h"] / 2, 2), i["x"])) if i["t"] == "t"]
    texts = [t for t in texts if t]
    photos = sum(1 for i in pg["items"] if i["t"] == "p")
    lines.append(f"## {label}")
    lines.append(f"_{photos} photo{'s' if photos != 1 else ''}_" if photos else "_no photos_")
    lines.extend(t + "\n" for t in texts)
open(os.path.join(HERE, "book-text.md"), "w").write("\n".join(lines))
print("pages:", len(out))

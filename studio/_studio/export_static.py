# -*- coding: utf-8 -*-
"""
Render committed STATIC assets with Pillow (free, offline, no AI):
  exports/<key>-connect-flyer.png   -> high-res poster flyer (1080x1528)
  exports/<key>-connect-advert.gif  -> animated advert (1280x720, looping)
Run from the Mathematics/ root:  python3 _studio/export_static.py
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from products import HMG, ALL
from PIL import Image, ImageDraw, ImageFont

OUT = "exports"
os.makedirs(OUT, exist_ok=True)
FD = "/usr/share/fonts/truetype/dejavu"

def font(sz, bold=True):
    f = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FD, f), sz)

def hx(c):
    c = c.lstrip("#"); return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

def lerp_col(a, b, t):
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

def vgrad(w, h, c1, c2):
    """Diagonal-ish vertical gradient."""
    base = Image.new("RGB", (1, h))
    for y in range(h):
        base.putpixel((0, y), lerp_col(c1, c2, y/max(1, h-1)))
    return base.resize((w, h))

def rrect(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)

def text_w(d, s, f):
    return d.textbbox((0, 0), s, font=f)[2]

def wrap(d, s, f, maxw):
    words, lines, line = s.split(), [], ""
    for w in words:
        t = (line + " " + w).strip()
        if text_w(d, t, f) <= maxw or not line:
            line = t
        else:
            lines.append(line); line = w
    if line: lines.append(line)
    return lines

def center(d, s, f, cx, y, fill):
    d.text((cx - text_w(d, s, f)/2, y), s, font=f, fill=fill)

# ---------------- FLYER PNG ----------------
def flyer_png(p):
    W, H = 1080, 1400
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    c1, c2, ac = hx(p["c1"]), hx(p["c2"]), hx(p["accent"])
    # hero
    heroH = 430
    img.paste(vgrad(W, heroH, c1, c2), (0, 0))
    # soft circles
    ov = Image.new("RGBA", (W, heroH), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([W-180, -180, W+180, 180], fill=(255, 255, 255, 18))
    od.ellipse([-140, heroH-150, 160, heroH+200], fill=(255, 255, 255, 14))
    img.paste(Image.alpha_composite(img.crop((0, 0, W, heroH)).convert("RGBA"), ov).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)
    # brand chip
    rrect(d, [56, 40, 56+58, 40+58], 16, (255, 255, 255, 60))
    d.rounded_rectangle([56, 40, 114, 98], radius=16, fill=lerp_col(c1, (255,255,255), .18))
    center(d, "HMG", font(22), 85, 58, (255, 255, 255))
    d.ellipse([104, 44, 118, 58], fill=ac)
    d.text((128, 48), HMG["name"], font=font(24), fill=(255, 255, 255))
    d.text((128, 80), HMG["tagline"], font=font(15, False), fill=(235, 238, 255))
    # eyebrow
    eb = "FOR " + p["for"].upper()
    ebf = font(17); ew = text_w(d, eb, ebf)
    d.rounded_rectangle([56, 132, 56+ew+34, 132+38], radius=19, fill=lerp_col(c1, (255,255,255), .22))
    d.text((73, 140), eb, font=ebf, fill=(255, 255, 255))
    # title
    title = p["name"] + ((" " + p["version"]) if p.get("version") else "")
    tf = font(64)
    if text_w(d, title, tf) > W-110: tf = font(52)
    d.text((56, 188), title, font=tf, fill=(255, 255, 255))
    # subtitle
    sf = font(24, False)
    for i, ln in enumerate(wrap(d, p["tagline"], sf, W-120)[:3]):
        d.text((56, 272 + i*34), ln, font=sf, fill=(240, 243, 255))
    # big icon (emoji likely tofu in DejaVu) -> draw a glyph circle instead
    d.ellipse([W-150, heroH-150, W-44, heroH-44], outline=(255, 255, 255), width=4)
    # problem bar
    y = heroH + 36
    d.rounded_rectangle([56, y, W-56, y+72], radius=12, fill=(255, 247, 237))
    d.rectangle([56, y, 62, y+72], fill=ac)
    pf = font(19, False)
    pls = wrap(d, "? " + p["problem"], pf, W-160)[:2]
    for i, ln in enumerate(pls):
        d.text((84, y+16 + i*26), ln, font=pf, fill=(146, 64, 14))
    # feature grid (2 cols x 4 rows)
    gy = y + 100
    colw = (W - 112) // 2
    nf, df = font(19), font(15, False)
    for i, (n, ds) in enumerate(p["features"][:8]):
        cx = 56 + (i % 2) * colw
        ry = gy + (i // 2) * 118
        d.ellipse([cx, ry, cx+30, ry+30], fill=c1)
        center(d, "\u2713", font(17), cx+15, ry+5, (255, 255, 255))
        d.text((cx+44, ry-2), n, font=nf, fill=(15, 23, 42))
        for j, ln in enumerate(wrap(d, ds, df, colw-60)[:2]):
            d.text((cx+44, ry+26 + j*20), ln, font=df, fill=(100, 116, 139))
    # why row
    wy = gy + 4*118 + 6
    items = [("\u20A60", "Monthly cost"), ("Minutes", "To launch"), ("100%", "You own data"), ("No AI", "API fees")]
    bw = (W - 112 - 3*14) // 4
    for i, (big, small) in enumerate(items):
        bx = 56 + i*(bw+14)
        d.rounded_rectangle([bx, wy, bx+bw, wy+96], radius=12, fill=(241, 245, 249))
        center(d, big, font(30), bx+bw/2, wy+18, c1)
        center(d, small, font(13, False), bx+bw/2, wy+62, (100, 116, 139))
    # sectors
    sy = wy + 118
    d.text((56, sy), "Perfect for:", font=font(16), fill=(15, 23, 42))
    sec = " \u00B7 ".join(p["sectors"])
    for i, ln in enumerate(wrap(d, sec, font(15, False), W-260)[:2]):
        d.text((196, sy + i*22), ln, font=font(15, False), fill=(71, 85, 105))
    # CTA band
    cy = H - 150
    img.paste((15, 23, 42), (0, cy, W, H-44))
    d = ImageDraw.Draw(img)
    d.text((56, cy+28), "Ready when you are", font=font(28), fill=(255, 255, 255))
    for i, ln in enumerate(wrap(d, "Send us your details & we build & deploy your platform — free tools, you own it.", font(15, False), 560)[:2]):
        d.text((56, cy+70 + i*22), ln, font=font(15, False), fill=(203, 213, 225))
    pill = "\u260E " + HMG["waText"]
    pf2 = font(22); pw = text_w(d, pill, pf2)
    d.rounded_rectangle([W-56-pw-40, cy+34, W-56, cy+34+50], radius=12, fill=c1)
    d.text((W-56-pw-20, cy+44), pill, font=pf2, fill=(255, 255, 255))
    center(d, HMG["site"].replace("https://", ""), font(15, False), W-56-(pw+40)/2, cy+92, (148, 163, 184))
    # footer strip
    d.rectangle([0, H-44, W, H], fill=(11, 18, 32))
    foot = "A product of %s \u00B7 %s \u00B7 %s \u00B7 Free tools \u00B7 No AI API" % (HMG["name"], HMG["tagline"], HMG["city"])
    center(d, foot, font(13, False), W/2, H-32, (148, 163, 184))
    img.save(os.path.join(OUT, "%s-connect-flyer.png" % p["key"]), "PNG")

# ---------------- ADVERT GIF ----------------
def gif_bg(W, H, c1, c2):
    return vgrad(W, H, c1, c2).convert("RGB")

def advert_gif(p):
    W, H = 1280, 720
    c1, c2, ac = hx(p["c1"]), hx(p["c2"]), hx(p["accent"])
    base = gif_bg(W, H, c1, c2)
    feats = [n for n, _ in p["features"][:6]]
    frames = []
    title = p["name"] + ((" " + p["version"]) if p.get("version") else "")

    def newframe():
        return base.copy()

    def foot(d):
        center(d, "%s \u00B7 %s" % (HMG["name"], HMG["tagline"]), font(20, False), W/2, H-46, (235, 238, 250))

    # Scene 1: intro (6 frames)
    for k in range(6):
        f = newframe(); d = ImageDraw.Draw(f)
        s = int(90 + k*8)
        d.rounded_rectangle([W/2-s/2, 210-s/2, W/2+s/2, 210+s/2], radius=int(s*.24), fill=lerp_col(c1, (255,255,255), .18))
        center(d, "HMG", font(int(s*.34)), W/2, 210-s*0.18, (255, 255, 255))
        center(d, title, font(72), W/2, 330, (255, 255, 255))
        center(d, p["for"], font(30, False), W/2, 430, (235, 238, 250))
        foot(d); frames.append((f, 500 if k == 5 else 90))

    # Scene 2: problem (3 frames)
    for k in range(3):
        f = newframe(); d = ImageDraw.Draw(f)
        center(d, "?", font(150), W/2, 150, (255, 255, 255))
        for i, ln in enumerate(wrap(d, p["problem"], font(40), W-260)[:3]):
            center(d, ln, font(40), W/2, 360 + i*56, (255, 255, 255))
        foot(d); frames.append((f, 700 if k == 2 else 250))

    # Scene 3: features (reveal, 1 frame per feature + hold)
    for shown in range(1, len(feats)+1):
        f = newframe(); d = ImageDraw.Draw(f)
        d.text((110, 90), "What you get", font=font(50), fill=(255, 255, 255))
        for i in range(shown):
            y = 200 + i*78
            d.ellipse([110, y-12, 150, y+28], fill=ac)
            center(d, "\u2713", font(24), 130, y-8, c2)
            d.text((170, y-8), feats[i], font=font(34, False), fill=(255, 255, 255))
        foot(d); frames.append((f, 760 if shown == len(feats) else 520))

    # Scene 4: why (2 frames)
    items = [("\u20A60", "Monthly cost"), ("Minutes", "To go live"), ("100%", "You own data"), ("No AI", "API fees")]
    for k in range(2):
        f = newframe(); d = ImageDraw.Draw(f)
        center(d, "Why HMG Connect?", font(50), W/2, 110, (255, 255, 255))
        cw, gap = 250, 30; tot = 4*cw+3*gap; sx = (W-tot)//2
        for i, (big, small) in enumerate(items):
            x = sx + i*(cw+gap)
            d.rounded_rectangle([x, 270, x+cw, 470], radius=20, fill=lerp_col(c1, (255,255,255), .14))
            center(d, big, font(54), x+cw/2, 320, ac)
            center(d, small, font(26, False), x+cw/2, 405, (255, 255, 255))
        foot(d); frames.append((f, 900 if k == 1 else 350))

    # Scene 5: sectors (1 frame)
    f = newframe(); d = ImageDraw.Draw(f)
    center(d, "Perfect for", font(48), W/2, 90, (255, 255, 255))
    for i, s in enumerate(p["sectors"][:6]):
        sf = font(28, False); sw = text_w(d, s, sf)
        d.rounded_rectangle([W/2-sw/2-24, 200+i*72-26, W/2+sw/2+24, 200+i*72+22], radius=24, fill=lerp_col(c1, (255,255,255), .18))
        center(d, s, sf, W/2, 200+i*72-20, (255, 255, 255))
    foot(d); frames.append((f, 1100))

    # Scene 6: CTA (pulse, 4 frames)
    for k in range(4):
        f = newframe(); d = ImageDraw.Draw(f)
        s = 110
        d.rounded_rectangle([W/2-s/2, 150-s/2, W/2+s/2, 150+s/2], radius=int(s*.24), fill=lerp_col(c1, (255,255,255), .18))
        center(d, "HMG", font(int(s*.34)), W/2, 150-s*0.18, (255, 255, 255))
        center(d, "Ready when you are.", font(56), W/2, 300, (255, 255, 255))
        for i, ln in enumerate(wrap(d, "Send us your details and we build & deploy your platform — free tools, you own it.", font(30, False), W-300)[:2]):
            center(d, ln, font(30, False), W/2, 390 + i*40, (240, 243, 255))
        pill = "\u260E " + HMG["waText"]; pf = font(34); pw = text_w(d, pill, pf)
        pad = 30 + k*4
        d.rounded_rectangle([W/2-pw/2-pad, 520-6, W/2+pw/2+pad, 580+6], radius=40, fill=(255, 255, 255))
        center(d, pill, pf, W/2, 532, c2)
        center(d, HMG["site"].replace("https://", ""), font(26, False), W/2, 612, (240, 243, 255))
        foot(d); frames.append((f, 1500 if k == 3 else 180))

    imgs = [fr for fr, _ in frames]
    durs = [du for _, du in frames]
    imgs[0].save(os.path.join(OUT, "%s-connect-advert.gif" % p["key"]),
                 save_all=True, append_images=imgs[1:], duration=durs, loop=0, optimize=True)

def main():
    for p in ALL:
        flyer_png(p); advert_gif(p)
        print("exported", p["key"])
    print("Static exports complete in ./%s" % OUT)

if __name__ == "__main__":
    main()

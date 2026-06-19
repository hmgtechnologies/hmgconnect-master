# -*- coding: utf-8 -*-
"""
Render committed MP4 advert videos with Pillow + ffmpeg (imageio-ffmpeg).
Output: exports/<key>-connect-advert.mp4  (1280x720, H.264, ~21s, social-ready)
Run from the Mathematics/ root:  python3 _studio/export_mp4.py
100% free (open-source ffmpeg via imageio-ffmpeg). NO AI API.

Reuses the exact scene drawing from export_static.py so the MP4 matches the GIF,
but renders at a steady 25 fps with smooth eased transitions.
"""
import os, sys, math, subprocess, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from products import HMG, ALL
from PIL import Image, ImageDraw, ImageFont

OUT = "exports"
os.makedirs(OUT, exist_ok=True)
FD = "/usr/share/fonts/truetype/dejavu"
FPS = 25
W, H = 1280, 720

def ffmpeg_exe():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"

def font(sz, bold=True):
    f = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FD, f), max(1, int(sz)))

def hx(c):
    c = c.lstrip("#"); return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

def mix(a, b, t):
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

def ease(t):
    t = 0 if t < 0 else 1 if t > 1 else t
    return 2*t*t if t < .5 else 1-((-2*t+2)**2)/2

def clamp(t):
    return 0.0 if t < 0 else 1.0 if t > 1 else t

def vgrad(c1, c2):
    col = Image.new("RGB", (1, H))
    for y in range(H):
        col.putpixel((0, y), mix(c1, c2, y/(H-1)))
    return col.resize((W, H))

def tw(d, s, f):
    return d.textbbox((0, 0), s, font=f)[2]

def ctext(d, s, f, cx, y, fill):
    d.text((cx - tw(d, s, f)/2, y), s, font=f, fill=fill)

def wrap(d, s, f, maxw):
    words, lines, line = s.split(), [], ""
    for w in words:
        t = (line+" "+w).strip()
        if tw(d, t, f) <= maxw or not line:
            line = t
        else:
            lines.append(line); line = w
    if line:
        lines.append(line)
    return lines

def rrect(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)


class Renderer:
    def __init__(self, p):
        self.p = p
        self.c1, self.c2, self.ac = hx(p["c1"]), hx(p["c2"]), hx(p["accent"])
        self.base = vgrad(self.c1, self.c2)
        self.feats = [n for n, _ in p["features"][:6]]
        self.title = p["name"] + ((" "+p["version"]) if p.get("version") else "")
        # scene durations (seconds)
        self.scenes = [("intro", 3.2), ("problem", 3.0), ("features", 6.0),
                       ("why", 3.0), ("sectors", 2.8), ("cta", 3.5)]
        self.total = sum(s[1] for s in self.scenes)

    def newframe(self):
        return self.base.copy()

    def foot(self, d):
        ctext(d, "%s  \u00B7  %s" % (HMG["name"], HMG["tagline"]), font(20, False), W/2, H-46, (235, 238, 250))

    def logo(self, d, cx, cy, s):
        s = max(8, s)
        rrect(d, [cx-s/2, cy-s/2, cx+s/2, cy+s/2], int(s*.24), mix(self.c1, (255, 255, 255), .18))
        ctext(d, "HMG", font(int(s*.34)), cx, cy-s*0.18, (255, 255, 255))
        d.ellipse([cx+s*0.22, cy-s*0.36, cx+s*0.22+s*0.13, cy-s*0.36+s*0.13], fill=self.ac)

    def chip(self, d, txt, cx, cy, f):
        w = tw(d, txt, f)
        rrect(d, [cx-w/2-24, cy-26, cx+w/2+24, cy+22], 24, mix(self.c1, (255, 255, 255), .18))
        ctext(d, txt, f, cx, cy-20, (255, 255, 255))

    def render(self, name, t):
        """t in [0,1] within the scene."""
        f = self.newframe(); d = ImageDraw.Draw(f)
        getattr(self, "s_"+name)(d, t)
        self.foot(d)
        return f

    def s_intro(self, d, t):
        a = ease(clamp(t*2))
        self.logo(d, W/2, 210, 90+50*a)
        if t > 0.15:
            ctext(d, self.title, font(72), W/2, 330, (255, 255, 255))
            ctext(d, self.p["for"], font(30, False), W/2, 430, (235, 238, 250))

    def s_problem(self, d, t):
        ctext(d, "?", font(150), W/2, 130, (255, 255, 255))
        for i, ln in enumerate(wrap(d, self.p["problem"], font(40), W-260)[:3]):
            ctext(d, ln, font(40), W/2, 360+i*56, (255, 255, 255))

    def s_features(self, d, t):
        d.text((110, 90), "What you get", font=font(50), fill=(255, 255, 255))
        n = len(self.feats)
        for i in range(n):
            start = i/(n+1)
            a = ease(clamp((t-start)*4))
            if a <= 0:
                continue
            y = 200+i*78
            x = 110+(1-a)*40
            d.ellipse([x, y-12, x+40, y+28], fill=self.ac)
            ctext(d, "\u2713", font(24), x+20, y-8, self.c2)
            d.text((x+60, y-8), self.feats[i], font=font(34, False), fill=(255, 255, 255))

    def s_why(self, d, t):
        items = [("\u20A60", "Monthly cost"), ("Minutes", "To go live"), ("100%", "You own data"), ("No AI", "API fees")]
        ctext(d, "Why HMG Connect?", font(50), W/2, 110, (255, 255, 255))
        cw, gap = 250, 30
        sx = (W-(4*cw+3*gap))//2
        for i, (big, small) in enumerate(items):
            dd = ease(clamp((t-i*0.12)*2.2))
            if dd <= 0:
                continue
            x = sx+i*(cw+gap)
            rrect(d, [x, 270, x+cw, 470], 20, mix(self.c1, (255, 255, 255), .14))
            ctext(d, big, font(54), x+cw/2, 320, self.ac)
            ctext(d, small, font(26, False), x+cw/2, 405, (255, 255, 255))

    def s_sectors(self, d, t):
        ctext(d, "Perfect for", font(48), W/2, 90, (255, 255, 255))
        for i, s in enumerate(self.p["sectors"][:6]):
            dd = ease(clamp((t-i*0.1)*2.4))
            if dd <= 0:
                continue
            self.chip(d, s, W/2, 200+i*72, font(28, False))

    def s_cta(self, d, t):
        a = ease(clamp(t*1.6))
        self.logo(d, W/2, 150, 110*a)
        ctext(d, "Ready when you are.", font(56), W/2, 300, (255, 255, 255))
        for i, ln in enumerate(wrap(d, "Send us your details and we build & deploy your platform \u2014 free tools, you own it.", font(30, False), W-300)[:2]):
            ctext(d, ln, font(30, False), W/2, 390+i*40, (240, 243, 255))
        pill = "\u260E " + HMG["waText"]
        pf = font(34)
        pw = tw(d, pill, pf)
        pad = 30 + 4*abs(math.sin(t*12))
        rrect(d, [W/2-pw/2-pad, 514, W/2+pw/2+pad, 586], 40, (255, 255, 255))
        ctext(d, pill, pf, W/2, 532, self.c2)
        ctext(d, HMG["site"].replace("https://", ""), font(26, False), W/2, 612, (240, 243, 255))


def encode(p):
    r = Renderer(p)
    tmp = tempfile.mkdtemp(prefix="mp4_")
    idx = 0
    # global time -> scene mapping
    nframes = int(round(r.total*FPS))
    acc = []
    t0 = 0.0
    bounds = []
    for name, dur in r.scenes:
        bounds.append((name, t0, t0+dur))
        t0 += dur
    for fi in range(nframes):
        gt = fi/FPS
        # find scene
        cur = bounds[-1]
        for b in bounds:
            if gt < b[2]:
                cur = b
                break
        name, s0, s1 = cur
        lt = (gt-s0)/(s1-s0)
        img = r.render(name, clamp(lt))
        img.save(os.path.join(tmp, "f%05d.png" % fi))
        idx += 1
    out = os.path.join(OUT, "%s-connect-advert.mp4" % p["key"])
    cmd = [ffmpeg_exe(), "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%05d.png"),
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "20",
           "-movflags", "+faststart", out]
    subprocess.run(cmd, capture_output=True)
    # cleanup frames
    for fn in os.listdir(tmp):
        os.unlink(os.path.join(tmp, fn))
    os.rmdir(tmp)
    return out, idx


def main():
    for p in ALL:
        out, n = encode(p)
        sz = os.path.getsize(out)/1048576 if os.path.exists(out) else 0
        print("mp4 %-12s %d frames  %.1f MB" % (p["key"], n, sz))
    print("MP4 exports complete in ./%s" % OUT)


if __name__ == "__main__":
    main()

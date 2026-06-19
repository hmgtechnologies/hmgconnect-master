# 📣 HMG Connect — Marketing Studio (folder: `Mathematics`)

Ready-to-share **e-flyers** and **advertisement videos** (plus social **caption
kits** and pre-rendered **PNG / MP4 / GIF** files) for every product in the
**HMG Connect Suite**, so you can create awareness that **HMG Concepts** can build
complete management platforms for clients the moment they share their details.

**100% free tools. NO AI API — deliberately, because it is not cost effective.**
HTML + Canvas + native browser recording for the live assets; Python/Pillow for
the static images; open-source **ffmpeg** (via `imageio-ffmpeg`) for the MP4s.
No paid services anywhere.

## 📦 What's inside (11 products)
| Product | e-Flyer (HTML) | Advert Video (HTML) | Caption Kit | Pre-rendered downloads |
|---|---|---|---|---|
| School Connect | `flyers/school-connect-flyer.html` | `videos/school-connect-video.html` | `captions/school-connect-captions.txt` | `exports/school-connect-flyer.png`, `exports/school-connect-advert.mp4`, `exports/school-connect-advert.gif` |
| Church Connect | `flyers/church-connect-flyer.html` | `videos/church-connect-video.html` | `captions/church-connect-captions.txt` | `exports/church-connect-flyer.png`, `exports/church-connect-advert.mp4`, `exports/church-connect-advert.gif` |
| Business Connect v3 | `flyers/business-connect-flyer.html` | `videos/business-connect-video.html` | `captions/business-connect-captions.txt` | `exports/business-connect-flyer.png`, `exports/business-connect-advert.mp4`, `exports/business-connect-advert.gif` |
| Clinic Connect new | `flyers/clinic-connect-flyer.html` | `videos/clinic-connect-video.html` | `captions/clinic-connect-captions.txt` | `exports/clinic-connect-flyer.png`, `exports/clinic-connect-advert.mp4`, `exports/clinic-connect-advert.gif` |
| DramaConnect | `flyers/drama-connect-flyer.html` | `videos/drama-connect-video.html` | `captions/drama-connect-captions.txt` | `exports/drama-connect-flyer.png`, `exports/drama-connect-advert.mp4`, `exports/drama-connect-advert.gif` |
| Hotel Connect new | `flyers/hotel-connect-flyer.html` | `videos/hotel-connect-video.html` | `captions/hotel-connect-captions.txt` | `exports/hotel-connect-flyer.png`, `exports/hotel-connect-advert.mp4`, `exports/hotel-connect-advert.gif` |
| Estate Connect new | `flyers/realestate-connect-flyer.html` | `videos/realestate-connect-video.html` | `captions/realestate-connect-captions.txt` | `exports/realestate-connect-flyer.png`, `exports/realestate-connect-advert.mp4`, `exports/realestate-connect-advert.gif` |
| Gym Connect new | `flyers/gym-connect-flyer.html` | `videos/gym-connect-video.html` | `captions/gym-connect-captions.txt` | `exports/gym-connect-flyer.png`, `exports/gym-connect-advert.mp4`, `exports/gym-connect-advert.gif` |
| Logistics Connect new | `flyers/logistics-connect-flyer.html` | `videos/logistics-connect-video.html` | `captions/logistics-connect-captions.txt` | `exports/logistics-connect-flyer.png`, `exports/logistics-connect-advert.mp4`, `exports/logistics-connect-advert.gif` |
| Salon Connect new | `flyers/salon-connect-flyer.html` | `videos/salon-connect-video.html` | `captions/salon-connect-captions.txt` | `exports/salon-connect-flyer.png`, `exports/salon-connect-advert.mp4`, `exports/salon-connect-advert.gif` |
| HMG Connect Suite | `flyers/suite-connect-flyer.html` | `videos/suite-connect-video.html` | `captions/suite-connect-captions.txt` | `exports/suite-connect-flyer.png`, `exports/suite-connect-advert.mp4`, `exports/suite-connect-advert.gif` |

Plus:
- `index.html` — the **Studio hub** (deploy as the home page). Each product card
  has **e-Flyer / Advert Video / Caption Kit** links and one-click **MP4 / PNG**
  download buttons; a gallery shows every flyer.
- `exports/` — **committed static files** ready to post now:
  `*-connect-flyer.png` (high-res posters), `*-connect-advert.mp4`
  (H.264, ~21s, 1280×720) and `*-connect-advert.gif` (looping).
- `captions/` — copy-and-paste social captions (short/medium/long + hashtags).
- `assets/` — shared logo. `manifest.json` — installable PWA. `.nojekyll`.
- `_studio/` — the **free generator scripts** (add products & re-render):
  - `_studio/products.py` — the single product list (edit this).
  - `_studio/generate.py` — rebuilds all HTML/captions/index/manifest.
  - `_studio/export_static.py` — re-renders PNG flyers + GIF adverts (Pillow).
  - `_studio/export_mp4.py` — re-renders MP4 adverts (Pillow + ffmpeg).

## ✨ Features of each asset (detailed)

### 🖼️ e-Flyers (`flyers/*.html` + `exports/*.png`)
- A4-portrait flyer: branded hero, the client's pain point, an **8-feature grid**,
  “why us” stats (₦0/month, minutes to launch, you own data, no AI fees), target
  sectors and a strong **call-to-action** with the HMG WhatsApp number & website.
- **Print / Save as PDF** (offline) and **Download as PNG** (2× hi-res) buttons.
- A ready-made **PNG** is also pre-rendered in `exports/` (no browser needed).
- Preview-safe: inline styling + SVG render even in sandboxed previews.

### 🎬 Advertisement Videos (`videos/*.html` + `exports/*.mp4` + `*.gif`)
- A real **16:9 animated advert** (~21s) on an HTML5 **Canvas**: animated
  intro/logo, problem, feature reveal, “why us” counters, sectors, pulsing CTA.
- **▶ Play / ↻ Restart** to preview; **⏺ Record & Download** saves a `.webm`
  via native **MediaRecorder** (no AI, no paid tools).
- Pre-rendered **MP4** (H.264, social-ready) **and** looping **GIF** versions are
  committed in `exports/` for instant sharing — no recording required. The MP4
  uploads directly to WhatsApp, Instagram, Facebook, TikTok & YouTube.

### 📝 Caption Kits (`captions/*.txt`)
- Short (WhatsApp/X), Medium (IG/FB) and Long (LinkedIn) captions + hashtags.

## 🆕 Products covered (11)
School · Church · Business (v3) · Clinic · Drama · Hotel · Estate/Property · Gym ·
**Logistics/Transport (new)** · **Salon/Spa (new)** · and the **HMG Connect Suite**
overview.

## 🚀 Deployment — step-by-step (all free)

### Option A — GitHub Pages (recommended)
1. Create a free account at <https://github.com> → **New repository**
   (e.g. `hmg-connect-studio`, **Public**) → **Create**.
2. **Add file → Upload files**.
3. Drag in **everything inside this `Mathematics` folder** (so `index.html` sits
   at the repo root beside `flyers/`, `videos/`, `captions/`, `exports/`,
   `assets/` and `.nojekyll`). **Commit changes**.
4. **Settings → Pages → Source: Deploy from a branch**; branch **main**, folder
   **/(root)**; **Save**.
5. Wait ~1 minute; your live URL appears, e.g.
   `https://<username>.github.io/hmg-connect-studio/`. Share it.

### Option B — Cloudflare Pages / Vercel (free)
1. Sign up free at <https://pages.cloudflare.com> or <https://vercel.com>.
2. **Create/Import project**, select this folder (or the GitHub repo).
3. Framework preset **None**; build command **(empty)**; output dir **/**;
   **Deploy**. Use the generated `*.pages.dev` / `*.vercel.app` URL.

### Option C — No hosting (instant)
- **Double-click `index.html`**. Flyers print to PDF, videos record locally, and
  the `exports/` PNG/MP4/GIF files are usable straight away — just attach & send.

> 💡 You no longer need to record anything: the committed `exports/*.mp4` and
> `*.png` are final, shareable files. The in-browser recorder is a bonus.

## ➕ Add more products later (no AI)
This studio is **data-driven**:
1. Add one entry to `_studio/products.py`.
2. Run `python3 _studio/generate.py` (HTML, captions, index, manifest).
3. Run `python3 _studio/export_static.py` (PNG flyers + GIF adverts).
4. Run `python3 _studio/export_mp4.py` (MP4 adverts).
Dependencies are free: `pip install pillow imageio-ffmpeg`.

## 🏷️ Brand embedding (lead generation)
Every flyer, video, caption and exported file carries **HMG Concepts** branding,
the WhatsApp number (**+234 810 086 6322**) and website — turning each shared asset into a
referral channel back to you.

---
© HMG Concepts. Built by Adewale Samson Adeagbo. Lagos, Nigeria. EdTech · DataTech · FaithTech.

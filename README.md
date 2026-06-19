# 🚀 HMG Connect — Master Launchpad

A single, deployable **home page for the entire HMG Connect ecosystem** by
**HMG Concepts** (His Marvellous Grace) — EdTech · DataTech · FaithTech.

It links, in one place:
- **10 free, no-code platform generators** — School, Church, Business (v3),
  Clinic, Hotel, Estate/Property, Gym, Logistics/Transport, Salon/Spa, Drama.
- **The HMG Connect Suite hub** — the public showcase that links all products.
- **The Marketing Studio** — flyers, advert videos (MP4/GIF/WebM) & caption kits
  (bundled here in the `studio/` subfolder, so flyer buttons work out of the box).
- The **live DramaConnect demo app**.

100% free tooling (static hosting). **No AI APIs.** This launchpad is a static
site — no database required.

## 📦 What's inside
```
HMG Connect Master/
├── index.html            # the launchpad (inline styles + SVG — preview-safe)
├── manifest.json         # installable PWA
├── sw.js                 # offline service worker
├── .nojekyll
├── README.md
├── assets/
│   ├── img/logo.png
│   └── js/links.js       # <-- put your deployed generator/hub URLs here
└── studio/               # the full Marketing Studio (flyers, videos, exports…)
```

## 🔧 One-time setup — point the buttons at your sites
Open `assets/js/links.js` and paste the public URL of each deployed generator and
the Suite hub. For example:
```js
window.HMG_LINKS = {
  school:   'https://yourname.github.io/school-connect/',
  business: 'https://business.yourdomain.com/',
  suite:    'https://yourname.github.io/hmg-connect-suite/',
  studio:   'studio/index.html',   // already bundled; leave as-is
  drama:    'https://hmgtechnologies.github.io/lp25-dramaconnect/'
  // ...fill the rest as you publish them
};
```
- Buttons with a URL open that site in a new tab.
- Buttons left empty show a friendly “set this URL” reminder (nothing breaks).
- The **Marketing Studio** and its **Flyer** buttons already work because the
  studio is bundled in `studio/`.

## 🚀 Deployment — clear, step-by-step (all free)

### Option A — GitHub Pages (recommended)
1. Create a free account at <https://github.com> → **New repository**
   (e.g. `hmg-connect`, **Public**) → **Create**.
2. **Add file → Upload files**.
3. Drag in **everything inside this `HMG Connect Master` folder** (so
   `index.html` is at the repo root, beside `assets/`, `studio/` and `.nojekyll`).
   **Commit changes**.
4. **Settings → Pages → Source: Deploy from a branch**; branch **main**, folder
   **/(root)**; **Save**.
5. Wait ~1 minute; your live URL appears, e.g.
   `https://<username>.github.io/hmg-connect/`. Share it everywhere.

### Option B — Cloudflare Pages / Vercel (free)
1. Sign up free at <https://pages.cloudflare.com> or <https://vercel.com>.
2. **Create/Import project** and select this folder (or the GitHub repo).
3. Framework preset **None**; build command **(empty)**; output dir **/**;
   **Deploy**. Use the generated `*.pages.dev` / `*.vercel.app` URL.

### Option C — No hosting (instant)
- **Double-click `index.html`** to open it in any browser. The Studio and flyers
  work locally; set generator URLs in `links.js` to enable those buttons.

## ✨ Features
- **One-screen overview** of the whole ecosystem with live stats.
- **10 generator cards** (data-driven in `index.html`) + Suite & Studio cards.
- **Bundled Marketing Studio** for instant flyers/videos/captions.
- **Installable PWA**, offline-capable, fully **preview-safe** (inline styles +
  embedded SVG — no external CSS/JS needed to render).
- **Brand embedding** throughout (WhatsApp +234 810 086 6322 + HMG links) so the
  launchpad itself is a lead-generation channel.

## ➕ Keeping it in sync
When you add a product to the Marketing Studio (`studio/_studio/products.py` →
re-run its scripts), also add a matching card object to the `GENS` array near the
bottom of `index.html`, and a key in `assets/js/links.js`. That's it.

---
© HMG Concepts. Built by Adewale Samson Adeagbo. Lagos, Nigeria. EdTech · DataTech · FaithTech.

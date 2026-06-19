# -*- coding: utf-8 -*-
"""
Generate all HMG Connect Marketing Studio web assets (flyers, videos, captions,
index, manifest, README). Re-run after editing products.py.
Usage:  python3 _studio/generate.py     (run from the Mathematics/ folder root)
100% free. NO AI API.
"""
import os, json, sys
sys.path.insert(0, os.path.dirname(__file__))
from products import HMG, PRODUCTS, SUITE, ALL

ROOT = "."

def hmg_mark(size=64, fg="#ffffff", bg="rgba(255,255,255,.15)"):
    return ('<svg width="%d" height="%d" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="HMG">'
            '<rect x="2" y="2" width="60" height="60" rx="15" fill="%s"/>'
            '<text x="32" y="39" font-family="Inter,Arial,sans-serif" font-size="22" font-weight="900" fill="%s" text-anchor="middle">HMG</text>'
            '<circle cx="50" cy="15" r="4" fill="#fde047"/></svg>') % (size, size, bg, fg)

STUDIO_CSS = """
:root{--ink:#0f172a;--muted:#64748b;--bg:#f1f5f9;--card:#fff;--border:#e2e8f0;--brand:#4f46e5}
*{box-sizing:border-box}
body{margin:0;font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--ink);line-height:1.5}
a{color:var(--brand);text-decoration:none}
.container{max-width:1080px;margin:0 auto;padding:0 20px}
.topbar{background:#fff;border-bottom:1px solid var(--border);position:sticky;top:0;z-index:40}
.topbar .container{display:flex;align-items:center;justify-content:space-between;height:64px}
.brandmark{display:flex;align-items:center;gap:10px;font-weight:800;color:var(--ink)}
.brandmark svg{height:34px;width:34px;border-radius:8px}
.btn{display:inline-flex;align-items:center;gap:8px;border:none;border-radius:11px;padding:11px 20px;font-weight:700;cursor:pointer;font-size:15px}
.btn-primary{background:var(--brand);color:#fff}.btn-ghost{background:#fff;color:var(--brand);border:1px solid var(--border)}
.hero{background:linear-gradient(135deg,#4f46e5,#7c3aed 55%,#0ea5e9);color:#fff;padding:60px 0 70px;text-align:center}
.hero h1{font-size:clamp(28px,5vw,46px);margin:0 0 14px;font-weight:900;letter-spacing:-.5px}
.hero p{font-size:18px;opacity:.95;max-width:720px;margin:0 auto}
.badge{display:inline-block;background:rgba(255,255,255,.18);padding:5px 14px;border-radius:999px;font-size:13px;font-weight:700;margin-bottom:16px}
.grid{display:grid;gap:20px}
.cards{grid-template-columns:repeat(3,1fr)}
@media(max-width:900px){.cards{grid-template-columns:1fr 1fr}}
@media(max-width:620px){.cards{grid-template-columns:1fr}}
.pcard{background:var(--card);border:1px solid var(--border);border-radius:18px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.05);transition:.15s;display:flex;flex-direction:column}
.pcard:hover{transform:translateY(-4px);box-shadow:0 12px 30px rgba(0,0,0,.10)}
.pcard .top{padding:26px 20px;color:#fff;text-align:center}
.pcard .top .ic{font-size:34px}
.pcard .top h2{margin:8px 0 2px;font-size:20px;font-weight:800}
.pcard .top .tag{opacity:.92;font-size:12px}
.pcard .body{padding:18px 20px;display:flex;flex-direction:column;flex:1}
.pcard .body p{color:var(--muted);font-size:14px;margin:0 0 14px}
.pcard .cta{margin-top:auto;display:flex;gap:8px;flex-wrap:wrap}
.pcard .cta a{flex:1;justify-content:center;font-size:13px;padding:9px 10px}
.section{margin-top:56px}
.section-title{font-size:28px;font-weight:900;text-align:center;margin:0 0 6px}
.section-sub{color:var(--muted);text-align:center;max-width:640px;margin:0 auto 28px}
.foot{background:#0f172a;color:#cbd5e1;text-align:center;padding:36px 0;margin-top:60px}
.foot a{color:#a5b4fc}
.linkrow{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:10px}
.note{background:#eef2ff;border:1px solid #c7d2fe;border-radius:14px;padding:16px 18px;color:#3730a3;font-size:14px}
.gallery{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
@media(max-width:620px){.gallery{grid-template-columns:1fr}}
.gallery img{width:100%;border-radius:12px;border:1px solid var(--border);display:block}
"""

def make_flyer(p):
    feats = "".join(
        '<div class="f-item"><div class="f-tick">&#10003;</div><div><b>%s</b><span>%s</span></div></div>' % (n, d)
        for n, d in p["features"][:8])
    sectors = " · ".join(p["sectors"])
    ver = ' <span class="ver">%s</span>' % p["version"] if p.get("version") else ""
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(name)s — e-Flyer | %(hname)s</title>
<meta name="description" content="%(name)s by %(hname)s: %(tag)s">
<style>
*{box-sizing:border-box}
body{margin:0;font-family:'Inter','Segoe UI',Arial,sans-serif;background:#334155;color:#0f172a;display:flex;flex-direction:column;align-items:center;padding:20px;gap:16px}
.bar{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}
.bar button{border:none;border-radius:10px;padding:11px 18px;font-weight:700;font-size:14px;cursor:pointer;background:#fff;color:#1e293b;box-shadow:0 2px 8px rgba(0,0,0,.2)}
.bar button.pri{background:%(c1)s;color:#fff}
.flyer{width:794px;max-width:100%%;background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.35)}
.f-hero{background:linear-gradient(135deg,%(c1)s,%(c2)s);color:#fff;padding:40px 44px;position:relative;overflow:hidden}
.f-hero::after{content:"";position:absolute;right:-60px;top:-60px;width:240px;height:240px;border-radius:50%%;background:rgba(255,255,255,.08)}
.f-hero::before{content:"";position:absolute;left:-40px;bottom:-80px;width:200px;height:200px;border-radius:50%%;background:rgba(255,255,255,.06)}
.f-top{display:flex;align-items:center;gap:12px;position:relative;z-index:2}
.f-top .brand{font-weight:800;font-size:15px}.f-top .brand small{display:block;opacity:.85;font-weight:500;font-size:11px}
.f-eyebrow{display:inline-block;background:rgba(255,255,255,.18);padding:5px 13px;border-radius:999px;font-size:12px;font-weight:700;margin:22px 0 12px;position:relative;z-index:2}
.f-title{font-size:46px;line-height:1.04;font-weight:900;margin:0;position:relative;z-index:2;letter-spacing:-1px}
.f-title .ver{font-size:16px;vertical-align:middle;background:rgba(255,255,255,.25);padding:3px 10px;border-radius:999px}
.f-sub{font-size:18px;opacity:.96;margin:12px 0 0;position:relative;z-index:2;max-width:560px}
.f-icon{position:absolute;right:40px;bottom:24px;font-size:96px;opacity:.9;z-index:2}
.f-body{padding:30px 44px 18px}
.f-prob{background:#fff7ed;border-left:4px solid %(accent)s;border-radius:10px;padding:13px 16px;font-weight:600;color:#92400e;margin:0 0 20px}
.f-grid{display:grid;grid-template-columns:1fr 1fr;gap:13px 22px}
.f-item{display:flex;gap:10px;align-items:flex-start}
.f-tick{flex-shrink:0;width:22px;height:22px;border-radius:50%%;background:%(c1)s;color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:900;margin-top:2px}
.f-item b{display:block;font-size:14px}.f-item span{display:block;font-size:12px;color:#64748b;line-height:1.35}
.f-why{display:flex;gap:10px;flex-wrap:wrap;margin:24px 0 6px}
.f-why div{flex:1;min-width:150px;background:#f1f5f9;border-radius:12px;padding:14px;text-align:center}
.f-why b{display:block;font-size:22px;color:%(c1)s;font-weight:900}.f-why span{font-size:12px;color:#64748b}
.f-sectors{margin-top:18px;font-size:13px;color:#475569}.f-sectors b{color:#0f172a}
.f-cta{background:#0f172a;color:#fff;padding:26px 44px;display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap}
.f-cta .big{font-size:22px;font-weight:900}.f-cta .small{font-size:13px;opacity:.85;margin-top:3px}
.f-cta .pill{background:%(c1)s;color:#fff;padding:11px 20px;border-radius:10px;font-weight:800;font-size:14px}
.f-foot{background:#0b1220;color:#94a3b8;text-align:center;font-size:11px;padding:12px}.f-foot b{color:#cbd5e1}
@media print{body{background:#fff;padding:0}.bar{display:none}.flyer{box-shadow:none;border-radius:0;width:100%%}@page{size:A4;margin:0}}
</style></head><body>
<div class="bar">
  <button class="pri" onclick="window.print()">&#128424;&#65039; Print / Save as PDF</button>
  <button onclick="downloadPNG()">&#11015;&#65039; Download as PNG</button>
  <a href="../index.html" style="text-decoration:none"><button>&larr; Back to Studio</button></a>
</div>
<div class="flyer" id="flyer">
  <div class="f-hero">
    <div class="f-top">%(mark)s<div class="brand">%(hname)s<small>%(htag)s</small></div></div>
    <span class="f-eyebrow">FOR %(forup)s</span>
    <h1 class="f-title">%(name)s%(ver)s</h1>
    <p class="f-sub">%(tag)s</p>
    <div class="f-icon">%(icon)s</div>
  </div>
  <div class="f-body">
    <p class="f-prob">&#10067; %(problem)s</p>
    <div class="f-grid">%(feats)s</div>
    <div class="f-why">
      <div><b>&#8358;0</b><span>Monthly software cost</span></div>
      <div><b>Minutes</b><span>To launch, not months</span></div>
      <div><b>100%%</b><span>You own your data</span></div>
      <div><b>No AI</b><span>API fees — ever</span></div>
    </div>
    <p class="f-sectors"><b>Perfect for:</b> %(sectors)s</p>
  </div>
  <div class="f-cta">
    <div><div class="big">Ready when you are &#128073;</div><div class="small">Send us your details &amp; we build &amp; deploy your platform — free tools, you own it.</div></div>
    <div style="text-align:right"><div class="pill">&#128241; %(wa)s</div><div class="small" style="margin-top:6px">%(siteplain)s</div></div>
  </div>
  <div class="f-foot">A product of <b>%(hname)s</b> (%(hfull)s) · %(htag)s · %(city)s · Built on free tools (Supabase + static hosting) · <b>No AI API</b></div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script>
function downloadPNG(){
  var el=document.getElementById('flyer');
  if(typeof html2canvas==='undefined'){alert('PNG export needs internet (it loads a small free library). Use "Print / Save as PDF" offline instead.');return;}
  html2canvas(el,{scale:2,backgroundColor:'#ffffff'}).then(function(c){var a=document.createElement('a');a.href=c.toDataURL('image/png');a.download='%(key)s-connect-flyer.png';a.click();});
}
</script></body></html>""" % {
        "name": p["name"], "hname": HMG["name"], "tag": p["tagline"], "c1": p["c1"], "c2": p["c2"],
        "accent": p["accent"], "mark": hmg_mark(44), "htag": HMG["tagline"], "forup": p["for"].upper(),
        "ver": ver, "icon": p["icon"], "problem": p["problem"], "feats": feats, "sectors": sectors,
        "wa": HMG["waText"], "siteplain": HMG["site"].replace("https://", ""), "hfull": HMG["full"], "city": HMG["city"],
        "key": p["key"],
    }

def make_video(p):
    feats_js = json.dumps([n for n, d in p["features"][:6]])
    sectors_js = json.dumps(p["sectors"])
    ver = p.get("version", "")
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(name)s — Advert Video | %(hname)s</title>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:'Inter','Segoe UI',Arial,sans-serif;background:#0b1120;color:#e2e8f0;display:flex;flex-direction:column;align-items:center;padding:18px;gap:14px}
h1{font-size:18px;margin:4px 0 0}.muted{color:#94a3b8;font-size:13px;text-align:center;max-width:640px}
.stage{width:100%%;max-width:720px;aspect-ratio:16/9;border-radius:14px;overflow:hidden;box-shadow:0 18px 50px rgba(0,0,0,.55);background:#000}
canvas{width:100%%;height:100%%;display:block}
.bar{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}
.bar button{border:none;border-radius:10px;padding:11px 18px;font-weight:700;font-size:14px;cursor:pointer;background:#1e293b;color:#e2e8f0}
.bar button.pri{background:%(c1)s;color:#fff}.bar button:disabled{opacity:.5;cursor:not-allowed}.bar a{text-decoration:none}
.status{font-size:12px;color:#94a3b8;min-height:16px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%%;background:#ef4444;margin-right:6px;animation:bl 1s infinite}@keyframes bl{50%%{opacity:.2}}
.tips{background:#111827;border:1px solid #1f2937;border-radius:12px;padding:14px 16px;max-width:680px;font-size:13px;color:#cbd5e1}.tips b{color:#fff}
</style></head><body>
<h1>%(icon)s %(name)s %(ver)s — Advertisement Video</h1>
<div class="muted">A free, animated 16:9 advert (~%(secs)ss). Press <b>Play</b> to preview, or <b>Record</b> to capture it as a downloadable video file — no AI, no paid tools.</div>
<div class="stage"><canvas id="cv" width="1280" height="720"></canvas></div>
<div class="bar">
  <button class="pri" id="play">&#9654; Play</button>
  <button id="rec">&#9210; Record &amp; Download</button>
  <button id="restart">&#8635; Restart</button>
  <a href="../index.html"><button>&larr; Back to Studio</button></a>
</div>
<div class="status" id="status"></div>
<div class="tips"><b>How to get a video file:</b> click <b>Record &amp; Download</b> — the advert plays once and a <code>.webm</code> file downloads automatically. Post it to WhatsApp Status, Instagram, Facebook &amp; YouTube. To convert to <code>.mp4</code>, use the free <a href="https://cloudconvert.com/webm-to-mp4" target="_blank" style="color:#93c5fd">CloudConvert</a> or offline <a href="https://handbrake.fr/" target="_blank" style="color:#93c5fd">HandBrake</a>. 100%% free — no AI API.</div>
<script>
const CV=document.getElementById('cv'), X=CV.getContext('2d'), W=CV.width, H=CV.height;
const C1="%(c1)s", C2="%(c2)s", ACCENT="%(accent)s";
const NAME="%(name)s", VER="%(ver)s", ICON="%(icon)s", FORWHO="%(forwho)s";
const TAGLINE="%(tag)s", PROBLEM="%(problem)s";
const FEATS=%(feats)s, SECTORS=%(sectors)s;
const BRAND="%(hname)s", WA="%(wa)s", SITE="%(siteplain)s", TAG="%(htag)s";
function lerp(a,b,t){return a+(b-a)*t;}
function clamp(t){return t<0?0:t>1?1:t;}
function ease(t){return t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;}
function rr(x,y,w,h,r){X.beginPath();X.moveTo(x+r,y);X.arcTo(x+w,y,x+w,y+h,r);X.arcTo(x+w,y+h,x,y+h,r);X.arcTo(x,y+h,x,y,r);X.arcTo(x,y,x+w,y,r);X.closePath();}
function bg(){const g=X.createLinearGradient(0,0,W,H);g.addColorStop(0,C1);g.addColorStop(1,C2);X.fillStyle=g;X.fillRect(0,0,W,H);
  X.globalAlpha=.07;X.fillStyle="#fff";X.beginPath();X.arc(W-120,120,260,0,7);X.fill();X.beginPath();X.arc(80,H-60,200,0,7);X.fill();X.globalAlpha=1;}
function chip(txt,cx,cy){X.font="600 26px Inter,Arial";const w=X.measureText(txt).width+44;X.fillStyle="rgba(255,255,255,.18)";rr(cx-w/2,cy-22,w,44,22);X.fill();X.fillStyle="#fff";X.textAlign="center";X.textBaseline="middle";X.fillText(txt,cx,cy+1);}
function logoMark(cx,cy,s){X.fillStyle="rgba(255,255,255,.16)";rr(cx-s/2,cy-s/2,s,s,s*0.24);X.fill();X.fillStyle="#fff";X.font="900 "+(s*0.34)+"px Inter,Arial";X.textAlign="center";X.textBaseline="middle";X.fillText("HMG",cx,cy+s*0.02);X.fillStyle=ACCENT;X.beginPath();X.arc(cx+s*0.3,cy-s*0.32,s*0.07,0,7);X.fill();}
const SCENES=[{t:3.2,draw:sceneIntro},{t:3.0,draw:sceneProblem},{t:6.0,draw:sceneFeatures},{t:3.0,draw:sceneWhy},{t:2.8,draw:sceneSectors},{t:3.5,draw:sceneCTA}];
const TOTAL=SCENES.reduce((a,s)=>a+s.t,0);
function frame(time){let acc=0;for(const s of SCENES){if(time<acc+s.t){s.draw((time-acc)/s.t);return;}acc+=s.t;}SCENES[SCENES.length-1].draw(1);}
function sceneIntro(t){bg();const a=ease(clamp(t*2));logoMark(W/2,H/2-150,140*a);X.globalAlpha=clamp(t*1.6);X.fillStyle="#fff";X.textAlign="center";X.textBaseline="middle";X.font="900 "+lerp(40,84,a)+"px Inter,Arial";X.fillText(NAME,W/2,H/2+10);if(VER){chip(VER.toUpperCase(),W/2,H/2+70);}X.font="500 30px Inter,Arial";X.fillStyle="rgba(255,255,255,.92)";X.fillText(FORWHO,W/2,H/2+(VER?140:110));X.globalAlpha=1;footer();}
function sceneProblem(t){bg();const a=ease(clamp(t*1.5));X.globalAlpha=a;X.textAlign="center";X.textBaseline="middle";X.font="900 120px Inter,Arial";X.fillText("?",W/2,H/2-120);X.fillStyle="#fff";X.font="700 40px Inter,Arial";wrap(PROBLEM,W/2,H/2+10,W-260,52);X.globalAlpha=1;footer();}
function sceneFeatures(t){bg();X.fillStyle="#fff";X.textAlign="left";X.textBaseline="alphabetic";X.font="800 46px Inter,Arial";X.fillText("What you get",110,140);const n=FEATS.length;for(let i=0;i<n;i++){const start=i/(n+1);const a=ease(clamp((t-start)*4));if(a<=0)continue;const y=210+i*78;const x=110+(1-a)*40;X.globalAlpha=a;X.fillStyle=ACCENT;X.beginPath();X.arc(x+18,y-10,20,0,7);X.fill();X.fillStyle=C2;X.font="900 22px Inter,Arial";X.textAlign="center";X.fillText("\\u2713",x+18,y-2);X.fillStyle="#fff";X.font="600 34px Inter,Arial";X.textAlign="left";X.fillText(FEATS[i],x+56,y);X.globalAlpha=1;}footer();}
function sceneWhy(t){bg();const a=ease(clamp(t*1.4));const items=[["\\u20A60","Monthly cost"],["Minutes","To go live"],["100%%","You own data"],["No AI","API fees"]];X.textAlign="center";X.textBaseline="middle";X.globalAlpha=a;X.fillStyle="#fff";X.font="800 46px Inter,Arial";X.fillText("Why HMG Connect?",W/2,120);const cw=250,gap=30,tot=items.length*cw+(items.length-1)*gap,sx=(W-tot)/2;items.forEach((it,i)=>{const d=ease(clamp((t-i*0.12)*2.2));if(d<=0)return;const x=sx+i*(cw+gap);X.globalAlpha=d;X.fillStyle="rgba(255,255,255,.14)";rr(x,H/2-90,cw,200,20);X.fill();X.fillStyle=ACCENT;X.font="900 54px Inter,Arial";X.fillText(it[0],x+cw/2,H/2-10);X.fillStyle="#fff";X.font="500 26px Inter,Arial";X.fillText(it[1],x+cw/2,H/2+55);X.globalAlpha=1;});X.globalAlpha=1;footer();}
function sceneSectors(t){bg();const a=ease(clamp(t*1.5));X.textAlign="center";X.textBaseline="middle";X.globalAlpha=a;X.fillStyle="#fff";X.font="800 46px Inter,Arial";X.fillText("Perfect for",W/2,130);SECTORS.forEach((s,i)=>{const d=ease(clamp((t-i*0.1)*2.4));if(d<=0)return;X.globalAlpha=d;chip(s,W/2,230+i*72);X.globalAlpha=1;});X.globalAlpha=1;footer();}
function sceneCTA(t){bg();const a=ease(clamp(t*1.6));logoMark(W/2,150,110*a);X.globalAlpha=clamp(t*1.6);X.textAlign="center";X.textBaseline="middle";X.fillStyle="#fff";X.font="900 56px Inter,Arial";X.fillText("Ready when you are.",W/2,330);X.font="500 30px Inter,Arial";X.fillStyle="rgba(255,255,255,.95)";wrap("Send us your details and we build & deploy your platform — free tools, you own it.",W/2,400,W-300,42);const pulse=1+0.04*Math.sin(t*18);X.save();X.translate(W/2,540);X.scale(pulse,pulse);X.fillStyle="#fff";rr(-260,-40,520,80,40);X.fill();X.fillStyle=C2;X.font="800 34px Inter,Arial";X.fillText("\\u260E "+WA,0,2);X.restore();X.fillStyle="rgba(255,255,255,.9)";X.font="600 26px Inter,Arial";X.fillText(SITE,W/2,620);X.globalAlpha=1;footer();}
function footer(){X.textAlign="center";X.textBaseline="middle";X.fillStyle="rgba(255,255,255,.8)";X.font="500 20px Inter,Arial";X.fillText(BRAND+" \\u00B7 "+TAG,W/2,H-34);}
function wrap(txt,cx,cy,maxw,lh){const words=txt.split(' ');let line="",lines=[];for(const w of words){const test=line+w+" ";if(X.measureText(test).width>maxw&&line){lines.push(line);line=w+" ";}else line=test;}lines.push(line);const start=cy-(lines.length-1)*lh/2;lines.forEach((l,i)=>X.fillText(l.trim(),cx,start+i*lh));}
let raf=null,startT=0,recording=false,recorder=null,chunks=[];const statusEl=document.getElementById('status');
function renderAt(sec){frame(Math.min(sec,TOTAL-0.001));}
function loop(now){if(!startT)startT=now;const sec=(now-startT)/1000;renderAt(sec);if(sec>=TOTAL){if(recording)stopRec();else{cancelAnimationFrame(raf);raf=null;}return;}raf=requestAnimationFrame(loop);}
function play(){cancelAnimationFrame(raf);startT=0;raf=requestAnimationFrame(loop);}
function restart(){play();}
renderAt(0.01);
document.getElementById('play').onclick=play;
document.getElementById('restart').onclick=restart;
document.getElementById('rec').onclick=function(){if(recording)return;if(!CV.captureStream){alert('Your browser cannot record canvas video. Use Chrome, Edge or Firefox (all free).');return;}let mime='video/webm;codecs=vp9';if(!MediaRecorder.isTypeSupported(mime))mime='video/webm';const stream=CV.captureStream(30);try{recorder=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:6000000});}catch(e){alert('Recording not supported: '+e.message);return;}chunks=[];recorder.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};recorder.onstop=function(){const blob=new Blob(chunks,{type:'video/webm'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='%(key)s-connect-advert.webm';a.click();statusEl.textContent='Saved %(key)s-connect-advert.webm ('+(blob.size/1048576).toFixed(1)+' MB). Convert to MP4 free if needed.';};recording=true;recorder.start();statusEl.innerHTML='<span class="dot"></span>Recording... the advert plays once; the file downloads when it finishes.';document.getElementById('rec').disabled=true;play();};
function stopRec(){if(recorder&&recorder.state!=='inactive')recorder.stop();recording=false;document.getElementById('rec').disabled=false;cancelAnimationFrame(raf);raf=null;}
</script></body></html>""" % {
        "name": p["name"], "hname": HMG["name"], "secs": p.get("secs", 21), "icon": p["icon"], "ver": ver,
        "c1": p["c1"], "c2": p["c2"], "accent": p["accent"], "forwho": p["for"], "tag": p["tagline"],
        "problem": p["problem"], "feats": feats_js, "sectors": sectors_js, "wa": HMG["waText"],
        "siteplain": HMG["site"].replace("https://", ""), "htag": HMG["tagline"], "key": p["key"],
    }

def make_captions(p):
    feats = "\n".join("   [+] %s - %s" % (n, d) for n, d in p["features"][:8])
    sectors = ", ".join(p["sectors"])
    name = p["name"] + ((" " + p["version"]) if p.get("version") else "")
    sp = HMG["site"].replace("https://", "")
    K = p["key"].capitalize()
    return """============================================================
%(name)s - SOCIAL MEDIA CAPTION KIT
Created with the HMG Connect Marketing Studio (free, no AI API).
Paste straight into WhatsApp / Instagram / Facebook / X / LinkedIn.
============================================================

--- SHORT (WhatsApp Status / X) ---
%(icon)s %(name)s by %(hname)s
%(tag)s
N0/month - You own your data - Ready in minutes.
Chat: %(wa)s  |  %(sp)s

--- MEDIUM (Instagram / Facebook) ---
%(icon)s Meet %(name)s - for %(forl)s.

%(problem)s
There is a better, FREE way. %(tag)s

What you get:
%(feats)s

Built on free tools (Supabase + static hosting). No monthly licence. No AI API fees. You own 100%% of your data.

Perfect for: %(sectors)s.

Ready when you are - send us your details and we build & deploy it for you.
WhatsApp: %(wa)s
Web: %(sp)s
#HMGConcepts #%(K)sConnect #EdTech #DataTech #NoCode

--- LONG (LinkedIn / Blog) ---
Most %(forl)s are paying for software that still doesn't fit how they work - or managing everything on paper and WhatsApp.

%(name)s changes that. It's a complete, modern management platform you can launch in minutes and run for free:
%(feats)s

Why it's different:
- N0 monthly software cost - built on the free Supabase tier + free static hosting.
- No AI API anywhere - deliberately, because it is not cost effective.
- Secure by design - Supabase Auth + Row Level Security, with an admin approval workflow.
- You own everything - the code and the data are yours.

We can build, brand and deploy it for you once you share your details - or self-deploy with our step-by-step guide.

A product of %(hname)s (%(hfull)s), %(htag)s, %(city)s.
%(wa)s  -  %(sp)s

--- HASHTAGS ---
#HMGConcepts #%(K)sConnect #EdTech #DataTech #FaithTech #NoCode #Supabase #SmallBusinessTools #DigitalTransformation #Nigeria #Lagos
""" % {
        "name": name, "icon": p["icon"], "hname": HMG["name"], "tag": p["tagline"], "wa": HMG["waText"],
        "sp": sp, "forl": p["for"].lower(), "problem": p["problem"], "feats": feats, "sectors": sectors,
        "K": K, "hfull": HMG["full"], "htag": HMG["tagline"], "city": HMG["city"],
    }

def make_index():
    cards = ""
    for p in ALL:
        ver = ' <span style="font-size:11px;background:rgba(255,255,255,.25);padding:1px 7px;border-radius:999px">%s</span>' % p["version"] if p.get("version") else ""
        cards += """
      <div class="pcard">
        <div class="top" style="background:linear-gradient(135deg,%s,%s)">
          <div class="ic">%s</div><h2>%s%s</h2><div class="tag">%s</div>
        </div>
        <div class="body">
          <p>%s</p>
          <div class="cta">
            <a class="btn btn-ghost" href="flyers/%s-connect-flyer.html">&#128444;&#65039; e-Flyer</a>
            <a class="btn btn-primary" href="videos/%s-connect-video.html">&#127916; Advert Video</a>
          </div>
          <div class="cta" style="margin-top:8px">
            <a class="btn btn-ghost" href="captions/%s-connect-captions.txt" style="flex:1;justify-content:center">&#128221; Caption Kit</a>
          </div>
          <div class="cta" style="margin-top:8px">
            <a class="btn btn-ghost" href="exports/%s-connect-advert.mp4" download style="flex:1;justify-content:center">&#11015;&#65039; MP4</a>
            <a class="btn btn-ghost" href="exports/%s-connect-flyer.png" download style="flex:1;justify-content:center">&#11015;&#65039; PNG</a>
          </div>
        </div>
      </div>""" % (p["c1"], p["c2"], p["icon"], p["name"], ver, p["for"], p["tagline"], p["key"], p["key"], p["key"], p["key"], p["key"])
    gallery = "".join(
        '<a href="exports/%s-connect-flyer.png" target="_blank"><img src="exports/%s-connect-flyer.png" alt="%s flyer" loading="lazy"></a>' % (p["key"], p["key"], p["name"])
        for p in ALL)
    links = " &middot;\n      ".join([
        '<a href="%s" target="_blank">HMG Concepts</a>' % HMG["site"],
        '<a href="https://hmgacademy.pages.dev" target="_blank">Academy</a>',
        '<a href="https://hmgmedia.pages.dev" target="_blank">Media</a>',
        '<a href="https://hmggospel.pages.dev" target="_blank">Gospel</a>',
        '<a href="%s" target="_blank">%s</a>' % (HMG["builder"], HMG["founder"]),
        '<a href="%s" target="_blank">WhatsApp</a>' % HMG["wa"],
    ])
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HMG Connect — Marketing Studio (Flyers &amp; Advert Videos)</title>
<meta name="description" content="Free e-flyers and advertisement videos for the HMG Connect Suite: School, Church, Business, Clinic, Hotel, Estate, Gym & Drama. By HMG Concepts. No AI API.">
<meta name="theme-color" content="#4f46e5"><link rel="icon" href="assets/img/logo.png"><link rel="manifest" href="manifest.json">
<style>%(css)s</style></head><body>
<div class="topbar"><div class="container">
  <a class="brandmark" href="index.html">%(mark)s HMG Connect Studio</a>
  <a class="btn btn-primary" href="%(wa)s" target="_blank" style="padding:9px 16px">&#128241; Talk to us</a>
</div></div>
<div class="hero"><div class="container">
  <span class="badge">Marketing Studio &middot; by %(hname)s &middot; %(htag)s</span>
  <h1>Flyers &amp; Advert Videos for Every Connect Product</h1>
  <p>Create awareness that we can build complete management platforms for clients the moment they're ready. Each product has a ready-to-share <b>e-flyer</b>, an animated <b>advertisement video</b> you can record &amp; download, and a <b>caption kit</b>. 100%% free tools — <b>no AI API</b>.</p>
</div></div>
<div class="container section">
  <h2 class="section-title">Pick a Product</h2>
  <p class="section-sub">Each card opens self-contained, deployable assets. Flyers print to PDF or export to PNG; videos record to a downloadable file you can post anywhere.</p>
  <div class="grid cards">%(cards)s
  </div>
</div>
<div class="container section">
  <h2 class="section-title">Ready-Made Downloads</h2>
  <p class="section-sub">Pre-rendered <b>PNG flyers</b>, <b>MP4 adverts</b> (H.264, ~21s) and looping <b>GIF adverts</b> live in <code>exports/</code> — click a flyer to open full size, or use the <b>MP4 / PNG</b> buttons on each product card above to download and share immediately. No browser recording needed.</p>
  <div class="gallery">%(gallery)s</div>
</div>
<div class="container section">
  <h2 class="section-title">How to Use These Assets</h2>
  <div class="grid cards">
    <div class="pcard"><div class="body"><h3 style="margin:0 0 8px">&#128444;&#65039; e-Flyers</h3><p>Open a flyer and click <b>Print / Save as PDF</b> (offline) or <b>Download as PNG</b>. Ready-made PNGs are also in <code>exports/</code>. Share on WhatsApp, print, or email.</p></div></div>
    <div class="pcard"><div class="body"><h3 style="margin:0 0 8px">&#127916; Advert Videos</h3><p>Open a video, click <b>Record &amp; Download</b> for a <code>.webm</code> file. Pre-rendered animated <b>GIF</b> adverts are in <code>exports/</code> for instant sharing. Convert to MP4 free if needed.</p></div></div>
    <div class="pcard"><div class="body"><h3 style="margin:0 0 8px">&#128221; Caption Kits</h3><p>Short, medium &amp; long captions plus hashtags — copy &amp; paste, no writing needed.</p></div></div>
  </div>
  <div class="note section" style="margin-top:28px"><b>Why no AI?</b> Every asset here is generated with free, native technology (HTML, Canvas, MediaRecorder, Python/Pillow) — deliberately avoiding paid AI APIs because they are not cost effective. You can run, edit and host all of this for N0.</div>
</div>
<div class="foot"><div class="container">
  %(markfoot)s
  <p style="margin:10px 0 4px">The <b style="color:#fff">HMG Connect Marketing Studio</b> is a product of <b style="color:#fff">%(hname)s</b> — %(hfull)s.<br>%(htag)s &middot; Founded %(since)s &middot; %(city)s.</p>
  <div class="linkrow">%(links)s</div>
</div></div>
</body></html>""" % {
        "css": STUDIO_CSS, "mark": hmg_mark(34, "#4f46e5", "#eef2ff"), "wa": HMG["wa"], "hname": HMG["name"],
        "htag": HMG["tagline"], "cards": cards, "gallery": gallery, "markfoot": hmg_mark(40, "#fff", "rgba(255,255,255,.12)"),
        "hfull": HMG["full"], "since": HMG["since"], "city": HMG["city"], "links": links,
    }

def write():
    for d in ["flyers", "videos", "captions"]:
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
    for p in ALL:
        open("%s/flyers/%s-connect-flyer.html" % (ROOT, p["key"]), "w").write(make_flyer(p))
        open("%s/videos/%s-connect-video.html" % (ROOT, p["key"]), "w").write(make_video(p))
        open("%s/captions/%s-connect-captions.txt" % (ROOT, p["key"]), "w").write(make_captions(p))
    open("%s/index.html" % ROOT, "w").write(make_index())
    open("%s/manifest.json" % ROOT, "w").write(json.dumps({
        "name": "HMG Connect Marketing Studio", "short_name": "HMG Studio", "start_url": "./index.html",
        "display": "standalone", "background_color": "#ffffff", "theme_color": "#4f46e5",
        "icons": [{"src": "assets/img/logo.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]
    }, indent=2))
    print("Generated web assets for %d products." % len(ALL))

if __name__ == "__main__":
    write()

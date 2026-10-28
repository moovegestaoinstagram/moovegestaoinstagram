"""Gera as artes do Instagram da Moove a partir de um JSON de post.

Uso:  python3 kit/render.py posts/AAAA-MM-DD-slug.json
Saída: midia/<slug>/NN.png (carrossel 1080x1350) ou midia/<slug>/reel.mp4 + capa.jpg (Reels 1080x1920).

JSON:
{
  "slug": "2026-11-02-planilha",
  "formato": "carrossel" | "reel",
  "segundos_por_cena": 3.5,          # só reel
  "slides": [ {tipo, kicker, titulo, destaque, texto, numero, card, lista, botao, rodape}, ... ]
}
Tipos de slide: capa, gancho, item, solucao, cta.
"destaque" = trecho do título pintado na cor de destaque. "card" aceita <b>.
Requer: playwright (chromium) e ffmpeg.
"""
import json, sys, base64, pathlib, html, subprocess

KIT = pathlib.Path(__file__).resolve().parent
ROOT = KIT.parent

def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()

FONT_CSS = "".join(
    f"@font-face{{font-family:'Open Sans';font-weight:{w};src:url(data:font/woff2;base64,{b64(KIT / 'fonts' / f'open-sans-latin-{w}-normal.woff2')}) format('woff2');}}"
    for w in (400, 600, 700, 800)
)
LOGO_COR = b64(KIT / "logo" / "logo-cor.png")
LOGO_BRANCA = b64(KIT / "logo" / "logo-branca.png")

CSS = """
:root{--teal:#33A6BC;--lime:#9DC129;--ink:#020817;--muted:#4B5768;--bg:#FFFFFF;--soft:#F1F5F9;--ok:#22C55E}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:var(--h);font-family:'Open Sans',sans-serif;overflow:hidden}
.s{width:1080px;height:var(--h);padding:var(--pad) 88px;position:relative;display:flex;flex-direction:column}
.dark{background:var(--ink);color:#fff}
.light{background:var(--bg);color:var(--ink)}
.tealbg{background:var(--teal);color:#fff}
.kicker{font-size:30px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--teal)}
.dark .kicker{color:var(--lime)} .tealbg .kicker{color:#fff;opacity:.85}
h1{font-size:92px;line-height:1.04;font-weight:800;letter-spacing:-.02em;margin-top:28px}
h2{font-size:72px;line-height:1.08;font-weight:800;letter-spacing:-.015em}
p{font-size:40px;line-height:1.38;font-weight:400;margin-top:36px;color:var(--muted)}
.dark p,.tealbg p{color:#E2E8F0}
.hl{color:var(--lime)} .light .hl{color:var(--teal)} .tealbg .hl{color:var(--ink)}
.num{width:132px;height:132px;border-radius:32px;background:var(--teal);color:#fff;font-size:72px;font-weight:800;display:flex;align-items:center;justify-content:center;margin-bottom:56px}
.card{background:var(--soft);border-radius:28px;padding:44px 48px;margin-top:48px;font-size:36px;line-height:1.4;color:var(--ink)}
.card b{color:var(--teal)}
.grow{flex:1;display:flex;flex-direction:column;justify-content:center}
.foot{display:flex;justify-content:space-between;align-items:flex-end}
.foot img{height:44px}
.pager{font-size:26px;font-weight:600;color:var(--muted)} .dark .pager,.tealbg .pager{color:#CBD5E1}
.bar{width:120px;height:12px;border-radius:6px;background:var(--lime);margin-top:44px}
.pill{display:inline-block;background:var(--lime);color:var(--ink);font-weight:800;font-size:40px;border-radius:999px;padding:22px 44px;margin-top:48px}
.list{margin-top:44px;font-size:38px;line-height:1.5}
.list div{padding-left:56px;position:relative;margin-bottom:14px}
.list div:before{content:'✓';position:absolute;left:0;color:var(--lime);font-weight:800}
.light .list div:before{color:var(--ok)} .tealbg .list div:before{color:#fff}
.swipe{font-size:30px;font-weight:700;color:var(--lime)}
"""

def esc(x):
    return html.escape(str(x))

def hl(text, word):
    t = esc(text)
    if word:
        t = t.replace(esc(word), f"<span class='hl'>{esc(word)}</span>", 1)
    return t

def slide_html(s, i, n, reel):
    tipo = s["tipo"]
    theme = s.get("tema") or {"capa": "dark", "cta": "dark", "solucao": "tealbg"}.get(tipo, "light")
    logo = LOGO_COR if theme == "light" else LOGO_BRANCA
    k = f"<div class='kicker'>{esc(s['kicker'])}</div>" if s.get("kicker") else ""
    texto = f"<p>{esc(s['texto'])}</p>" if s.get("texto") else ""
    if tipo == "capa":
        inner = f"{k}<h1>{hl(s['titulo'], s.get('destaque'))}</h1><div class='bar'></div>{texto}"
        rod = "" if reel else "<span class='swipe'>Arraste para o lado →</span>"
    elif tipo == "item":
        card = f"<div class='card'>{s['card']}</div>" if s.get("card") else ""
        inner = f"{k}<div style='height:40px'></div><div class='num'>{esc(s['numero'])}</div><h2>{hl(s['titulo'], s.get('destaque'))}</h2>{texto}{card}"
        rod = "" if reel else f"<span class='pager'>{i}/{n}</span>"
    elif tipo in ("gancho", "solucao"):
        lst = "".join(f"<div>{esc(x)}</div>" for x in s.get("lista", []))
        inner = f"{k}<h2 style='margin-top:28px'>{hl(s['titulo'], s.get('destaque'))}</h2>{texto}" + (f"<div class='list'>{lst}</div>" if lst else "")
        rod = "" if reel else f"<span class='pager'>{i}/{n}</span>"
    elif tipo == "cta":
        botao = f"<div><span class='pill'>{esc(s['botao'])}</span></div>" if s.get("botao") else ""
        inner = f"{k}<h2 style='margin-top:28px'>{hl(s['titulo'], s.get('destaque'))}</h2>{texto}{botao}"
        rod = f"<span class='pager'>{esc(s.get('rodape', 'moovesales.com.br'))}</span>"
    else:
        raise ValueError(f"tipo desconhecido: {tipo}")
    h, pad = (1920, 260) if reel else (1350, 96)
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}{CSS}"
            f":root{{--h:{h}px;--pad:{pad}px}}</style></head><body><div class='s {theme}'>"
            f"<div class='grow'>{inner}</div><div class='foot'>{rod}<img src='data:image/png;base64,{logo}'></div></div></body></html>"), h

def render(spec_path):
    from playwright.sync_api import sync_playwright
    spec = json.loads(pathlib.Path(spec_path).read_text())
    reel = spec.get("formato") == "reel"
    out = ROOT / "midia" / spec["slug"]
    out.mkdir(parents=True, exist_ok=True)
    slides = spec["slides"]; n = len(slides); files = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920 if reel else 1350})
        for i, s in enumerate(slides, 1):
            doc, h = slide_html(s, i, n, reel)
            pg.set_viewport_size({"width": 1080, "height": h})
            pg.set_content(doc); pg.wait_for_timeout(150)
            f = out / f"{i:02d}.png"; pg.screenshot(path=str(f)); files.append(f)
        b.close()
    if not reel:
        # JPEG reduz o peso para o Instagram sem perda visível
        from PIL import Image
        jpgs = []
        for f in files:
            j = f.with_suffix(".jpg"); Image.open(f).convert("RGB").save(j, "JPEG", quality=92); f.unlink(); jpgs.append(j)
        return jpgs
    return [make_reel(files, out, float(spec.get("segundos_por_cena", 3.5)))]

def make_reel(frames, out, dur, fade=0.4):
    """Cenas com leve aproximação (zoom) e transição suave entre elas."""
    fps = 30; inputs = []; filters = []
    for i, f in enumerate(frames):
        inputs += ["-loop", "1", "-t", f"{dur}", "-i", str(f)]
        frames_n = int(dur * fps)
        filters.append(f"[{i}:v]scale=1188:2112,zoompan=z='min(1+0.0009*on,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames_n}:s=1080x1920:fps={fps},setsar=1,format=yuv420p[v{i}]")
    last = "v0"; offset = dur - fade
    for i in range(1, len(frames)):
        filters.append(f"[{last}][v{i}]xfade=transition=fade:duration={fade}:offset={offset:.2f}[x{i}]")
        last = f"x{i}"; offset += dur - fade
    mp4 = out / "reel.mp4"
    cmd = ["ffmpeg", "-y", *inputs, "-f", "lavfi", "-t", f"{offset + fade:.2f}", "-i", "anullsrc=r=44100:cl=stereo",
           "-filter_complex", ";".join(filters), "-map", f"[{last}]", "-map", f"{len(frames)}:a",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(mp4)]
    subprocess.run(cmd, check=True, capture_output=True)
    from PIL import Image
    Image.open(frames[0]).convert("RGB").save(out / "capa.jpg", "JPEG", quality=92)
    for f in frames: f.unlink()
    return mp4

if __name__ == "__main__":
    for f in render(sys.argv[1]):
        print(f.relative_to(ROOT))

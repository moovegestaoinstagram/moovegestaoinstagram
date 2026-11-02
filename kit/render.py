"""Gera as artes do Instagram da Moove a partir de um JSON de post.

Uso:  python3 kit/render.py posts/AAAA-MM-DD-slug.json
Saída: midia/<slug>/NN.jpg (carrossel 1080x1350), midia/<slug>/reel.mp4 + capa.jpg (Reels 1080x1920)
       ou midia/<slug>/NN.jpg (stories 1080x1920, "formato": "stories", "serie": "Nome do destaque").

JSON:
{
  "slug": "2026-11-02-planilha",
  "formato": "carrossel" | "reel",
  "segundos_por_cena": 3.5,          # só reel
  "slides": [ {tipo, kicker, titulo, destaque, texto, numero, card, lista, botao, rodape}, ... ]
}
Tipos de slide: capa, gancho, item, solucao, cta, tela, plano.
plano: {tipo, kicker, titulo (nome do plano), selo, mensal, anual, anual_total, lista}.
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
:root{--teal:#33A6BC;--tealtxt:#16798C;--lime:#9DC129;--ink:#020817;--muted:#4B5768;--bg:#FFFFFF;--soft:#F1F5F9;--ok:#22C55E}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:var(--h);font-family:'Open Sans',sans-serif;overflow:hidden}
.s{width:1080px;height:var(--h);padding:var(--pad) 88px;position:relative;display:flex;flex-direction:column}
.dark{background:var(--ink);color:#fff}
.light{background:var(--bg);color:var(--ink)}
.tealbg{background:var(--teal);color:#fff}
.kicker{font-size:30px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--tealtxt)}
.dark .kicker{color:var(--lime)} .tealbg .kicker{color:#fff;opacity:.85}
h1{font-size:92px;line-height:1.04;font-weight:800;letter-spacing:-.02em;margin-top:28px}
h2{font-size:72px;line-height:1.08;font-weight:800;letter-spacing:-.015em}
p{font-size:40px;line-height:1.38;font-weight:400;margin-top:36px;color:var(--muted)}
.dark p,.tealbg p{color:#E2E8F0}
.hl{color:var(--lime)} .light .hl{color:var(--tealtxt)} .tealbg .hl{color:var(--ink)}
.num{width:132px;height:132px;border-radius:32px;background:var(--tealtxt);color:#fff;font-size:72px;font-weight:800;display:flex;align-items:center;justify-content:center;margin-bottom:56px}
.card{background:var(--soft);border-radius:28px;padding:44px 48px;margin-top:48px;font-size:36px;line-height:1.4;color:var(--ink)}
.card b{color:var(--tealtxt)}
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
.tela-wrap{flex:1;display:flex;flex-direction:column}
.tela-wrap h2{font-size:62px;margin-top:22px}
.tela-wrap p{font-size:36px;margin-top:22px}
.device{flex:1;display:flex;align-items:center;justify-content:center;margin-top:40px}
.notebook{width:100%}
.notebook .screen{background:#0F172A;border-radius:22px;padding:14px;box-shadow:0 30px 60px rgba(2,8,23,.18)}
.notebook .screen img{display:block;width:100%;border-radius:10px}
.notebook .base{height:18px;margin:0 -28px;background:#CBD5E1;border-radius:0 0 18px 18px}
.dark .notebook .base,.tealbg .notebook .base{background:#475569}
.phone{background:#0F172A;border-radius:56px;padding:16px;box-shadow:0 30px 60px rgba(2,8,23,.22)}
.phone img{display:block;border-radius:42px}
.zoom{width:100%;background:#fff;border-radius:24px;padding:10px;box-shadow:0 30px 60px rgba(2,8,23,.18);border:3px solid var(--teal)}
.zoom img{display:block;width:100%;border-radius:16px}
.fwrap{position:relative;overflow:hidden;border-radius:16px}
.foco{position:absolute;border:7px solid var(--lime);border-radius:18px;box-shadow:0 0 0 9999px rgba(2,8,23,.28)}
.dark .zoom{border-color:var(--lime)}
.b0 .grow p,.b0 .device,.b0 .list,.b0 .card,.b0 .pill,.b0 .preco,.b0 .anual,.b1 .device,.b1 .list,.b1 .card,.b1 .pill{opacity:0}
.story-top{position:absolute;top:150px;left:88px;right:88px;display:flex;justify-content:space-between;font-size:28px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.dark .story-top,.tealbg .story-top{color:#CBD5E1}
.tap{font-size:30px;font-weight:700;color:var(--tealtxt)} .dark .tap{color:var(--lime)} .tealbg .tap{color:#fff}
.selo{display:inline-block;background:var(--lime);color:var(--ink);font-size:28px;font-weight:800;border-radius:999px;padding:10px 28px;margin-top:28px;text-transform:uppercase;letter-spacing:.05em}
.preco{font-size:110px;font-weight:800;letter-spacing:-.03em;margin-top:44px;line-height:1}
.preco small{font-size:40px;font-weight:700;letter-spacing:0}
.anual{background:var(--soft);border-radius:28px;padding:36px 44px;margin-top:40px;font-size:36px;line-height:1.4;color:var(--ink)}
.anual b{color:var(--tealtxt)}
"""

def tela_src(nome, recorte=None):
    """Data URI da tela; recorte = [x0, y0, x1, y1] em frações amplia um trecho."""
    from PIL import Image
    import io
    im = Image.open(KIT / "telas" / nome).convert("RGB")
    if recorte:
        w, h = im.size
        x0, y0, x1, y1 = recorte
        im = im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
    buf = io.BytesIO(); im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), im.size

def esc(x):
    return html.escape(str(x))

def hl(text, word):
    t = esc(text)
    if word:
        t = t.replace(esc(word), f"<span class='hl'>{esc(word)}</span>", 1)
    return t

def slide_html(s, i, n, reel, story=None, build=''):
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
    elif tipo == "tela":
        src, (tw, th) = tela_src(s["tela"], s.get("recorte"))
        movel = s["tela"].endswith("-m.webp") and not s.get("recorte")
        foco = ""
        if s.get("foco"):
            x0, y0, x1, y1 = s["foco"]
            foco = f"<div class='foco' style='left:{x0*100}%;top:{y0*100}%;width:{(x1-x0)*100}%;height:{(y1-y0)*100}%'></div>"
        if s.get("recorte"):
            dev = f"<div class='zoom'><div class='fwrap'><img src='{src}'>{foco}</div></div>"
        elif movel:
            ph = (1000 if story is not None else 1180) if reel else 760
            dev = f"<div class='phone'><img src='{src}' style='height:{ph}px'></div>"
        else:
            dev = f"<div class='notebook'><div class='screen'><img src='{src}'></div><div class='base'></div></div>"
        inner = (f"<div class='tela-wrap'>{k}<h2>{hl(s['titulo'], s.get('destaque'))}</h2>{texto}"
                 f"<div class='device'>{dev}</div></div>")
        rod = "" if reel else f"<span class='pager'>{i}/{n}</span>"
    elif tipo == "cta":
        botao = f"<div><span class='pill'>{esc(s['botao'])}</span></div>" if s.get("botao") else ""
        inner = f"{k}<h2 style='margin-top:28px'>{hl(s['titulo'], s.get('destaque'))}</h2>{texto}{botao}"
        rod = f"<span class='pager'>{esc(s.get('rodape', 'moovesales.com.br'))}</span>"
    elif tipo == "plano":
        selo = f"<div><span class='selo'>{esc(s['selo'])}</span></div>" if s.get("selo") else ""
        lst = "".join(f"<div>{esc(x)}</div>" for x in s.get("lista", []))
        inner = (f"{k}<h2 style='margin-top:28px;font-size:96px'>{esc(s['titulo'])}</h2>{selo}"
                 f"<div class='preco'>{esc(s['mensal'])}<small>/mês no mensal</small></div>"
                 f"<div class='anual'>ou <b>{esc(s['anual'])}/mês no plano anual</b><br>({esc(s['anual_total'])}/ano, cobrança anual)</div>"
                 f"<div class='list'>{lst}</div>")
        rod = ""
    else:
        raise ValueError(f"tipo desconhecido: {tipo}")
    if story is not None:
        if tipo != "cta":
            rod = "<span class='tap'>Toque para continuar →</span>"
        pass
    h, pad = (1920, 260) if reel else (1350, 96)
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}{CSS}"
            f":root{{--h:{h}px;--pad:{pad}px}}</style></head><body><div class='s {theme} {build}'>"
            f"<div class='grow'>{inner}</div><div class='foot'>{rod}<img src='data:image/png;base64,{logo}'></div></div></body></html>"), h

def render(spec_path):
    from playwright.sync_api import sync_playwright
    spec = json.loads(pathlib.Path(spec_path).read_text())
    fmt = spec.get("formato")
    story = spec.get("serie", "") if fmt == "stories" else None
    reel = fmt in ("reel", "stories")
    out = ROOT / "midia" / spec["slug"]
    out.mkdir(parents=True, exist_ok=True)
    slides = spec["slides"]; n = len(slides); files = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920 if reel else 1350})
        anim = reel and story is None
        dur = float(spec.get("segundos_por_cena", 3.5))
        for i, s in enumerate(slides, 1):
            estados = [("b0", .30), ("b1", .25), ("", .45)] if anim else [("", 1)]
            for bi, (bc, frac) in enumerate(estados):
                doc, h = slide_html(s, i, n, reel, story, bc)
                pg.set_viewport_size({"width": 1080, "height": h})
                pg.set_content(doc); pg.wait_for_timeout(150)
                f = out / f"{i:02d}{'abc'[bi] if anim else ''}.png"; pg.screenshot(path=str(f))
                files.append((f, dur * frac) if anim else f)
        b.close()
    if story is not None or not reel:
        # JPEG reduz o peso para o Instagram sem perda visível
        from PIL import Image
        jpgs = []
        for f in files:
            j = f.with_suffix(".jpg"); Image.open(f).convert("RGB").save(j, "JPEG", quality=92); f.unlink(); jpgs.append(j)
        return jpgs
    return [make_reel(files, out)]

def make_reel(segs, out, fade=0.22):
    """Cada cena entra em etapas (título, texto, tela/lista) com transições suaves.
    segs = [(png, segundos), ...]."""
    import hashlib
    # remove etapas idênticas à anterior (cena sem texto ou sem tela)
    clean = []
    for f, d in segs:
        hsh = hashlib.md5(f.read_bytes()).hexdigest()
        if clean and clean[-1][2] == hsh:
            clean[-1] = (clean[-1][0], clean[-1][1] + d, hsh); f.unlink()
        else:
            clean.append((f, d, hsh))
    fps = 30; inputs = []; filters = []
    for i, (f, d, _) in enumerate(clean):
        d = max(d, fade * 2 + 0.1)
        inputs += ["-loop", "1", "-t", f"{d:.2f}", "-i", str(f)]
        filters.append(f"[{i}:v]fps={fps},scale=1080:1920,setsar=1,format=yuv420p[v{i}]")
    last = "v0"; offset = max(clean[0][1], fade * 2 + 0.1) - fade
    for i in range(1, len(clean)):
        filters.append(f"[{last}][v{i}]xfade=transition=fade:duration={fade}:offset={offset:.2f}[x{i}]")
        last = f"x{i}"; offset += max(clean[i][1], fade * 2 + 0.1) - fade
    mp4 = out / "reel.mp4"
    cmd = ["ffmpeg", "-y", *inputs, "-f", "lavfi", "-t", f"{offset + fade:.2f}", "-i", "anullsrc=r=44100:cl=stereo",
           "-filter_complex", ";".join(filters), "-map", f"[{last}]", "-map", f"{len(clean)}:a",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(mp4)]
    subprocess.run(cmd, check=True, capture_output=True)
    from PIL import Image
    capa = next((f for f, _, _ in clean if f.name.startswith("01") and f.stem.endswith("c")), clean[0][0])
    first_full = [f for f, _, _ in clean if f.name.startswith("01")][-1]
    Image.open(first_full).convert("RGB").save(out / "capa.jpg", "JPEG", quality=92)
    for f, _, _ in clean: f.unlink()
    return mp4

if __name__ == "__main__":
    for f in render(sys.argv[1]):
        print(f.relative_to(ROOT))

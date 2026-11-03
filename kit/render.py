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
Tipos de slide: capa, gancho, item, solucao, cta, tela, plano + v2: numero, versus, conversa, checklist, enquete, nota, tabela, passos, frase (ver kit/slides.py).
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
LOGO_INK = b64(KIT / "logo" / "logo-ink.png")

CSS = open(KIT / "estilo.css", encoding="utf-8").read()

def tela_src(nome, recorte=None):
    """Data URI da tela; recorte = [x0, y0, x1, y1] em frações amplia um trecho."""
    from PIL import Image
    import io
    im = Image.open(KIT / "telas" / nome).convert("RGB")
    if recorte:
        w, h = im.size
        x0, y0, x1, y1 = recorte
        im = im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))
        if im.size[0] < 1600:  # recorte pequeno: amplia para ocupar a largura do slide
            f = 1600 / im.size[0]
            im = im.resize((1600, int(im.size[1] * f)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), im.size

sys.path.insert(0, str(KIT))
import slides as L  # layouts ficam em kit/slides.py; estilos em kit/estilo.css

def slide_html(s, i, n, reel, story=None, build=''):
    theme, inner, rod, extra = L.corpo(s, i, n, reel, story, tela_src)
    logo = LOGO_INK if theme == "lime" else LOGO_COR if theme in ("light", "mist") else LOGO_BRANCA
    h, pad = (1920, 260) if reel else (1350, 96)
    if story is not None and s["tipo"] != "cta":
        rod = "<span class='tap'>Toque para continuar</span>"
    fmt = "vert" if reel else "feed"
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{FONT_CSS}{CSS}"
            f":root{{--h:{h}px;--pad:{pad}px;--imgmax:{1000 if reel else 560}px}}</style></head><body><div class='s {theme} {fmt} {build}'>"
            f"{extra}<div class='grow'>{inner}</div><div class='foot'>{rod}<img src='data:image/png;base64,{logo}'></div></div></body></html>"), h

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

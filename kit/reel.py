"""Renderiza um Reels feito em HyperFrames (HTML + GSAP -> MP4) com a identidade da Moove.

Uso:  python3 kit/reel.py posts/reels/AAAA-MM-DD-slug [--capa 0.8] [--sem-check]
Entrada: posts/reels/<slug>/index.html (comece copiando kit/reels/base/index.html)
Saída:   midia/<slug>/reel.mp4, midia/<slug>/capa.jpg e posts/reels/<slug>/.revisao/quadros.jpg (para conferir)

O "check" do HyperFrames mede: texto vazando da caixa, contraste, fonte < 28 px e tempo de leitura
(0,5 s + 0,3 s por palavra). Erros bloqueiam o render; avisos são impressos para você decidir.
Tudo roda no container, sem conta e sem custo (HyperFrames é Apache 2.0; telemetria desligada).
"""
import json, os, pathlib, shutil, subprocess, sys

KIT = pathlib.Path(__file__).resolve().parent
ROOT = KIT.parent


def chromium():
    out = subprocess.run(["node", "-e", "console.log(require('playwright').chromium.executablePath())"],
                         capture_output=True, text=True)
    return out.stdout.strip()


def preparar(proj):
    if not (KIT / "node_modules" / "hyperframes").exists():
        subprocess.run(["npm", "install", "--no-audit", "--no-fund", "--silent"], cwd=KIT, check=True)
    a = proj / "assets"
    for sub in ("fonts", "vendor", "img"):
        (a / sub).mkdir(parents=True, exist_ok=True)
    for f in (KIT / "fonts").glob("*.woff2"):
        shutil.copy(f, a / "fonts" / f.name)
    shutil.copy(KIT / "vendor" / "gsap.min.js", a / "vendor" / "gsap.min.js")
    for f in (KIT / "logo").glob("*.png"):
        shutil.copy(f, a / "img" / f.name)
    (proj / ".gitignore").write_text("assets/\n.hyperframes/\n.revisao/\nnode_modules/\n")
    if not (proj / "hyperframes.json").exists():
        (proj / "hyperframes.json").write_text(json.dumps({"name": proj.name}, indent=1))


def env():
    e = dict(os.environ)
    e.update(HYPERFRAMES_TELEMETRY_DISABLED="1", HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1", HYPERFRAMES_SKIP_SKILLS="1",
             HYPERFRAMES_BROWSER_PATH=chromium())
    return e


def hf(*args, cwd):
    return subprocess.run([str(KIT / "node_modules" / ".bin" / "hyperframes"), *args],
                          cwd=cwd, env=env(), capture_output=True, text=True)


def checar(proj):
    r = hf("check", "--json", cwd=proj)
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        print(r.stdout[-2000:], r.stderr[-2000:])
        sys.exit("check do HyperFrames não devolveu JSON")
    erros = []
    for sec in ("lint", "runtime", "layout", "contrast", "craft", "motion"):
        for f in d.get(sec, {}).get("findings", []):
            if f["severity"] == "info" or f.get("code") == "nested_structure_needs_subcomposition":
                continue
            linha = f"[{f['severity']}] {sec}/{f['code']} {f.get('selector','')}: {f.get('message','')[:220]}"
            print(linha)
            if f.get("fixHint"):
                print("    como corrigir:", f["fixHint"][:220])
            if f["severity"] == "error":
                erros.append(linha)
    return erros


def quadros(mp4, destino, dur):
    destino.mkdir(exist_ok=True)
    ts = [0.0] + [round(dur * k / 6, 2) for k in range(1, 6)] + [max(dur - 0.3, 0)]
    from PIL import Image, ImageDraw
    ims = []
    for t in ts:
        f = destino / f"q_{t}.png"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", str(mp4), "-frames:v", "1", str(f)], check=True)
        im = Image.open(f).convert("RGB")
        d = ImageDraw.Draw(im)
        for y in (168, 1330):  # faixa segura do Reels
            d.line([(0, y), (1080, y)], fill=(255, 0, 0), width=5)
        d.text((20, 20), f"{t}s", fill=(255, 0, 0))
        ims.append(im.resize((360, 640)))
    c = Image.new("RGB", (370 * len(ims) + 10, 660), "#888")
    for i, im in enumerate(ims):
        c.paste(im, (10 + i * 370, 10))
    c.save(destino / "quadros.jpg", quality=85)
    return destino / "quadros.jpg"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    proj = (ROOT / sys.argv[1]).resolve() if not pathlib.Path(sys.argv[1]).is_absolute() else pathlib.Path(sys.argv[1])
    capa_t = float(sys.argv[sys.argv.index("--capa") + 1]) if "--capa" in sys.argv else 0.8
    preparar(proj)
    if "--sem-check" not in sys.argv:
        erros = checar(proj)
        if erros:
            sys.exit(f"{len(erros)} erro(s) no check: corrija o index.html e rode de novo.")
    out = ROOT / "midia" / proj.name
    out.mkdir(parents=True, exist_ok=True)
    mp4 = out / "reel.mp4"
    r = hf("render", "--output", str(mp4), cwd=proj)
    if r.returncode != 0 or not mp4.exists():
        print(r.stdout[-3000:], r.stderr[-3000:])
        sys.exit("render falhou")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(capa_t), "-i", str(mp4), "-frames:v", "1",
                    "-q:v", "2", str(out / "capa.jpg")], check=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                               capture_output=True, text=True).stdout.strip())
    q = quadros(mp4, proj / ".revisao", dur)
    print(f"ok: {mp4} ({dur:.1f}s), capa: {out / 'capa.jpg'}, quadros para revisão: {q}")


if __name__ == "__main__":
    main()

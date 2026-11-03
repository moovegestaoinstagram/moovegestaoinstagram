"""Layouts dos slides da Moove (sistema visual v2).

corpo(s, i, n, reel, story, tela_src) -> (tema, html_interno, rodape, extra_de_fundo)

Tipos herdados: capa, gancho, item, solucao, cta, tela, plano.
Tipos novos (v2):
  numero    {numero, unidade, titulo, texto, chips[]}            número grande verificável
  versus    {titulo, antes_titulo, antes[], depois_titulo, depois[]}
  conversa  {titulo, grupo, sub, mensagens:[{de, texto, hora, eu}]}  conversa ILUSTRATIVA (nomes fictícios)
  checklist {titulo, itens[], texto}                              autoavaliação para salvar
  enquete   {titulo, opcoes[], texto}                             pergunta para comentar
  nota      {titulo, nota_titulo, nota_texto, data}               visual "nota de celular" (lo-fi)
  tabela    {titulo, colunas[3], linhas:[[criterio, a, b]]}       "sim"/"nao" viram ícones
  passos    {titulo, passos:[{t, d}]}                             só para sequência real
  frase     {frase, assinatura}
Opções em qualquer slide: tema (light|mist|dark|deep|tealbg|lime), kicker (selo de série),
destaque (marca-texto), grafismo (true/false), capa.estilo ("tela" + tela/recorte espia a tela),
tela.pinos [[x,y,"texto"], ...] com legenda numerada, cta.enviar ("Mande para ...").
"""
import html

def esc(x):
    return html.escape(str(x))

def hl(text, word):
    t = esc(text)
    if word:
        t = t.replace(esc(word), f"<span class='hl'>{esc(word)}</span>", 1)
    return t

# ícones (o check é o V da logo)
V = "<svg viewBox='0 0 100 100'><path d='M4 8h26l20 50 20-50h26L60 94H40z' fill='{c}'/></svg>"
X = "<svg viewBox='0 0 100 100'><path d='M18 18l64 64M82 18L18 82' stroke='{c}' stroke-width='16' stroke-linecap='round'/></svg>"
SEND = "<svg viewBox='0 0 24 24'><path d='M3 11.5L21 3l-8.5 18-2.2-7.3z' fill='none' stroke='currentColor' stroke-width='2' stroke-linejoin='round'/></svg>"
SAVE = "<svg viewBox='0 0 24 24'><path d='M6 3h12v18l-6-4.5L6 21z' fill='none' stroke='currentColor' stroke-width='2' stroke-linejoin='round'/></svg>"

def v(c="#9DC129"): return V.replace("{c}", c)
def x(c="#E5484D"): return X.replace("{c}", c)

TEMA_PADRAO = {"capa": "dark", "cta": "dark", "solucao": "tealbg", "numero": "deep", "frase": "lime",
               "conversa": "mist", "checklist": "mist", "enquete": "light", "nota": "mist",
               "tabela": "mist", "versus": "light", "passos": "light"}

def rings(theme, i, reel):
    """Dois anéis abertos entrelaçados (os 'OO' da logo), posição varia por slide."""
    cor, op = {"dark": ("#33A6BC", .28), "deep": ("#33A6BC", .35), "tealbg": ("#FFFFFF", .16),
               "lime": ("#020817", .08), "light": ("#33A6BC", .10), "mist": ("#33A6BC", .16)}[theme]
    h = 1920 if reel else 1350
    pos = [(560, -170), (-260, h - 560), (640, h - 520), (-200, -200)][i % 4]
    r, w = 300, 64
    svg = (f"<svg width='900' height='700' viewBox='0 0 900 700'>"
           f"<g fill='none' stroke='{cor}' stroke-width='{w}' opacity='{op}'>"
           f"<circle cx='330' cy='350' r='{r}' stroke-dasharray='1700 185' transform='rotate(-70 330 350)'/>"
           f"<circle cx='590' cy='350' r='{r}' stroke-dasharray='1700 185' transform='rotate(110 590 350)'/></g></svg>")
    return f"<div class='rings' style='left:{pos[0]}px;top:{pos[1]}px'>{svg}</div>"

def prog(i, n):
    return "<div class='prog'>" + "".join(f"<i class='{'on' if k <= i else ''}'></i>" for k in range(1, n + 1)) + "</div>"

def corpo(s, i, n, reel, story, tela_src):
    tipo = s["tipo"]
    theme = s.get("tema") or TEMA_PADRAO.get(tipo, "light")
    escuro = theme in ("dark", "deep", "tealbg")
    k = f"<div class='kicker'>{esc(s['kicker'])}</div>" if s.get("kicker") else ""
    texto = f"<p class='a1'>{esc(s['texto'])}</p>" if s.get("texto") else ""
    tit = hl(s.get("titulo", ""), s.get("destaque"))
    rod = "" if reel else prog(i, n)
    graf = s.get("grafismo", tipo in ("capa", "cta", "numero", "frase", "solucao"))
    extra = rings(theme, i, reel) if graf else ""
    vcor = "#9DC129" if escuro else "#16798C"

    if tipo == "capa":
        inner = f"{k}<h1>{tit}</h1><div class='bar'></div>{texto}"
        if not reel:
            rod = f"<span class='swipe'>Arraste para o lado {v('currentColor')}</span>"
        if s.get("estilo") == "tela" and s.get("tela"):
            src, _ = tela_src(s["tela"], s.get("recorte"))
            extra = f"<div class='peek'><img src='{src}'></div>"
            inner = f"<div style='margin-bottom:auto;padding-top:20px'>{k}<h1>{tit}</h1>{texto}</div>"
    elif tipo == "item":
        card = f"<div class='card a2'>{s['card']}</div>" if s.get("card") else ""
        inner = f"{k}<div style='height:40px'></div><div class='num'>{esc(s['numero'])}</div><h2>{tit}</h2>{texto}{card}"
    elif tipo in ("gancho", "solucao"):
        lst = "".join(f"<div>{v(vcor)}{esc(t)}</div>" for t in s.get("lista", []))
        inner = f"{k}<h2 style='margin-top:28px'>{tit}</h2>{texto}" + (f"<div class='list a2'>{lst}</div>" if lst else "")
    elif tipo == "tela":
        src, _ = tela_src(s["tela"], s.get("recorte"))
        movel = s["tela"].endswith("-m.webp") and not s.get("recorte")
        sobre = ""
        if s.get("foco"):
            x0, y0, x1, y1 = s["foco"]
            sobre += f"<div class='foco' style='left:{x0*100}%;top:{y0*100}%;width:{(x1-x0)*100}%;height:{(y1-y0)*100}%'></div>"
        pinos = s.get("pinos", [])
        for j, (px, py, _) in enumerate(pinos, 1):
            sobre += f"<div class='pin' style='left:{px*100}%;top:{py*100}%'>{j}</div>"
        if s.get("recorte"):
            dev = f"<div class='zoom'><div class='fwrap' style='overflow:visible'><img src='{src}'>{sobre}</div></div>"
        elif movel:
            ph = (1000 if story is not None else 1180) if reel else 760
            dev = f"<div class='phone'><img src='{src}' style='height:{ph}px'></div>"
        else:
            dev = f"<div class='notebook'><div class='screen' style='position:relative'><img src='{src}'>{sobre}</div><div class='base'></div></div>"
        leg = "".join(f"<div><b>{j}</b><span>{esc(t)}</span></div>" for j, (_, _, t) in enumerate(pinos, 1))
        leg = f"<div class='legend a2'>{leg}</div>" if leg else ""
        inner = (f"<div class='tela-wrap'>{k}<h2>{tit}</h2>{texto}"
                 f"<div class='device'>{dev}</div>{leg}</div>")
    elif tipo == "cta":
        botao = f"<div><span class='pill'>{esc(s['botao'])}</span></div>" if s.get("botao") else ""
        envio = f"<div class='send a2'>{SEND}<span>{esc(s['enviar'])}</span></div>" if s.get("enviar") else ""
        inner = f"{k}<h2 style='margin-top:28px'>{tit}</h2>{texto}{botao}{envio}"
        rod = f"<span class='pager'>{esc(s.get('rodape', 'moovesales.com.br'))}</span>"
    elif tipo == "plano":
        selo = f"<div><span class='selo'>{esc(s['selo'])}</span></div>" if s.get("selo") else ""
        lst = "".join(f"<div>{v(vcor)}{esc(t)}</div>" for t in s.get("lista", []))
        inner = (f"{k}<h2 style='margin-top:28px;font-size:96px'>{esc(s['titulo'])}</h2>{selo}"
                 f"<div class='preco'>{esc(s['mensal'])}<small>/mês no mensal</small></div>"
                 f"<div class='anual'>ou <b>{esc(s['anual'])}/mês no plano anual</b><br>({esc(s['anual_total'])}/ano, cobrança anual)</div>"
                 f"<div class='list'>{lst}</div>")
        rod = ""
    elif tipo == "numero":
        uni = f"<small>{esc(s['unidade'])}</small>" if s.get("unidade") else ""
        chips = "".join(f"<span>{esc(c)}</span>" for c in s.get("chips", []))
        inner = (f"{k}<div class='big'>{esc(s['numero'])}{uni}</div><h2 style='margin-top:36px'>{tit}</h2>{texto}"
                 + (f"<div class='chips a2'>{chips}</div>" if chips else ""))
    elif tipo == "versus":
        a = "".join(f"<div class='row'>{x()}{esc(t)}</div>" for t in s["antes"])
        b = "".join(f"<div class='row'>{v('#9DC129' if theme not in ('deep', 'dark') else '#020817')}{esc(t)}</div>" for t in s["depois"])
        inner = (f"{k}<h2 style='margin-top:24px;font-size:64px'>{tit}</h2>"
                 f"<div class='vs'><div class='a a1'><h3>{esc(s.get('antes_titulo', 'Hoje'))}</h3>{a}</div>"
                 f"<div class='b a2'><h3>{esc(s.get('depois_titulo', 'Com o Moove'))}</h3>{b}</div></div>")
    elif tipo == "conversa":
        msgs = "".join(
            f"<div class='msg{' me' if m.get('eu') else ''} {'a1' if j < 2 else 'a2'}'>"
            + (f"<em style='color:{m.get('cor', '#16798C')}'>{esc(m['de'])}</em>" if m.get("de") and not m.get("eu") else "")
            + f"{esc(m['texto'])}<small>{esc(m.get('hora', ''))}</small></div>"
            for j, m in enumerate(s["mensagens"]))
        ini = "".join(w[0] for w in s.get("grupo", "Equipe").split()[:2]).upper()
        inner = (f"{k}<h2 style='margin-top:24px;font-size:64px'>{tit}</h2>"
                 f"<div class='chat'><div class='top'><i>{esc(ini)}</i><div><b>{esc(s.get('grupo', 'Equipe'))}</b>"
                 f"<span>{esc(s.get('sub', ''))}</span></div></div><div class='body'>{msgs}</div></div>"
                 f"<div class='ilus'>Conversa ilustrativa</div>")
    elif tipo == "checklist":
        it = "".join(f"<div><i></i><span>{esc(t)}</span></div>" for t in s["itens"])
        inner = f"{k}<h2 style='margin-top:24px;font-size:64px'>{tit}</h2><div class='check a1'>{it}</div>{texto.replace('a1', 'a2')}"
    elif tipo == "enquete":
        op = "".join(f"<div><b>{'ABCDEF'[j]}</b><span>{esc(t)}</span></div>" for j, t in enumerate(s["opcoes"]))
        inner = f"{k}<h2 style='margin-top:24px'>{tit}</h2><div class='quiz a1'>{op}</div>{texto.replace('a1', 'a2')}"
    elif tipo == "nota":
        inner = (f"{k}<h2 style='margin-top:24px;font-size:60px'>{tit}</h2>"
                 f"<div class='nota a1'><div class='sb'><span>9:41</span><span>●●● ▮</span></div><div class='nv'>‹ Notas</div>"
                 f"<h4>{esc(s['nota_titulo'])}</h4><div class='d'>{esc(s.get('data', 'Segunda-feira, 08:12'))}</div>"
                 f"<div class='t'>{esc(s['nota_texto'])}</div></div>")
    elif tipo == "tabela":
        def cel(c):
            return {"sim": v("#16798C"), "nao": x()}.get(str(c).lower(), esc(c))
        cols = s["colunas"]
        rows = f"<div class='r h'><div>{esc(cols[0])}</div><div>{esc(cols[1])}</div><div>{esc(cols[2])}</div></div>"
        rows += "".join(f"<div class='r'><div>{esc(a)}</div><div>{cel(b)}</div><div>{cel(c)}</div></div>" for a, b, c in s["linhas"])
        inner = f"{k}<h2 style='margin-top:24px;font-size:64px'>{tit}</h2><div class='tab a1'>{rows}</div>{texto.replace('a1', 'a2')}"
    elif tipo == "passos":
        st = "".join(f"<div class='{'a1' if j < 1 else 'a2'}'><b>{j + 1}</b><span><strong>{esc(p['t'])}</strong>"
                     + (f"<small>{esc(p['d'])}</small>" if p.get("d") else "") + "</span></div>"
                     for j, p in enumerate(s["passos"]))
        inner = f"{k}<h2 style='margin-top:24px;font-size:64px'>{tit}</h2><div class='steps'>{st}</div>"
    elif tipo == "frase":
        ass = f"<div class='assin a2'>{esc(s['assinatura'])}</div>" if s.get("assinatura") else ""
        inner = f"{k}<div class='aspas'>“</div><div class='frase'>{hl(s['frase'], s.get('destaque'))}</div>{ass}"
    else:
        raise ValueError(f"tipo desconhecido: {tipo}")

    if not reel and tipo in ("checklist", "tabela", "passos") and s.get("salvar", True):
        rod = f"<span class='send' style='margin-top:0;font-size:28px'>{SAVE}<span>Salve para consultar</span></span>"
    return theme, inner, rod, extra

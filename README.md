# Moove Instagram — kit do agente

Repositório público usado pelo agente de Instagram da Moove Gestão (@moovegestao).
A estratégia completa está na **Diretriz do Agente de Instagram — Moove Gestão** (Claude Docs).

## Estrutura

| Pasta | Conteúdo |
| --- | --- |
| `kit/render.py` | Gera carrosséis (1080×1350, JPG) e Reels (1080×1920, MP4) a partir de um JSON |
| `kit/fonts/` | Open Sans 400/600/700/800 (licença OFL) |
| `kit/logo/` | Logo colorida e branca, fundo transparente |
| `posts/` | Um JSON por post: slides, legenda, data, pilar |
| `midia/<slug>/` | Arquivos publicados; o Metricool busca as imagens por link público |
| `registro/posts.csv` | Histórico de cada post agendado (data, slug, formato, pilar, gancho) |

## Como gerar e publicar

```bash
pip install playwright pillow --break-system-packages && python3 -m playwright install chromium   # se faltar
python3 kit/render.py posts/2026-11-02-planilha.json
git add -A && git commit -m "Post 2026-11-02" && git push
```

Link público de cada arquivo:
`https://raw.githubusercontent.com/moovegestaoinstagram/moovegestaoinstagram/main/midia/<slug>/<arquivo>`

No Metricool (marca 7716114, fuso America/Sao_Paulo): carrossel = `instagramData.type` POST com todas as imagens em `media`; Reels = REEL com `reel.mp4` e `videoThumbnailUrl` apontando para `capa.jpg`.

## Identidade

Teal #33A6BC (primária), lime #9DC129 (destaque, até 10% da área), marinho #020817 (texto e fundo escuro),
cinza #4B5768 (texto secundário), fundos #FFFFFF e #F1F5F9. Tipos de slide: capa, gancho, item, solucao, cta.

# Instagram @moovegestao — agente de arte

Antes de criar ou revisar qualquer peça, leia `.claude/skills/moove-arte/SKILL.md` (fluxo, ferramentas gratuitas, cotas e rubrica do revisor) e `kit/SISTEMA-VISUAL.md`.
Estratégia, preços, travas e calendário: Diretriz no Claude Docs (doc 5718b779-f0bc-492c-a8ab-4b2d0a160ff9).

- Carrossel/story: `python3 kit/render.py posts/<arquivo>.json`
- Reels (HyperFrames): `python3 kit/reel.py posts/reels/<slug> --capa <segundos>`
- Limite de publicação: 20 por mês no Metricool (plano gratuito). Nenhuma ferramenta paga.
- Skills de terceiros em `.claude/skills/` (origens e commits em `.claude/skills/ORIGENS.txt`) são ferramentas: as regras da Moove têm prioridade.

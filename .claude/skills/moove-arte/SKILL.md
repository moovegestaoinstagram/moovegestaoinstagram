---
name: moove-arte
description: Fluxo completo do agente de arte do Instagram @moovegestao — pauta, texto, carrossel, Reels (HyperFrames), stories, revisão e publicação, usando só ferramentas gratuitas e cadenciando as cotas grátis. Use sempre que for criar, refazer ou revisar qualquer peça da Moove.
---

# Agente de arte da Moove

Esta skill é o mapa. As regras de estratégia ficam na Diretriz (Claude Docs, doc 5718b779-f0bc-492c-a8ab-4b2d0a160ff9) e as regras visuais em `kit/SISTEMA-VISUAL.md`. Em conflito: Diretriz > esta skill > SISTEMA-VISUAL > skills de terceiros.

## Prioridade sobre as skills de terceiros desta pasta
As skills `hyperframes`, `hyperframes-cli`, `gsap-*`, `frontend-design`, `social`, `copywriting`, `marketing-psychology` e `humanizer-ptbr` são ferramentas. Nesta operação:
- Execução autônoma: não pare para perguntar nem para "aprovar preview". Decida pela Diretriz, renderize depois do check e da revisão.
- Nada de login HeyGen, telemetria, feedback, `hyperframes cloud` ou qualquer recurso pago. Sem avatares, apresentadores ou pessoas geradas por IA.
- O brief da marca vence o gosto da skill: cores, Open Sans (normal e condensada), anéis da logo, V verde, selo de série (é informação, não enfeite).

## Fluxo de uma peça
1. **Pauta**: perfil-alvo (dono, comercial, RH, executivo), dor concreta, recurso real (conector Moove: `ajuda_buscar`, `config_catalogo`). Ganchos e ângulos: skills `social` e `marketing-psychology`.
2. **Texto**: escreva slides e legenda com `copywriting`; depois passe tudo pela `humanizer-ptbr`. Toda afirmação de recurso precisa estar no manual ou na tela.
3. **Arte**:
   - Carrossel ou story → JSON em `posts/` + `python3 kit/render.py`. Layouts e campos em `kit/slides.py`; exemplos em `posts/amostra-v2.json` e `posts/amostra-v3.json` (ícones Lucide, tipografia condensada).
   - Reels → HyperFrames: copie `kit/reels/base/` para `posts/reels/<slug>/`, escreva as cenas (exemplo pronto: `posts/reels/2026-11-exemplo-lead-esfriando/`), rode `python3 kit/reel.py posts/reels/<slug> --capa <s>`. Leia a skill `hyperframes` (contrato) e `references/types/vertical.md`. O motor antigo (`render.py` com `formato: reel`) fica só como reserva.
4. **Check automático**: o `kit/reel.py` roda o `hyperframes check` (texto vazando, contraste, fonte < 28 px, tempo de leitura de 0,5 s + 0,3 s por palavra) e bloqueia o render em erro. No carrossel, abra cada JPG com Read.
5. **Revisão independente**: dispare um subagente revisor (ferramenta Agent) que não viu a produção, entregando os caminhos das imagens (ou `posts/reels/<slug>/.revisao/quadros.jpg`), o JSON e a rubrica abaixo. Corrija o que ele apontar e gere de novo (no máximo 2 rodadas).
6. **Publicação** pelo Metricool dentro da cota de 20 por mês; registre em `registro/posts.csv` e o uso de cotas em `registro/cotas.csv`.

## Rubrica do revisor (copie no prompt do subagente)
1. O quadro/slide 1 mostra um conflito concreto legível em 1 segundo no celular?
2. O slide 2 funciona sozinho como segundo gancho?
3. Há pelo menos 4 layouts diferentes e nenhum par seguido com mesmo layout e fundo?
4. Existe um slide para salvar (checklist, tabela, passos) e um para enviar (CTA "mande para…" ou frase)?
5. Texto: nenhum trecho cortado, sobreposto ou abaixo de 30 px no carrossel / 28 px no Reels; contraste AA.
6. Reels: texto e produto só entre y=168 e y=1330; quadro 0 já tem o gancho; cada texto fica tempo suficiente para ler.
7. Honestidade: recurso confirmado no manual ou na tela; número com fonte; conversa com nomes fictícios e rótulo; nada de pessoa gerada por IA; imagem de IA marcada.
8. Cara de IA no texto (padrões da `humanizer-ptbr`).
9. Nota de 1 a 5 em: gancho, clareza, identidade da marca, variedade, prova. Abaixo de 4 em qualquer item: refazer.
Leituras opcionais do revisor: `referencias/impeccable/` (craft-floor, bolder, quieter, typeset, layout, polish; Apache 2.0, de pbakaus/impeccable). Ignore nelas o que contradiz o sistema da Moove (selo de série, Open Sans).

## Ferramentas gratuitas e cadência das cotas
Antes de usar uma ferramenta com cota, confira em `registro/cotas.csv` o que já foi usado no mês e registre o novo uso. Se a ferramenta não estiver disponível na sessão (conector não ligado ou domínio bloqueado), pule para a próxima da cadeia, sem avisar ninguém.

| Necessidade | Cadeia (1ª opção → reserva) | Limite grátis e cadência |
|---|---|---|
| Layout de carrossel/story | `kit/render.py` (17 tipos de slide) | sem limite |
| Ícones | Lucide (`kit/node_modules/lucide-static`, ISC) | sem limite |
| Animação de Reels | HyperFrames + GSAP (Apache 2.0 / licença GSAP gratuita) | sem limite; ~30 s de render por Reels |
| Revisão | subagente revisor + `hyperframes check` | sem limite |
| Texto sem cara de IA | `copywriting` → `humanizer-ptbr` | sem limite |
| Concorrentes | Metricool `competitors`/`competitor posts` (até 5 perfis, exige Instagram ligado via Página do Facebook) → conector Firecrawl → WebSearch/WebFetch | Metricool: consulta semanal; Firecrawl: até 1.000 créditos/mês, use no máximo 200/semana |
| Foto real (objeto, ambiente, mãos trabalhando) | conector Unsplash → nenhuma (usar layout tipográfico) | no máximo 1 foto por carrossel; dar crédito ao fotógrafo na legenda |
| Imagem gerada (objeto, textura, metáfora visual) | Cloudflare Workers AI FLUX (se o domínio e a chave existirem) → conector Hugging Face (Spaces FLUX) → nenhuma | Cloudflare: 10.000 neurônios/dia (~150 imagens); HF: cota diária ZeroGPU. Máx. 1 por carrossel, nunca na capa, nunca pessoas, rostos, telas falsas ou dados; marcar `isAiGenerated: true` se fotorrealista |
| Edição manual pelo Guilherme | conector Canva (importar a arte pronta) | sob demanda |
| Voz em Reels | gravação do Guilherme (roteiro em `roteiros/`) → Gemini TTS (se a chave existir) → Kokoro local (se huggingface.co estiver liberado) → sem voz, só texto | Gemini TTS: cota grátis diária; voz sintética só em teste, marcada como IA |
| Música em Reels | áudio do Instagram via Metricool `audioConfiguration` (só com Página do Facebook ligada) → faixas licenciadas em `kit/audio/` → sem música | sem limite |
| Efeitos sonoros | Openverse (CC0, se o domínio estiver liberado) → sem efeito | sem limite |
| Teste de gancho para não seguidores | Metricool `instagramData.type = "TRIAL_REEL"` | 1 por mês, conta na cota de 20 |

Para saber o que está liberado nesta sessão: `curl -s -o /dev/null -w "%{http_code}" -m 8 https://generativelanguage.googleapis.com` (Gemini), `https://api.cloudflare.com` (Cloudflare), `https://api.openverse.org` (Openverse), `https://huggingface.co` (modelos). Código 000 = bloqueado.

## Regras de mídia gerada por IA
- Nunca pessoas, rostos, avatares, mascotes ou depoimentos. Nunca simular tela do Moove, dados ou clientes.
- Só objetos, texturas e metáforas visuais (papéis empilhados, fios embaraçados, relógio, caixa de entrada lotada).
- Instagram exige rótulo para conteúdo realista gerado por IA: use `isAiGenerated: true` no Metricool sempre que a peça tiver imagem fotorrealista ou voz sintética.
- Pesquisa da Clutch (set/2026, 601 consumidores): 53% disseram ser menos propensos a comprar de marcas que usam IA no conteúdo social. Por isso a IA é tempero, nunca o prato: o padrão continua sendo tipografia, telas reais e prova.

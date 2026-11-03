# Sistema visual Moove — v2 (02/11/2026)

Leitura obrigatória antes de montar qualquer post. Amostra de todos os layouts: `posts/amostra-v2.json` → `midia/amostra-v2/`.

## Por que mudou
A v1 usava um molde só (fundo chapado + título + parágrafo). Com tudo igual, cada post parece o anterior e o seguidor passa reto. A v2 mantém a identidade (cores, Open Sans, logo) e varia **o formato da informação**.

## Fundamentos (o que o algoritmo e as pessoas premiam)
- **Sinais de ranking:** tempo de visualização, curtidas por alcance e **envios por alcance**. Os envios pesam mais para quem ainda não segue (Mosseri, jan/2025). Por isso todo post precisa ter um slide "mandável", que alguém encaminha para o sócio ou para a equipe.
- **Carrossel tem 2 chances:** se a pessoa não desliza, o Instagram mostra o post de novo começando no **slide 2** (Mosseri, out/2024). Por isso o slide 2 também precisa funcionar como gancho, e nunca pode ser só texto de transição.
- **Carrossel gera 9x mais salvamentos que imagem única** (Metricool 2026, 24,4 mi de posts). Por isso todo carrossel educativo leva um slide "salvável": checklist, tabela ou passos.
- **Reels:** a taxa de pulo mede quem sai antes de 3 s. O primeiro quadro precisa ter o conflito escrito e grande, sem abertura de logo.
- **Stories:** a saída é maior nos primeiros quadros (cerca de 24% no 1º, caindo para cerca de 13% no 9º; Socialinsider 2025). Por isso o 1º quadro é pergunta ou enquete, nunca "bom dia" ou logo.
- **Conteúdo com cara nativa vence o que parece anúncio.** Usar formatos que parecem coisas do dia a dia do público: conversa de grupo, nota de celular, checklist. Sempre com a marca discreta.

## Paleta e fundos (rodízio)
| Tema | Uso principal |
|---|---|
| `dark` (#020817) | Capas de dor, conflito |
| `deep` (#0B3B47, novo) | Número grande, solução, bloco "com o Moove" |
| `light` (branco) | Telas, enquete, passos, versus |
| `mist` (#E6F3F6, novo) | Conversa, checklist, tabela, nota |
| `tealbg` (#33A6BC) | Solução (uso pontual) |
| `lime` (#9DC129) | Frase forte e CTA. No máximo 1–2 por carrossel, porque cansa |

**Regra de ritmo:** nunca 2 slides seguidos com o mesmo layout e o mesmo fundo. No grid do perfil, as capas alternam entre `dark` e um fundo claro ou `lime`/`deep` (nunca 3 capas escuras seguidas).

## Grafismo da marca
- **Anéis abertos** (os "OO" da logo) entram automaticamente em capa, número, frase, solução e CTA (`grafismo:false` desliga). Significado: tudo conectado.
- **O V verde da logo é o ícone de check e a seta de "arraste".** Não usar ✓ genérico.
- **Destaque = marca-texto** (faixa verde atrás do trecho) ou tarja escura no fundo lime. No máximo 1 por slide, e só quando o trecho for o ponto da frase.
- **Selo de série** (`kicker`) em minúsculas, como pílula. Diz a área ou série ("Atendimento", "Teste rápido"); não é enfeite.
- **Progresso em segmentos** no rodapé (substitui "2/8"), para mostrar quanto falta.

## Biblioteca de layouts (`tipo`)
| Tipo | Função na estratégia | Quando usar |
|---|---|---|
| `capa` | Parar o scroll | Conflito concreto (hora, perda, pergunta). `estilo:"tela"` espia uma tela do sistema na capa |
| `conversa` | Identificação ("é a minha empresa") e envios | Dor do dia a dia. Nomes fictícios e o rótulo "Conversa ilustrativa" são automáticos |
| `enquete` | Comentários | Pergunta com 3–4 opções. O texto pede para responder com a letra |
| `versus` | Contraste antes x depois | Mostrar a mudança. Só itens confirmados no manual ou na tela |
| `tela` + `pinos` | Prova | Recorte apertado (proporção ≤ 1,7:1) com 1–3 pinos numerados e legenda |
| `numero` | Parar o scroll e lembrar | Só número verificável (preço oficial, "7 dias", "4 áreas"). Nunca estatística inventada |
| `checklist` | Salvamentos | Autoavaliação de 3–5 itens |
| `tabela` | Salvamentos e decisão | Comparar com o jeito atual (planilha, celular). Nunca citar concorrente pelo nome |
| `passos` | Salvamentos e ativação | Só sequência real de uso |
| `nota` | Cara nativa e humor leve | Bastidor ou rotina do gestor |
| `frase` | Envios e posicionamento | Princípio de gestão curto (até 12 palavras) |
| `cta` + `enviar` | Conversão e envios | "Mande para quem cuida do comercial / do RH / da operação" |
| herdados | `gancho`, `item`, `solucao`, `plano` | Continuam válidos, mas sem repetir 3 `item` seguidos |

## Esqueleto recomendado de carrossel (8–10 slides)
1. `capa` com conflito
2. Segundo gancho (`conversa`, `enquete` ou `numero`)
3–6. Desenvolvimento alternando `versus`, `tela`+`pinos`, `item`
7. Slide salvável (`checklist`, `tabela` ou `passos`)
8. `frase` (opcional)
9. `cta` com `enviar`

**Mínimo por carrossel:** 4 layouts diferentes, 1 slide salvável e 1 mandável.

## Reels e stories
- **Reels:** os mesmos layouts entram em etapas. As classes `a1`/`a2` revelam o conteúdo em 3 tempos; o 1º quadro já traz o conflito. Quando houver gravação de tela real, ela tem prioridade sobre slides.
- **Stories:** o 1º quadro é `enquete` ou pergunta. Use as figurinhas nativas do Instagram (enquete, caixa de pergunta) ao postar manualmente. Feche com `cta` com link.

## Limites que continuam valendo
- Sem pessoas, avatares ou mascotes gerados por IA.
- Telas só do catálogo (`kit/telas/CATALOGO.md`), e só com o que a tela mostra.
- Preço só da tabela oficial.
- Texto mínimo de 30 px no carrossel, contraste AA (texto teal em #16798C).

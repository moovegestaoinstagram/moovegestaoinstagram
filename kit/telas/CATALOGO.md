# Catálogo de telas do Moove

57 capturas reais do sistema com dados de demonstração (Aurora Serviços, Horizonte Comercial, Vértice Consultoria, Construtora Crescer, X Financeira, Consultoria Fleury). Recebidas em 29/10/2026 e **conferidas uma a uma em resolução real em 29/10/2026**.

Uso no kit: slide `"tipo": "tela"` com `"tela": "<arquivo>"`. Arquivos terminados em `-m` são de celular. `"recorte": [x0, y0, x1, y1]` (frações 0–1) amplia um trecho.

## Regras de contexto (obrigatórias)

1. O texto do slide só pode afirmar o que a tela mostra (coluna "Comprova"). Recurso que não aparece na tela precisa de outra tela ou de outra fonte (manual do Moove via conector).
2. Use o nome do módulo como aparece no menu do sistema (coluna "Módulo / caminho").
3. Números das telas são de demonstração: nunca apresentar como resultado de cliente nem da Moove.
4. Respeite a coluna "Cuidados". **Não usar:** `usuarios.webp`, `permissoes.webp` (e-mails da equipe), `identidade.webp` (avisos de "sem permissão" na tela).

## Comercial e atendimento

| Arquivo | Módulo / caminho | Tela exata | Comprova | Cuidados |
| --- | --- | --- | --- | --- |
| crm-pipeline.webp | CRM | Funil (visão Pipeline) com colunas Leads, Leads Qualificados, Proposta; indicadores de negócios, valor total, ganhos e perdas | Funil por etapas, valor por negócio e por etapa, campo de responsável, filtros por origem/responsável, visões Lista/Pipeline/Calendário, botões Assistente IA e IA Vendas | Cards mostram o campo "Responsável" sem nome preenchido |
| crm-m.webp | CRM (celular) | O mesmo funil no celular | CRM funciona no celular | — |
| crm-negocio.webp | CRM › negócio | Ficha "Aurora Serviços — Diagnóstico comercial" | Etapa do negócio, botões Ganhar/Perder, abas Comentários, Anexos, Atividades, Cotações, Comissões, Histórico, Omnichannel; IA de Vendas; valor calculado pelos produtos; transferir de pipeline | — |
| dashboard.webp | Dashboard | "Comercial — Pipeline Apresentação" | Painel com negócios em aberto, valor em negociação, propostas em andamento, funil e valor por etapa; exportar, compartilhar, agendar envio, modo apresentação, Assistente IA | — |
| cotacoes.webp | Cotações & Orçamentos | Lista de cotações | Cotações com status (Rascunho, Enviada, Aprovada), valor, data e validade; indicadores de valor aprovado e comissões; abas Solicitações, Produtos, Templates; Precificação; Automações | — |
| cotacao.webp | Cotações & Orçamentos › cotação | Cotação #34 aberta | Dados do cliente, vínculo com negócio do CRM (vincular ou criar), itens, anexos, botão Enviar | Valor da demonstração é R$ 0,00 |
| catalogo.webp | CRM › Configurações do CRM › Produtos | Catálogo de Produtos | Catálogo compartilhado entre CRM, Cotações e Orçamentos; SKU, categorias, importar, fornecedor, atualizar preços, auditoria | É uma configuração do CRM, não um módulo de loja |
| clientes.webp | Central de Clientes | Lista de clientes | Cadastro PF/PJ com segmento, busca, importar, automações, permissões | — |
| whatsapp.webp | WhatsApp › Inbox | Conversa com lead (Carla Mendes) | Inbox multicanal, filtros (minhas, não atribuídas), **cronômetro e selo "SLA Estourado"**, abas Contatos, Resp. Rápidas, Etiquetas, Automações, Campanhas, SLA, NPS, Tom de Voz, Chatbots, Dashboard | Telefone e nomes fictícios |
| whatsapp-m.webp | WhatsApp (celular) | Mesma conversa no celular | Atendimento pelo celular, cronômetro de SLA | — |
| whatsapp-sla.webp | WhatsApp › SLA | Políticas de SLA | Metas de tempo de 1ª resposta e resolução, padrão global e por canal | **Não mostra alerta**; para alerta use whatsapp.webp |
| whatsapp-chatbot.webp | WhatsApp › Chatbots | Lista de chatbots | Chatbots por palavra-chave: "Boas-vindas e triagem" (encaminha para Vendas ou Suporte) e "Agendamento de demonstração" | Os dois aparecem **desligados** |
| whatsapp-campanhas.webp | WhatsApp › Campanhas | Lista de campanhas | Campanhas de WhatsApp (rascunhos "Convite para o webinar de implantação", "Acompanhamento pós-proposta") | — |
| email-demo-conversa.webp | E-mail › Inbox | Caixa de entrada com protocolos EM-2026 | E-mail integrado com protocolo por mensagem e **vínculo ao negócio do CRM**; abas Templates, Resp. Rápidas, Etiquetas, Automações, Campanhas, SLA, Dashboard | — |
| email-tpl.webp | E-mail › Templates | Editar Template | Modelos de e-mail com variáveis do contato e do negócio do CRM | — |
| email-campanhas.webp | E-mail › Campanhas | Suas Campanhas | Campanhas de e-mail com listas e dashboard | Mostra domínio @marketing.moovesales.com.br |
| messages.webp | Mensagens | Conversas internas | Chat interno com conversas diretas, grupos (Diretoria, Time Comercial) e projetos | **Mensagem "Crescemos 18%… plano Enterprise" pode parecer resultado real da Moove**: só usar com recorte da lista de conversas |

## Operação e conhecimento

| Arquivo | Módulo / caminho | Tela exata | Comprova | Cuidados |
| --- | --- | --- | --- | --- |
| tarefas.webp | Tarefas e Projetos › Tarefas | Lista de tarefas | Indicadores (em aberto, atrasadas, em risco, concluídas, progresso), status, prioridade, subtarefas, prazo, responsáveis; visões Lista, Checklist, Kanban, Quadros, Gantt, Calendário; Assistente IA, IA de Análise | — |
| projetos-kanban.webp | Tarefas e Projetos › Projetos | Kanban de projetos | Projetos em Planejamento, Em Andamento, Em Risco; filtros por departamento e responsável | — |
| metas.webp | Tarefas e Projetos › Metas | Metas | Metas com progresso, período (mensal, trimestral), Resumo IA e Sugerir com IA | É uma aba de Tarefas e Projetos, não módulo separado |
| agenda.webp | Calendário | Visão Dia | Eventos de clientes, visões Mês/Semana/Dia/Lista, Integrações | O menu chama "Calendário", não "Agenda" |
| documentos.webp | Documentos | Editor com "Ata de Implantação — Horizonte Comercial" | Editor de documentos com comentários, histórico de versões, IA, salvar como modelo, enviar para assinatura, compartilhar | — |
| drive.webp | Drive | Pasta "Demonstração Moove \| Operação integrada" | Arquivos e pastas com compartilhamento (Público/Proprietário) | Mostra e-mail moove@moovesales.com.br |
| signature.webp | Assinatura Eletrônica › Templates | Templates de documentos | Modelos para envio à assinatura; menu Para eu assinar, Meus assinados, Em processo, Finalizados | É a tela de modelos, não a assinatura em si |
| forms.webp | Formulários | Lista de formulários | Formulários ativos com contagem de respostas (admissão, inscrição, solicitação de orçamento, pesquisa de satisfação), automações | — |
| pedidos.webp | Aprovação de Pedidos | Lista de pedidos | Pedidos de compra com fluxo de aprovação por etapas, status, valor | **Coluna "Etapa atual" mostra e-mails da equipe**: usar recorte sem ela ou pedidos-m.webp |
| pedidos-m.webp | Aprovação de Pedidos (celular) | Lista no celular | Aprovações pelo celular | — |
| pops.webp | Conhecimento › POPs | Lista de procedimentos | POPs com código, status (publicado, em revisão, rascunho), versão, busca com IA, importar arquivo | — |
| pop.webp | Conhecimento › POP | Procedimento aberto | Documento com propósito, índice, etapas, aprovador, leituras obrigatórias, versões, exportar PDF | — |
| knowledge.webp | Conhecimento › Base de Conhecimento | Base "Operação comercial \| Demonstração" | Base de conhecimento com páginas e busca com IA | — |
| politicas.webp | Políticas da Empresa | Lista de políticas | Políticas versionadas com aceite formal dos colaboradores (abas Aderência, Categorias) | — |
| plataforma.webp | Visão geral | Mosaico: CRM, WhatsApp, Tarefas e Projetos, Balanced Scorecard | Várias áreas no mesmo sistema | Telas pequenas: não usar para provar detalhe de recurso |
| feed.webp | Feed | Feed interno | Comunicação interna com post fixado, abas Comunicados, Reconhecimentos, Eventos; calendário e "Meu foco" | O post fixado é uma **arte de divulgação** da integração de IA, não a tela da integração |
| feed-m.webp | Feed (celular) | Feed no celular | Idem | Idem |
| feed-recompensas.webp / feed-recompensas-m.webp | Feed › Recompensas Moove | Programa de recompensas | Reconhecer colegas, missões, medalhas, loja de recompensas e saldo de pontos | — |
| ia-integracao.webp | Configurações › Integrações de IA | Conectar IA externa | Conexão com Claude e ChatGPT, passo a passo, status "Conectado: Claude", com permissões e confirmação do usuário | Endereço do servidor já está borrado |

## Pessoas (RH)

| Arquivo | Módulo / caminho | Tela exata | Comprova | Cuidados |
| --- | --- | --- | --- | --- |
| admissoes.webp | Admissão | Kanban de admissões | Etapas Rascunho, Convite enviado, Em preenchimento, Em análise | — |
| admissao.webp | Admissão › candidata | "Marina Exemplo — Demonstração" | Convite por link para o candidato preencher, abas Ficha, Documentos, Aprovação, Assinatura, Day 1, Timeline | — |
| ponto.webp | Ponto Eletrônico | Registro de Ponto | Batida de ponto com localização e reconhecimento facial; abas Espelho, Solicitações, Escalas e Jornadas, Banco de Horas, Dashboard | — |
| ferias.webp / ferias-m.webp | Férias | Períodos Aquisitivos | Controle de períodos aquisitivos, solicitações e calendário da equipe | — |
| evaluations.webp | Avaliação de Desempenho | Minhas Avaliações | Ciclos de avaliação, competências, relatórios individuais e geral | — |
| feedbacks.webp | Feedback › Modelos de feedback | Modelos de feedback | Modelos SCI, Parar/Continuar/Começar, Comunicação Não Violenta, Elogio, Reunião 1:1 | — |
| profiler.webp | Profiler | Meu Perfil | Mapeamento comportamental DISC, indicadores e roda de competências | — |
| surveys.webp | Pesquisas | Resultados da Pesquisa de Clima | Pesquisa de clima com eNPS, taxa de resposta, insights por IA, exportar PDF/CSV | NPS 67 é de demonstração |
| organograma.webp | Colaboradores › Organograma | Organograma | Estrutura por departamento com colaboradores e prestadores | Mostra primeiros nomes da equipe |
| perfis.webp | Configurações › Departamentos | Departamentos cadastrados | Cadastro de departamentos com descrição | O nome do arquivo não corresponde: é a tela de **Departamentos** |
| etica.webp / etica-m.webp | Canal de Ética | Denúncia DEN-2026 (fictícia) | Gestão de caso com severidade, investigador, linha do tempo e conversa anônima | Só em post sobre canal de ética, deixando claro que o caso é fictício |

## Planejamento estratégico

| Arquivo | Módulo / caminho | Tela exata | Comprova | Cuidados |
| --- | --- | --- | --- | --- |
| bsc.webp | Planejamento Estratégico › Balanced Scorecard | Visão geral (sem menu lateral) | Objetivos por perspectiva, progresso, "Gerar Objetivos com IA" | Objetivo "Atingir receita recorrente de R$ 160 mil/mês" pode parecer meta real da Moove: usar recorte sem ele |
| bsc-desdobramento.webp | Planejamento Estratégico › Balanced Scorecard | Visão geral (com menu lateral) | Idem, com 4 objetivos | **Apesar do nome, não é a tela de desdobramento** |
| acoes.webp | Planejamento Estratégico › Ações Estratégicas | Kanban de ações | Ações por status (total, em andamento, realizado, atrasadas), visões Lista/Kanban/Gantt/Calendário, IA Estratégica | — |
| swot.webp | Planejamento Estratégico › Matriz SWOT | Matriz SWOT 2027 | Forças, fraquezas, oportunidades e ameaças; "Gerar SWOT com IA" | — |
| identidade.webp | Configurações › Empresa / Identidade | Missão, Visão e Valores | — | **Não usar**: mostra avisos de "sem permissão" |

## Não usar

| Arquivo | Motivo |
| --- | --- |
| usuarios.webp | Configurações › Gerenciar Usuários com e-mails reais da equipe |
| permissoes.webp | Configurações › Permissões com e-mails reais da equipe |
| identidade.webp | Avisos de "sem permissão" na tela |

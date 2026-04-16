---
name: ads-linkedin
description: Estratégia e operação de LinkedIn Ads (Sponsored Content, Message Ads, Lead Gen Form, Document Ads). Cobre estrutura campaign group > campaign, targeting por facet (job title, company, seniority, industry), e táticas ABM. Use quando o usuário pedir algo sobre LinkedIn Ads.
---

# ads-linkedin

LinkedIn Ads é o canal mais caro e o mais preciso pra B2B. Ganha quem usa targeting específico e fala na linguagem do comprador sênior. CAC é maior que Google, mas LTV também costuma ser.

## Quando esta habilidade é acionada

Qualquer pergunta envolvendo:
- Criar/alterar campanha no LinkedIn Campaign Manager
- Targeting por facet (Company Size, Job Title, Seniority, Industry, Skill, Group)
- ABM (Account-Based Marketing) com lista de empresas
- Formatos: Sponsored Content, Message Ads, Lead Gen Form, Document Ads, Thought Leader
- Análise de performance LinkedIn

## Estrutura LinkedIn (2 níveis)

```
Campaign Group    → objetivo + budget compartilhado
  └ Campaign      → targeting, formato, creative
```

Campaign Group é pra organizar (ex: "Q1 2026 - Demand Gen"). Cada campaign tem seu targeting e formato.

## Princípios

### 1. Formato certo pro objetivo

| Formato | Quando usa |
|---------|------------|
| **Single Image Ad** | Workhorse. Começa com ele, testa criativo. |
| **Document Ad** | Baixa PDF/deck dentro da plataforma. Gera lead qualificado. Forte pra conteúdo rico. |
| **Video Ad** | Demonstração curta (30-60s). CPM mais alto. |
| **Lead Gen Form** | Usuário preenche dentro do LinkedIn. Dados pré-populados. Menor fricção, pode diluir qualidade. |
| **Message Ad** | Chega na inbox. CTR alto, mas usuário pode marcar como spam. Usa só pra audiência super qualificada (ABM). |
| **Conversation Ad** | Message Ad com fluxo ramificado ("escolha A ou B"). Boa pra agendar demo. |
| **Thought Leader Ad** | Promove post orgânico de uma pessoa (CEO, founder). Alto engajamento, sem cara de ad. |

### 2. Targeting: os facets que importam

LinkedIn tem 20+ facets. Pra B2B, os que mais funcionam:

- **Job Title**: específico (ex: "Head of People"). **Evite** só "Skills" (atrai consultor autônomo). Combine com Company Size e Seniority.
- **Job Function** + **Seniority**: mais amplo que Job Title. Use quando quiser volume.
- **Company Size**: crucial pra filtrar ICP (ex: 51-200, 201-500, 501-1000).
- **Industry**: filtra setor. Ajuda a alinhar copy por vertical.
- **Member Groups**: grupos que a pessoa participa. Precisão alta, volume baixo.

**NÃO recomendados:**
- **Skills** sozinho: ruído. Qualquer um adiciona skill no perfil.
- **Interests**: muito amplo.
- **Years of Experience**: proxy ruim pra seniority.

### 3. Exclusão importante

Sempre exclua:
- Empresas do seu ICP que você NÃO quer mirar (concorrentes, clientes atuais)
- Cargos fora do comitê de compra (estagiário, assistente júnior)
- Países fora do seu mercado

### 4. ABM (Account-Based Marketing)

Se o seu produto vende pra contas nominais (Tier 1 de 200 empresas alvo), use:

**Matched Audience > Company List**: sobe CNPJ/nome/URL das empresas-alvo. LinkedIn tenta dar match. Match rate tipicamente 40-60%.

Combina com:
- Job Title ou Seniority alvo (decisor dentro da empresa)
- Copy nominal ("Oi time da [Empresa], vi que vocês...") pra ads 1-to-few

### 5. Bid strategy

LinkedIn tem:
- **Maximum Delivery**: gasta o budget. Usa quando campanha validada e objetivo é escala.
- **Manual Bidding (CPC ou CPM)**: controle maior. Usa pra testar criativo sem queimar.
- **Target Cost**: similar a tCPA, mas precisa de volume de conversão.

Default: começa **Manual CPC** em campanha nova, migra pra **Maximum Delivery** depois que tiver sinal.

### 6. Budget mínimo realista

- Campanha com Job Title específico + Company Size: **mínimo R$ 200/dia** pra sair de "Limited" e ter volume razoável
- ABM Matched Audience: **mínimo R$ 100/dia** (audiência é menor mesmo)
- Campanha generalista: **mínimo R$ 500/dia** pra competir em leilão

## Copy LinkedIn

- **Introductory text**: 150 caracteres recomendado (pode ir até 600)
- **Headline**: 70 caracteres
- **CTA**: opções padrão (Learn more, Download, Register, Sign up)

Tom LinkedIn:
- Não vende, educa
- Usa número real e case
- Evita hype e "mudando o mercado"
- Audiência sênior responde a contraste e provocação respeitosa, não a "10 dicas"

## Document Ads (formato forte)

Document Ads permite subir PDF/deck que o usuário visualiza sem sair do LinkedIn. Precisa preencher Lead Gen Form depois das primeiras 2 páginas pra continuar.

Funciona bem com:
- Guia prático ("10 perguntas pra fazer no próximo one-on-one")
- Checklist ("Checklist de onboarding de funcionário")
- Dataset ("Benchmark de eNPS no setor de tecnologia")

**Conteúdo fraco não salva.** O documento tem que ter valor autônomo.

## Ações operacionais

### Subir campanha

Confirmar com usuário:
- Campaign Group (existe ou cria novo)
- Formato
- Targeting (Job Title, Company Size, Industry, Geo)
- Exclusões
- Budget diário
- Criativo (imagem + copy) e URL de destino

```bash
python api/linkedin-ads/create_campaign_group.py \
  --name "Q1 2026 - Demand Gen"

python api/linkedin-ads/create_campaign.py \
  --group-id 123456 \
  --name "Heads of RH - Company Size 100-500 - Sponsored Content" \
  --type SPONSORED_UPDATES \
  --daily-budget 20000
```

### Análise

```bash
python api/linkedin-ads/read_analytics.py --days 30
```

## Sinais de problema

- CTR < 0.4% em Sponsored Content: copy fraco ou targeting amplo demais
- Lead Gen Form com taxa alta de preenchimento mas baixa qualidade: falta pergunta-filtro ou audiência descalibrada
- Audience size "Limited" vermelho: muito restrito. Relaxe 1 facet.
- Custo por lead subindo após 30 dias sem mudança: fadiga de criativo (veja skill `creative-fatigue`)

## O que NÃO fazer

- Não usa só Skill como targeting (ruído)
- Não cria Lead Gen Form sem pergunta-filtro (Company Size é quase sempre a mais útil)
- Não vira ad texto corrido sem quebra (ninguém lê)
- Não usa "Click Bait". LinkedIn audiência sênior pune clickbait com ignore ou report
- Não ignora exclusão de clientes atuais e concorrentes (gasto inútil)
- Não desista depois de 7 dias. LinkedIn leva 14-21 dias pra otimizar em conversões.

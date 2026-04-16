---
name: ads-google
description: Estratégia e operação de Google Ads (Search, Performance Max, Display, Brand). Cobre estrutura de campanha, naming, bid strategies, keywords e match types, quando usar cada tipo de campanha. Use quando o usuário pedir algo sobre Google Ads.
---

# ads-google

Google Ads é intent-heavy: a pessoa está buscando algo ativamente. Campanhas bem feitas pegam demanda existente; mal feitas, queimam budget em busca genérica.

## Quando esta habilidade é acionada

Qualquer pergunta envolvendo:
- Criar/alterar campanha no Google Ads
- Keywords, match types, negativações
- Bid strategy (Max Conversions, tCPA, Target Impression Share, Manual CPC)
- Performance Max (PMax)
- Brand defense (proteger busca pelo próprio nome)
- Análise de performance Google

## Princípios

### 1. Um objetivo por campanha

Nunca misture intent diferente na mesma campanha. Separe por:

- **Intent principal** (ex: "diagnosticar clima organizacional", "comparar ferramentas")
- **Estágio do funil** (awareness: "o que é X"; consideração: "melhor X"; decisão: "X vs Y")
- **Brand vs Non-brand** (sempre separado)

Exemplo de estrutura pra AcmeRH:

| Campanha | Intent | Bid strategy |
|----------|--------|--------------|
| AcmeRH - Brand | Defende busca pelo nome | Target Impression Share 90% |
| AcmeRH - Clima Organizacional | "pesquisa de clima" e variações | Max Conversions com tCPA |
| AcmeRH - Engajamento | "engajamento de funcionários" | Max Conversions com tCPA |
| AcmeRH - Feedback Contínuo | "software de feedback" | Max Conversions com tCPA |
| AcmeRH - Concorrentes | "feedz", "teamculture" (busca de alternativa) | Manual CPC, lance baixo |

### 2. Naming convention

Padrão sugerido:

```
[Marca] - [Categoria] - [Geo] - [Idioma]
```

Exemplo: `AcmeRH - Clima Organizacional - BR - PT`

Dentro da campanha, ad groups:

```
[Tema] - [Match type principal]
```

Exemplo: `Pesquisa de Clima - Phrase`

### 3. Match types

- **Broad match**: só com audience signal forte E tCPA apertado. Sem isso, queima.
- **Phrase match**: default pra maioria dos casos. Controle decente, volume razoável.
- **Exact match**: intent alta, pouca variação, high-value. Brand é sempre exact.

### 4. Bid strategy por objetivo

| Campanha | Bid strategy recomendada | Por quê |
|----------|-------------------------|---------|
| Brand | Target Impression Share 90%+ | Presença, não conversão. Impedir que concorrente compre teu nome. |
| Non-brand conversão | Max Conversions com tCPA | O Google otimiza bid automaticamente. Precisa ter conversão configurada. |
| Non-brand awareness | Target CPM ou Manual CPC | Se o objetivo é ver marca, não conversão |
| Concorrentes | Manual CPC baixo | Não queima se não vence leilão; serve pra capturar "alternativa a" |
| Remarketing | Max Conversions | Retargeting de visitantes da LP |

**Regra importante**: nunca use Max Conversions SEM tCPA. Sem limite, a plataforma gasta o que o budget deixar sem se importar com CAC.

### 5. Performance Max (PMax)

PMax é Google IA rodando em todos os canais (search, display, YouTube, Gmail, Maps) com você dando asset (texto, imagem, vídeo) e audience signal.

**Quando usa PMax:**
- Você tem audience signal forte (lista de clientes, conversões recorrentes)
- tCPA apertado pra servir de freio
- Conta com histórico decente de conversão (min 30 conversões/mês pra dar sinal)

**Quando NÃO usa:**
- Começando do zero (vai servir ad em display ruim e queimar)
- Sem conversão configurada
- Produto B2B nicho (PMax tende a otimizar pra volume de clique, não pra qualidade do lead)

No histórico da AcmeRH (ver `knowledge/ads-history.md`), PMax falhou 2x. Default é não usar sem razão forte.

### 6. Keywords e negativações

**Pra escolher keywords iniciais:**

1. Leia `knowledge/product.md` (o que faz) e `knowledge/positioning.md` (como o cliente busca)
2. Comece com 10 a 15 keywords phrase match
3. Use o Google Ads Keyword Planner pra estimar volume
4. Evite keywords super amplas ("RH", "software", "gestão"). Elas atraem TUDO.

**Negativações iniciais** (importa MUITO):

- Termos gratuitos: `grátis`, `free`, `download grátis`, `apostila`, `pdf`
- Termos acadêmicos: `tcc`, `monografia`, `artigo`, `universidade`, `curso`
- Termos de emprego: `vaga`, `currículo`, `emprego`, `clt`
- Concorrente que compra tráfego cruzado: conferir lista em `knowledge/ads-history.md`
- Intent errada: pra AcmeRH, `folha de pagamento`, `ponto eletrônico`, `ats` são negativados (não somos isso)

**Dica**: mantenha lista de negativações em `api/google-ads/assets/negative-keywords.txt` pra reusar entre campanhas.

## Ações operacionais

### Subir campanha nova

Pede pro usuário confirmar:
- Nome da campanha (com padrão)
- Budget diário
- Bid strategy e tCPA
- Lista de keywords
- Lista de negativações
- Copy (15 headlines + 4 descriptions pra responsive search)
- URL final

Depois roda:
```bash
python api/google-ads/create_search_campaign.py \
  --name "AcmeRH - Clima Organizacional - BR - PT" \
  --budget 100 \
  --bid-strategy MAXIMIZE_CONVERSIONS \
  --target-cpa 60000000 \
  --keywords keywords.txt \
  --negatives negatives.txt
```

(`target-cpa` em micros, 60000000 = R$ 60)

Nunca rode sem confirmação.

### Auditar performance

Sem entrar em detalhe técnico (é a skill `search-terms-pruning`), o básico:

```bash
python api/google-ads/read_performance.py --days 30
```

Retorna por campanha: gasto, conversões, CAC, CTR, conv rate.

## Limites técnicos da plataforma (respeitar sempre)

- Headline: 30 caracteres
- Description: 90 caracteres
- Mínimo 3 headlines e 2 descriptions pra responsive search ad
- Máximo 15 headlines e 4 descriptions

## Sinais de problema em campanha Google

- CTR < 2% em search: copy ruim ou keyword mal escolhida
- Impressão alta com clique baixo: audiência errada ou copy não bate com busca
- Gasto alto com 0 conversão (>7 dias): pausa ou diagnostica
- Quality Score < 5: pausa, revisa landing page, expectativa de busca vs página

## O que NÃO fazer

- Não usa Max Conversions sem tCPA (explica CAC)
- Não mistura brand e non-brand na mesma campanha
- Não ativa PMax sem conversão histórica decente
- Não cria 1 campanha com 20 ad groups de temas diferentes (vira caos de bid)
- Não esquece de ativar tracking de conversão ANTES de subir a campanha
- Não compra nome de concorrente sem ler termos de serviço da plataforma (pode levar ao bloqueio em alguns mercados)

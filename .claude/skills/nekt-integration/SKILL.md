---
name: nekt-integration
description: Como conectar o MCP da Nekt no Claude Cowork ou Claude Code, e como usar pra puxar dados do CRM, ads e produto que o usuário conectou na Nekt. Inclui queries SQL prontas pra perguntas comuns (CAC real, ICP por dado, performance cross-canal). Use quando o usuário tiver MCP Nekt conectado ou quiser conectar.
---

# nekt-integration

A Nekt é uma plataforma de integração de dados. O usuário conecta as fontes dele (HubSpot, Salesforce, Google Ads, Meta, LinkedIn, Pipedrive, ActiveCampaign, Stripe, etc.) e tudo fica disponível pro Claude consultar via SQL através do servidor MCP.

No contexto deste projeto, o MCP da Nekt vira o "atalho" pra responder perguntas com dado real, sem o usuário precisar exportar CSV de cada plataforma.

## Quando esta habilidade é acionada

- Usuário menciona "conectar a Nekt" ou pergunta como integrar
- Usuário quer puxar dado real (CAC, deals, performance) e o assistente precisa decidir se vai via MCP ou pede CSV
- Pergunta complexa que envolve cruzar fontes (ex: "deals fechados que vieram do Google" cruza HubSpot com Google Ads)
- Usuário quer atualizar `knowledge/icp.md`, `knowledge/ads-history.md` com base em dados reais

## Como conectar (passo a passo)

### No Claude Cowork

1. Abre o Cowork
2. Vai em **Configurações > Conectores (MCP)**
3. Clica em **Adicionar conector**
4. Escolhe "Custom MCP" e adiciona URL: `https://mcp.nekt.com/mcp`
5. Faz o fluxo OAuth (login na conta Nekt)
6. Quando conectado, ícone fica verde

### No Claude Code

Edita `~/.claude.json` (Mac/Linux) e adiciona o servidor MCP:

```json
{
  "mcpServers": {
    "nekt": {
      "type": "http",
      "url": "https://mcp.nekt.com/mcp"
    }
  }
}
```

Reinicia o Claude Code. Confirma com:

```
/mcp
```

Deve listar `nekt` como conectado.

## Pré-requisito do lado da Nekt

Antes de o MCP servir dados, o usuário precisa:

1. Ter conta gratuita em [nekt.com](https://nekt.com)
2. Conectar pelo menos 1 fonte de dado (CRM, ads, produto)
3. Aguardar o sincronismo inicial (depende da fonte, geralmente 1 a 4 horas)

## Como descobrir o que está disponível

Antes de rodar query, descubra schema:

> Use o MCP da Nekt. Lista as tabelas disponíveis nos schemas `raw` e `trusted`.

Tipicamente o usuário tem:
- `raw.hubspot.contacts`, `raw.hubspot.deals`, `raw.hubspot.companies`
- `raw.google_ads.campaigns`, `raw.google_ads.ad_groups`, `raw.google_ads.search_terms`
- `raw.meta_ads.campaigns`, `raw.meta_ads.adsets`, `raw.meta_ads.ads`
- `raw.linkedin_ads.campaigns`, `raw.linkedin_ads.creatives`
- `trusted.deals`, `trusted.contacts` (já tratados, schema mais limpo)

Schemas variam por conta. Sempre confira primeiro.

## Queries prontas pra perguntas comuns

### CAC real por canal (últimos 90 dias)

> Use o MCP da Nekt. Calcula CAC real por canal pros últimos 90 dias:
>
> ```sql
> WITH spend_por_canal AS (
>   SELECT 'google_ads' as canal, SUM(cost_micros / 1e6) as gasto
>   FROM raw.google_ads.campaign_performance
>   WHERE date >= current_date - 90
>   UNION ALL
>   SELECT 'meta_ads', SUM(spend) FROM raw.meta_ads.insights
>   WHERE date_start >= current_date - 90
>   UNION ALL
>   SELECT 'linkedin_ads', SUM(cost_in_local_currency) FROM raw.linkedin_ads.analytics
>   WHERE date_range_start >= current_date - 90
> ),
> deals_por_canal AS (
>   SELECT
>     COALESCE(properties.hs_analytics_source, 'unknown') as canal,
>     COUNT(*) as deals
>   FROM raw.hubspot.deals
>   WHERE properties.dealstage IN ('closedwon')
>     AND properties.closedate >= current_date - 90
>   GROUP BY 1
> )
> SELECT
>   s.canal,
>   s.gasto,
>   COALESCE(d.deals, 0) as deals,
>   s.gasto / NULLIF(d.deals, 0) as cac_real
> FROM spend_por_canal s
> LEFT JOIN deals_por_canal d ON s.canal = d.canal;
> ```
>
> Adapta os nomes de tabela ao schema disponível.

### Análise de ICP via clientes fechados

> Use o MCP da Nekt. Pega clientes que fecharam nos últimos 12 meses cruzados com a tabela de empresas. Mostra distribuição por:
> - Setor
> - Tamanho (faixa de funcionários)
> - Geografia
> - Ticket mensal
>
> Filtra os 20% com maior LTV (ticket × meses ativos). Compara com `knowledge/icp.md` Tier 1 e me diz onde a hipótese está errada.

### Pruning de search terms cruzado com deals

> Use o MCP da Nekt. Pega search terms do Google Ads dos últimos 90 dias. Pra cada term, traz:
> - Gasto total
> - Cliques
> - Conversões reportadas pelo Google
> - Deals fechados que tiveram esse term como `utm_term` no primeiro touchpoint
>
> Lista os termos com gasto > R$ 500 e zero deal fechado real (ignora a conversão do Google se ela não corresponde a deal). São candidatos a negativação.

### Quais cargos respondem mais ao LinkedIn

> Use o MCP da Nekt. Cruza leads do HubSpot que vieram de `utm_source=linkedin` com os deals fechados. Agrupa por cargo (`properties.jobtitle`) e mostra:
> - Total de leads
> - Total convertido em deal
> - Taxa de conversão
>
> Mostra top 10 cargos por taxa de conversão (mínimo 5 leads pra entrar na lista).

### Calcular ROI de canal de awareness (incremental)

> Use o MCP da Nekt. Pega gasto em LinkedIn dos últimos 6 meses, mês a mês. Cruza com volume de buscas brand no Google Ads (search terms que contém o nome da empresa) no mesmo período. Roda correlação simples. Quanto cada R$ 1k em LinkedIn gera de busca brand no Google?

## Boas práticas usando o MCP

1. **Sempre olhe o schema antes de assumir nome de tabela**. Cada conta tem o seu.
2. **Filtre por data sempre** (últimos 30/90/365 dias). Evita query gigante.
3. **Use `trusted.*` quando disponível**, é mais limpo que `raw.*`.
4. **Cache local em CSV** se for análise recorrente. MCP query toda vez gasta tempo.
5. **Combine com o histórico** em `knowledge/ads-history.md`. O MCP mostra o "agora", o arquivo mostra a "memória".

## Quando NÃO usar o MCP

- Pergunta puramente conceitual ("o que é CTR")
- Geração de copy (não precisa de dado pra escrever bom anúncio)
- Análise de tendência muito antiga (anterior à conexão da fonte)
- Quando o usuário quer um número específico que ele já sabe (mais rápido perguntar)

## Se o MCP falhar

1. Confere se a conta Nekt está ativa (login em [nekt.com](https://nekt.com))
2. Confere se a fonte específica que você está consultando está conectada e sincronizada
3. Tenta query simples primeiro (`SELECT 1`) pra confirmar que o MCP responde
4. Se a fonte está OK mas o MCP retorna timeout, simplifica a query (menos joins, filtra mais)

## Contar pro Claude o que é a Nekt (recomendado)

Mesmo conectado, o Claude se beneficia de saber **o que** é a Nekt e **por que** ele tem acesso a esses dados. Sem esse contexto, ele pode subutilizar a integração.

No primeiro prompt de cada sessão (ou no `CLAUDE.md` se tiver), inclui:

> A Nekt é a plataforma de integração de dados que eu uso. Ela conecta meu CRM (HubSpot), minhas plataformas de ads (Google, Meta, LinkedIn) e meu produto (eventos do app). Você tem acesso a tudo isso via MCP. Sempre que precisar de dado real pra responder, prefira consultar a Nekt em vez de me pedir CSV. Schema disponível: `raw.*` (dados crus) e `trusted.*` (dados tratados).

Isso instrui o assistente a usar o MCP por default, ao invés de pedir export manual.

## Atualização de `knowledge/` com dado real

Toda vez que rodar análise relevante via MCP, ofereça atualizar o knowledge file correspondente:

- Análise de ICP → atualiza `knowledge/icp.md`
- Análise de CAC por canal → atualiza `knowledge/ads-history.md`
- Análise de LTV → atualiza `knowledge/pricing.md` (se mudou significativamente)

Sempre confirma com o usuário antes de aplicar Edit.

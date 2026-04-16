---
name: ads-attribution
description: Como atribuir conversões aos canais de ads corretamente. Cobre UTMs, last-click vs data-driven vs MMM, view-through, cross-device, e por que o número da plataforma nunca bate com o CRM. Use quando o usuário quiser calcular CAC real, comparar canais ou diagnosticar discrepância entre plataforma e CRM.
---

# ads-attribution

Atribuição é como você decide qual canal levou o crédito de uma conversão. Plataformas infere (cada uma com lógica própria, geralmente generosa pra ela mesma); o CRM do usuário é quem tem a verdade.

Sem atribuição honesta, é impossível alocar budget com inteligência.

## Quando esta habilidade é acionada

- Usuário pergunta "qual canal está trazendo mais cliente"
- Plataforma diz que gerou N leads mas CRM tem número diferente
- Usuário quer calcular CAC real por canal
- Usuário quer decidir se pausa/expande canal
- Implementar ou auditar UTMs

## Conceitos-chave

### Last-click (modelo mais comum, mas não o melhor)

Dá 100% do crédito pro último canal antes do lead/compra. Simples, mas penaliza topo de funil (LinkedIn que gerou awareness, Google que capturou a demanda) pra favorecer retargeting e brand search.

### First-click

Dá 100% pro primeiro. Bom pra ver o que gera descoberta, ruim pra decidir gasto de conversão.

### Multi-touch (linear, time-decay, position-based)

Distribui o crédito entre todos os touchpoints. Mais justo, mas exige que você consiga trackear a jornada (precisa cookie/ID cross-session).

### Data-driven attribution (Google Analytics 4)

ML decide como distribuir o crédito com base em padrões. Exige volume mínimo.

### Marketing Mix Modeling (MMM)

Análise estatística do gasto total por canal vs receita total ao longo do tempo. Não depende de cookie/ID. Precisa de volume e histórico (pelo menos 12 meses).

### View-through (Meta principalmente)

Conta como atribuição mesmo se a pessoa só **viu** o ad (não clicou). Infla número do Meta. No seu CRM, só vai ver click-through.

## Por que o número da plataforma nunca bate com o CRM

Razões comuns:

1. **Plataforma usa view-through**, CRM usa click-through
2. **Plataforma usa last-touch dentro dela**, CRM usa last-touch geral
3. **Plataforma conta conversão auto-reportada pelo usuário** ("fiz um cadastro"), CRM conta só deal fechado
4. **Cross-device**: plataforma faz match cross-device (Meta com login, Google com cookie), CRM só tem um device
5. **Janela de atribuição diferente**: Meta default 7 dias click + 1 dia view; Google 30-90 dias click; CRM conforme você configura

**Regra**: o CRM é a fonte de verdade. A plataforma é estimativa útil.

## Implementação de UTMs

Toda URL de ad deve carregar UTMs. Padrão recomendado:

```
https://site.com/landing?
  utm_source=google
  &utm_medium=cpc
  &utm_campaign=acmerh-clima-br
  &utm_content=responsive-search-ad-a
  &utm_term={keyword}
  &gclid={gclid}
```

Facetas:
- **utm_source**: `google`, `meta`, `linkedin`, `newsletter`, `partner`
- **utm_medium**: `cpc` (busca paga), `paid-social`, `display`, `email`, `organic` (não usa em ad)
- **utm_campaign**: nome da campanha no padrão interno
- **utm_content**: variante de criativo ou ad
- **utm_term**: termo de busca (Google). LinkedIn e Meta usa pra cargo ou audiência.

**Use dynamic parameters** da plataforma pra auto-popular (ex: `{keyword}` no Google Ads, `{{ad.id}}` no Meta).

## Cálculo de CAC real (o que importa)

Se o MCP da Nekt está conectado:

> Use o MCP da Nekt. Pega:
> - Deals closed-won dos últimos 90 dias (de `hubspot.deals`)
> - Pra cada deal, o primeiro touchpoint e o último (de `hubspot.contacts` com campos `hs_analytics_source`, `hs_analytics_source_data_1`, etc.)
> - Gasto de ads do mesmo período, por canal (das fontes `google_ads.campaigns`, `meta_ads.campaigns`, `linkedin_ads.campaigns`)
>
> Calcula:
> 1. CAC last-touch por canal
> 2. CAC first-touch por canal
> 3. Razão LTV/CAC por canal (assuma LTV de `knowledge/pricing.md`)
> 4. Diferença entre o que a plataforma reporta como conversão e o que seu CRM reporta

Sem MCP, pede pro usuário exportar:
- CSV de deals closed-won com `hs_analytics_source` ou equivalente
- CSV de gasto por canal (das 3 plataformas)

E cruza manualmente.

## Regra simples pra decidir se um canal vale

Pra cada canal, calcule **LTV/CAC**:

- LTV/CAC > 3: saudável, pode expandir
- LTV/CAC 2-3: aceitável, otimiza antes de expandir
- LTV/CAC < 2: desliga ou reestrutura

Use o **CAC real do CRM**, não o que a plataforma reporta.

## Cuidados

### iOS 14.5+ (Meta principalmente)

Pixel do Meta perdeu precisão desde iOS 14.5. Compensa ativando **Conversion API** (server-side) pra enviar eventos direto do servidor ao Meta. Precisa do time de dev.

### Google Consent Mode v2 (Europa especialmente)

Se você mira Europa/UK, tem que implementar Consent Mode. Sem isso, bid strategies do Google ficam cegas.

### Cookie de terceiros

Está sendo depreciado. Atribuição multi-device/multi-browser fica cada vez mais difícil. MMM e server-side tracking ganham relevância.

## Cross-canal: o problema real

Se você roda LinkedIn (awareness) + Google (demand capture), o cliente típico:

1. Vê ad no LinkedIn, marca a empresa
2. Dias depois, busca no Google, clica no ad
3. Converte

Last-click dá 100% pro Google. First-click dá 100% pro LinkedIn. A verdade é que os dois contribuíram.

**Solução pragmática** (sem MMM completo):
- Pra decisões de budget, olhe CAC last-click MAS considere ROI do canal de awareness como "assist"
- Roda experimentos: pausa LinkedIn por 4 semanas, mede queda em conversão Google last-click. A queda é a contribuição indireta.

## O que NÃO fazer

- Não acredite cegamente no número da plataforma. Ele existe pra te fazer gastar mais.
- Não compare ROI de plataformas entre si usando o número delas. Cada uma usa janela e modelo diferente.
- Não esqueça de UTM em nenhum ad. Link sem UTM é atribuição perdida.
- Não pause canal de awareness olhando só last-click. Faça o experimento de "pausa e vê o que cai" antes.
- Não confunda "canal trouxe o clique" com "canal trouxe o cliente". Clique é barato, cliente é caro.

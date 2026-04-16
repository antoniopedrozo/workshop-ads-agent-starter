---
name: creative-fatigue
description: Detecta fadiga de criativo no Meta e LinkedIn (CTR caindo, CPM subindo, frequency alto) e sugere quando trocar. Cobre métricas de alerta, cadência de teste de novo criativo e bibliotecas de inspiração. Use quando performance estiver decaindo sem mudança de targeting/budget.
---

# creative-fatigue

Criativo em mídia paga tem prazo de validade. Quanto mais a mesma pessoa vê o mesmo ad, menos ela engaja. Essa é a fadiga de criativo. Detectar cedo evita queima de budget em ad que já não funciona.

## Quando esta habilidade é acionada

- CTR caindo ao longo de semanas sem mudança em targeting
- CPM subindo na mesma audiência
- Frequency > 3 em 7 dias (Meta, LinkedIn)
- Custo por resultado subindo gradualmente
- Cadência preventiva mensal

## Métricas de alerta (Meta e LinkedIn)

| Métrica | Sinal verde | Sinal amarelo | Sinal vermelho |
|---------|-------------|---------------|----------------|
| **Frequency 7d** (Meta) | < 1.5 | 1.5 - 3 | > 3 |
| **CTR vs baseline** | dentro de ±10% | -10% a -25% | < -25% |
| **CPM vs baseline** | dentro de ±10% | +10% a +30% | > +30% |
| **CPL/CAC tendência** | estável ou caindo | subindo gradualmente | subindo +30% em 14 dias |
| **Engagement rate** (LinkedIn) | dentro de ±10% | -10% a -25% | < -25% |

Quando 2+ métricas estão amarelas OU 1+ vermelha: hora de substituir criativo.

## Por que fadiga acontece

1. **Saturação da audiência**: a mesma audiência viu o ad várias vezes. Eficácia cai.
2. **Concorrência**: mais anunciantes mirando a mesma audiência, leilão fica caro.
3. **Sazonalidade**: feriados, mudança de comportamento de consumo.
4. **Mudança no algoritmo**: plataforma muda lógica de delivery.

A 1 (saturação) é a mais comum e a única que **substituir criativo resolve**. As outras 3, troca de criativo ajuda menos.

Diagnóstico rápido: se frequency > 3 e CTR caindo, é fadiga. Se frequency baixa mas CPM subindo, é provavelmente leilão competitivo.

## Workflow recorrente

### 1. Cadência de revisão

- Semanal: olhar frequency e CTR do top 5 criativos por gasto
- Quinzenal: gerar lista de criativos a substituir
- Mensal: lançar lote novo de criativos (3-5 variações)

### 2. Pega os números

Meta:
```bash
python api/meta-ads/read_insights.py \
  --level ad \
  --days 14 \
  --fields ad_id,ad_name,impressions,clicks,ctr,cpm,frequency,spend
```

LinkedIn:
```bash
python api/linkedin-ads/read_analytics.py \
  --pivot CREATIVE \
  --days 14
```

### 3. Análise assistida

Pede pro Claude:

> Leu o output da última análise (anexo). Pra cada criativo ativo:
> 1. Compara as métricas dos últimos 14 dias com os 14 anteriores
> 2. Classifica: SAUDÁVEL, ATENÇÃO, FADIGA
> 3. Pra os em FADIGA, sugere o que substituir e quando (essa semana, semana que vem)
> 4. Recomenda 3 ângulos de novo criativo baseado em `knowledge/positioning.md` e nos JTBD descritos lá

### 4. Substituir, não pausar de uma vez

Boa prática:
- Mantém o ad antigo rodando enquanto sobe o novo
- Deixa rodar em paralelo por 7 dias
- Se o novo bate o antigo: pausa o antigo
- Se o novo é pior: pausa o novo, investiga por quê

### 5. Documentar resultado

Atualiza `knowledge/ads-history.md` na seção do canal correspondente, marcando:
- O que pausou e por quê
- O que entrou e qual era a hipótese

## Cadência sugerida de novos criativos

| Canal | Cadência mínima | Volume por lote |
|-------|----------------|-----------------|
| Meta (Reels, feed) | A cada 2-3 semanas | 3-5 variações |
| Meta (Stories) | A cada 2 semanas | 2-3 variações |
| LinkedIn Sponsored Content | A cada 4-6 semanas | 2-3 variações |
| LinkedIn Document Ads | A cada 6-8 semanas (conteúdo demora pra fadigar) | 1-2 variações |
| LinkedIn Message Ads | A cada 4 semanas | 2 variações |

## Ângulos de criativo pra evitar fadiga

Em vez de variar só headline/cor, varie a estrutura:

1. **Dor/problema** ("Você ainda monta planilha pra...")
2. **Resultado/promessa** ("Ela cancelou no final do mês...")
3. **Prova social/case** ("A Empresa X reduziu turnover em 18%")
4. **Comparação** ("Vs planilha + Google Forms")
5. **Educacional** ("3 perguntas que todo Head de RH faz no pulse")
6. **UGC/depoimento** (vídeo no celular do cliente real)
7. **Provocação** ("A pesquisa de clima que sua empresa fez é teatro?")
8. **Bastidores** ("Como a gente desenhou as perguntas do pulse")

Mantém uma biblioteca de criativos passados em `assets/creatives/` (não versionado se for arquivo grande, mas um índice em CSV ajuda).

## Sinais de que NÃO é fadiga (e sim outra coisa)

- CTR caiu de uma vez (não gradual): provável mudança de audiência ou problema de tracking
- Frequency baixo mas CPM alto: leilão concorrido, não fadiga
- CPL alto mas CTR estável: problema na landing page, não no ad
- Performance variando dia a dia sem padrão: amostra pequena, aguarda mais dados

## O que NÃO fazer

- Não pausa criativo sem ter substituto pronto (perde delivery acumulado)
- Não troca tudo de uma vez (perde sinal histórico de comparação)
- Não ignora frequency, é o sinal mais antecipado de fadiga
- Não confunde fadiga com problema de targeting (faz o diagnóstico antes)
- Não desmereça o trabalho do criativo anterior. Foi bom enquanto foi.

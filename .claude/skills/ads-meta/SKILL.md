---
name: ads-meta
description: Estratégia e operação de Meta Ads (Facebook e Instagram). Cobre estrutura campaign > adset > ad, objetivo, targeting, criativo, fluxo awareness vs conversion e regras específicas pra B2B. Use quando o usuário pedir algo sobre Meta Ads.
---

# ads-meta

Meta Ads é interrupção: a pessoa está scrolando, não buscando. Ganha quem para o scroll e entrega a mensagem em 3 segundos. Estruturalmente mais simples que Google, mas criativo pesa muito mais.

## Quando esta habilidade é acionada

Qualquer pergunta envolvendo:
- Criar/alterar campanha no Meta (Facebook + Instagram)
- Adsets, targeting, lookalike, custom audience
- Criativo (imagem, carousel, vídeo, reel)
- CBO vs ABO (budget no campaign vs adset)
- Análise de performance Meta

## Estrutura Meta (3 níveis)

```
Campanha         → objetivo (Conversion, Traffic, Awareness, Lead)
  └ Adset        → targeting, budget, schedule, placement
      └ Ad       → criativo (imagem/vídeo), texto, CTA
```

Você pode ter múltiplos adsets por campanha (pra testar targeting) e múltiplos ads por adset (pra testar criativo).

## Princípios

### 1. Objetivo de campanha certo

- **Conversions**: você tem Pixel/Conversion API configurado E histórico de pelo menos 50 conversões/semana. Default pra B2C e pra B2B com funil curto.
- **Lead Generation**: usa formulário dentro do Meta (Lead Gen Form). Bom pra B2B onde usuário resiste a sair da plataforma.
- **Traffic**: só se você ainda não tem volume pra Conversions. Otimiza pra clique, não pra lead.
- **Awareness**: só com motivo forte (lançamento de marca, institucional). Meta gera CPM barato otimizando pra quem olha o ad, mas não pra quem converte.
- **Engagement**: não recomendamos pra gerar lead. Atrai curtida de conta fake.

### 2. CBO (Campaign Budget Optimization) vs ABO (Ad Set Budget Optimization)

- **CBO**: budget no nível da campanha, Meta distribui entre adsets. Default pra campanhas já validadas.
- **ABO**: budget por adset. Use quando você está testando targeting e quer garantir volume equalizado entre eles.

Começa ABO pra descobrir targeting vencedor; migra pra CBO depois que valida.

### 3. Targeting

Tipos de audiência:

- **Cold prospecting (interesses, comportamentos)**: em B2B, use com cuidado. Meta não tem a mesma granularidade do LinkedIn.
- **Custom Audience**: lista que você sobe (CRM, lista de clientes, visitantes da LP via Pixel)
- **Lookalike (LAL)**: Meta gera audiência parecida com Custom Audience. 1% é mais próximo, 5-10% é mais amplo.

**Pra B2B**, ordem de preferência de volume:

1. Retargeting de visitantes da LP (quente, converte melhor)
2. Lookalike de clientes fechados (não de leads, que tem ruído)
3. Interesses + comportamento (frio, CAC mais alto)

### 4. Criativo

Meta é criativo-driven. Regras:

- **Primeiros 3 segundos**: pra vídeo, se não parou o scroll nos 3 primeiros segundos, perdeu
- **Legenda curta**: 80% das pessoas não lê mais que as 3 primeiras linhas. Coloque o gancho no início.
- **Formato**: Reels e Stories tem CPM mais baixo e performam melhor que feed, em geral
- **UGC (user-generated content)**: em B2B, depoimento real de cliente (mesmo gravado no celular) bate criativo de agência
- **Texto na imagem**: Meta já não pune mais tanto como antes, mas menos texto ainda performa melhor

### 5. Copy Meta

- **Headline**: 40 caracteres
- **Primary text**: 125 caracteres recomendado (pode ir até 2200, mas corta no mobile)
- **Description**: 30 caracteres
- **CTA**: escolha entre opções padrão ("Saiba mais", "Cadastre-se", "Baixar", etc.)

Tom pra B2B:
- Fala em negócio, não em feature
- Usa dor específica em vez de solução genérica
- Prova social (número, case) aumenta CTR

## Meta pra B2B: cuidado

Meta é canal de **volume**, não de precisão. Pra B2B nicho, CAC tende a ser mais alto que Google e LinkedIn.

No histórico da AcmeRH (ver `knowledge/ads-history.md`):
- Retargeting funciona como assist
- Prospecting cold em B2B falhou, CAC > R$ 80k

**Regra pra decidir se Meta vale:**

- Teste 90 dias com budget 10-15% do total
- Se CAC > 2x do canal mais barato (Google geralmente), desliga
- Se CAC < 1.5x, mantém como diversificação
- Se CAC = outros canais, expande

## Ações operacionais

### Subir campanha nova

Confirmar com usuário:
- Objetivo da campanha (Conversion, Lead, Traffic)
- Audiência (Custom, Lookalike, Interest-based)
- Budget diário e duração
- Criativo (imagem/vídeo e copy)
- Placement (auto ou manual)

Depois:
```bash
python api/meta-ads/create_campaign.py \
  --name "AcmeRH - Retargeting - LP Clima" \
  --objective CONVERSIONS \
  --status PAUSED
```

Sempre cria campanha pausada. Usuário revisa no Ads Manager antes de ativar.

Depois:
```bash
python api/meta-ads/create_adset.py \
  --campaign-id 120150000000000 \
  --name "Adset - LAL 1% clientes" \
  --daily-budget 5000 \
  --custom-audience-id ... \
  --optimization-goal OFFSITE_CONVERSIONS
```

(daily-budget em cents, 5000 = R$ 50,00)

### Upload de criativo

```bash
python api/meta-ads/upload_creative.py --image path/to/image.jpg
```

Retorna `image_hash` pra referenciar em `create_ad.py`.

### Análise de insights

```bash
python api/meta-ads/read_insights.py --level adset --days 30
```

## Sinais de problema

- Frequency > 3 em 7 dias: criativo está sendo visto muitas vezes, vai fadigar. Substitui.
- CPM alto com CTR baixo: criativo ruim ou audiência errada. Teste novo criativo antes de mudar targeting.
- Muitos leads de baixa qualidade via Lead Gen Form: adiciona pergunta-filtro no form (tamanho da empresa, cargo)
- Custo por resultado subindo ao longo do tempo sem mudança: pode ser fadiga. Veja skill `creative-fatigue`.

## O que NÃO fazer

- Não ativa campanha sem Pixel/Conversion API funcionando
- Não usa audiência < 1.000 pessoas (Meta avisa "audience too narrow")
- Não sobrepõe adsets com mesma audiência na mesma campanha (auction entre si)
- Não mistura cold e warm no mesmo adset (diluição)
- Não acredita cegamente em "Meta says it's working" do Ads Manager. Atribuição Meta é liberal. Cruze com seu CRM via MCP da Nekt ou planilha pra ver CAC real.

# Meta Ads API Scripts

Scripts Python pra subir e operar campanhas no Meta (Facebook + Instagram) via Marketing API.

Todos os scripts:
- Leem credenciais do `.env`
- Usam o SDK oficial [`facebook-business`](https://github.com/facebook/facebook-python-business-sdk)
- Aceitam parâmetros via CLI

## Pré-requisito

- Business Manager verificado em https://business.facebook.com
- App Meta criado, com produto Marketing API adicionado
- System User com role Admin no ad account, com token gerado nos escopos `ads_management`, `ads_read`, `business_management`
- Variáveis no `.env`:
  ```
  META_APP_ID=
  META_APP_SECRET=
  META_ACCESS_TOKEN=
  META_AD_ACCOUNT_ID=act_...   # com prefixo act_
  ```

## Estrutura Meta

```
Campaign         (objetivo)
  └ Ad Set       (targeting, budget, schedule)
      └ Ad       (criativo)
```

Você sobe nessa ordem: criar Campaign → criar Ad Set vinculado à Campaign → fazer upload do criativo (imagem/vídeo) → criar Ad usando o Ad Set + Creative.

## Scripts disponíveis

| Script | O que faz |
|--------|-----------|
| `create_campaign.py` | Cria campanha com objetivo (Conversions, Leads, Traffic, etc.) |
| `create_adset.py` | Cria Ad Set vinculado à campanha (targeting, budget, schedule) |
| `upload_creative.py` | Sobe imagem ou vídeo, retorna hash/ID pra usar em ad |
| `create_ad.py` | Cria Ad usando Ad Set + Creative |
| `read_insights.py` | Puxa relatórios de performance |

## Convenções

### Valores em centavos

A API Meta usa centavos pra valores: 1 BRL = 100 cents.

Os scripts deste projeto fazem a conversão automaticamente quando você passa em reais (ex: `--daily-budget 50` vira `5000`).

### Status

Sempre crie campanha como `PAUSED`. Revise no Ads Manager e ative depois.

### Ad Account ID

Sempre com prefixo `act_`. Ex: `act_1234567890`.

## Exemplos

### Criar campanha de Conversions

```bash
python api/meta-ads/create_campaign.py \
  --name "AcmeRH - Retargeting LP Clima" \
  --objective OUTCOME_SALES \
  --status PAUSED
```

### Criar Ad Set

```bash
python api/meta-ads/create_adset.py \
  --campaign-id 120150000000000 \
  --name "Adset - LAL 1% clientes" \
  --daily-budget 50 \
  --optimization-goal OFFSITE_CONVERSIONS \
  --custom-audience-id 23850000000000 \
  --start-time "2026-04-20T10:00:00-0300"
```

### Upload de imagem

```bash
python api/meta-ads/upload_creative.py --image path/to/image.jpg
```

Retorna `image_hash` pra usar em `create_ad.py`.

### Criar Ad

```bash
python api/meta-ads/create_ad.py \
  --adset-id 12000000000 \
  --name "Ad v1 - depoimento texto" \
  --image-hash abc123def456 \
  --primary-text "Sua planilha de clima já não dá conta?" \
  --headline "Pulse direto no Slack" \
  --link "https://acmerh.com.br/clima" \
  --cta LEARN_MORE
```

### Insights

```bash
python api/meta-ads/read_insights.py --level adset --days 30
```

## Troubleshooting

- `(#100) Invalid parameter`: 99% das vezes é o ad account ID sem o prefixo `act_`.
- `(#190) Invalid OAuth access token`: token expirou ou foi revogado. Gera outro no Business Manager.
- `(#10) Permission denied`: o system user não tem permissão no ad account. Adicione no Business Manager > Users > System Users > Atribuir Ativo.
- `(#2641) Image hash not found`: a imagem não foi processada. Aguarde alguns segundos e tente de novo.

# LinkedIn Ads API Scripts

Scripts Python pra subir e operar campanhas no LinkedIn Campaign Manager via REST API.

LinkedIn não tem SDK Python oficial maintido, então usamos `requests` direto.

## Pré-requisito

- App LinkedIn com produtos `Marketing Developer Platform` e `Advertising API` aprovados
- Access token OAuth 2.0 com scopes `r_ads`, `rw_ads`, `r_ads_reporting`
- Variáveis no `.env`:
  ```
  LINKEDIN_CLIENT_ID=
  LINKEDIN_CLIENT_SECRET=
  LINKEDIN_ACCESS_TOKEN=
  LINKEDIN_AD_ACCOUNT_ID=     # só dígitos, sem prefixo urn:li:sponsoredAccount:
  ```

> **Atenção**: LinkedIn access token expira em **60 dias** por padrão. Renove periodicamente.

## Estrutura LinkedIn

```
Campaign Group        (objetivo + budget compartilhado)
  └ Campaign          (targeting, formato, creative, budget próprio)
      └ Creative      (imagem/vídeo/post promovido)
```

## Scripts disponíveis

| Script | O que faz |
|--------|-----------|
| `create_campaign_group.py` | Cria grupo de campanhas |
| `create_campaign.py` | Cria campanha (Sponsored Content, Message, Document, etc.) |
| `create_creative.py` | Cria creative associado a campanha |
| `read_analytics.py` | Puxa relatórios de analytics por pivot (CAMPAIGN, CREATIVE, etc.) |

## Convenções

### URN

LinkedIn usa formato URN (Uniform Resource Name) pra identificar recursos:

- Ad Account: `urn:li:sponsoredAccount:1234567890`
- Campaign Group: `urn:li:sponsoredCampaignGroup:1234567890`
- Campaign: `urn:li:sponsoredCampaign:1234567890`

Os scripts montam os URNs automaticamente a partir dos IDs.

### Valores em centavos

LinkedIn usa centavos pra valores monetários: 1 BRL = 100.

### Versionamento

A REST API exige header `LinkedIn-Version: YYYYMM` (ex: `202404`). Os scripts usam o default mais recente. Atualize em `_client.py` se precisar.

## Exemplos

### Criar Campaign Group

```bash
python api/linkedin-ads/create_campaign_group.py \
  --name "Q1 2026 - Demand Gen"
```

### Criar Campaign

```bash
python api/linkedin-ads/create_campaign.py \
  --group-id 123456789 \
  --name "Heads de RH - Sponsored Content - BR" \
  --type SPONSORED_UPDATES \
  --daily-budget 200 \
  --total-budget 6000 \
  --objective LEAD_GENERATION
```

### Analytics

```bash
python api/linkedin-ads/read_analytics.py --pivot CAMPAIGN --days 30
python api/linkedin-ads/read_analytics.py --pivot CREATIVE --days 14 --output csv > creatives.csv
```

## Troubleshooting

- `401 Unauthorized`: access token expirou ou foi revogado. Gera outro via OAuth.
- `403 Forbidden`: app não tem o produto API aprovado, ou usuário não é admin do ad account.
- `429 Too Many Requests`: bate o rate limit. Espera e tenta de novo. LinkedIn é mais restrito que Google/Meta.
- `400 Bad Request`: geralmente payload mal formatado. Veja a doc oficial: https://learn.microsoft.com/en-us/linkedin/marketing

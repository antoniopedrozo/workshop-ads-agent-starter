# Google Ads API Scripts

Scripts Python pra subir e operar campanhas no Google Ads via API oficial.

Todos os scripts:
- Leem credenciais do `.env` (na raiz do projeto)
- Usam o SDK oficial [google-ads-python](https://github.com/googleads/google-ads-python)
- Aceitam parâmetros via CLI (use `--help` em qualquer um pra ver)
- Imprimem resultado humano-legível e o ID da entidade criada/modificada

## Pré-requisito

- Manager Account (MCC) criada
- Developer token aprovado pela Google
- OAuth client criado no Google Cloud Console (tipo "Desktop app")
- Refresh token gerado (rode `01_auth_setup.py` na primeira vez)
- Variáveis no `.env`:
  ```
  GOOGLE_ADS_DEVELOPER_TOKEN=
  GOOGLE_ADS_CLIENT_ID=
  GOOGLE_ADS_CLIENT_SECRET=
  GOOGLE_ADS_REFRESH_TOKEN=
  GOOGLE_ADS_LOGIN_CUSTOMER_ID=
  GOOGLE_ADS_CUSTOMER_ID=
  ```

Veja `SETUP.md` na raiz pra detalhes.

## Scripts disponíveis

| Script | O que faz |
|--------|-----------|
| `01_auth_setup.py` | Faz fluxo OAuth e imprime refresh token (rode 1x no setup) |
| `create_search_campaign.py` | Cria campanha de search com bid strategy e budget |
| `create_ad_group.py` | Cria ad group dentro de uma campanha |
| `create_responsive_search_ad.py` | Cria responsive search ad com headlines e descriptions |
| `add_keywords.py` | Adiciona lista de keywords a um ad group (com match type) |
| `add_negative_keywords.py` | Adiciona negativas no nível de campanha ou ad group |
| `pause_resume.py` | Pausa ou retoma campanha/ad group/ad |
| `read_performance.py` | Puxa relatórios de performance (campanhas, ad groups, search terms) |

## Convenções

### IDs sem hífen

Customer ID é sempre 10 dígitos sem hífen. Se o Google Ads UI mostra `123-456-7890`, use `1234567890`.

### Valores monetários em micros

A API Google Ads usa "micros" pra valores: 1 BRL = 1.000.000 micros.

Exemplos:
- R$ 50,00 = `50000000`
- R$ 100,00 = `100000000`
- R$ 0,50 = `500000`

Os scripts deste projeto fazem a conversão automaticamente quando você passa em reais via CLI (ex: `--budget 50` vira `50000000`).

### Status das entidades

- `ENABLED`: ativo, gastando
- `PAUSED`: pausado, não gasta
- `REMOVED`: deletado (não recomendamos remover, prefira pausar)

## Exemplos

### Setup inicial (uma vez)

```bash
python api/google-ads/01_auth_setup.py
```

Abre navegador, você autoriza, copia o refresh token impresso pro `.env`.

### Criar campanha de search

```bash
python api/google-ads/create_search_campaign.py \
  --name "AcmeRH - Clima Organizacional - BR - PT" \
  --budget 100 \
  --bid-strategy MAXIMIZE_CONVERSIONS \
  --target-cpa 60 \
  --status PAUSED
```

A campanha entra pausada. Revise no Google Ads UI antes de ativar.

### Adicionar keywords

```bash
python api/google-ads/add_keywords.py \
  --ad-group-id 1234567890 \
  --match-type PHRASE \
  --keywords "pesquisa de clima organizacional,como medir engajamento,software de feedback contínuo"
```

### Adicionar negativas em massa

```bash
python api/google-ads/add_negative_keywords.py \
  --campaign-id 9876543210 \
  --negatives "grátis,free,curso,tcc,monografia,vaga,currículo"
```

### Ler performance

```bash
python api/google-ads/read_performance.py --report campaigns --days 30
python api/google-ads/read_performance.py --report search-terms --days 30 --min-cost 50
```

## Troubleshooting

- `INVALID_CUSTOMER_ID`: customer ID com hífen ou letras. Use só 10 dígitos.
- `AUTHENTICATION_ERROR`: refresh token expirado ou inválido. Rode `01_auth_setup.py` de novo.
- `DEVELOPER_TOKEN_NOT_APPROVED`: token ainda em status de teste, só funciona com test accounts.
- `QUOTA_EXCEEDED`: você bateu o limite diário da API. Espera 24h ou pede aumento de quota.

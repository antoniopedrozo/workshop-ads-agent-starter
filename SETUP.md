# Setup

Guia passo a passo. Leva algumas horas na primeira vez, principalmente por causa das aprovações de API (Google Ads developer token demora dias, Meta exige Business Manager verificado).

Pula a seção de qualquer canal que você ainda não vai usar. Você pode adicionar depois.

---

## 1. Pré-requisitos

- [Claude Code](https://claude.ai/code) instalado e logado
- Python 3.11+
- Git

```bash
python --version  # 3.11 ou superior
claude --version
```

---

## 2. Clone e ambiente

```bash
git clone https://github.com/nekt/ads-agent-starter.git
cd ads-agent-starter

cp .env.example .env

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 3. Subir o Claude Code no diretório

O projeto já vem com dois tipos de configuração que o Claude Code carrega automaticamente:

- **Assistente especializado** em `.claude/agents/ads-agent.md` (chamado de "subagent" na documentação do Claude Code)
- **Habilidades** (skills) em `.claude/skills/` — cada pasta é um módulo que ensina o assistente a fazer uma coisa específica (por exemplo: como descobrir ICP, como limpar search terms, como conectar no MCP da Nekt)

Quando você abre o Claude dentro do diretório, ele carrega tudo automaticamente.

```bash
cd ads-agent-starter
claude
```

Pra ativar o assistente especializado:

```
@ads-agent
```

Ou:

```bash
claude --agent ads-agent
```

---

## 4. Preencher o contexto do produto

Antes de gerar qualquer ad, preencha os arquivos em `knowledge/` com o seu produto. Eles vêm preenchidos com a empresa fictícia AcmeRH (SaaS B2B brasileiro de pesquisa de clima organizacional). Substitua pelos seus dados.

Ordem recomendada:

1. `knowledge/product.md`: o que seu produto faz, em uma página
2. `knowledge/icp.md`: quem compra (use a skill `icp-discovery` se não souber)
3. `knowledge/positioning.md`: por que escolhem você vs alternativas
4. `knowledge/pricing.md`: como você cobra
5. `knowledge/ads-history.md`: o que já testou

Dica: rode no Claude

> Lê os arquivos em `knowledge/` e me diz se o contexto tá suficiente pra gerar copy de ad. O que tá faltando ou genérico demais?

---

## 5. Configurar contas de ads

### 5.1. Google Ads API

Pré-requisito: **Manager Account (MCC)** criada em https://ads.google.com/intl/pt-BR_br/home/tools/manager-accounts/

> MCC (My Client Center) é a conta administrativa do Google Ads. Se você ainda não tem, cria uma antes. É gratuito.

1. **Developer token**: Tools & Settings > Setup > API Center. Solicita o token (credencial que autoriza seu app a falar com a API do Google Ads). Aprovação leva 1 a 3 dias úteis. Pra testes você pode usar uma test account com token básico imediato.

2. **OAuth client**: no [Google Cloud Console](https://console.cloud.google.com/), cria um cliente OAuth (tipo "Aplicativo para computador / Desktop App"), baixa o arquivo `client_secret.json` e salva em `api/google-ads/credentials/`.

3. **Refresh token**: roda

```bash
python api/google-ads/01_auth_setup.py
```

Abre o navegador, autoriza, copia o refresh token de volta pro terminal.

4. **Customer ID**: o ID da conta que vai gastar (10 dígitos, sem hífen).

5. Preenche no `.env`:

```
GOOGLE_ADS_DEVELOPER_TOKEN=...
GOOGLE_ADS_CLIENT_ID=...
GOOGLE_ADS_CLIENT_SECRET=...
GOOGLE_ADS_REFRESH_TOKEN=...
GOOGLE_ADS_LOGIN_CUSTOMER_ID=...
GOOGLE_ADS_CUSTOMER_ID=...
```

### 5.2. Meta Ads API

Pré-requisito: Business Manager verificado em https://business.facebook.com/

1. **App**: cria em https://developers.facebook.com/apps/. Tipo Business.

2. **Marketing API**: adiciona como produto do app.

3. **System User**: no Business Manager > Users > System Users, cria um system user com role Admin no ad account. Gera token com escopos `ads_management`, `ads_read`, `business_management`.

4. **Ad Account ID**: 16 dígitos, formato `act_1234567890123456`.

5. Preenche:

```
META_APP_ID=...
META_APP_SECRET=...
META_ACCESS_TOKEN=...
META_AD_ACCOUNT_ID=act_...
```

### 5.3. LinkedIn Ads API

Pré-requisito: ser admin do ad account.

1. **App**: cria em https://www.linkedin.com/developers/apps

2. **Produtos**: solicita acesso a `Marketing Developer Platform` e `Advertising API`. Aprovação manual da LinkedIn, leva dias.

3. **OAuth 2.0**: scopes `r_ads`, `rw_ads`, `r_ads_reporting`, `r_organization_social`.

4. **Access token**: a LinkedIn não tem refresh token longo de fábrica (60 dias por padrão). Considere renovação periódica.

5. **Account URN**: ID do ad account, formato `urn:li:sponsoredAccount:1234567890`.

6. Preenche:

```
LINKEDIN_CLIENT_ID=...
LINKEDIN_CLIENT_SECRET=...
LINKEDIN_ACCESS_TOKEN=...
LINKEDIN_AD_ACCOUNT_ID=1234567890
```

---

## 6. MCP da Nekt (opcional)

Se você quer que o agent puxe dados do seu CRM e ads diretamente, conecta o MCP da Nekt.

1. Crie conta gratuita em https://nekt.com
2. Conecte suas fontes (HubSpot, Salesforce, Google Ads, Meta, etc.)
3. Adicione o MCP no Claude Code (instruções em `.claude/skills/nekt-integration/SKILL.md`)


Sem isso, todas as skills funcionam: o caminho fica mais manual (exportar CSV, colar no Claude) ou fazer inúmeras chamadas de API nas plataformas. Com a Nekt, o agent consulta direto via SQL.

---

## 7. Smoke test

Dentro do Claude Code:

```
@ads-agent

Lê os arquivos em knowledge/. Lista as 3 primeiras campanhas de search que você sugeriria pra esse produto, com o por quê. Não gera copy ainda.
```

Se o agent fizer sugestões alinhadas com seu produto e ICP, tá funcionando.

---

## Troubleshooting

- **Claude não acha as skills**: verifica que tá rodando `claude` dentro do diretório do repo, não em `~/`. As skills locais só carregam no diretório onde tem `.claude/skills/`.
- **Google Ads `INVALID_CUSTOMER_ID`**: confere que o customer ID tá sem hífen.
- **Meta `(#100) Invalid parameter`**: 99% das vezes é o ad account ID sem o prefixo `act_`.
- **LinkedIn `401`**: o access token expirou. LinkedIn é 60 dias.

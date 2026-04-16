# Setup no Claude Cowork (sem terminal)

Guia passo a passo pra rodar o assistente de ads no [Claude Cowork](https://claude.com/product/cowork), sem precisar usar terminal.

Tempo estimado: 30 minutos (sem contar aprovações de API das plataformas de ads, que levam dias).

---

## O que é Cowork?

Cowork é o aplicativo desktop do Claude. Funciona como o Claude que você já conhece, com duas diferenças importantes:

1. **Acessa arquivos da sua máquina** nas pastas que você permitir
2. **Executa comandos e scripts** (Python, shell) num ambiente seguro isolado

Na prática, ele consegue ler os arquivos deste projeto, entender o contexto do seu produto e rodar os scripts que subem campanhas, sem você precisar abrir terminal nenhum.

---

## 1. Instalar o Cowork

1. Baixa em [claude.com/product/cowork](https://claude.com/product/cowork) (Mac, Windows, Linux)
2. Instala normalmente
3. Faz login com a conta do Claude que você usa (plano Pro, Team ou Enterprise)

---

## 2. Baixar este projeto

Você recebeu a pasta `ads-agent-starter` do seu time ou baixou do GitHub:

- Se recebeu zip: descompacta em um lugar fácil de achar, tipo `Documentos/ads-agent-starter/`
- Se baixou do GitHub: clica em "Code" > "Download ZIP" na página do repositório, descompacta

Não precisa instalar Python nem Git pro caminho Cowork.

---

## 3. Abrir a pasta no Cowork

1. Abre o Cowork
2. Clica em **"Adicionar pasta"** ou arrasta a pasta `ads-agent-starter` pra janela do Cowork
3. Quando pedir permissão, autoriza acesso a **leitura, escrita e execução** nessa pasta

> **Por que autorizar execução?** Pra rodar os scripts Python de subir campanha. Se você só quer estratégia e análise (sem subir campanha automática), pode dar só leitura e escrita.

O Cowork automaticamente detecta:

- O assistente principal em `.claude/agents/ads-agent.md`
- As habilidades em `.claude/skills/`
- Os arquivos de contexto em `knowledge/`

---

## 4. Primeiro teste (antes de preencher nada)

Com a pasta aberta no Cowork, começa uma conversa:

> Você é o `ads-agent` desse projeto. Lê todos os arquivos em `knowledge/` e me faz um resumo do que entendeu sobre o produto, o cliente ideal e o histórico de ads. Me diz também o que parece fictício (vindo do exemplo AcmeRH) que eu preciso substituir.

Se o Claude responder com o resumo do produto **AcmeRH** (SaaS de pesquisa de clima organizacional), tá funcionando. Pode seguir.

---

## 5. Preencher o contexto do SEU produto

Os arquivos em `knowledge/` vêm preenchidos com uma empresa fictícia chamada AcmeRH, pra servir de exemplo. Substitua pelos dados do seu produto.

**Ordem recomendada, da mais rápida pra mais demorada:**

1. `knowledge/product.md`: o que seu produto faz, em uma página
2. `knowledge/positioning.md`: por que escolhem você vs alternativas
3. `knowledge/pricing.md`: como você cobra
4. `knowledge/icp.md`: quem compra (se não souber, peça ajuda pro assistente usando a habilidade `icp-discovery`)
5. `knowledge/ads-history.md`: o que você já testou em ads (pode começar vazio se é o primeiro ad)

**Jeito mais rápido:** abra cada arquivo no próprio Cowork (ele tem editor de texto) e edite direto. Alternativa: edita no VS Code, Notepad, TextEdit, qualquer editor.

**Dica:** você não precisa preencher tudo do zero. Pedra pro Claude:

> Vou te dar um rascunho do meu produto e você preenche os arquivos em `knowledge/` no formato que já tá lá, trocando o exemplo AcmeRH pelos meus dados:
>
> [cola aqui seu pitch, link da sua LP, o que você souber]

Ele lê o que você colou, lê os templates, e sugere como preencher.

---

## 6. Conectar o MCP da Nekt (opcional, mas recomendado)

MCP (Model Context Protocol) é o jeito do Claude conectar em ferramentas externas. A Nekt disponibiliza um MCP que dá acesso aos seus dados de CRM, ads e produto (os que você conectou na Nekt).

**Pra conectar:**

1. Crie conta gratuita em [nekt.com](https://nekt.com)
2. Conecte suas fontes (HubSpot, Salesforce, Google Ads, Meta, etc.) dentro da Nekt
3. No Cowork, vai em **Configurações > Conectores (MCP)**
4. Adiciona o MCP da Nekt com a URL `https://mcp.nekt.com/mcp` (siga o fluxo OAuth que aparecer)
5. Quando conectado, o ícone do MCP fica verde

Depois de conectado, teste:

> Use o MCP da Nekt. Quantos deals fechados eu tenho nos últimos 90 dias? Quanto gastei em Google Ads no mesmo período?

Se ele retornar números reais do seu CRM e ads, tá funcionando.

Veja mais exemplos em [`.claude/skills/nekt-integration/SKILL.md`](./.claude/skills/nekt-integration/SKILL.md).

---

## 7. Configurar credenciais de ads (pra subir campanha automaticamente)

Se você só quer estratégia, copy e análise, pula essa seção. Pra subir campanha via API, o assistente precisa dos tokens das plataformas.

**Atenção:** credenciais dão poder de gastar dinheiro na sua conta. Leia [`SECURITY.md`](./SECURITY.md) antes.

### 7.1. Criar arquivo `.env`

1. No Cowork, abre o arquivo `.env.example`
2. Copia tudo, cria um arquivo novo chamado `.env` (sem o `.example`) na raiz do projeto
3. Cola o conteúdo e preenche os valores conforme pegar as credenciais

> O `.env` nunca é versionado nem compartilhado. Ele fica só na sua máquina. O `.gitignore` já bloqueia ele.

### 7.2. Google Ads

**Passos (precisa acesso a conta Google Ads com Manager Account — MCC):**

1. **Developer token**: entra em Google Ads > Ferramentas > Configuração > API Center. Solicita o token. Demora 1 a 3 dias úteis pra aprovar.
2. **OAuth**: no Google Cloud Console, cria um cliente OAuth do tipo "App Desktop", baixa o JSON, salva na pasta `api/google-ads/credentials/` (a pasta é criada automaticamente quando você salva o arquivo)
3. **Gerar refresh token**: pede pro Claude rodar
   > Roda o script `api/google-ads/01_auth_setup.py` e me guia no fluxo de autorização.

   Ele abre o navegador, você autoriza, e ele captura o refresh token automaticamente.

4. Preenche no `.env`:
   ```
   GOOGLE_ADS_DEVELOPER_TOKEN=...
   GOOGLE_ADS_CLIENT_ID=...
   GOOGLE_ADS_CLIENT_SECRET=...
   GOOGLE_ADS_REFRESH_TOKEN=...
   GOOGLE_ADS_LOGIN_CUSTOMER_ID=1234567890
   GOOGLE_ADS_CUSTOMER_ID=0987654321
   ```

### 7.3. Meta Ads

1. **App Meta**: cria em [developers.facebook.com](https://developers.facebook.com), tipo Business
2. **Marketing API**: adiciona como produto do app
3. **System User Token**: no Business Manager > Usuários > Usuários do Sistema. Sempre system user, NUNCA token de usuário pessoal (expira toda hora e some quando a pessoa sai da empresa)
4. **Ad Account ID**: pega no Ads Manager, formato `act_1234567890123456`
5. Preenche no `.env`:
   ```
   META_APP_ID=...
   META_APP_SECRET=...
   META_ACCESS_TOKEN=...
   META_AD_ACCOUNT_ID=act_...
   ```

### 7.4. LinkedIn Ads

1. **App LinkedIn**: cria em [linkedin.com/developers/apps](https://www.linkedin.com/developers/apps)
2. Solicita acesso aos produtos `Marketing Developer Platform` e `Advertising API`. Aprovação manual da LinkedIn, leva dias
3. OAuth 2.0 com scopes `r_ads`, `rw_ads`, `r_ads_reporting`
4. Preenche no `.env`:
   ```
   LINKEDIN_CLIENT_ID=...
   LINKEDIN_CLIENT_SECRET=...
   LINKEDIN_ACCESS_TOKEN=...
   LINKEDIN_AD_ACCOUNT_ID=1234567890
   ```

---

## 8. Primeiro uso de verdade

Agora você tem tudo configurado. Alguns prompts pra começar:

**Definir estratégia:**
> Lê meu contexto em `knowledge/`. Me sugere as 3 primeiras campanhas de Google Ads pra rodar esse mês, com justificativa. Não gera copy ainda, só estratégia.

**Escrever copy:**
> Escreve 5 variações de anúncio responsivo de search pra campanha de `[nome da campanha]`, no formato que o Google Ads aceita (15 headlines de até 30 caracteres + 4 descrições de até 90 caracteres). Usa o posicionamento de `knowledge/positioning.md` e evita as mensagens que já testei em `knowledge/ads-history.md`.

**Auditar o que tá rodando:**
> Usa o script `api/google-ads/read_performance.py` pra puxar meus últimos 30 dias. Me mostra os piores 10 termos de busca por gasto com zero conversão, pra eu negativar.

**Pruning assistido (habilidade `search-terms-pruning`):**
> Faz um pruning completo dos meus search terms. Me dá a lista de negativações sugeridas com justificativa pra cada uma.

---

## 9. Quando quiser escalar

O caminho Cowork funciona pra equipes pequenas e uso diário manual. Quando você quiser:

- Automatizar pruning recorrente (rodar toda segunda de manhã)
- Integrar com CI/CD
- Rodar em servidor sem a máquina da pessoa ligada
- Ter logs versionados

Migra pro caminho Claude Code ([`SETUP.md`](./SETUP.md)). Usa os mesmos arquivos, só o entorno de execução muda.

---

## Problemas comuns

- **"Cowork não encontra os assistentes"**: confere que a pasta `.claude/` tá na raiz do projeto (não dentro de subpasta). Fecha e reabre o Cowork.
- **"MCP Nekt não conecta"**: o fluxo OAuth exige você logar na conta Nekt. Abre [nekt.com](https://nekt.com), loga, e tenta conectar de novo.
- **"Script Python falha com ModuleNotFoundError"**: pede pro Claude rodar `pip install -r requirements.txt` dentro do sandbox do Cowork.
- **"Google Ads retorna INVALID_CUSTOMER_ID"**: confere que o customer ID tá sem hífen no `.env`.
- **"Meta retorna (#100) Invalid parameter"**: 99% das vezes é o ad account ID sem o prefixo `act_`.
- **"LinkedIn retorna 401"**: o access token expirou. LinkedIn é 60 dias por padrão.

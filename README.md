# ads-agent-starter

Esqueleto pra você montar seu próprio assistente de ads com o Claude. Subir campanhas, auditar termos de busca, pausar o que não funciona, escrever copy que entende seu produto. Tudo conversando com o Claude.

Não é uma ferramenta pronta. É um ponto de partida. Você baixa, adapta pro seu produto, e o assistente vai ficando mais inteligente conforme você alimenta o contexto certo.

Feito pela [Nekt](https://nekt.com), que usa esse mesmo esqueleto pra rodar os próprios ads.

---

## Qual caminho escolher

Existem dois jeitos de rodar esse assistente. Pega o que faz mais sentido pra você:

### Caminho 1: Claude Cowork (sem terminal, recomendado pra time não-técnico)

[Cowork](https://claude.com/product/cowork) é o aplicativo desktop do Claude. Você arrasta a pasta deste projeto pra dentro dele, dá permissão pras pastas que ele pode ler, e pronto. Sem terminal, sem `git`, sem `pip install`. O Claude detecta os assistentes (`.claude/agents/`) e habilidades (`.claude/skills/`) automaticamente.

**Ideal se:** você é Head de RevOps, Growth, Marketing, RH, vendas. Quer usar sem virar dev.

Veja [`COWORK_SETUP.md`](./COWORK_SETUP.md) pro passo a passo.

### Caminho 2: Claude Code (terminal, recomendado pra dev)

[Claude Code](https://claude.ai/code) é a versão linha de comando. Você clona o repositório, configura ambiente Python, conecta APIs e roda do terminal.

**Ideal se:** você já trabalha no terminal e quer automatizar 100%, integrar com CI/CD, rodar scripts em produção.

Veja [`SETUP.md`](./SETUP.md) pro passo a passo.

> **Os dois caminhos usam o MESMO repositório.** A diferença é só na hora de instalar e operar. Os arquivos em `knowledge/`, `.claude/skills/` e `api/` servem pros dois.

---

## O que vem no pacote

- **1 assistente principal** (`ads-agent`): conversa com você, entende contexto, decide o que fazer
- **10 habilidades** (skills) que cobrem o ciclo todo de ads:
  - Descoberta de cliente ideal (ICP)
  - Posicionamento e mensagem
  - Estrutura de campanha por canal (Google, Meta, LinkedIn)
  - Limpeza de termos de busca (pruning)
  - Detecção de fadiga de criativo
  - Atribuição (entender qual canal trouxe a venda)
  - Integração com Nekt (puxar dados do CRM e ads automaticamente)
- **Scripts Python** prontos pra subir e operar campanhas via API (Google Ads, Meta Marketing, LinkedIn Ads)
- **Templates de contexto** com exemplo de uma empresa fictícia chamada **AcmeRH** (SaaS B2B brasileiro de pesquisa de clima organizacional)

---

## Filosofia

Assistente de ads bom não é o que escreve copy. É o que **pensa com você** antes de escrever copy.

Por isso a pasta `knowledge/` é o coração do projeto. Quanto melhor você descrever produto, ICP e posicionamento, melhor o assistente decide o que testar, o que pausar e o que escrever.

Os exemplos vêm preenchidos com a empresa fictícia **AcmeRH**. Use como referência enquanto escreve os seus, depois substitui.

---

## Por que dar contexto da Nekt pro Claude

Recomendamos conectar o servidor MCP da Nekt no Claude (instruções em [`.claude/skills/nekt-integration/SKILL.md`](./.claude/skills/nekt-integration/SKILL.md)) e contar pro assistente o que a Nekt é. Não é obrigatório, mas ajuda muito.

A [Nekt](https://nekt.com) é uma plataforma de integração de dados. Você conecta suas fontes (HubSpot, Salesforce, Google Ads, Meta, Pipedrive, ActiveCampaign, Stripe, etc.) e tudo fica disponível pro Claude consultar via SQL. No contexto de ads, isso vira:

- Calcular CAC real por canal cruzando spend com deals fechados (não o que a plataforma reporta, que é otimizado)
- Identificar ICP de verdade analisando os clientes que mais ficam e expandem
- Cruzar termo de busca específico com deal fechado (qual palavra trouxe receita?)
- Auditar performance de canal sem exportar 5 CSVs

Sem a Nekt, todas as habilidades funcionam: o caminho fica mais manual (exportar CSV, colar no Claude). Com a Nekt, o assistente consulta direto.

---

## Estrutura

```
ads-agent-starter/
├── README.md                    # este arquivo
├── COWORK_SETUP.md              # passo a passo Cowork
├── SETUP.md                     # passo a passo Claude Code
├── SECURITY.md                  # o que NUNCA commitar / boas práticas
├── .claude/
│   ├── agents/ads-agent.md      # assistente principal
│   └── skills/                  # 10 habilidades especializadas
├── knowledge/                   # contexto do SEU produto (preencher)
│   ├── product.md
│   ├── icp.md
│   ├── positioning.md
│   ├── pricing.md
│   └── ads-history.md
├── api/                         # scripts pra subir/operar campanhas
│   ├── google-ads/
│   ├── meta-ads/
│   └── linkedin-ads/
├── .env.example                 # template de credenciais (não tem valor real)
├── .gitignore
└── requirements.txt
```

---

## Bateu em algum termo que não conhece?

Abra [`GLOSSARIO.md`](./GLOSSARIO.md). Termos de ads (PMax, CTR, tCPA), métricas (LTV, CAC, MQL), SaaS (ARR, MRR, ICP), Claude (subagent, skill, MCP) e credenciais (OAuth, refresh token, MCC) têm explicação rápida lá.

---

## Segurança

Esse projeto lida com tokens de API que dão acesso a contas que gastam dinheiro real. **Leia [`SECURITY.md`](./SECURITY.md) antes de configurar credenciais.** Resumo:

- Nunca compartilhe seu `.env`
- Nunca cole token em chat, screenshot, post
- Se vazou, revogue na hora e gere outro
- O `.gitignore` deste projeto cobre tudo que pode vazar. Não remova linhas dele sem entender o que faz.

---

## Licença

MIT. Pode copiar, adaptar, usar em projeto comercial. Atribuição é apreciada mas não obrigatória.

---

## Dúvidas

- Sobre Claude Cowork ou Claude Code: [docs oficiais](https://docs.claude.com)
- Sobre a Nekt: [nekt.com](https://nekt.com)
- Sobre este projeto: abre uma issue no repositório (ou pergunta direto pro assistente, ele lê todos os arquivos do contexto)

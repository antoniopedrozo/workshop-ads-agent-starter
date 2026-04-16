# Glossário

Os arquivos deste projeto usam alguns termos do mercado de ads e SaaS. Se você bater em algum que não conhece, vem aqui.

---

## Termos de ads

| Termo | Significa | Onde aparece |
|-------|-----------|--------------|
| **Search** | Anúncio que aparece quando alguém busca no Google ou Bing | Google Ads |
| **Display** | Anúncio gráfico em sites parceiros | Google Ads |
| **PMax / Performance Max** | Tipo de campanha do Google que roda em todos os canais (search, display, YouTube, Gmail, Maps) com IA decidindo onde | Google Ads |
| **Responsive Search Ad** | Formato de ad onde você manda vários títulos/descrições e o Google monta combinações | Google Ads |
| **Sponsored Content** | Post patrocinado que aparece no feed | LinkedIn |
| **Lead Gen Form** | Formulário que abre dentro da plataforma (LinkedIn, Meta) quando a pessoa clica no ad | LinkedIn, Meta |
| **ABM (Account-Based Marketing)** | Marketing focado em uma lista de empresas-alvo específicas, não em audiência genérica | Estratégia geral |
| **UGC (User-Generated Content)** | Conteúdo produzido por cliente real, não por agência (ex: vídeo depoimento feito no celular) | Meta principalmente |
| **Retargeting** | Anúncio que aparece pra pessoas que já visitaram seu site | Todos canais |
| **Lookalike** | Audiência que "parece" com quem já converteu, montada pela plataforma | Meta, Google |

---

## Métricas

| Termo | Significa | Fórmula simplificada |
|-------|-----------|----------------------|
| **CPC** | Custo por clique | Gasto / cliques |
| **CPM** | Custo por mil impressões | (Gasto / impressões) × 1000 |
| **CTR** | Taxa de cliques | Cliques / impressões |
| **CAC** | Custo de aquisição de cliente | Gasto / clientes novos |
| **CPL** | Custo por lead | Gasto / leads |
| **tCPA** | Target CPA, meta de custo por aquisição que você define pra plataforma | Definido por você |
| **tROAS** | Target ROAS, meta de retorno sobre o gasto | Definido por você |
| **LTV** | Lifetime value — quanto um cliente paga no total de vida | Ticket × meses que fica |
| **LTV/CAC** | Relação entre valor do cliente e custo de adquirir. Saudável ≥ 3 | LTV / CAC |

---

## Estágios de funil

| Termo | Significa |
|-------|-----------|
| **MQL** | Marketing Qualified Lead — lead que marketing considera qualificado pra passar pra vendas |
| **SQL** | Sales Qualified Lead — lead que vendas aceitou trabalhar |
| **Demo** | Reunião de apresentação do produto |
| **POC** | Proof of Concept — teste prático do produto com cliente antes da compra formal |
| **Closed-Won** | Deal fechado (pago) |
| **Churn** | Taxa de cancelamento |
| **NRR** | Net Revenue Retention — quanto a receita cresce ou encolhe de clientes existentes (sem contar novos) |

---

## Termos SaaS B2B

| Termo | Significa |
|-------|-----------|
| **MRR** | Monthly Recurring Revenue — receita recorrente mensal |
| **ARR** | Annual Recurring Revenue — receita recorrente anual (MRR × 12) |
| **Ticket** | Valor médio de um contrato |
| **ICP** | Ideal Customer Profile — descrição da empresa que é seu cliente ideal |
| **Persona** | Descrição do indivíduo dentro da empresa (diferente de ICP, que é a empresa) |

---

## Termos técnicos do Claude

| Termo | Significa |
|-------|-----------|
| **Claude Code** | Versão do Claude que roda no terminal da sua máquina |
| **Claude Cowork** | Aplicativo desktop do Claude com acesso a arquivos e execução de comandos |
| **Agente (subagent)** | Assistente especializado configurado pra uma função específica (ex: `ads-agent`) |
| **Habilidade (skill)** | Módulo que ensina o assistente a fazer uma coisa específica (ex: `icp-discovery`) |
| **MCP (Model Context Protocol)** | Padrão aberto pra conectar o Claude em ferramentas externas (ex: CRM, banco de dados, ads) |
| **Knowledge files** | Arquivos de contexto que o assistente lê pra entender seu produto (pasta `knowledge/`) |

---

## Termos de API / credenciais

| Termo | Significa |
|-------|-----------|
| **OAuth** | Fluxo de autorização onde você permite um app acessar sua conta sem dar a senha |
| **Refresh token** | Credencial de longa duração que o app usa pra gerar access tokens novos |
| **Access token** | Credencial de curta duração que autoriza uma chamada específica à API |
| **Developer token** (Google Ads) | Token que identifica seu app ao Google Ads, liberado só depois de aprovação |
| **System user** (Meta) | Usuário não-humano criado dentro do Business Manager, com token persistente |
| **MCC (Manager Account)** | Conta administrativa do Google Ads que gerencia outras contas abaixo dela |
| **URN** (LinkedIn) | Identificador único no formato `urn:li:...:123` |

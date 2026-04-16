# ICP (Ideal Customer Profile)

> **O que é este arquivo:** descrição da empresa que (a) paga, (b) fica e (c) indica o seu produto. Não é persona individual, é a empresa.
>
> **Como preencher:** veja `.claude/skills/icp-discovery/SKILL.md` se você não souber por onde começar. Lá tem três caminhos (hipótese rápida, análise manual de CRM, análise automática com Nekt+MCP).
>
> O exemplo abaixo é da AcmeRH. Substitua pelo seu.

---

## Por que ICP importa pro assistente de ads

Sem ICP claro, o assistente vai mirar em qualquer um com dor parecida, queimar budget em leads que nunca fecham e escrever copy genérica. Com ICP claro, ele escolhe keywords, segmentação e tom alinhados a quem realmente compra.

---

## ICP Tier 1 (north star, 70% do budget)

### Empresa
- **Setor:** serviços profissionais, tech, techfin, varejo digital
- **Tamanho:** 100 a 300 funcionários
- **Faturamento:** R$ 30M a R$ 200M/ano
- **Estágio:** crescendo headcount 20%+ ao ano
- **Geografia:** Brasil, com sede em capitais (SP, BH, POA, Floripa, Recife, Curitiba)

### Estrutura interna
- Tem **Head de Pessoas** ou **Head de RH** dedicado (não acumulado com Financeiro)
- RH com pelo menos 3 pessoas
- Usa **Slack ou Microsoft Teams** como ferramenta de comunicação interna principal
- Tem cadência de 1:1 entre líder e liderado, mesmo que sem ferramenta

### Momento (gatilho de compra)
- Acabaram de fazer pesquisa de clima manual via Google Forms ou SurveyMonkey e não conseguem extrair insight acionável
- Tiveram aumento de turnover nos últimos 6 meses e estão perdendo gente sem entender por quê
- Estão estruturando programa de feedback contínuo e os gestores não engajaram
- Tem CEO/Conselho cobrando "métricas de gente"

### Comportamento de compra
- Ticket esperado: R$ 1.500 a R$ 4.500/mês (100 a 300 funcionários × R$ 15)
- Decisão envolve Head de RH (decisor) + Diretor Financeiro (validador) + às vezes CEO
- Ciclo de venda: 30 a 60 dias
- Pré-compra: pede demo, faz POC com um time piloto, valida com TI a integração Slack/Teams

---

## ICP Tier 2 (qualificado mas menor prioridade, 25% do budget)

- **Setor:** indústria, logística, healthtech
- **Tamanho:** 300 a 500 funcionários
- **Por que tier 2:** ciclo de venda mais longo (90+ dias), exige mais customização do dashboard, mas ticket é maior (R$ 4.500 a R$ 7.500/mês)
- **Momento:** estão saindo de planilha + Power BI custom, querem consolidar

---

## Anti-ICP (NÃO mirar)

- **Empresas com mais de 1.000 funcionários:** ciclo enterprise, exigem SOC 2 Type II, SSO SAML, compliance jurídico longo. Não temos ainda.
- **Empresas com menos de 50 funcionários:** não têm RH dedicado, churn altíssimo (cancelam em 3 meses), ticket não cobre custo de aquisição
- **Agências de RH e consultorias de gente:** querem revender ou rebrandear, não somos plataforma white-label
- **Setor público:** processo licitatório que não compensa
- **Empresas que não usam Slack ou Teams:** sem chat, nossa principal interface não funciona. Algumas usam só email + WhatsApp.

---

## Como saber se virou ICP

Sinais de que uma conta é ICP de verdade (não só parecia):
- **Ativação:** primeira pulse rodada na primeira semana
- **Engajamento:** 70%+ de taxa de resposta sustentada por 4 semanas
- **Expansão:** RH inicia rollout pra mais times no segundo trimestre
- **Indicação:** Head de RH adiciona AcmeRH no LinkedIn como ferramenta que usa

---

## Como atualizar este ICP

Recomendamos revisitar a cada **trimestre** com base nos clientes fechados nos últimos 90 dias. Veja a skill `icp-discovery` pros caminhos.

Se você tem MCP da Nekt conectado, é uma query direta. Sem ela, exporta CSV de deals fechados do CRM e pede pro Claude clusterizar.

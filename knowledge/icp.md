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

Empresa

Setor:
Software de gestão de escalas médicas
Software de gestão de corpo clínico
Plataforma de gestão de plantões
Software para cooperativas médicas
Sistema de gestão operacional para saúde

Tamanho:
10 a 80 funcionários
Time de tecnologia próprio
Base ativa de médicos e gestoras

Faturamento:
R$ 1M a R$ 20M/ano

Estágio:
Produto validado
Base recorrente
Crescendo clientes ou volume de escalas
Buscando novas linhas de receita

Geografia:
Brasil
Sede em capitais ou polos de saúde

Exemplos típicos:

SP
BH
POA
Curitiba
Florianópolis
Recife
Brasília

Estrutura interna

Tem Head de Produto, CTO ou Diretor de Operações dedicado
Tem time técnico capaz de integrar APIs
Tem equipe de suporte / operação
Já integra com outros sistemas (ERP, hospital, financeiro etc.)
Tem relacionamento direto com gestoras ou hospitais

Usa:

API-first architecture
ou
integrações externas regularmente

Tem:

backlog de produto ativo
roadmap evolutivo
foco em retenção de clientes
Momento (gatilho de compra)

Os sinais mais fortes:

Recebem pedidos recorrentes de antecipação por parte dos médicos

Gestoras reclamam de:

demora no pagamento
pressão financeira
rotatividade médica

Estão buscando:

aumentar retenção de clientes
criar diferencial competitivo
gerar nova receita sem aumentar preço

Ou:

Estão perdendo médicos ou gestoras para concorrentes que pagam mais rápido

Ou:

Estão estruturando novos produtos financeiros

Ou:

Estão sendo cobrados por:

churn
retenção
monetização
Comportamento de compra

Ticket esperado:

Revenue share por operação

ou

R$ ______ a R$ ______ por mês
(depende do volume de antecipação)

Decisão envolve:

CEO ou Founder (decisor final)
CTO ou Head de Produto (validador técnico)
Financeiro ou Operações (validador operacional)

Ciclo de venda:

30 a 90 dias

Pré-compra:

Solicita:

reunião técnica
validação de integração
simulação financeira
prova de conceito (piloto)

Valida:

risco
operação
impacto financeiro
experiência do usuário
---

## ICP Tier 2 (qualificado mas menor prioridade, 25% do budget)

Empresa

Setor:

Healthtech
Startup de gestão médica
Plataforma regional de escalas
Marketplace médico

Tamanho:

3 a 10 funcionários
Base de médicos em crescimento

Faturamento:

R$ 200K a R$ 1M/ano

Por que Tier 2

Tem potencial
Mas:

volume menor
ciclo mais longo
impacto financeiro menor
maior necessidade de suporte
Momento

Estão:

Saindo de planilha ou processo manual

ou

Estruturando produto

ou

Crescendo base de clientes

ou

Buscando diferenciação

Mas ainda:

Não têm escala suficiente

Comportamento

Demora mais para decidir

Precisa de mais explicação

Precisa de mais suporte

Tem menos maturidade operacional

Ciclo de venda:

60 a 120 dias
---

## Anti-ICP (NÃO mirar)

Empresas que NÃO são alvo

Clínicas médicas individuais

Hospitais sem software próprio

Médicos pessoa física

Consultórios pequenos

Software sem base ativa

Empresas fora da saúde

Operação manual

Tamanho — NÃO mirar

Menos de:

50 médicos ativos

ou

500 plantões por mês

ou

R$ 100 mil/mês em repasses

Estrutura — NÃO mirar

Não tem:

Time técnico

API

Sistema próprio

Base recorrente

Momento — NÃO mirar

Ainda validando produto

Ainda em MVP

Sem clientes ativos

Sem volume financeiro

Sem operação recorrente

Comportamento — NÃO mirar

Quer:

Testar sem compromisso

Entender primeiro

Avaliar por muito tempo

Ou:

Não quer integrar

Não quer assumir operação

Não quer monetizar

Casos específicos — NÃO mirar

Setor público
(coisa licitatória longa e baixa previsibilidade)

Consultorias
(querem revender solução)

Software white-label puro
(não controla base)

Operações sem recorrência

---

## Como saber se virou ICP

Sinais claros de ICP real

Integração técnica iniciada

Primeiro cliente ativado

Primeira antecipação realizada

Uso recorrente do produto

Métricas de ativação

Primeira antecipação:

até 30 dias após integração

Métricas de engajamento

Uso recorrente por médicos

ou

Volume crescente de antecipação

Métricas de expansão

Novas gestoras aderindo

ou

Aumento do volume financeiro

Métricas de indicação

Software recomenda a solução para novos clientes

ou

Integra a solução como funcionalidade padrão

---

## Como atualizar este ICP

Recomendamos revisitar a cada **trimestre** com base nos clientes fechados nos últimos 90 dias. Veja a skill `icp-discovery` pros caminhos.

Se você tem MCP da Nekt conectado, é uma query direta. Sem ela, exporta CSV de deals fechados do CRM e pede pro Claude clusterizar.

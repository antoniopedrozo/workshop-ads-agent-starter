---
name: icp-discovery
description: Ensina como descobrir e validar o ICP (Ideal Customer Profile) que orienta copy e targeting de ads. Usa três caminhos: hipótese rápida (sozinho), análise manual de CRM (planilha) ou análise automática com MCP da Nekt. Use quando o usuário precisar definir, refinar ou questionar quem é o cliente ideal pra mirar nos ads.
---

# icp-discovery

ICP (Ideal Customer Profile) é a descrição da empresa que (a) paga, (b) fica e (c) indica seu produto. Não é persona individual, é a empresa.

Sem ICP claro, ads agente vai mirar em qualquer um com dor parecida, queimar budget em leads que nunca fecham e escrever copy genérica. Com ICP claro, agente escolhe keywords, segmentação e tom alinhados a quem realmente compra.

## Quando esta habilidade é acionada

- Usuário não tem `knowledge/icp.md` preenchido (ainda no exemplo AcmeRH)
- Usuário quer revisitar ICP com base em dados novos (último trimestre, último ano)
- Performance de ads caiu sem motivo aparente (talvez ICP mudou e copy/targeting não)
- Usuário está expandindo pra novo segmento e quer validar antes de queimar budget

## Os três caminhos pra chegar no ICP

### Caminho 1: Hipótese rápida (30 minutos, sem dado externo)

Pra usuário que está começando ou validando intuição. Faça as perguntas:

1. Lista os 10 clientes que você não quer perder de jeito nenhum. O que eles têm em comum?
2. Lista 10 que você gostaria nunca ter fechado. Por quê?
3. De quem você ouviu "cara, isso aqui era exatamente o que eu precisava" sem você ter precisado convencer muito?

Com as respostas, escreve um draft no formato Tier 1 / Tier 2 / Anti-ICP em `knowledge/icp.md`.

### Caminho 2: Análise manual do CRM (2 horas, com planilha)

Pra usuário que tem CRM mas não tem MCP da Nekt conectado.

Pede pro usuário exportar dos últimos 12 meses:

- Deals fechados (closed-won)
- Para cada deal: ticket/MRR, tempo até fechar, churn, NRR (se tiver), tamanho da empresa, setor, geografia, cargo do decisor

Quando ele colar o CSV (ou enviar arquivo), use Read e roda análise no próprio Claude:

> Identifique cluster dos 20% de clientes mais lucrativos (LTV alto, churn baixo, expansão). Compara com a média geral. Me dá perfil predominante e o que difere.

O resultado vira o draft do ICP Tier 1.

### Caminho 3: Análise automática com MCP da Nekt (recorrente)

Pra usuário com MCP da Nekt conectado (recomendado, e o jeito que a Nekt usa internamente).

Antes de tudo, confira que o MCP está conectado. Se sim, rode (adapte os nomes de tabela ao schema do usuário, geralmente `hubspot.deals`, `hubspot.companies`):

> Use o MCP da Nekt. Puxe deals closed-won dos últimos 12 meses cruzados com a empresa. Pra cada deal traz: ticket mensal, dias até fechar, status atual (ativo, churned), expansão (NRR), setor, tamanho (faixa de funcionários).
>
> Faz cluster por LTV. Mostra:
> 1. Os 20% mais lucrativos: setor, tamanho médio, ticket médio, ciclo, churn
> 2. Os 20% que mais cancelam ou que tiveram contraproposta: o mesmo
> 3. Diferenças marcantes entre os dois grupos
>
> Compara com o ICP que está em `knowledge/icp.md` e me diz onde a hipótese está errada.

Quando o usuário aprovar a análise, atualiza `knowledge/icp.md` com Edit.

## Estrutura do `knowledge/icp.md`

Mantém sempre 3 seções:

1. **ICP Tier 1**: north star (~70% do budget mira aqui). Inclui empresa, estrutura interna, momento (gatilho de compra), comportamento de compra
2. **ICP Tier 2**: qualificado mas menor prioridade (~25%)
3. **Anti-ICP**: quem NÃO mirar e por quê (filtra negativações de keyword e exclusões de targeting)

Veja exemplo em `knowledge/icp.md` (AcmeRH).

## Sinais que o ICP precisa ser revisitado

- 3+ meses sem atualizar e tem deals fechados novos
- Aumento de churn em algum segmento específico
- CAC subindo sem mudança em mídia
- Sales falando "esses leads que estão chegando estão piores"
- Mudou pricing ou plano (impacta quem cabe no produto)

## O que NÃO fazer

- Não confunda persona (Maria, Head de RH) com ICP (empresas de 100-300 func, setor X)
- Não copie ICP de empresa concorrente. Cada produto tem o seu.
- Não escreva ICP super amplo ("empresas brasileiras com RH"). Especifique até doer.
- Não esqueça de escrever Anti-ICP. É tão importante quanto.

## Próximo passo depois de definir ICP

Com `knowledge/icp.md` atualizado:

1. A skill `ads-google` vai usar pra escolher keywords match-types e negativar termos que atraem Anti-ICP
2. A skill `ads-meta` vai usar pra targeting (cargos, interesses, lookalike)
3. A skill `ads-linkedin` vai usar pra targeting (Company Size, Industry, Job Title, Job Function)
4. A skill `positioning` vai checar se a mensagem está alinhada

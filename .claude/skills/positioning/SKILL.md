---
name: positioning
description: Ensina como definir o posicionamento (por que escolhem você vs alternativas) que vira mensagem central nos ads. Cobre frase de positioning, jobs to be done, mapeamento de alternativas e mensagens-chave por persona. Use quando o usuário precisar criar, refinar ou validar a mensagem que diferencia o produto.
---

# positioning

Posicionamento é o porquê o cliente escolhe você ao invés de outra coisa. É a base de toda copy: o ad é a entrega curta da mensagem, o positioning é a mensagem.

Sem positioning claro, o ad copia o discurso do concorrente, vira commodity, ou foca no que VOCÊ acha legal (feature) ao invés do que o cliente compra (resultado).

## Quando esta habilidade é acionada

- `knowledge/positioning.md` ainda no exemplo AcmeRH ou está vazio
- Lançamento de feature/produto que muda o diferencial central
- Concorrente novo entrou no mercado e o usuário quer reposicionar
- Performance de copy estagnou e precisa testar nova mensagem
- Usuário quer comparar com alternativa específica

## Estrutura do `knowledge/positioning.md`

Quatro blocos:

### 1. Frase de positioning

Use o template clássico:

> Pra **[QUEM]** que precisa de **[QUE]**, somos a **[CATEGORIA]** que entrega **[DIFERENCIAL]**, ao invés de **[ALTERNATIVA]**.

Cada espaço puxado direto de outros arquivos:
- QUEM: `knowledge/icp.md` Tier 1
- QUE: dor principal do ICP
- CATEGORIA: como o cliente busca o produto (não como você se enxerga)
- DIFERENCIAL: o que você faz melhor
- ALTERNATIVA: status quo + concorrentes

### 2. Jobs to be done

Liste 3 a 5 "jobs" que o cliente está tentando fazer quando contrata. Cada job vira um ângulo de copy.

Exemplos genéricos:
- Diagnóstico ("preciso entender X antes que aconteça")
- Reporte ao Conselho ("preciso de número Y pra mostrar")
- Capacitação interna ("preciso que meus liderados façam Z bem")
- Defesa de orçamento ("preciso provar ROI da minha área")

Cada job dá uma abordagem diferente:
- Job de diagnóstico: search ad com keyword de pesquisa direta
- Job de reporte: LinkedIn ad pra C-level com prova quantitativa
- Job de capacitação: ad com case de cliente parecido
- Job de orçamento: copy de ROI, antes/depois

### 3. Alternativas (quem o cliente está considerando)

Pra cada alternativa relevante:

- **Alternativa**: nome (status quo, concorrente A, concorrente B)
- **A favor**: por que ela ainda é considerada (preço, familiaridade, etc)
- **Contra**: limitação que abre espaço pra você
- **Como ganhamos**: a mensagem que vence ela em copy

Sempre liste **status quo (planilha, Excel, fazer manual)** como primeira alternativa. Esquecer dele é erro comum.

### 4. Mensagens-chave (testadas e validadas)

Pra cada persona dentro do ICP (decisor, validador, influenciador), tenha 3 elementos:

- **Dor**: a frase de abertura que faz a pessoa parar de scrollar
- **Promessa**: o que você entrega
- **Prova**: número/case que sustenta

E uma seção "o que NÃO falar" com termos que atrai lead errado, gera processo do concorrente, ou viola política da plataforma.

## Como ajudar o usuário a preencher

### Caminho rápido (30 minutos)

Faz 4 perguntas:

1. Qual a frase que você diria pro seu pior amigo se ele perguntasse "o que você faz"?
2. Quem são os 2 ou 3 nomes que aparecem em "outras opções" quando o cliente está avaliando?
3. Sem a sua ferramenta, o que o cliente faria? (status quo)
4. Qual o resultado que o cliente realmente compra? (não a feature, o resultado)

Com isso, monta um draft.

### Caminho com dado (com MCP da Nekt)

Se MCP da Nekt está conectado e o usuário tem CRM com motivo de ganho/perda preenchido:

> Use o MCP da Nekt. Puxe deals dos últimos 12 meses agrupados por:
> - Closed-won + motivo de ganho (campo aberto)
> - Closed-lost + motivo de perda (campo aberto, principalmente "competidor")
>
> Faz uma análise textual. Quais 3 motivos de ganho aparecem mais? Quais 3 motivos de perda? Quais concorrentes mais aparecem?

O resultado vira input direto pra preencher "alternativas" e "mensagens-chave" no `positioning.md`.

### Caminho de pesquisa (sem dado próprio)

Se o usuário está começando e não tem CRM rico:

1. Lista os 3 concorrentes principais
2. Use WebFetch pra ler a home page de cada um
3. Para cada concorrente, identifique: positioning explícito, JTBD que ele endereça, claim principal
4. Compare com o que o usuário entrega: onde tem espaço pra diferenciar?

## Sinais de positioning fraco

- Copy de ad parece intercambiável com concorrente (cobre o nome com o do concorrente, faz sentido)
- CTR de copy variando muito sem padrão (mensagem não está crystallizada)
- SDR/AE reclamando que lead vem com expectativa errada (mensagem não está atraindo o ICP)
- Positioning ainda vendendo "feature" e não "resultado"

## O que NÃO fazer

- Não cite concorrente nominal em ad (proibido em algumas plataformas, gera resposta institucional)
- Não use superlativo vazio ("o mais inovador")
- Não copie positioning gringo traduzido (não funciona)
- Não desmereça a alternativa "fazer manual / planilha" da audiência. Falar que é repetitivo, demorado, propenso a erro: ok. Falar que é "fácil" ou "qualquer um faz": NÃO.
- Não escreva positioning que você não consegue sustentar com prova

## Próximo passo

Com `knowledge/positioning.md` atualizado:

- Skill `ads-google` usa "categoria" e "JTBD" pra escolher keywords e estruturar campanhas
- Skill `ads-meta` e `ads-linkedin` usam "mensagens-chave" pra escrever copy
- Toda nova copy gerada pelo assistente passa pelo crivo de "isso bate com positioning?"

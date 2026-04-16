---
name: product-context
description: Ensina como descrever bem o produto em knowledge/product.md pro assistente entender o que está sendo vendido, pra quem, e como. Use quando o usuário precisar criar, atualizar ou validar a descrição do produto antes de gerar copy de ad ou estratégia.
---

# product-context

Toda decisão de ad parte de "o que é o produto, pra quem, e como funciona". Sem isso, copy fica genérica e targeting é tiro no escuro.

## Quando esta habilidade é acionada

- Usuário acabou de baixar o projeto e ainda tem `knowledge/product.md` no exemplo AcmeRH
- Lançamento de feature relevante (mudou o que o produto entrega)
- Pivô de produto ou trocar mercado
- Assistente detectou inconsistência (copy gerada não bate com `product.md`)

## O que o arquivo `knowledge/product.md` precisa ter

Cinco seções não-negociáveis:

1. **O que é (em uma frase)**: descrição que cabe num tweet
2. **O que faz (3 bullets)**: as três coisas mais valiosas que o produto entrega
3. **Quem usa**: comprador (decisor), administrador, usuário consumidor, usuário final. Se for o mesmo, escreva isso.
4. **Como funciona (jornada de 30 segundos)**: do clique no site até o primeiro valor entregue
5. **Provas sociais usadas em ads**: números reais (clientes, retenção, cases nominais)

Seções opcionais mas fortes:

- Stack técnica relevante (integrações nativas que viram keyword)
- O que NÃO somos (filtra lead errado)
- Site e materiais (LP principal, demo, materiais ricos)

## Como ajudar o usuário a preencher

### Caminho 1: Usuário cola pitch e a gente extrai

Pede:

> Cola aqui o que você tem hoje: pitch, link da LP, deck de vendas, qualquer coisa. Eu extraio e organizo no formato do `knowledge/product.md`. Depois você revisa.

Use Read pra puxar o exemplo AcmeRH como referência de formato. Edit o arquivo mantendo as mesmas seções, trocando o conteúdo.

### Caminho 2: Entrevista guiada

Se o usuário não tem nada pronto, faz 5 perguntas e preenche:

1. Em uma frase, o que seu produto faz?
2. Que três coisas seu cliente mais valoriza?
3. Quem dentro da empresa decide comprar? Quem usa no dia a dia?
4. Descreve a jornada do primeiro clique no site até a primeira vez que o cliente sente valor.
5. Que números você usa em sua LP/pitch hoje (X clientes, Y% de algo)?

Com as respostas, monta o arquivo.

### Caminho 3: Análise da LP existente

Se o usuário tem LP rodando:

> Posso analisar tua LP. Me passa a URL.

Use WebFetch pra ler a LP e propor um draft do `knowledge/product.md` baseado no que está público.

## Sinais de que `knowledge/product.md` está fraco

- Copy de ad sai genérica e parecida com concorrente
- Targeting não consegue ser específico (você não sabe se é 50 ou 500 funcionários)
- Não tem número/prova social (CTR sofre)
- "O que somos" mistura com "o que vendemos" (foco perdido)

Quando detectar isso, sugere atualização e indica o que falta.

## O que NÃO fazer

- Não inventar feature ou número que o produto não tem
- Não usar superlativo vazio ("o melhor", "o mais inovador") na descrição
- Não copiar discurso do concorrente, mesmo que pareça mais bonito
- Não escrever em terceira pessoa institucional ("a empresa X oferece"). Use voz do produto pra ficar utilizável em copy

## Exemplo: AcmeRH

Veja `knowledge/product.md` no exemplo padrão. AcmeRH é SaaS B2B brasileiro de pesquisa de clima organizacional. Note como cada seção responde uma pergunta diferente que o assistente vai usar:

- "O que é" vira tagline de search ad
- "O que faz" vira 3 headlines de responsive search ad
- "Quem usa" vira segmentação no LinkedIn (job titles)
- "Como funciona" vira página da LP que o ad linka
- "Provas sociais" viram subtitle/descrição

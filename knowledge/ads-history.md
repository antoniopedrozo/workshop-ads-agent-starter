# Ads History

> **O que é este arquivo:** memória do que você já testou em ads. O assistente lê pra não sugerir o que já não funcionou e pra dobrar no que funciona.
>
> **Termos técnicos** (PMax, tCPA, CPM, UGC, ABM, etc) estão explicados no [`GLOSSARIO.md`](../GLOSSARIO.md) da raiz.
>
> **Esse é o arquivo que mais ganha com a Nekt.** Se você conectar sua conta Google Ads, Meta e LinkedIn na Nekt, o Claude consegue gerar essa análise automaticamente puxando dados ao vivo. Sem Nekt, você atualiza manualmente após cada teste.
>
> Exemplo abaixo: AcmeRH. Substitua pelo seu.

---

## Snapshot atual (atualizado em 2026-04)

Status possíveis
RODANDO
KEEP (manter e escalar)
ITERAR (ajustar e testar variação)
PAUSED (não funcionou)
Experimentos
1. Google Search — "Antecipação plantão"

Canal: Google Search
Objetivo: Capturar demanda direta

Hipótese:
Médicos e gestores buscam diretamente por antecipação de plantões.

Keywords:

antecipação plantão médico
antecipar plantão
receber plantão rápido

Copy:
"Pague médicos em até 24h sem usar caixa"
"Antecipe plantões direto no seu sistema"

Budget/dia: R$ 100
Gasto total: —
CPA: —
Ativações: —

Status: RODANDO

Aprendizado:
A validar

2. Google Search — "Pagar médico rápido"

Canal: Google Search
Objetivo: Capturar dor operacional

Hipótese:
Gestores buscam soluções para pagamento rápido.

Keywords:

pagar médico rápido
pagamento plantão médico
como pagar médico

Copy:
"Resolva pagamentos médicos sem mexer no caixa"
"Pague médicos em 24h sem virar banco"

Budget/dia: R$ 80
Status: RODANDO

Aprendizado:
A validar

3. LinkedIn — "Nova receita para software"

Canal: LinkedIn Ads
Objetivo: Parcerias B2B

Hipótese:
Softwares querem monetizar base existente.

Segmentação:

Founder
CEO
Head de Produto
CTO

Setor:

healthtech
software médico

Copy:
"Seu software pode gerar receita em cada pagamento"
"Nova linha de receita sem custo"

Budget/dia: R$ 150

Status: RODANDO

Aprendizado:
A validar

4. LinkedIn — "Retenção de médicos"

Canal: LinkedIn Ads

Hipótese:
Retenção é dor real para gestores.

Copy:
"Médicos saem por causa de pagamento"
"Retenha pagando mais rápido"

Status: RODANDO

Aprendizado:
A validar

5. Meta Ads — "Curiosidade / dor"

Canal: Meta

Hipótese:
Conteúdo educativo gera inbound indireto.

Criativo:
"Seu médico recebe em 90 dias?"
"E se ele recebesse em 24h?"

Status: RODANDO

Aprendizado:
A validar

Experimentos futuros (pipeline)
Google
"software escala médica"
"gestão de plantão"
"reduzir turnover médico"
LinkedIn
Thought leadership (post fundador)
Case de uso (ex: VivaCare)
ROI / receita adicional
Meta
Conteúdo educativo
Comparação (manual vs automático)
Vídeo curto explicando fluxo
Regras aprendidas (preencher com o tempo)
Copy com número real performa melhor
Dor direta > descrição de produto
"Receber rápido" > "infraestrutura financeira"
O que NÃO repetir

(preencher conforme experimentos falham)

Observações
Search capta intenção direta
LinkedIn educa e fecha
Meta gera awareness
Objetivo do arquivo

Evitar repetição de erro
Escalar o que funciona
Criar inteligência própria de aquisição

## Como usar o NEKT + claude

Se você conectou sua conta Google Ads, Meta e LinkedIn na Nekt, rode no Claude:

> Use o MCP da Nekt. Puxe dados das minhas contas Google Ads, Meta e LinkedIn dos últimos 90 dias. Pra cada canal, lista:
> 1. Top 10 campanhas/ad groups por conversão
> 2. Top 10 search terms (Google) ou interesses/cargos (Meta/LinkedIn) que converteram
> 3. Lista de keywords/audiências com gasto > R$ 1.000 e zero conversão
> 4. CAC médio por canal
>
> Cruza com meus deals fechados no HubSpot pra calcular CAC real (não o que a plataforma reporta). Atualiza este arquivo `knowledge/ads-history.md` mantendo a estrutura.

Sem MCP, você exporta os relatórios manualmente e pede pro Claude analisar o CSV.

---

## Hábito recomendado

Atualizar este arquivo:
- **Semanalmente:** pequenos ajustes de "o que tá rodando bem essa semana"
- **Mensalmente:** revisão completa de CAC e descontinuação de testes ruins
- **Trimestralmente:** revisão estratégica de mix de canal

O assistente vai consultar este arquivo SEMPRE antes de sugerir qualquer mudança em campanha. Mantenha vivo.

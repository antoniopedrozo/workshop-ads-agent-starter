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

### Investimento mensal por canal
| Canal      | Budget/mês  | CAC médio | Notas |
|------------|-------------|-----------|-------|
| Google Ads | R$ 35.000   | R$ 22.000 | Search domina, PMax desligado |
| LinkedIn   | R$ 25.000   | R$ 38.000 | CAC alto mas LTV maior, sustenta |
| Meta       | R$ 8.000    | R$ 45.000 | Em teste, cético do canal pra B2B RH |

---

## Google Ads

### O que funciona
- **Search "pesquisa de clima organizacional"** (e variações): CTR 6%, conv 4%, CAC R$ 18.000. Manter no ar.
- **Search "engajamento de funcionários"**: CTR 5%, conv 3,5%, CAC R$ 24.000.
- **Brand search ("acmerh", "acme rh")**: CAC R$ 1.500. Defesa contra concorrente que dá lance no nome.
- **Estrutura de campanha:** 1 campanha por intent (clima | engajamento | feedback contínuo | brand). Não misturar.

### O que não funciona
- **PMax**: subiu 2x, queimou R$ 40k cada vez. Lead quality péssima (autônomos, microempresas). Desligado.
- **Display network**: zero conversão útil. Desligado.
- **Search "software de RH"**: muito amplo, atrai folha/ponto. Negativado.
- **Search "ATS" / "recrutamento"**: não somos isso. Negativado.

### Negativações importantes (lista completa em `assets/negative-keywords-google.txt`)
`folha de pagamento`, `ponto eletrônico`, `recrutamento`, `ats`, `currículo`, `gratis`, `tcc`, `apostila`, `concurso`, `curso`, `udemy`

### Estratégia de lance
- Brand: Target Impression Share, 90%
- Search ICP: Maximize Conversions com tCPA R$ 600 (alvo SQL)
- Brand de concorrente (Feedz, TeamCulture): Manual CPC, lance baixo (R$ 4 max), pra filtrar quem busca alternativa

### Próximos testes
- Search "como medir clima organizacional" (intent informacional, qualificar via LP educativa)
- Performance Max só com audience signal de cargos de RH em empresas 100-500

---

## LinkedIn Ads

### O que funciona
- **Sponsored Content com case study em PDF**: CTR 0,8%, MQL R$ 280, CAC R$ 32.000. Manter.
- **Targeting:** Job title "Head of People", "Diretor de Recursos Humanos", "RH Business Partner" + Company Size 100-500 + Indústria "Tecnologia, Serviços Profissionais, Varejo"
- **Conversation Ads** pra Heads de RH: Demo agendada R$ 1.200, CAC R$ 28.000. Boa eficiência mas volume baixo.

### O que não funciona
- **Targeting por Skills** (ex: "Employee Engagement"): muito ruído, atinge consultor independente
- **Lead Gen Form sem qualificação**: lead bruto, qualquer um preenche. Sempre incluir 1 pergunta filtro: "Tamanho da empresa".
- **Vídeo de produto (45 segundos)**: caro demais pro engajamento que gera. Pausado.

### Próximos testes
- Account-Based Marketing com lista de 200 empresas Tier 1 nominais
- Document Ads (PDF nativo) com guia "10 perguntas pra fazer no próximo pulse"

---

## Meta Ads

### O que funciona (parcialmente)
- **Retargeting de visitantes da LP**: CPM baixo, traz de volta, mas conv abaixo do esperado (1%). Mantemos como assist.

### O que não funciona
- **Prospecting cold em B2B RH**: público profissional não consome conteúdo de B2B no Instagram. CAC R$ 80k+ em todos os testes. Pausado.
- **Lookalike de clientes**: público fica grande demais e dilui. Não converte.

### Próximos testes
- Reels com depoimento real de Head de RH (UGC) pra prospecting frio
- Decisão antes de janeiro/2026: se Meta não der CAC < R$ 50k em 90 dias, desligar canal

---

## Como gerar este arquivo automaticamente com Nekt + MCP

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

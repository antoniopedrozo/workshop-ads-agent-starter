---
name: search-terms-pruning
description: Workflow recorrente de auditoria e limpeza dos search terms do Google Ads. Identifica termos que gastam sem converter pra negativar, termos que convertem pra promover a exact match, e padrões de busca que sugerem nova campanha. Use semanalmente ou quando o usuário sentir que CAC subiu sem motivo claro.
---

# search-terms-pruning

Search terms são as buscas reais que dispararam seu ad (diferente de keywords, que são o que VOCÊ definiu). O Google match keyword com search term de várias formas (broad, phrase, exact), e quase sempre algumas combinações são desperdício.

Pruning recorrente é o cuidado básico de manutenção do Google Ads. Sem ele, o gasto cresce sem performance correspondente.

## Quando esta habilidade é acionada

- Cadência semanal ou quinzenal (recomendado)
- CAC subindo sem mudança em campanha
- Aumento de cliques sem aumento proporcional de conversão
- Suspeita de keyword amplificada matchando errado
- Antes de aumentar budget de campanha (limpar primeiro)

## O workflow padrão (45 minutos)

### 1. Puxar os search terms dos últimos 30 dias

Via script:

```bash
python api/google-ads/read_performance.py --report search-terms --days 30 --min-cost 50
```

Filtro `--min-cost 50` ignora termos que custaram menos de R$ 50 (ruído).

Via UI: Google Ads > Keywords > Search Terms > exportar CSV.

### 2. Classificar cada termo

Pra cada search term, decidir uma das ações:

| Decisão | Critério | Ação |
|---------|----------|------|
| **NEGATIVAR** | Gastou >R$ 100 com 0 conversão E intent não bate | Adicionar como negativa |
| **NEGATIVAR (intent errada)** | Atrai público fora do ICP, mesmo se converteu (ex: "curso de") | Negativar |
| **PROMOVER PRA EXACT** | Converteu 2+ vezes com CAC abaixo do alvo | Adicionar como exact match na campanha apropriada |
| **NOVA CAMPANHA** | Volume alto + intent diferente das campanhas existentes | Sugerir nova campanha (não adicionar na atual, vai poluir) |
| **MANTER** | Performando bem na campanha atual | Nada |
| **OBSERVAR** | Pouco volume ainda, intent OK | Aguardar mais dados |

### 3. Padrões comuns que viram negativações em massa

Quando você ver 5+ termos com o mesmo padrão, negativa o padrão broad ao invés de cada um:

- `[termo] grátis`, `[termo] free`, `[termo] download` → negativa `grátis`, `free`, `download grátis`
- `[termo] tcc`, `[termo] artigo`, `[termo] universidade` → negativa `tcc`, `monografia`, `universidade`
- `[termo] vaga`, `[termo] currículo`, `[termo] emprego` → negativa `vaga`, `currículo`, `emprego`
- `[termo] curso`, `[termo] aprender`, `[termo] como fazer` → negativa `curso`, `aula`, `como fazer` (cuidado: depende se você vende educação)
- `[termo] api`, `[termo] github`, `[termo] open source` → negativa se você vende SaaS, não API standalone

### 4. Aplicar negativações

```bash
python api/google-ads/add_negative_keywords.py \
  --campaign-id 123456789 \
  --negatives "free,grátis,curso,tcc,monografia"
```

Ou no nível de ad group, ou na lista de negativas compartilhada (recomendado pra não duplicar).

### 5. Documentar no `knowledge/ads-history.md`

Atualiza a seção "Negativações importantes" com o que foi adicionado.

## Heurísticas práticas

### "Quando negativar agressivo vs ser paciente"

- Se gasto > 3x o CAC alvo sem conversão: negativa imediato
- Se gasto entre 1x e 3x do CAC alvo, sem conversão: aguarda mais 7 dias
- Se converteu 1 vez mas com CAC 2x acima do alvo: aguarda 14 dias antes de decidir

### "Quando promover pra exact match"

- Search term apareceu 5+ vezes
- Converteu 2+ vezes
- CAC do search term < CAC alvo da campanha
- Tem volume justificável (>10 buscas/mês)

Adiciona como exact match e roda em ad group dedicado, pra você poder dar lance específico.

### "Quando search term sugere nova campanha"

Sinal: você vê 10+ search terms com intent claramente diferente da campanha atual, com volume alto.

Exemplo: campanha "AcmeRH - Clima Organizacional" começa a receber muito search por "feedback contínuo software". É hora de criar campanha nova "AcmeRH - Feedback Contínuo".

## Auditoria assistida com Claude

Pega o CSV exportado e cola na conversa, ou (melhor) usa o script:

```bash
python api/google-ads/read_performance.py --report search-terms --days 30 --min-cost 50 > search_terms.csv
```

Pede pro Claude:

> Leu `search_terms.csv` (anexo). Pra cada termo:
> 1. Classifica em uma das ações: NEGATIVAR, NEGATIVAR (intent errada), PROMOVER PRA EXACT, NOVA CAMPANHA, MANTER, OBSERVAR
> 2. Justifica em 1 linha
> 3. Se for NEGATIVAR, sugere se vai como negativa específica ou padrão broad
> 4. No final, agrupa as negativações por padrão (ex: todas com "grátis" viram 1 broad)
>
> Considera CAC alvo de `knowledge/pricing.md` (R$ 30k pra Tier 1) e ICP de `knowledge/icp.md`.

Confirma com usuário o que negativar antes de rodar `add_negative_keywords.py`.

## Métricas de saúde do pruning

Mantenha histórico no `knowledge/ads-history.md`:

- **% de gasto em search terms convertendo**: alvo > 70% (do gasto total, quanto está em terms que já trouxeram pelo menos 1 conv)
- **Taxa de novos search terms negativados**: depois de 6 meses de pruning, deve cair pra <5% por semana. Se continuar 15%+, sua keyword raiz está broad demais.
- **CAC médio antes/depois do pruning**: trimestralmente

## O que NÃO fazer

- Não negativa palavra que aparece junto com termo bom (cuidado: `grátis` é seguro; `software` é arriscado pode matar busca legítima)
- Não negativa imediato sem ler intent. Search term que parece estranho pode ser cliente real.
- Não promova pra exact com 1 conversão. Pode ter sido sorte.
- Não esquece de aplicar negativa em todas as campanhas relevantes (lista compartilhada resolve)
- Não pula a documentação. Sem histórico, daqui 6 meses você não sabe por que negativou X.

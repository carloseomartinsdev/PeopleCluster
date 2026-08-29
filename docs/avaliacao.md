# Avaliação

Código: `notebooks/05_avaliacao.ipynb`
Módulo: `src/model/avaliacao.py`

## Escopo

Avaliar a segmentação com os rótulos reservados abertos (`Attrition`, `PerformanceRating`), medir estabilidade e propor ações por perfil.

## Critérios

| Critério | Valor | Situação |
|---|---:|:---|
| k entre 2 e 5 | 2 | ok |
| Menor segmento ≥ 5% | ≈ 50% | ok |
| Silhueta Gower | ≈ 0,07 | fraca (esperada na base sintética) |
| ARI médio bootstrap K-Means | ≈ 0,67 | ok |
| ARI médio bootstrap K-Medoids | ≈ 0,27 | atenção |
| Concordância entre métodos (ARI) | ≈ 0 | baixa — métodos divergem |
| Cada grupo com ação de RH | 2 | ok |

## Concordância entre métodos

O ARI entre K-Medoids (Gower), hierárquica (Gower) e K-Means fica próximo de zero: as partições **não coincidem**. A leitura de negócio adota o K-Medoids/Gower como modelo principal (adequado a dados mistos), com as demais vias como comparativo.

## Perfis (K-Medoids / Gower)

| Cluster | n | Attrition % | Renda mediana | Anos empresa | Hipótese Canvas |
|---|---:|---:|---:|---:|---|
| 0 | 733 | 11,1 | 6.347 | 8 | Estáveis e engajados |
| 1 | 737 | 21,2 | 3.376 | 4 | Risco de attrition + início de carreira |

## Ações recomendadas

| Cluster | Ações | KPI |
|---|---|---|
| 0 | Retenção de longo prazo; reconhecimento; benefícios de permanência | Attrition; JobSatisfaction; OverTime |
| 1 | Revisão salarial; clima; acompanhamento; mentoria; capacitação; onboarding | Attrition; JobSatisfaction; OverTime |

## Hipóteses do Canvas

| Hipótese | Situação |
|---|---|
| Estáveis e engajados | sustentada (cluster 0) |
| Risco de attrition | sustentada (cluster 1) |
| Início de carreira | sustentada parcialmente (cluster 1) |
| Alta performance e alta carga | não emergiu como segmento próprio em k=2 |
| Baixo engajamento | não emergiu como segmento próprio em k=2 |

## Artefatos

- `reports/tables/avaliacao_*.csv`
- `reports/figures/10_ari_metodos.png`
- `reports/figures/11_bootstrap_ari.png`
- `reports/figures/12_attrition_por_cluster.png`
- `models/catalogo_personas.json`

## Limitações

Estrutura de grupos fraca (silhueta baixa, ARI entre métodos baixo, bootstrap do K-Medoids modesto). O valor do resultado está no contraste de attrition e no pacote de ações, não na separação geométrica forte.

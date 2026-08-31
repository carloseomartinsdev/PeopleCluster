# Avaliação

Código: `notebooks/05_avaliacao.ipynb`
Módulos: `src/model/avaliacao.py`, `src/model/associacao.py`

## O que esta fase faz

Abre os rótulos que estavam reservados (`Attrition`, `PerformanceRating`), mede estabilidade, descreve coocorrências e propõe ação por perfil.

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

O ARI entre K-Medoids (Gower), hierárquica (Gower) e K-Means fica próximo de zero: as partições **não coincidem**. A leitura de negócio usa o K-Medoids/Gower como modelo principal.

## Associação

Apriori e FP-Growth devolvem os **mesmos** conjuntos frequentes (suporte 0,12, tamanho ≤ 3). Regras com consequente em `cluster:` ou `OverTime:` em `reports/tables/avaliacao_regras_associacao.csv`. Leitura típica: cargo/departamento coocorrem com o cluster (ex.: Sales Executive com cluster 0).

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

Perguntas SMART: `reports/tables/avaliacao_perguntas_smart.csv`.
Vazamento: `Attrition`, `PerformanceRating` e `EmployeeNumber` **não** estão nas features (`avaliacao_auditoria_vazamento.csv`).

## Artefatos

- `reports/tables/avaliacao_*.csv`
- `reports/figures/10_ari_metodos.png`
- `reports/figures/11_bootstrap_ari.png`
- `reports/figures/12_attrition_por_cluster.png`
- `models/catalogo_personas.json`

## Limitações

A estrutura de grupos é fraca (silhueta baixa, ARI entre métodos baixo, bootstrap do K-Medoids modesto). O que justifica a implantação é o contraste de attrition (~11% vs ~21%) e o conjunto de ações por grupo.

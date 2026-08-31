# Modelagem

Código: `notebooks/04_modelagem_clusters.ipynb`
Módulos: `src/model/` (Gower, K-Medoids, hierárquica, DBSCAN, GMM)

## Objetivo

Obter grupos que o RH consiga nomear (k entre 2 e 5) e comparar métodos, porque o dado é misto.

## Desenho do experimento

| Família | Método | Espaço | Papel |
|---|---|---|---|
| Particional | K-Medoids | Gower | **Oficial** |
| Particional | K-Means | one-hot + StandardScaler | Comparativo |
| Hierárquica | average / complete / single | Gower | Comparativo |
| Densidade | DBSCAN | one-hot + StandardScaler | Comparativo |
| Mistura | GMM | one-hot + StandardScaler | Comparativo (grau de pertencimento) |
| Redução | PCA (visualização) | one-hot + StandardScaler | Diagnóstico |
| Associação | Apriori / FP-Growth | transações do colaborador | Avaliação (notebook 05) |

## Escolha de k

Varredura k = 2…5. Critério principal: silhueta do K-Medoids sobre Gower, respeitando o teto de 5 grupos e a possibilidade de ler os perfis em linguagem de RH.

| k | Silhueta Gower (K-Medoids) | Silhueta K-Means |
|---|---:|---:|
| 2 | 0,075 | 0,111 |
| 3 | 0,052 | 0,083 |
| 4 | 0,053 | 0,096 |
| 5 | 0,042 | 0,089 |

**Decisão:** k = **2** (maior silhueta em Gower).

A silhueta absoluta é baixa, o que é coerente com o enunciado do Tema 08. O que decidiu o k = 2 foi a combinação de maior silhueta no Gower e perfis que ainda dão para explicar.

## Resultado principal (K-Medoids / Gower, k=2)

| Cluster | n | Attrition % | OverTime % | Satisfação (méd.) | Renda mediana | Idade méd. | Anos empresa |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 733 | 11,1 | 26,2 | 2,77 | 6.347 | 37 | 8 |
| 1 | 737 | 21,2 | 30,4 | 2,69 | 3.376 | 34 | 4 |

- **Cluster 0 — mais estável:** renda e tempo de casa maiores, menor attrition.
- **Cluster 1 — maior risco:** renda e tempo de casa menores, maior attrition e overtime.

## GMM (comparativo)

Varredura em `reports/tables/varredura_gmm.csv`. No k oficial, a covariância de menor BIC foi **full** (silhueta ≈ 0,08). Premissa gaussiana frágil com Likert e dummies: o GMM **não** substitui Gower. Rótulos em `cluster_gmm` de `rotulos_clusters.csv`.

## Outros métodos

- Hierárquica (Gower): ligação `average` com melhor cofenético.
- DBSCAN: predomina um componente denso — pouco útil para definir trilha de desenvolvimento.
- PCA-2D: visualização (~18–29% da variância conforme o espaço).

## Artefatos

| Arquivo | Conteúdo |
|---|---|
| `data/processed/rotulos_clusters.csv` | Rótulos por método (inclui GMM) |
| `models/decisao_modelagem.json` | Parâmetros da decisão oficial |
| `models/decisao_gmm.json` | Configuração GMM comparativa |
| `reports/tables/varredura_*.csv` | Varreduras de k |
| `reports/figures/07_escolha_k.png` | Curvas de silhueta |
| `reports/figures/08_dendrograma_gower.png` | Dendrograma |
| `reports/figures/09_pca_clusters.png` | Projeção PCA |

# Modelagem

Código: `notebooks/04_modelagem_clusters.ipynb`
Módulos: `src/model/` (Gower, K-Medoids, hierárquica, DBSCAN)

## Objetivo técnico

Obter segmentos interpretáveis de colaboradores (k entre 2 e 5), comparando métodos para dados mistos.

## Desenho do experimento

| Família | Método | Espaço |
|---|---|---|
| Particional | K-Medoids | Gower |
| Particional | K-Means | one-hot + StandardScaler |
| Hierárquica | average / complete / single | Gower |
| Densidade | DBSCAN | one-hot + StandardScaler |
| Redução | PCA (visualização) | one-hot + StandardScaler |

## Escolha de k

Varredura k = 2…5. Critério principal: silhueta do K-Medoids sobre Gower, sujeita ao teto de 5 grupos e à interpretabilidade de RH.

| k | Silhueta Gower (K-Medoids) | Silhueta K-Means |
|---|---:|---:|
| 2 | 0,075 | 0,111 |
| 3 | 0,052 | 0,083 |
| 4 | 0,053 | 0,096 |
| 5 | 0,042 | 0,089 |

**Decisão:** k = **2** (maior silhueta em Gower).

A silhueta absoluta é baixa, coerente com o enunciado do Tema 08 (estrutura de grupos fraca em base sintética). O critério decisivo é a legibilidade gerencial dos perfis.

## Resultado principal (K-Medoids / Gower, k=2)

| Cluster | n | Attrition % | OverTime % | Satisfação (méd.) | Renda mediana | Idade méd. | Anos empresa |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 733 | 11,1 | 26,2 | 2,77 | 6.347 | 37 | 8 |
| 1 | 737 | 21,2 | 30,4 | 2,69 | 3.376 | 34 | 4 |

- **Cluster 0 — mais estável:** renda e tempo de casa maiores, menor attrition.
- **Cluster 1 — maior risco:** renda e tempo de casa menores, maior attrition e overtime.

## Outros métodos

- Hierárquica (Gower): ligação `average` com melhor cofenético no comparativo.
- DBSCAN (espaço padronizado): calibração por joelho da curva k-distância; na configuração testada predomina um único componente denso com pouco ruído — pouco útil para segmentação acionável nesta base.
- PCA-2D: usado apenas para visualização (~18% da variância).

## Artefatos

| Arquivo | Conteúdo |
|---|---|
| `data/processed/rotulos_clusters.csv` | Rótulos por método |
| `models/decisao_modelagem.json` | Parâmetros da decisão |
| `reports/tables/varredura_*.csv` | Varreduras de k |
| `reports/tables/perfil_clusters_kmedoids.csv` | Perfis |
| `reports/figures/07_escolha_k.png` | Curvas de silhueta |
| `reports/figures/08_dendrograma_gower.png` | Dendrograma |
| `reports/figures/09_pca_clusters.png` | Projeção PCA |

## Próxima fase

Avaliação de negócio: confrontar hipóteses do Canvas, estabilidade entre métodos e ações por perfil (`docs/avaliacao.md`).

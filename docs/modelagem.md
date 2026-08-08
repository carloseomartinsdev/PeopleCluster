# Modelagem

## Objetivo técnico

Obter de 2 a 5 segmentos de colaboradores interpretáveis, comparando métodos adequados a dados mistos e validando estabilidade entre algoritmos.

## Desenho do experimento

1. Entrada: `data/processed/hr_features_cluster.csv` e tipologia associada
2. Dissimilaridade de Gower
3. K-Medoids, clusterização hierárquica e DBSCAN
4. Comparativo com K-Means/GMM sobre matriz one-hot padronizada
5. PCA nas variáveis numéricas correlacionadas, se agregar interpretação
6. Seleção de \(k\) por métricas internas e legibilidade de negócio

Notebook: `notebooks/04_modelagem_clusters.ipynb`

## Regras de associação

- Discretização / flags a partir das variáveis relevantes
- Apriori e/ou FP-Growth
- Confrontação das regras com a segmentação obtida

Notebook: `notebooks/05_regras_associacao.ipynb`

## Critérios de comparação

- Silhueta e coerência dos perfis
- Estabilidade entre métodos
- Adequação ao limite de cinco grupos

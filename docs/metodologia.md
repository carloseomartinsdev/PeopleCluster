# Metodologia

O projeto adota o **CRISP-DM** (Cross-Industry Standard Process for Data Mining):

```mermaid
flowchart LR
  A[Negócio] --> B[Dados]
  B --> C[Preparação]
  C --> D[Modelagem]
  D --> E[Avaliação]
  E --> F[Implantação]
  E -.-> B
```

## Técnicas

| Família | Métodos |
|---|---|
| Distância | Gower (dados mistos) |
| Clusterização | K-Medoids / PAM, Hierárquica, DBSCAN |
| Comparativo | K-Means, GMM |
| Redução dimensional | PCA |
| Associação | Apriori, FP-Growth |

## Restrições de modelagem

- No máximo **5** segmentos acionáveis
- Variáveis `Attrition` e `PerformanceRating` reservadas para avaliação externa (não entram na formação dos clusters)
- Preferência por interpretabilidade de negócio em relação a índices internos isolados

## Ferramentas

- Python 3.12 (`uv` / `pyproject.toml`)
- Jupyter notebooks em `notebooks/`
- Documentação MkDocs Material em `docs/`

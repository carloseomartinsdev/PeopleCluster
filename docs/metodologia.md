# Metodologia

O projeto adota o **CRISP-DM**:

```mermaid
flowchart LR
  A[Negocio] --> B[Dados]
  B --> C[Preparacao]
  C --> D[Modelagem]
  D --> E[Avaliacao]
  E --> F[Implantacao]
  E -.-> B
```

## Técnicas e papel

| Família | Métodos | Papel neste projeto |
|---|---|---|
| Distância | Gower | Espaço do **modelo oficial** (dados mistos) |
| Clusterização | K-Medoids / PAM | Partição publicada (k=2) |
| Clusterização | Hierárquica, DBSCAN, K-Means | Comparativo |
| Mistura | GMM (sklearn) | Comparativo no espaço one-hot + StandardScaler; BIC/AIC; não substitui Gower |
| Redução dimensional | PCA | Diagnóstico e visualização |
| Associação | Apriori e FP-Growth (`mlxtend`) | Coocorrência colaborador × itens; conjuntos equivalentes nos mesmos limiares |

## Restrições de modelagem

- No máximo **5** segmentos acionáveis
- `Attrition` e `PerformanceRating` reservadas para avaliação externa
- Preferência por interpretabilidade de negócio em relação a índices internos isolados

## Ferramentas

- Python 3.12 (`uv` / `pyproject.toml`)
- Jupyter notebooks em `notebooks/`
- Documentação MkDocs Material em `docs/`
- Streamlit em `src/deployment/app.py`

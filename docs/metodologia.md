# Metodologia

O projeto segue o **CRISP-DM**: entendimento do negócio, dos dados, preparação, modelagem, avaliação e implantação. A avaliação pode devolver à preparação ou à modelagem — foi o caso da escolha de k.

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

- No máximo **5** grupos, por decisão da diretoria do cenário
- `Attrition` e `PerformanceRating` reservadas para avaliação externa
- Quando o índice interno e a leitura de RH não coincidem, prevalece a leitura de RH (nesta base a silhueta nunca foi alta)

## Ferramentas

- Python 3.12 (`uv` / `pyproject.toml`)
- Jupyter notebooks em `notebooks/`
- Documentação MkDocs Material em `docs/`
- Streamlit em `src/deployment/app.py`


## Ferramentas

- Python 3.12 (`uv` / `pyproject.toml`)
- Jupyter notebooks em `notebooks/`
- Documentação MkDocs Material em `docs/`
- Streamlit em `src/deployment/app.py`

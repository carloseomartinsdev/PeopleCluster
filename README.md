# PeopleCluster

Segmentação de colaboradores e trilhas de desenvolvimento — Tema 08 (RH e People Analytics), CRISP-DM, k=2 (K-Medoids / Gower).

**Base:** [IBM HR Analytics Employee Attrition & Performance](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) (1.470 × 35).

## Reprodução

```bash
uv sync
uv run python scripts/rodar_modelagem.py    # gera matriz Gower local (~8 MB, gitignore)
uv run python scripts/rodar_avaliacao.py
uv run python scripts/rodar_fechamento.py   # EDA extra, GMM, associação, relatório
uv run invoke app                           # http://localhost:8501
uv run invoke docs                          # http://127.0.0.1:8000
uv run invoke test
```

Semente do projeto: **42** (`src/config.py`).

## Documentação

Conteúdo principal em [`docs/`](docs/). Relatório final: [`reports/relatorio-final.md`](reports/relatorio-final.md).

## Notebooks

| Notebook | Conteúdo |
|---|---|
| `notebooks/01_exploracao_inicial.ipynb` | Carga e visão inicial |
| `notebooks/02_eda.ipynb` | EDA (inclui Spearman, Tukey, PCA) |
| `notebooks/03_preparacao.ipynb` | Limpeza, tipologia, sensibilidade à escala |
| `notebooks/04_modelagem_clusters.ipynb` | Gower, K-Medoids, hierárquica, DBSCAN, GMM |
| `notebooks/05_avaliacao.ipynb` | ARI, bootstrap, associação, SMART |
| `notebooks/06-implantacao.ipynb` | Pacote, scoring, relatório final |
| `notebooks/07_modelagem_bonus.ipynb` | Grade sklearn (contraste) |

## Equipe

- [Carlos E. O. Martins](https://github.com/carloseomartinsdev)
- [Ana Caroline Amorim](https://github.com/amorinana)

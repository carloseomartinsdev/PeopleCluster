# PeopleCluster

Segmentação de colaboradores e trilhas de desenvolvimento — Tema 08 (RH e People Analytics), aprendizado não supervisionado com CRISP-DM.

**Base:** [IBM HR Analytics Employee Attrition & Performance](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) (1.470 × 35).

## Documentação

```bash
uv sync
uv run invoke docs    # http://127.0.0.1:8000
uv run invoke lab     # notebooks
```

Conteúdo principal em [`docs/`](docs/).

## Notebooks

| Notebook | Conteúdo |
|---|---|
| `notebooks/01_exploracao_inicial.ipynb` | Carga e visão inicial |
| `notebooks/02_eda.ipynb` | Análise exploratória |
| `notebooks/03_preparacao.ipynb` | Preparação dos dados |
| `notebooks/04_modelagem_clusters.ipynb` | Gower, K-Medoids, hierárquica, DBSCAN |
| `notebooks/05_avaliacao.ipynb` | ARI, bootstrap, personas e ações |
| `notebooks/06-implantacao.ipynb` | Pacote operacional, scoring, monitoramento |
| `notebooks/07_modelagem_bonus.ipynb` | Grade KMeans / MiniBatch / Bisecting (contraste) |

## Estrutura

```
data/raw/          # dados originais
data/processed/    # dados preparados
docs/              # documentação MkDocs
notebooks/         # análises
references/        # canvas, dicionário, enunciados
reports/figures/   # figuras
src/               # código / app
```

## Equipe

- [Carlos E. O. Martins](https://github.com/carloseomartinsdev)
- [Ana Caroline Amorim](https://github.com/amorinana)

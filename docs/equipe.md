# Equipe e critérios

Integrantes:

- **Carlos E. O. Martins** ([@carloseomartinsdev](https://github.com/carloseomartinsdev))
- **Ana Caroline Amorim** ([@amorinana](https://github.com/amorinana))

O trabalho tem nove critérios (0 a 8). Quatro são em grupo e cinco são individuais.

| Modalidade | Critérios |
|---|---|
| Grupo | 0, 6, 7 e 8 |
| Individual | 1, 2, 3, 4 e 5 |

A parte individual segue o CRISP-DM: canvas e EDA com Carlos; preparação, modelagem e avaliação com Ana. Nos critérios de grupo os dois participam. A coluna “coordenação” só indica quem inicia a apresentação.

O [canvas](canvas_problema.md) e o [relatório de EDA](analise-exploratoria.md) publicados no site são textos de Ana Caroline Amorim.

| # | Critério | Modalidade | Coordenação / responsável | Onde está |
|:-:|:---|:---|:---|:---|
| **0** | Repositório, ambiente, dados brutos | Grupo | Carlos | `pyproject.toml`, `uv.lock`, `data/raw/`, README |
| **1** | Canvas e perguntas | Individual | Carlos | [Canvas](canvas_problema.md), [quadro PBL](pbl/quadro-pbl.md) |
| **2** | Relatório de EDA e insights | Individual | Carlos | [EDA](analise-exploratoria.md), notebooks `01`–`02` |
| **3** | Preparação | Individual | Ana | notebook `03`, [preparação](preparacao.md) |
| **4** | Modelagem | Individual | Ana | notebook `04`, [modelagem](modelagem.md) |
| **5** | Avaliação | Individual | Ana | notebook `05`, [avaliação](avaliacao.md) |
| **6** | Streamlit | Grupo | Ana | `src/deployment/app.py`, `uv run invoke app` |
| **7** | Artefatos do repositório | Grupo | Carlos | GitHub, `reports/`, MkDocs |
| **8** | Relatório final | Grupo | Carlos | [relatório](relatorio-final.md) |

### Critérios 1 e 2 (Carlos) e coordenação de 0, 7 e 8

- **1 — Canvas:** por que `Attrition` fica fora do cluster, teto de cinco grupos, e o que o k = 2 fez com as hipóteses.
- **2 — EDA:** OverTime, renda, Likert, outliers mantidos, bloco JobLevel/renda.
- **0, 7 e 8:** ambiente `uv`, estrutura do repositório, relatório final.

### Critérios 3, 4 e 5 (Ana) e coordenação do 6

- **3 — Preparação:** constantes, tipologia, Gower versus scaler.
- **4 — Modelagem:** k = 2 no Gower; GMM, hierárquica e DBSCAN como comparativo.
- **5 — Avaliação:** attrition 11% vs 21%, ARI, Apriori equivalente a FP-Growth, auditoria de vazamento.
- **6 — Streamlit:** personas, classificação de colaborador, monitoramento.

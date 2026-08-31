# Implantação

Publicação operacional da segmentação PeopleCluster (K-Medoids + Gower, **k = 2**), com classificação de novos colaboradores pelo medoide Gower mais próximo.

Notebook: [`notebooks/06-implantacao.ipynb`](../notebooks/06-implantacao.ipynb).
Relatório final: [`relatorio-final.md`](relatorio-final.md) (cópia de `reports/relatorio-final.md`).

## Artefatos

| Artefato | Destino |
|---|---|
| Pacote de scoring | `models/pacote_implantacao.json` |
| Carteira classificada | `data/processed/carteira_classificada.csv` |
| Metadados | `models/metadados_implantacao.json` |
| Entregas / monitoramento / pitch | `reports/tables/implantacao_*.csv` |
| Relatório final | `reports/relatorio-final.md` |
| App Streamlit | `src/deployment/app.py` — `uv run invoke app` |
| Módulo de classificação | `src/deployment/scoring.py` |

## Contrato de classificação

1. Entrada: atributos do colaborador nas colunas do pacote.
2. Distância Gower ao medoide de cada cluster.
3. Atribuição ao cluster de menor distância; margem entre 1º e 2º medoide → confiança (`alta` / `media` / `baixa`).
4. Saída: cluster, persona, ações e KPI.

Reprodução na base de treino: acordância **100%** com os rótulos publicados.

O app tem três abas: personas, **classificar colaborador** (formulário + `scoring.classificar_colaborador`) e monitoramento.

## Segmentos publicados

| Cluster | Persona | Attrition (ref.) | Foco operacional |
|---|---|---|---|
| 0 | Estáveis e engajados | ~11% | Permanência, reconhecimento, sucessão |
| 1 | Risco de attrition / início de carreira | ~21% | Remuneração, clima, mentoria, onboarding |

## Monitoramento

Ver `reports/tables/implantacao_monitoramento.csv` (attrition, satisfação, OverTime, confiança baixa, reciclagem anual).

## Bônus (sklearn)

Notebook [`07_modelagem_bonus.ipynb`](../notebooks/07_modelagem_bonus.ipynb): grade KMeans / MiniBatchKMeans / BisectingKMeans — contraste, sem substituir Gower em produção.

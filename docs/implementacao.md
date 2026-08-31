# Implantação

Classificação de colaboradores novos pelo medoide Gower mais próximo (K-Medoids, **k = 2**). O uso previsto é o aplicativo Streamlit e a carteira em CSV.

Notebook: [`notebooks/06-implantacao.ipynb`](../notebooks/06-implantacao.ipynb).
Relatório final: [`relatorio-final.md`](relatorio-final.md).

## Artefatos

| Artefato | Destino |
|---|---|
| Pacote de scoring | `models/pacote_implantacao.json` |
| Carteira classificada | `data/processed/carteira_classificada.csv` |
| Metadados | `models/metadados_implantacao.json` |
| Entregas / monitoramento / pitch | `reports/tables/implantacao_*.csv` |
| Relatório final | [relatorio-final.md](relatorio-final.md) |
| App Streamlit | `src/deployment/app.py` — `uv run invoke app` |
| Módulo de classificação | `src/deployment/scoring.py` |

## Como um colaborador novo é classificado

1. Entram os atributos do colaborador nas colunas do pacote.
2. Calcula-se a distância Gower até o medoide de cada cluster.
3. O colaborador vai para o cluster de menor distância. A margem entre o 1º e o 2º medoide vira confiança (`alta` / `media` / `baixa`).
4. A saída é cluster, persona, ações e KPI.

Na base de treino o scoring reproduz **100%** dos rótulos publicados — esperado, porque os medoides saíram dessa base. Colaborador novo é outra situação.

O app tem três abas: personas, classificar colaborador e monitoramento.

## Grupos

| Cluster | Persona | Attrition (ref.) | Foco |
|---|---|---|---|
| 0 | Estáveis e engajados | ~11% | Permanência, reconhecimento, sucessão |
| 1 | Risco de attrition / início de carreira | ~21% | Remuneração, clima, mentoria, onboarding |

## Monitoramento

Ver `reports/tables/implantacao_monitoramento.csv` (attrition, satisfação, OverTime, confiança baixa, reciclagem anual).

## Bônus (sklearn)

Notebook [`07_modelagem_bonus.ipynb`](../notebooks/07_modelagem_bonus.ipynb): grade KMeans / MiniBatchKMeans / BisectingKMeans — contraste, sem substituir Gower em produção.

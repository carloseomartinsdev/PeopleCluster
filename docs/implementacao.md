# Implantação

Publicação operacional da segmentação PeopleCluster (K-Medoids + Gower, **k = 2**), com classificação de novos colaboradores pelo medoide Gower mais próximo.

Notebook: [`notebooks/06-implantacao.ipynb`](../notebooks/06-implantacao.ipynb).

## Artefatos

| Artefato | Destino |
|---|---|
| Pacote de scoring | `models/pacote_implantacao.json` |
| Carteira classificada | `data/processed/carteira_classificada.csv` |
| Metadados | `models/metadados_implantacao.json` |
| Entregas / monitoramento / pitch | `reports/tables/implantacao_*.csv` |
| Figura de segmentos | `reports/figures/13_implantacao_segmentos.png` |
| App Streamlit (personas) | `src/deployment/app.py` |
| Módulo de classificação | `src/deployment/scoring.py` |

## Contrato de classificação

1. Entrada: atributos do colaborador nas colunas do pacote (`Age`, `MonthlyIncome`, `OverTime`, …).
2. Distância Gower ao medoide de cada cluster (EmployeeNumber **476** e **933** na base de referência).
3. Atribuição ao cluster de menor distância; margem entre 1º e 2º medoide → confiança (`alta` / `media` / `baixa`).
4. Saída: cluster, persona, ações e KPI do `catalogo_personas.json`.

Reprodução na base de treino: acordância **100%** com os rótulos publicados.

## Segmentos publicados

| Cluster | Persona | Attrition (ref.) | Foco operacional |
|---|---|---|---|
| 0 | Estáveis e engajados | ~11% | Permanência, reconhecimento, sucessão |
| 1 | Risco de attrition / início de carreira | ~21% | Remuneração, clima, mentoria, onboarding |

## Monitoramento

| KPI | Segmento | Frequência |
|---|---|---|
| Taxa de attrition | 0 e 1 | mensal |
| JobSatisfaction / WorkLifeBalance | 0 e 1 | trimestral |
| % OverTime | 1 (prioridade) | mensal |
| Adesão a mentoria/capacitação | 1 | trimestral |
| Permanência / reconhecimento | 0 | semestral |

## Uso operacional

1. Classificar novos colaboradores com `scoring.classificar_colaborador` (ou o app Streamlit).
2. Acionar o pacote de ações do catálogo de personas.
3. Revisar a segmentação periodicamente (reamostragem / nova base HR).

## Bônus (sklearn)

Notebook [`07_modelagem_bonus.ipynb`](../notebooks/07_modelagem_bonus.ipynb): grade KMeans / MiniBatchKMeans / BisectingKMeans na matriz escalada — contraste com o modelo principal Gower, sem substituí-lo em produção.

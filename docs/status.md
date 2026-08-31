# Status do projeto

As seis fases do CRISP-DM estão fechadas. O modelo adotado na implantação é **K-Medoids com Gower, k = 2**.

| Indicador | Valor |
|:---|---:|
| Fases do CRISP-DM | 6 de 6 |
| Notebooks da cadeia | 01–07 |
| Modelo oficial | K-Medoids / Gower, k=2 |
| Comparativos | K-Means, hierárquica, DBSCAN, GMM |
| Associação | Apriori e FP-Growth (mesmos conjuntos frequentes) |
| Relatório final | [relatorio-final.md](relatorio-final.md) |

## Fase 0–1: Ambiente e negócio

- [x] Repositório e ambiente `uv` / pre-commit
- [x] [Canvas do Problema](canvas_problema.md)
- [x] Critérios de sucesso e perguntas orientadas a dados
- [x] [Quadro PBL](pbl/quadro-pbl.md) (reconstituído; não há foto do quadro da sala)

## Fase 2: Entendimento dos dados

- [x] Base bruta 1.470 × 35
- [x] EDA (univariada, bivariada Spearman/Cramér, Tukey, PCA exploratório)
- [x] Coleção de insights em `reports/tables/eda_insights.csv`

## Fase 3: Preparação

- [x] Limpeza, tipologia, rótulos reservados
- [x] Experimento de escala
- [x] Gower (arquivo local) e StandardScaler

## Fase 4: Modelagem

- [x] Varredura de k, K-Medoids, hierárquica, DBSCAN, GMM
- [x] Bônus sklearn (notebook 07)

## Fase 5: Avaliação

- [x] ARI, bootstrap, personas, perguntas SMART, auditoria de vazamento
- [x] Regras de associação

## Fase 6: Implantação

- [x] Pacote de scoring e carteira classificada
- [x] Streamlit (personas, classificar, monitoramento)
- [x] Relatório final (capítulos I–IX)

## O que ficou em aberto

1. A base é sintética: os padrões podem não se repetir em um RH real.
2. Reciclagem do modelo a cada 12 meses, ou antes se a carteira mudar de forma relevante.

# Status do projeto

**Ciclo CRISP-DM concluído.** Decisão: **implantar** a partição K-Medoids/Gower (k = 2).

| Indicador | Valor |
|:---|---:|
| Fases do CRISP-DM | 6 de 6 |
| Notebooks da cadeia | 01–07 |
| Modelo oficial | K-Medoids / Gower, k=2 |
| Comparativos | K-Means, hierárquica, DBSCAN, GMM |
| Associação | Apriori ≡ FP-Growth |
| Relatório final | `reports/relatorio-final.md` |

???+ success "Fase 0–1: Ambiente e negócio"
    - [x] Repositório e ambiente `uv` / pre-commit
    - [x] [Canvas do Problema](pbl/canvas-do-problema.md)
    - [x] Critérios de sucesso e perguntas orientadas a dados
    - [x] [Quadro PBL](pbl/quadro-pbl.md) reconstituído (sem fotos do quadro físico)

???+ success "Fase 2: Entendimento dos dados"
    - [x] Base bruta 1.470 × 35
    - [x] EDA (univariada, bivariada Spearman/Cramér, Tukey, PCA exploratório)
    - [x] Coleção de insights em `reports/tables/eda_insights.csv`

???+ success "Fase 3: Preparação"
    - [x] Limpeza, tipologia, rótulos reservados
    - [x] Experimento de escala
    - [x] Gower (local) e StandardScaler

???+ success "Fase 4: Modelagem"
    - [x] Varredura k, K-Medoids, hierárquica, DBSCAN, GMM
    - [x] Bônus sklearn (notebook 07)

???+ success "Fase 5: Avaliação"
    - [x] ARI / bootstrap / personas / SMART / vazamento
    - [x] Regras de associação

???+ success "Fase 6: Implantação"
    - [x] Pacote de scoring e carteira classificada
    - [x] Streamlit (personas + classificar + monitoramento)
    - [x] Relatório final Cap. I–IX

## O que ficou em aberto

1. Base sintética: padrões podem não se repetir em um RH real.
2. Reciclagem do modelo a cada 12 meses.

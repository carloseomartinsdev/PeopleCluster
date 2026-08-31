# PeopleCluster

## Introdução

PeopleCluster é um projeto de People Analytics para segmentar colaboradores e propor trilhas de desenvolvimento. A organização do cenário usa a mesma política de carreira e retenção para todos. A modelagem (K-Medoids com distância de Gower, k = 2) separou **dois perfis**, com taxa de saída de cerca de **11%** em um grupo e **21%** no outro.

!!! success "Resultado da modelagem"
    Cluster 0 — estáveis e engajados (renda e tempo de casa maiores). Cluster 1 — risco / início de carreira. App de consulta e classificação: `uv run invoke app`. Relatório: [relatório final](relatorio-final.md).

A abordagem é **CRISP-DM**, com clusterização em dados mistos (Gower) e regras de associação (Apriori / FP-Growth) como evidência de coocorrência. GMM entra como comparativo no espaço euclidiano, **não** como modelo oficial. O canvas completo e o relatório de EDA estão em [Canvas do problema](canvas_problema.md) e [Análise exploratória](analise-exploratoria.md).

## Dados do projeto

| Campo | Valor |
|---|---|
| Nome | PeopleCluster |
| Tema | 08 – RH e People Analytics |
| Entidade de análise | Funcionário (Employee) |
| Base | IBM HR Analytics Employee Attrition & Performance |
| Volume | 1.470 registros × 35 variáveis |
| Licença | ODbL / DbCL 1.0 |
| Restrição da diretoria | No máximo 5 grupos |
| Stack | Python 3.12, `uv`, pandas, scikit-learn, mlxtend, Streamlit, MkDocs |

### Tipo do projeto

!!! info ""
    - [x] Análise exploratória
    - [ ] Modelo preditivo
    - [ ] Modelo de classificação
    - [x] Modelo de agrupamento
    - [ ] Detecção de anomalias

### Confidencialidade

!!! warning ""
    - [x] Público
    - [ ] Interno
    - [ ] Restrito

### Objetivo de negócio

!!! quote ""
    Identificar perfis distintos de colaboradores e propor trilhas de desenvolvimento específicas para cada grupo, aumentando retenção, satisfação e desempenho organizacional.

## Perguntas orientadoras

1. Quantos grupos existem e por que esse número?
2. O que caracteriza cada grupo em linguagem de negócio?
3. Que padrões de coocorrência sustentam ou contradizem a segmentação?
4. Qual ação diferenciada cada grupo deve receber, e como medir o sucesso?

## Como reproduzir

```bash
uv sync
uv run python scripts/rodar_modelagem.py   # Gower local + rótulos
uv run python scripts/rodar_avaliacao.py
uv run python scripts/rodar_fechamento.py  # EDA extra, GMM, associação, relatório
uv run invoke app                          # http://localhost:8501
uv run invoke docs                         # http://127.0.0.1:8000
```

A matriz `data/processed/matriz_gower.npy` não vai para o Git (~8 MB). Regenere com o script de modelagem.

## Histórico do documento

| Data | Versão | Descrição | Autor |
| :--------- | :----- | :-------- | :---- |
| 07/08/2026 | 1.0 | Estrutura inicial do projeto e Canvas | Carlos E. O. Martins |
| 08/08/2026 | 1.1 | Documentação das fases de negócio, dados e preparação | Carlos E. O. Martins |
| 31/08/2026 | 2.0 | Ciclo CRISP-DM fechado: k=2, GMM, associação, app e relatório final | Carlos E. O. Martins |

## Equipe

- Carlos E. O. Martins ([@carloseomartinsdev](https://github.com/carloseomartinsdev))
- Ana Caroline Amorim ([@amorinana](https://github.com/amorinana))

Divisão dos nove critérios (0–8): **grupo** 0, 6, 7 e 8 · **individual** 1–5. Tabela completa em [Equipe e critérios](equipe.md).

## Solicitante

Diretoria Executiva (cenário PBL — memorando do Encontro 1).

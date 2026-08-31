# PeopleCluster — relatório final

**Tema 08 · RH e People Analytics** · CRISP-DM fases 1 a 6 · modelo K-Medoids/Gower, k = 2

> Gerado a partir das tabelas e JSON em `reports/` e `models/`. Números não foram redigitados à mão.

## I · Sumário executivo

A base IBM HR (1.470 colaboradores) se organiza em **dois perfis acionáveis**:

- **Cluster 0 — estáveis e engajados:** n = 733, attrition ≈ 11.1%, renda mediana 6347, 8 anos de casa.
- **Cluster 1 — risco / início de carreira:** n = 737, attrition ≈ 21.2%, renda mediana 3376, 4 anos de casa.

Silhueta Gower = 0.0748 (fraca, esperada na base sintética). O critério decisivo é o **contraste de attrition** (~11% vs ~21%) e o catálogo de ações por persona. O modelo publicado é K-Medoids sobre Gower; GMM e regras de associação são comparativos.

## II · O problema

A organização opera com **política única** de carreira e retenção. Pergunta do Canvas: *que perfis existem, e que trilha cabe a cada um?* Restrição da diretoria: no máximo **cinco** grupos.

## III · Dados e preparação

1.470 × 35 na origem. Sem ausentes nem duplicatas. Removidas três constantes (`EmployeeCount`, `StandardHours`, `Over18`). `EmployeeNumber` é chave. `Attrition` e `PerformanceRating` ficaram **fora** da clusterização.

Dissimilaridade de Gower nas 29 features mistas; via euclidiana = one-hot + StandardScaler. Experimento de escala (k=2 K-Means):

| escalador | silhueta | inercia |
| --- | --- | --- |
| StandardScaler | 0.1111 | 68255.6 |
| RobustScaler | 0.1588 | 21159.4 |
| MinMaxScaler | 0.116 | 7306.7 |

**Decisão:** manter StandardScaler na via euclidiana. RobustScaler sobe a silhueta ao comprimir caudas, mas não é o espaço do modelo oficial (Gower). A matriz `.npy` de Gower é local (gitignore); regenerar com `uv run python scripts/rodar_modelagem.py`.

## IV · Modelagem

| Família | Método | Papel |
|---|---|---|
| Particional | K-Medoids / Gower | **Oficial** (k=2) |
| Particional | K-Means | Comparativo euclidiano |
| Hierárquica | average / complete / single (Gower) | Comparativo |
| Densidade | DBSCAN | Pouco útil nesta base |
| Mistura | GMM (full, k=2) | Comparativo; BIC -48388.2; silhueta 0.0789 |
| Associação | Apriori = FP-Growth (1159 conjuntos) | Coocorrência com cluster/OverTime |

GMM opera no espaço one-hot padronizado. Premissa gaussiana é frágil em Likert e nominais; **não substitui** Gower.

## V · Avaliação

| criterio | valor | status |
| --- | --- | --- |
| k entre 2 e 5 | 2.0 | ok |
| menor segmento >= 5% | 49.86 | ok |
| silhueta Gower (referência) | 0.0747558109598283 | fraca_esperada_base_sintetica |
| ARI médio bootstrap K-Means | 0.67262 | ok |
| ARI médio bootstrap K-Medoids | 0.273225 | atencao |
| cada grupo com ação RH | 2.0 | ok |

Auditoria de vazamento: nenhuma das colunas reservadas entra nas features.

| coluna | esta_nas_features | papel |
| --- | --- | --- |
| Attrition | False | rótulo reservado |
| EmployeeNumber | False | rótulo reservado |
| PerformanceRating | False | identificador |

Perguntas SMART:

| pergunta | resposta |
| --- | --- |
| Quais perfis emergem? | Dois: estáveis (0) e risco/início de carreira (1) |
| Existe segmento com maior attrition? | Sim — cluster 1 com ~21% contra ~11% no 0 |
| O que caracteriza alta performance? | PerformanceRating não separou grupo próprio em k=2 |
| Satisfação, remuneração e permanência? | Cluster 0: renda e tempo de casa maiores, satisfação um pouco maior |
| Horas extras e risco de saída? | OverTime eleva attrition na EDA; cluster 1 tem overtime um pouco maior |
| Onde investir em retenção? | Prioridade no cluster 1 (mentoria, salário, clima) |

## VI · Personas e ações

| cluster | n | pct_attrition | persona | acoes | kpi_monitoramento |
| --- | --- | --- | --- | --- | --- |
| 0 | 733 | 11.05 | Estáveis e engajados | Programas de retenção de longo prazo; Reconhecimento contínuo; Benefícios de permanência | Attrition do segmento; JobSatisfaction; OverTime |
| 1 | 737 | 21.17 | Risco de attrition, Início de carreira | Revisão salarial; Pesquisa de clima; Acompanhamento próximo do gestor; Mentoria; Trilhas de capacitação; Onboarding estruturado | Attrition do segmento; JobSatisfaction; OverTime |

## VII · Implantação

Pacote `models/pacote_implantacao.json`: classificação pelo medoide Gower mais próximo, com faixa de confiança. App: `uv run invoke app` (personas, classificar colaborador, monitoramento).

## VIII · Limitações

- Base sintética IBM; padrões podem não se repetir em um RH real.
- Silhueta baixa e ARI entre métodos próximo de zero: as geometrias divergem.
- Bootstrap do K-Medoids é modesto (~0,27).
- Dois grupos fundem hipóteses do Canvas (alta carga e baixo engajamento não emergiram sozinhas).

## IX · Próximos passos

1. Monitorar attrition e OverTime do cluster 1 mensalmente.
2. Reciclar o modelo a cada 12 meses ou mudança estrutural de headcount.
3. Se houver base real, reabrir k e regras de associação com suporte calibrado.

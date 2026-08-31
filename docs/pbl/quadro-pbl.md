# Quadro PBL — os cinco encontros

Não há fotografias do quadro físico. Esta página **reconstitui** o percurso PBL a partir do Canvas, dos notebooks e das evidências em `reports/`. É a evidência do raciocínio, não do resultado.

**Regra do quadro:** uma hipótese só sai da coluna 2 quando houver evidência que a confirme (vira Fato) ou que a refute (fica no relatório). Hipótese derrubada **não é apagada**.

Canvas textual: [Canvas do Problema](canvas-do-problema.md).

---

## Encontro 1 — Confronto com o problema

| FATOS | HIPÓTESES | QUESTÕES DE APRENDIZAGEM | PLANO DE AÇÃO |
|:---|:---|:---|:---|
| 1.470 colaboradores × 35 colunas (IBM HR, sintético) | Existem até 5 perfis naturais alinhados ao Canvas | Como validar um agrupamento quando não há gabarito de RH? | Preencher o Canvas e o dicionário |
| A empresa opera com política única de carreira e retenção | Attrition deve ser o melhor separador dos grupos | O que é silhueta, e a partir de que valor ela é aceitável nesta base? | Reservar Attrition e PerformanceRating |
| A diretoria limita a no máximo 5 grupos acionáveis | OverTime define um grupo de “alta carga” | Por que Gower, e não só K-Means euclidiano? | Carregar a base e listar constantes |
| Três colunas são constantes (`EmployeeCount`, `StandardHours`, `Over18`) | | | |

**Socialização.** A discussão travou em: *se Attrition explica a saída, por que não usá-lo no cluster?* A resposta da equipe — eixo do projeto — é que usá-lo devolveria um modelo de rotatividade, que o RH já mede. A pergunta feita era outra: *quais perfis existem **antes** da saída*.

---

## Encontro 2 — Análise exploratória e preparação

| FATOS | HIPÓTESES | QUESTÕES DE APRENDIZAGEM | PLANO DE AÇÃO |
|:---|:---|:---|:---|
| ✅ Zero ausentes e zero duplicatas | Os discrepantes de renda são erro de cadastro e devem sair | Quando um outlier é cauda legítima de RH? | Tukey em renda, idade e tempo de casa |
| ✅ Taxa de attrition 16%; OverTime eleva a saída | `JobLevel`, renda e anos de carreira medem a mesma coisa | Spearman vs Pearson; V de Cramér nas nominais | Heatmap + pares Spearman / Cramér |
| ✅ ρ ≈ 0,92 entre `MonthlyIncome` e `JobLevel` | PCA deve substituir o espaço de clusterização | Por que a escala muda o K-Means? | Experimento Standard / Robust / MinMax |
| ✅ 7,8% da renda e 7,1% de `YearsAtCompany` fora de Tukey 1,5×IQR | | | Separar features de cluster vs avaliação |

**Hipótese derrubada.** «Discrepantes de renda são erro.» São colaboradores seniores. Decisão: **manter**. Evidência: `reports/tables/eda_discrepantes_tukey.csv`.

**Hipótese derrubada.** «RobustScaler é o espaço certo porque a silhueta sobe.» A silhueta sobe ao comprimir caudas; o modelo oficial continua Gower. MinMax diverge (ARI ≈ 0 vs StandardScaler). Evidência: `reports/tables/preparacao_sensibilidade_escala.csv`.

---

## Encontro 3 — Clusterização particional e hierárquica

| FATOS | HIPÓTESES | QUESTÕES DE APRENDIZAGEM | PLANO DE AÇÃO |
|:---|:---|:---|:---|
| ✅ Silhueta Gower máxima em k = 2 (~0,075) e cai até k = 5 | k = 5 é o melhor, porque a diretoria cabe 5 grupos | O que a silhueta mede em dado misto? | Varredura k = 2…5 no K-Medoids/Gower |
| ✅ K-Means (one-hot + scaler) e Gower quase não concordam (ARI ≈ 0) | Gower e K-Means contam a mesma história de RH | Como funciona a dissimilaridade de Gower? | Comparar ligações do dendrograma |
| ✅ Ligação `average` com melhor cofenético | O dendrograma confirma o k do K-Means | O que é coeficiente cofenético? | Bootstrap de estabilidade |

**Hipótese derrubada.** «k = 5 é o melhor.» A silhueta piora; dois grupos já são acionáveis e respeitam o teto. Evidência: `reports/tables/varredura_kmedoids_gower.csv`.

**Hipótese derrubada.** «Gower e K-Means coincidem.» As partições são distintas; publica-se **Gower** (dados mistos). Evidência: `reports/tables/avaliacao_ari_metodos.csv`.

---

## Encontro 4 — Densidade, GMM e PCA

| FATOS | HIPÓTESES | QUESTÕES DE APRENDIZAGEM | PLANO DE AÇÃO |
|:---|:---|:---|:---|
| ✅ DBSCAN: um bloco denso e pouco ruído | O DBSCAN acha grupos de forma que o K-Medoids não vê | Como calibrar `eps` sem tentativa e erro? | Curva k-distância |
| ✅ GMM (covariância `full`, k = 2) entra só como comparativo | O BIC escolhe k com clareza | Por que o BIC penaliza a complexidade? | Varredura k × tipo de covariância |
| ✅ PCA-2D explica fração baixa da variância | PCA deve ser o espaço de produção | O que se perde ao projetar em 2D? | Usar PCA só para desenhar |

**Hipótese derrubada.** «DBSCAN entrega segmentos de RH.» Predomina um único componente denso — pouco útil para trilha de desenvolvimento.

**Hipótese parcialmente sustentada.** O GMM roda e grava `cluster_gmm`, mas a premissa gaussiana é frágil em Likert e dummies: **não** substitui Gower. Evidência: `reports/tables/varredura_gmm.csv`, `models/decisao_gmm.json`.

---

## Encontro 5 — Associação, avaliação e implantação

| FATOS | HIPÓTESES | QUESTÕES DE APRENDIZAGEM | PLANO DE AÇÃO |
|:---|:---|:---|:---|
| ✅ Apriori e FP-Growth devolvem os mesmos conjuntos frequentes | Haverá as 5 personas do Canvas | Como calibrar suporte e confiança em 1.470 linhas? | Regras com consequente `cluster:` ou `OverTime:` |
| ✅ Attrition ≈ 11% (cluster 0) vs ≈ 21% (cluster 1) | Silhueta baixa invalida o projeto | O que é vazamento neste problema? | Auditoria: Attrition, Performance e ID fora das features |
| ✅ Bootstrap ARI: K-Means ~0,67; K-Medoids ~0,27 | | Como classificar um colaborador novo? | Pacote de scoring + Streamlit + relatório final |

**Hipótese derrubada.** «Cinco personas distintas.» Em k = 2, risco de attrition e início de carreira **fundem**; alta carga e baixo engajamento não emergiram sozinhos. Evidência: `reports/tables/avaliacao_hipoteses_canvas.csv`.

**Hipótese derrubada.** «Silhueta baixa impede implantar.» O contraste de attrition sustenta ação diferenciada; as limitações vão para o relatório. Evidência: `reports/tables/avaliacao_perfil_principal.csv`.

**Hipótese confirmada.** «Existe um grupo com maior propensão a sair.» Cluster 1.

---

## Consolidado das hipóteses

| # | Hipótese | Destino | Evidência |
|:-:|:---|:---|:---|
| H1 | Attrition deve entrar na clusterização | **descartada por método** | vazamento; `data/processed/hr_avaliacao.csv` |
| H2 | Discrepantes de renda são erro de cadastro | **derrubada** | `reports/tables/eda_discrepantes_tukey.csv` |
| H3 | RobustScaler é o espaço certo porque a silhueta sobe | **derrubada** | `reports/tables/preparacao_sensibilidade_escala.csv` |
| H4 | k = 5 é o melhor (teto da diretoria) | **derrubada** | `reports/tables/varredura_kmedoids_gower.csv` |
| H5 | Gower e K-Means coincidem | **derrubada** | `reports/tables/avaliacao_ari_metodos.csv` |
| H6 | DBSCAN acha grupos que o K-Medoids não vê | **derrubada** | notebook `04_modelagem_clusters.ipynb` |
| H7 | As cinco personas do Canvas emergem intactas | **derrubada em parte** | `reports/tables/avaliacao_hipoteses_canvas.csv` |
| H8 | Silhueta baixa impede implantar | **derrubada** | contraste 11% vs 21% |
| H9 | Existe grupo com maior attrition | **confirmada** | cluster 1 |
| H10 | Há estáveis vs risco/início de carreira | **confirmada** | k = 2; `models/catalogo_personas.json` |

Oito hipóteses derrubadas ou descartadas, duas confirmadas, uma parcialmente sustentada (GMM como comparativo). É o retrato do percurso, não só do modelo publicado.

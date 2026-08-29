# Relatório de Análise Exploratória de Dados (EDA)
## People Analytics — Base IBM HR Analytics Employee Attrition & Performance

| Item | Descrição |
|---|---|
| **Disciplina** | Aprendizagem de Máquina Não Supervisionado — MBA (UNIFOR) |
| **Tema** | Tema 08 — RH e People Analytics |
| **Etapa** | Fase 1 — Análise Exploratória (Cap. III do relatório final) |
| **Base de dados** | `WA_Fn-UseC_-HR-Employee-Attrition.csv` — 1.470 colaboradores × 35 variáveis |
| **Notebooks de origem** | `01_exploracao_inicial.ipynb` e `02_eda.ipynb` |
| **Próxima fase** | `03_preparacao.ipynb` (tratamento de variáveis e clusterização) |

---

## 1. Introdução e Objetivo da Fase

Este relatório consolida a análise exploratória da base IBM HR Analytics Employee Attrition & Performance, etapa preparatória para o problema de segmentação não supervisionada de colaboradores (Canvas do Problema). O objetivo desta fase é entender a estrutura, a qualidade e o comportamento das variáveis disponíveis, gerar evidências de negócio sobre a rotatividade (`Attrition`) e o desempenho (`PerformanceRating`), e produzir hipóteses testáveis para a etapa de clusterização.

> **Importante:** `Attrition` e `PerformanceRating` são utilizadas aqui apenas para leitura de negócio e **não** entrarão como variáveis de entrada da clusterização — servirão de critério de validação externa dos grupos formados na Fase 3.

---

## 2. Estrutura da Base (Bloco 1)

- **Dimensão:** 1.470 linhas (colaboradores) × 35 colunas (variáveis) — cada linha representa um colaborador único.
- **Tipos de variável:** 9 categóricas (texto) e 26 numéricas, incluindo 5 escalas Likert (1–4) de satisfação/engajamento.

**Categóricas (9):** `Attrition`, `BusinessTravel`, `Department`, `EducationField`, `Gender`, `JobRole`, `MaritalStatus`, `Over18`, `OverTime`.

**Likert — satisfação e engajamento (1–4):** `EnvironmentSatisfaction`, `JobSatisfaction`, `RelationshipSatisfaction`, `JobInvolvement`, `WorkLifeBalance`.

**Demais numéricas (21):** `Age`, `DailyRate`, `DistanceFromHome`, `Education`, `EmployeeCount`, `EmployeeNumber`, `HourlyRate`, `JobLevel`, `MonthlyIncome`, `MonthlyRate`, `NumCompaniesWorked`, `PercentSalaryHike`, `PerformanceRating`, `StandardHours`, `StockOptionLevel`, `TotalWorkingYears`, `TrainingTimesLastYear`, `YearsAtCompany`, `YearsInCurrentRole`, `YearsSinceLastPromotion`, `YearsWithCurrManager`.

---

## 3. Qualidade dos Dados (Bloco 2)

| Verificação | Resultado |
|---|---|
| Valores ausentes (total) | 0 — base completa, sem necessidade de imputação |
| Linhas duplicadas | 0 |
| EmployeeNumber duplicado | 0 — identificador único e consistente |
| Colunas constantes (variância zero) | `EmployeeCount` (=1), `Over18` (='Y'), `StandardHours` (=80) |

As três colunas constantes e o identificador `EmployeeNumber` não carregam nenhuma informação discriminante e devem ser removidos antes da clusterização — decisão já prevista no Canvas do Problema.

---

## 4. Análise Univariada — Variáveis Numéricas de Carreira (Bloco 3)

| Variável | Média | Desvio-padrão | Mín. | Mediana | Máx. |
|---|---|---|---|---|---|
| Age (anos) | 36,9 | 9,1 | 18 | 36 | 60 |
| MonthlyIncome (US$) | 6.502,9 | 4.707,9 | 1.009 | 4.919 | 19.999 |
| TotalWorkingYears | 11,3 | 7,8 | 0 | 10 | 40 |
| YearsAtCompany | 7,0 | 6,1 | 0 | 5 | 40 |
| YearsInCurrentRole | 4,2 | 3,6 | 0 | 3 | 18 |
| YearsSinceLastPromotion | 2,2 | 3,2 | 0 | 1 | 15 |
| DistanceFromHome (km) | 9,2 | 8,1 | 1 | 7 | 29 |
| PercentSalaryHike (%) | 15,2 | 3,7 | 11 | 14 | 25 |

![Distribuição das variáveis numéricas de carreira](imagem/01_hist_carreira.png)

*Figura 1 — Distribuição das variáveis numéricas de carreira*

A base é predominantemente jovem/mid-career: idade mediana de 36 anos e mediana de 5 anos de casa. `MonthlyIncome`, `YearsAtCompany` e `YearsSinceLastPromotion` apresentam forte assimetria à direita, evidenciando uma minoria de colaboradores sênior com muitos anos de casa e alta remuneração puxando a média para cima da mediana — um sinal relevante para a padronização de variáveis antes da clusterização.

---

## 5. Análise Univariada — Categóricas e Likert (Bloco 4)

### 5.1 Variáveis categóricas de negócio

| Variável | Distribuição (%) |
|---|---|
| Department | Research & Development 65,4% · Sales 30,3% · Human Resources 4,3% |
| JobRole (9 cargos) | Sales Executive 22,2% · Research Scientist 19,9% · Laboratory Technician 17,6% · demais cargos 3,5–9,9% |
| BusinessTravel | Travel_Rarely 71,0% · Travel_Frequently 18,8% · Non-Travel 10,2% |
| OverTime | Não 71,7% · Sim 28,3% |
| MaritalStatus | Married 45,8% · Single 32,0% · Divorced 22,2% |
| Gender | Male 60,0% · Female 40,0% |
| EducationField | Life Sciences 41,2% · Medical 31,6% · Marketing 10,8% · demais < 10% |

A base é fortemente concentrada em Research & Development e em viagens raras; quase 1 em cada 3 colaboradores faz hora extra (`OverTime = Yes`), variável que se mostrará central na análise bivariada.

### 5.2 Escalas Likert (satisfação e engajamento, 1=baixo a 4=alto)

![Distribuição das escalas Likert](figures/02_likert.png)

*Figura 2 — Distribuição das escalas Likert de satisfação e engajamento*

As distribuições de `EnvironmentSatisfaction`, `JobSatisfaction` e `RelationshipSatisfaction` são relativamente equilibradas entre os 4 níveis, com leve concentração nos níveis 3 e 4. `JobInvolvement` e `WorkLifeBalance` concentram-se fortemente no nível 3 (868 e 893 colaboradores, respectivamente — cerca de 59-61% da base), indicando que a maioria relata engajamento e equilíbrio "bons", mas não "ótimos" — pouca variabilidade nesses dois indicadores pode reduzir seu poder discriminante na clusterização.

---

## 6. Variável de Referência — Attrition e Performance (Bloco 5)

![Distribuição de Attrition](figures/03_attrition.png)

*Figura 3 — Distribuição da variável Attrition*

**Attrition:** 1.233 colaboradores permaneceram (83,9%) e 237 saíram (16,1%) — desbalanceamento típico de bases de rotatividade, relevante para a fase de validação dos clusters (um cluster "de risco" tende a ter poucos registros).

**PerformanceRating:** apenas 2 valores observados na base — nota 3 ("Excelente", 1.244 colaboradores, 84,6%) e nota 4 ("Excepcional", 226 colaboradores, 15,4%). Não há notas 1 ou 2 registradas, o que limita o uso desta variável como critério fino de avaliação — ela distingue essencialmente "bom" de "excepcional".

---

## 7. Análise Bivariada com Attrition (Bloco 6)

### 7.1 Taxa de saída por variável categórica

| Variável / categoria | % Attrition |
|---|---|
| OverTime = Sim | 30,5% (vs. 10,4% sem hora extra — quase 3× maior) |
| MaritalStatus = Single | 25,5% (vs. 12,5% casados e 10,1% divorciados) |
| BusinessTravel = Frequente | 24,9% (vs. 15,0% raramente e 8,0% sem viagens) |
| Department = Sales | 20,6% (vs. 19,1% RH e 13,8% P&D) |
| JobRole = Sales Representative | 39,8% (o maior de todos os cargos) |
| JobRole = Research Director | 2,5% (o menor de todos os cargos) |
| Gender = Masculino | 17,0% (vs. 14,8% feminino — diferença pequena) |

![Attrition por OverTime e Departamento](figures/07_attrition_overtime_dept.png)

*Figura 4 — Taxa de Attrition por OverTime e por Departamento*

### 7.2 Variáveis numéricas: quem sai é diferente de quem fica?

![Boxplots por Attrition](figures/04_boxplot_attrition.png)

*Figura 5 — Distribuição de renda, idade e tempo de casa por Attrition*

| Indicador | Quem ficou (No) | Quem saiu (Yes) |
|---|---|---|
| MonthlyIncome — média | US$ 6.832,7 | US$ 4.787,1 |
| MonthlyIncome — mediana | US$ 5.204 | US$ 3.202 |
| Age — média | 37,6 anos | 33,6 anos |
| Age — mediana | 36 anos | 32 anos |
| YearsAtCompany — mediana | 6 anos | 3 anos |

Colaboradores que saíram têm, em mediana, renda 38% menor, são cerca de 4 anos mais jovens e têm metade do tempo de casa dos que permaneceram — um padrão consistente de perfil de início/meio de carreira e sub-remuneração relativa associado a maior risco de saída.

### 7.3 Satisfação e engajamento vs. Attrition

![Likert vs Attrition](figures/05_likert_vs_attrition.png)

*Figura 6 — Taxa de Attrition por nível de satisfação/engajamento/equilíbrio*

O gradiente é claro nas três escalas: `JobSatisfaction` cai de 22,8% (nível 1) para 11,3% (nível 4); `EnvironmentSatisfaction` cai de 25,4% para 13,5%; `WorkLifeBalance` tem seu ponto mais crítico no nível 1 (31,3% de Attrition), caindo para 14,2% no nível 3. Satisfação mais baixa está sistematicamente associada a maior saída, embora a relação não seja estritamente linear em todos os casos (`WorkLifeBalance` nível 4 sobe levemente para 17,6%).

### 7.4 Outros cruzamentos relevantes

- **StockOptionLevel:** colaboradores sem opções de ações (nível 0) têm 24,4% de Attrition, contra 7,6–9,4% nos níveis 1 e 2 — participação acionária parece funcionar como retenção.
- **JobLevel:** nível 1 (entrada) tem 26,3% de Attrition, caindo para 4,7–9,7% nos níveis 2 a 5 — reforça o padrão de risco concentrado no início de carreira.
- **EducationField:** Human Resources (25,9%) e Technical Degree (24,2%) têm as maiores taxas; Medical (13,6%) e Other (13,4%), as menores.

---

## 8. Correlações e Multicolinearidade (Bloco 7)

![Mapa de correlação](figures/06_correlacao.png)

*Figura 7 — Mapa de correlação entre variáveis numéricas selecionadas*

| Par de variáveis | Correlação (r) |
|---|---|
| MonthlyIncome × JobLevel | 0,95 (redundância muito forte) |
| JobLevel × TotalWorkingYears | 0,78 |
| PercentSalaryHike × PerformanceRating | 0,77 |
| MonthlyIncome × TotalWorkingYears | 0,77 |
| YearsAtCompany × YearsWithCurrManager | 0,77 |
| YearsAtCompany × YearsInCurrentRole | 0,76 |
| YearsInCurrentRole × YearsWithCurrManager | 0,71 |
| Age × TotalWorkingYears | 0,68 |

Há multicolinearidade relevante em dois blocos: (i) remuneração/senioridade — `MonthlyIncome`, `JobLevel`, `TotalWorkingYears` e `Age` caminham juntos (r entre 0,68 e 0,95); (ii) tempo de vínculo — `YearsAtCompany`, `YearsInCurrentRole` e `YearsWithCurrManager` também são altamente correlacionadas (r entre 0,71 e 0,77). Na etapa de preparação, será necessário decidir entre seleção de um representante por bloco, agregação (ex.: escore de senioridade) ou uso de técnica de redução compatível com dados mistos, para evitar que esses blocos dominem a distância de Gower na clusterização.

---

## 9. Coleção de Insights

| # | Insight | Evidência |
|---|---|---|
| 1 | Retenção desigual entre perfis | Attrition geral de 16,1%, mas varia de 2,5% (Research Director) a 39,8% (Sales Representative) por cargo |
| 2 | Hora extra é o fator isolado mais associado à saída | 30,5% de Attrition com OverTime=Sim vs. 10,4% sem — quase o triplo |
| 3 | Perfil de risco combina juniorização e sub-remuneração | Quem sai é ~4 anos mais jovem, tem metade do tempo de casa e renda mediana 38% menor |
| 4 | Satisfação/engajamento tem gradiente consistente com Attrition | Taxa de saída cai de forma monotônica (ou quase) do nível 1 ao 4 em JobSatisfaction e EnvironmentSatisfaction |
| 5 | Stock options e nível hierárquico parecem reter | Attrition cai de 24,4% (sem ações) para 7,6–9,4% (níveis 1–2 de ações); de 26,3% (JobLevel 1) para <10% nos níveis seguintes |
| 6 | Multicolinearidade em dois blocos de variáveis | Bloco remuneração/senioridade (r até 0,95) e bloco tempo de vínculo (r até 0,77) — tratar antes de clusterizar |
| 7 | Colunas sem valor analítico já identificadas | EmployeeCount, StandardHours, Over18 (constantes) e EmployeeNumber (ID) — remover na preparação |
| 8 | Base sintética com possível estrutura de cluster fraca | Distribuições Likert concentradas (ex. WorkLifeBalance 61% no nível 3) reduzem variância disponível para separar grupos |

---

## 10. Hipóteses para a Fase de Clusterização

| Hipótese (Canvas) | Sinal na EDA | Status |
|---|---|---|
| Existe grupo de alta carga / overtime | OverTime eleva Attrition em quase 3× | A validar com cluster |
| Existe grupo estável / engajado | Alta satisfação + baixa saída andam juntas | A validar com cluster |
| Existe grupo de risco (baixa satisfação/renda) | Renda e satisfação menores entre quem sai | A validar com cluster |
| Existe perfil de início de carreira | Idade e tempo de casa menores entre quem sai | A validar com cluster |
| No máximo 5 grupos acionáveis | Restrição de negócio (diretoria) | Regra de modelagem |

---

## 11. Conclusão e Próximos Passos

A base está tecnicamente limpa (sem ausentes ou duplicatas) e rica em sinais de negócio coerentes com a literatura de retenção: sobrecarga de trabalho (`OverTime`), início de carreira, remuneração relativa e satisfação explicam boa parte da variação observada em `Attrition`. Esses mesmos eixos — carga de trabalho, estágio de carreira/remuneração e satisfação/engajamento — são candidatos naturais a dimensões de segmentação na Fase 3.

### Checklist cumprido nesta fase

- [x] Estrutura e tipos de variável mapeados
- [x] Qualidade da base verificada (ausentes, duplicatas, constantes, ID)
- [x] Univariada numérica e categórica/Likert concluída
- [x] Attrition e Performance descritos sob a ótica de negócio
- [x] Bivariada com Attrition realizada
- [x] Correlações e multicolinearidade mapeadas
- [x] Insights e hipóteses documentados

### Próximo passo — Fase 2 (`03_preparacao.ipynb`)

- Remover `EmployeeCount`, `StandardHours`, `Over18` e `EmployeeNumber`.
- Tratar os blocos de variáveis correlacionadas (remuneração/senioridade e tempo de vínculo).
- Separar explicitamente features de clusterização (entrada) de `Attrition`/`PerformanceRating` (avaliação).
- Preparar a matriz de distância de Gower para variáveis mistas e seguir para K-Medoids, Hierárquica e DBSCAN.

---

*Relatório elaborado a partir da execução real da base `WA_Fn-UseC_-HR-Employee-Attrition.csv` (1.470 registros), seguindo a estrutura dos notebooks `01_exploracao_inicial.ipynb` e `02_eda.ipynb`.*

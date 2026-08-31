# Canvas do Problema e Perguntas Orientadas a Dados
## People Analytics — Segmentação de Colaboradores para Trilhas de Desenvolvimento

Texto de **Ana Caroline Amorim**. O quadro dos encontros PBL está em [Percurso PBL](pbl/quadro-pbl.md).

| Item | Descrição |
|---|---|
| **Disciplina** | Aprendizagem de Máquina Não Supervisionado — MBA (UNIFOR) |
| **Tema** | Tema 08 — RH e People Analytics |
| **Base de dados** | IBM HR Analytics Employee Attrition & Performance (`WA_Fn-UseC_-HR-Employee-Attrition.csv`) — 1.470 colaboradores, 35 variáveis |
| **Fase do projeto** | Abertura: canvas e exploração. A clusterização (k = 2) veio depois; o desfecho está no fim desta página. |

---

## 1. Contexto e Motivação do Negócio

A organização enfrenta perda de talentos e desengajamento distribuídos de forma desigual entre áreas, cargos e perfis de carreira. A diretoria de Gente & Gestão não dispõe hoje de uma segmentação analítica dos colaboradores — as decisões de retenção e desenvolvimento são tomadas de forma genérica ("um tamanho serve a todos"), sem diferenciar quem está em risco de saída, quem está estagnado na carreira ou quem está engajado e pronto para crescer.

O projeto nasce da necessidade de transformar dados de RH já coletados (perfil demográfico, histórico de carreira, remuneração, satisfação e engajamento) em grupos homogêneos e interpretáveis de colaboradores, que sirvam de base para trilhas de desenvolvimento personalizadas e ações de retenção direcionadas.

---

## 2. Problema de Negócio

**Pergunta de negócio central:** Quais perfis distintos de colaboradores existem na organização, e como cada perfil deveria ser tratado em termos de retenção, engajamento e desenvolvimento de carreira?

Trata-se de um problema de agrupamento (não existe rótulo de "perfil" pré-definido) — por isso a abordagem é de **Aprendizado Não Supervisionado**, e não de classificação. As variáveis `Attrition` (saída) e `PerformanceRating` (desempenho) existem na base, mas **não serão usadas para treinar os grupos**: serão reservadas para avaliar, a posteriori, se os clusters encontrados de fato diferenciam risco de saída e desempenho — o que dá validação de negócio ao resultado técnico.

---

## 3. Objetivo Analítico

- Segmentar os 1.470 colaboradores em um número reduzido de grupos homogêneos (perfis) a partir de variáveis mistas — demográficas, de carreira, remuneração e de satisfação/engajamento (escalas Likert).
- Interpretar cada grupo em linguagem de negócio (ex.: "alta carga e risco de saída", "início de carreira", "estável e engajado").
- Propor, para cada perfil, uma trilha de desenvolvimento e uma ação prioritária de RH (retenção, engajamento ou aceleração de carreira).
- Validar os grupos cruzando-os (fora do treinamento) com `Attrition` e `PerformanceRating`, para checar se a segmentação tem poder discriminante sobre esses desfechos de negócio.

---

## 4. Perguntas Orientadas a Dados

Perguntas que a análise exploratória e a clusterização devem responder, organizadas por dimensão:

### 4.1 Estrutura e qualidade da base
- A base tem valores ausentes, duplicatas ou colunas sem variância que precisam ser tratadas antes da modelagem?
- Quais variáveis são de fato mistas (numéricas contínuas, categóricas nominais e ordinais tipo Likert) e como isso deve ser tratado na medida de distância (Gower)?

### 4.2 Perfil demográfico e de carreira
- Como se distribuem idade, tempo de casa, tempo no cargo atual e tempo desde a última promoção? Há sinais de estagnação de carreira em algum subgrupo?
- Existe correlação forte entre nível hierárquico (`JobLevel`), renda mensal e tempo total de experiência que gere redundância na modelagem?

### 4.3 Satisfação e engajamento
- Como se distribuem as escalas de satisfação (ambiente, trabalho, relacionamento), envolvimento no cargo e equilíbrio vida-trabalho?
- Esses indicadores Likert se comportam de forma coerente entre si (ex.: quem tem baixa satisfação no ambiente também relata baixo envolvimento)?

### 4.4 Relação com desfechos de negócio (Attrition e Performance)
- Quais variáveis (`OverTime`, estado civil, remuneração, satisfação) mais se associam a maior taxa de saída, na análise exploratória bivariada?
- A distribuição de `PerformanceRating` varia entre departamentos, cargos ou faixas de remuneração?

### 4.5 Segmentação (a responder na Fase 3 — Clusterização)
- Quantos grupos naturais existem nos dados quando combinamos as variáveis de carreira, remuneração e satisfação (respeitando o teto de 5 grupos definido pela diretoria)?
- Os grupos resultantes diferem de forma significativa em taxa de `Attrition` e em `PerformanceRating`, mesmo sem terem sido treinados com essas variáveis?
- Cada grupo é interpretável e "acionável" — ou seja, é possível descrever um perfil claro e sugerir uma trilha de desenvolvimento específica?

---

## 5. Hipóteses de Negócio a Validar

| Hipótese | Sinal esperado / já observado na EDA | Como será testada |
|---|---|---|
| **H1** — Existe um grupo de "alta carga" com hora extra frequente e maior risco de saída | `OverTime = Yes` eleva fortemente a taxa de Attrition observada na base | Cluster + taxa de Attrition por grupo |
| **H2** — Existe um grupo estável e engajado, com baixo risco de saída | Maior satisfação/engajamento associado a menor Attrition | Cluster + Likert médio por grupo |
| **H3** — Existe um grupo de risco por renda/satisfação mais baixas | Quem sai tem renda e satisfação médias menores que quem fica | Cluster + renda/Likert médios |
| **H4** — Existe um perfil de início de carreira (jovem, pouco tempo de casa) | Idade e tempo de casa médios menores entre quem sai | Cluster + idade/tempo de casa médios |
| **H5** — É possível segmentar em no máximo 5 grupos acionáveis | Restrição de negócio definida pela diretoria | Comparação de métricas (silhueta, interpretabilidade) para k ≤ 5 |

---

## 6. Dados Disponíveis

**Fonte:** IBM HR Analytics Employee Attrition & Performance (arquivo `WA_Fn-UseC_-HR-Employee-Attrition.csv`).

**Granularidade:** 1 linha = 1 colaborador; 1.470 registros, 35 colunas, sem valores ausentes e sem duplicatas de `EmployeeNumber`.

**Grupos de variáveis:**
- **Demográficas:** `Age`, `Gender`, `MaritalStatus`, `DistanceFromHome`, `Education`, `EducationField`.
- **Carreira/estrutura:** `Department`, `JobRole`, `JobLevel`, `BusinessTravel`, `TotalWorkingYears`, `YearsAtCompany`, `YearsInCurrentRole`, `YearsSinceLastPromotion`, `YearsWithCurrManager`, `NumCompaniesWorked`.
- **Remuneração/benefícios:** `MonthlyIncome`, `DailyRate`, `HourlyRate`, `MonthlyRate`, `PercentSalaryHike`, `StockOptionLevel`, `OverTime`.
- **Satisfação/engajamento (Likert 1–4):** `EnvironmentSatisfaction`, `JobSatisfaction`, `RelationshipSatisfaction`, `JobInvolvement`, `WorkLifeBalance`.

**Variáveis reservadas para avaliação (não entram na clusterização):** `Attrition` e `PerformanceRating`.

**Variáveis a excluir (sem valor analítico):** `EmployeeCount`, `StandardHours`, `Over18` (constantes) e `EmployeeNumber` (identificador).

---

## 7. Restrições e Regras de Negócio

- Máximo de 5 grupos (k ≤ 5): restrição definida pela diretoria para garantir viabilidade operacional das trilhas de desenvolvimento.
- Os grupos precisam ser interpretáveis por RH, não apenas estatisticamente separáveis — silhueta alta sem leitura de negócio não atende ao objetivo.
- A base é sintética/anonimizada (dataset público da IBM) — resultados devem ser tratados como prova de conceito metodológica, não como diagnóstico real da empresa.
- `Attrition` e `PerformanceRating` não podem ser usados como variáveis de entrada da clusterização, apenas de validação externa.

---

## 8. Métricas de Sucesso

### 8.1 Técnicas
- Qualidade de agrupamento: coeficiente de silhueta e/ou índice de Davies-Bouldin, comparando K-Medoids, Hierárquica e DBSCAN.
- Estabilidade dos grupos frente a variações de parâmetros (k, linkage, eps/min_samples).

### 8.2 De negócio
- Diferenciação clara de Attrition entre grupos (ex.: grupo de risco com taxa de saída bem acima da média geral de 16,1%).
- Cada grupo com um "rótulo de negócio" e uma trilha de desenvolvimento associada, validados como plausíveis por quem conhece o contexto de RH.

---

## 9. Riscos e Limitações

- **Estrutura de cluster fraca:** por ser uma base sintética, é possível que não existam fronteiras naturais nítidas entre grupos (risco já identificado na EDA).
- **Multicolinearidade** entre variáveis de carreira e renda (ex.: `MonthlyIncome` x `JobLevel`, r ≈ 0,95) pode distorcer distâncias se não tratada (seleção de variáveis ou redução de dimensionalidade).
- **Mistura de tipos de variável** (numéricas, categóricas nominais e ordinais) exige medida de distância adequada (ex.: distância de Gower), sob pena de resultados enviesados.
- Dataset em inglês e de contexto norte-americano — validade externa limitada para generalizar diretamente à realidade de outra empresa.

---

## 10. Stakeholders e Entregáveis

| Fase | Entregável | Público-alvo |
|---|---|---|
| Fase 0 | Canvas do problema e perguntas orientadas a dados (este documento) | Professor / avaliação MBA |
| Fase 1 | Relatório de Análise Exploratória (EDA) e coleção de insights — Cap. III | Professor / avaliação MBA |
| Fase 2 | Base preparada (tratamento de variáveis mistas, remoção de colunas irrelevantes) | Uso técnico interno do projeto |
| Fase 3 | Modelos de clusterização (K-Medoids, Hierárquica, DBSCAN) e escolha do melhor k ≤ 5 | Professor / diretoria fictícia de RH |
| Fase 4 | Interpretação dos perfis e proposta de trilhas de desenvolvimento | Diretoria de RH (simulada) |

---

## 11. O que a clusterização mostrou

O canvas acima foi escrito na abertura. Com K-Medoids e distância de Gower, o k que melhor se sustenta (e ainda cabe no teto de 5) é **2**:

| Cluster | n | Attrition | Renda mediana | Tempo de casa (mediana) | Leitura |
|---|---:|---:|---:|---:|---|
| 0 | 733 | ~11% | US$ 6.347 | 8 anos | Mais estáveis, renda e tempo de casa maiores |
| 1 | 737 | ~21% | US$ 3.376 | 4 anos | Mais risco / início de carreira |

H1 (grupo próprio de “alta carga”) e o perfil de baixo engajamento **não** saíram sozinhos. Hora extra continua associada à saída na EDA (30,5% vs 10,4%), mas não foi o eixo que partiu a base. H2 e H4 aparecem misturadas nos dois clusters. H5 (k ≤ 5) foi atendida.

Números e personas: [modelagem](modelagem.md) e [avaliação](avaliacao.md).

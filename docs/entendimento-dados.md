# Entendimento dos dados

## Visão geral

| Item | Valor |
|---|---|
| Arquivo | `data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv` |
| Dimensão | 1.470 × 35 |
| Entidade | Colaborador |
| Dicionário | `references/dicionario_dados.md` |

## Qualidade

| Checagem | Resultado |
|---|---|
| Valores ausentes | Nenhum |
| Linhas duplicadas | Nenhuma |
| Unicidade de `EmployeeNumber` | Confirmada |
| Colunas de variância zero | `EmployeeCount`, `StandardHours`, `Over18` |

## Tipologia das variáveis

| Família | Qtd | Variáveis |
|---|---:|---|
| Categóricas nominais | 7 | BusinessTravel, Department, EducationField, Gender, JobRole, MaritalStatus, OverTime |
| Likert (clima/engajamento) | 5 | EnvironmentSatisfaction, JobSatisfaction, RelationshipSatisfaction, JobInvolvement, WorkLifeBalance |
| Ordinais | 3 | Education, JobLevel, StockOptionLevel |
| Numéricas | 14 | Age, DailyRate, DistanceFromHome, HourlyRate, MonthlyIncome, MonthlyRate, NumCompaniesWorked, PercentSalaryHike, TotalWorkingYears, TrainingTimesLastYear, YearsAtCompany, YearsInCurrentRole, YearsSinceLastPromotion, YearsWithCurrManager |

## Variáveis fora da clusterização

| Variável | Motivo |
|---|---|
| `EmployeeNumber` | Identificador |
| `Attrition` | Rótulo de avaliação a posteriori |
| `PerformanceRating` | Rótulo de avaliação a posteriori |

Tipologia serializada: `data/processed/tipologia_variaveis.json`.

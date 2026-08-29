# Decisões de preparação — Tema 08 RH

**Gerado via:** `notebooks/03_preparacao.ipynb` e fechamento em `notebooks/04_modelagem_clusters.ipynb`
**Docs:** `docs/preparacao.md`

## Remoções

- Colunas constantes: `EmployeeCount`, `StandardHours`, `Over18`
- Motivo: variância zero

## Fora da clusterização

- ID: `EmployeeNumber`
- Avaliação a posteriori: `Attrition`, `PerformanceRating`

## Tipologia para modelagem

- Categóricas nominais (7): BusinessTravel, Department, EducationField, Gender, JobRole, MaritalStatus, OverTime
- Likert clima (5): EnvironmentSatisfaction, JobSatisfaction, RelationshipSatisfaction, JobInvolvement, WorkLifeBalance
- Ordinais (3): Education, JobLevel, StockOptionLevel
- Numéricas (14): Age, DailyRate, DistanceFromHome, HourlyRate, MonthlyIncome, MonthlyRate, NumCompaniesWorked, PercentSalaryHike, TotalWorkingYears, TrainingTimesLastYear, YearsAtCompany, YearsInCurrentRole, YearsSinceLastPromotion, YearsWithCurrManager

## Fechamento da preparação

1. Matriz Gower (`data/processed/matriz_gower.npy`) — numéricas + Likert + ordinais + nominais
2. One-hot + StandardScaler (`data/processed/hr_kmeans_scaled.csv`) — via K-Means/DBSCAN/PCA

## Dimensões

- Original: (1470, 35)
- Limpo: (1470, 32)
- Features cluster: (1470, 29)
- Gower: (1470, 1470)

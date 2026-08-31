# Decisões de preparação — Tema 08 RH

**Data de geração:** automática via `03_preparacao.ipynb`

## Remoções
- Colunas constantes: `EmployeeCount, StandardHours, Over18`
- Motivo: variância zero (quebram padronização / não informam cluster)

## Fora da clusterização
- ID: `EmployeeNumber`
- Avaliação a posteriori: `Attrition, PerformanceRating`

## Tipologia para modelagem
- Categóricas nominais (7): ['BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole', 'MaritalStatus', 'OverTime']
- Likert clima (5): ['EnvironmentSatisfaction', 'JobSatisfaction', 'RelationshipSatisfaction', 'JobInvolvement', 'WorkLifeBalance']
- Ordinais (3): ['Education', 'JobLevel', 'StockOptionLevel']
- Numéricas (14): ['Age', 'DailyRate', 'DistanceFromHome', 'HourlyRate', 'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked', 'PercentSalaryHike', 'TotalWorkingYears', 'TrainingTimesLastYear', 'YearsAtCompany', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager']

## Fechamento da preparação
1. Matriz Gower (`data/processed/matriz_gower.npy`, local) — numéricas + Likert + ordinais + nominais
2. One-hot + StandardScaler — via K-Means/DBSCAN/PCA/GMM
3. Experimento de escala: StandardScaler mantido

## Dimensões
- Original: (1470, 35)
- Limpo: (1470, 32)
- Features cluster: (1470, 29)
- One-hot esboço: (1470, 50)

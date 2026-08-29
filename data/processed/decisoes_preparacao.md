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

## Estratégia prevista (Fase 3)
1. **Principal:** distância de Gower + K-Medoids / Hierárquica / DBSCAN (k ≤ 5)
2. **Comparativo:** K-Means/GMM sobre matriz one-hot + scaler (`hr_kmeans_raw_onehot.csv`)
3. **PCA:** explorar redundância (JobLevel / MonthlyIncome / TotalWorkingYears)
4. **Associação:** Apriori/FP-Growth em variáveis discretizadas / flags

## Dimensões
- Original: (1470, 35)
- Limpo: (1470, 32)
- Features cluster: (1470, 29)
- One-hot esboço: (1470, 50)

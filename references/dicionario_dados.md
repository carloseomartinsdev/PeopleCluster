# Dicionário de Dados – IBM HR Analytics Employee Attrition & Performance

**Projeto:** People Analytics – Segmentação de Funcionários e Trilhas de Desenvolvimento
**Arquivo-fonte:** `data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv`
**Entidade:** Funcionário (Employee) – cada linha representa um colaborador
**Volume:** ~1.470 registros | 35 variáveis

---

## Variáveis demográficas e cadastrais

| Coluna (EN) | Nome (PT) | Descrição | Tipo / Observação |
|---|---|---|---|
| Age | Idade | Idade do colaborador em anos | Numérica |
| Gender | Gênero | Sexo do colaborador | Categórica (`Male`, `Female`) |
| MaritalStatus | Estado civil | Situação conjugal | Categórica (`Single`, `Married`, `Divorced`) |
| Education | Escolaridade | Nível de formação (escala Likert) | 1 = Below College … 5 = Doctor |
| EducationField | Área de formação | Campo de estudo / formação acadêmica | Categórica |
| DistanceFromHome | Distância de casa | Distância entre residência e empresa | Numérica (unidades do dataset) |
| EmployeeNumber | Número do funcionário | Identificador único do colaborador | ID (não usar em clusterização) |
| EmployeeCount | Contagem de funcionários | Sempre 1 (coluna constante) | Remover (variância zero) |
| Over18 | Maior de 18 anos | Sempre `Y` (coluna constante) | Remover (variância zero) |

---

## Variáveis de cargo, área e carreira

| Coluna (EN) | Nome (PT) | Descrição | Tipo / Observação |
|---|---|---|---|
| Department | Departamento | Área organizacional | Categórica (`Sales`, `Research & Development`, `Human Resources`) |
| JobRole | Cargo | Função / papel do colaborador | Categórica |
| JobLevel | Nível do cargo | Senioridade / hierarquia do posto | Numérica ordinal (1–5) |
| BusinessTravel | Viagens a trabalho | Frequência de viagens corporativas | Categórica (`Non-Travel`, `Travel_Rarely`, `Travel_Frequently`) |
| NumCompaniesWorked | Nº de empresas anteriores | Quantidade de empresas em que já trabalhou | Numérica |
| TotalWorkingYears | Anos totais de experiência | Tempo total de carreira profissional | Numérica |
| YearsAtCompany | Anos na empresa | Tempo de casa na organização atual | Numérica |
| YearsInCurrentRole | Anos no cargo atual | Tempo na função atual | Numérica |
| YearsSinceLastPromotion | Anos desde a última promoção | Tempo sem promoção | Numérica |
| YearsWithCurrManager | Anos com o gestor atual | Tempo sob a mesma liderança | Numérica |
| TrainingTimesLastYear | Treinamentos no último ano | Quantidade de treinamentos realizados no ano anterior | Numérica |

---

## Variáveis de remuneração e benefícios

| Coluna (EN) | Nome (PT) | Descrição | Tipo / Observação |
|---|---|---|---|
| DailyRate | Taxa diária | Valor de referência diário de remuneração | Numérica |
| HourlyRate | Taxa horária | Valor de referência por hora | Numérica |
| MonthlyIncome | Renda mensal | Salário mensal do colaborador | Numérica (relevante para retenção) |
| MonthlyRate | Taxa mensal | Outra métrica de remuneração mensal do dataset | Numérica |
| PercentSalaryHike | % de aumento salarial | Percentual do último aumento | Numérica |
| StockOptionLevel | Nível de stock options | Faixa de opções de ações concedidas | Numérica ordinal (0–3) |
| StandardHours | Horas padrão | Sempre 80 (coluna constante) | Remover (variância zero) |

---

## Variáveis de engajamento, satisfação e clima (Likert)

| Coluna (EN) | Nome (PT) | Descrição | Tipo / Observação |
|---|---|---|---|
| EnvironmentSatisfaction | Satisfação com o ambiente | Percepção do ambiente de trabalho | 1 = Low … 4 = Very High |
| JobSatisfaction | Satisfação com o trabalho | Satisfação geral com a função | 1 = Low … 4 = Very High |
| RelationshipSatisfaction | Satisfação com relacionamentos | Qualidade das relações no trabalho | 1 = Low … 4 = Very High |
| JobInvolvement | Envolvimento no trabalho | Grau de comprometimento / engajamento | 1 = Low … 4 = Very High |
| WorkLifeBalance | Equilíbrio vida–trabalho | Percepção de equilíbrio entre vida pessoal e profissional | 1 = Bad … 4 = Best |

---

## Variáveis de desempenho, carga e retenção

| Coluna (EN) | Nome (PT) | Descrição | Tipo / Observação |
|---|---|---|---|
| PerformanceRating | Avaliação de desempenho | Nota de performance do colaborador | Tipicamente 3–4 neste dataset |
| OverTime | Horas extras | Indica se faz hora extra com frequência | Categórica (`Yes` / `No`) – risco de burnout/attrition |
| Attrition | Rotatividade / saída | Indica se o colaborador saiu da empresa | Alvo de negócio (`Yes` / `No`) |

---

## Observações para o projeto

1. **Colunas a remover na preparação:** `EmployeeCount`, `StandardHours`, `Over18` (variância zero).
2. **Identificador:** `EmployeeNumber` não deve entrar em modelos de clusterização.
3. **Variáveis Likert** (satisfação, envolvimento, equilíbrio) são ordinais; tratar com cuidado na distância (ex.: Gower).
4. **Mistura de tipos:** numéricas + categóricas + Likert → favorece distância de Gower e métodos como K-Medoids / hierárquico / DBSCAN.
5. **Perguntas de negócio associadas:** perfis de colaboradores, risco de attrition, alta performance, relação satisfação–salário–permanência, impacto de horas extras.

---

## Mapa rápido (EN → PT)

```
Age                        → Idade
Attrition                  → Rotatividade / saída
BusinessTravel             → Viagens a trabalho
DailyRate                  → Taxa diária
Department                 → Departamento
DistanceFromHome           → Distância de casa
Education                  → Escolaridade
EducationField             → Área de formação
EmployeeCount              → Contagem de funcionários (constante)
EmployeeNumber             → Número do funcionário (ID)
EnvironmentSatisfaction    → Satisfação com o ambiente
Gender                     → Gênero
HourlyRate                 → Taxa horária
JobInvolvement             → Envolvimento no trabalho
JobLevel                   → Nível do cargo
JobRole                    → Cargo
JobSatisfaction            → Satisfação com o trabalho
MaritalStatus              → Estado civil
MonthlyIncome              → Renda mensal
MonthlyRate                → Taxa mensal
NumCompaniesWorked         → Nº de empresas anteriores
Over18                     → Maior de 18 anos (constante)
OverTime                   → Horas extras
PercentSalaryHike          → % de aumento salarial
PerformanceRating          → Avaliação de desempenho
RelationshipSatisfaction   → Satisfação com relacionamentos
StandardHours              → Horas padrão (constante)
StockOptionLevel           → Nível de stock options
TotalWorkingYears          → Anos totais de experiência
TrainingTimesLastYear      → Treinamentos no último ano
WorkLifeBalance            → Equilíbrio vida–trabalho
YearsAtCompany             → Anos na empresa
YearsInCurrentRole         → Anos no cargo atual
YearsSinceLastPromotion    → Anos desde a última promoção
YearsWithCurrManager       → Anos com o gestor atual
```

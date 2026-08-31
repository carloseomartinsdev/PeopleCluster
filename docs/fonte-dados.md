# Fonte dos dados

## Base

| Campo | Valor |
|---|---|
| Nome | IBM HR Analytics Employee Attrition & Performance |
| Origem | Kaggle (`pavansubhasht`) |
| Arquivo | `data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv` |
| Dimensões | 1.470 × 35 |
| Licença | ODbL / DbCL 1.0 |
| Natureza | Sintético (IBM) |

## Entidade

Cada registro representa um colaborador, com atributos demográficos, de cargo, remuneração, clima (Likert), desempenho e indicador de saída (`Attrition`).

## Observações da fonte

- Colunas constantes: `EmployeeCount`, `StandardHours`, `Over18`
- Variáveis numéricas, nominais e Likert na mesma base — daí a distância de Gower
- Grupos pouco nítidos (a silhueta baixa na modelagem confirma isso)

## Materiais de referência

| Material | Local |
|---|---|
| Dicionário de dados | `references/dicionario_dados.md` |
| Canvas do problema | [canvas_problema.md](canvas_problema.md) |
| Relatório de EDA | [analise-exploratoria.md](analise-exploratoria.md) |
| Checklist CRISP-DM (status) | `references/checklist_crisp_dm_status.md` |
| Roteiro do trabalho | `references/roteiro_trabalho.md` |

Os PDFs de enunciado/checklist da disciplina, se usados em aula, ficam fora deste repositório.

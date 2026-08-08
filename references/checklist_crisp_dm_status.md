# Checklist CRISP-DM × status do PeopleCluster

**Fonte do professor:** `references/03-Checklist-CRISP-DM.pdf`
**Atualizado em:** 08/08/2026

Legenda: ✅ feito · 🟡 parcial · ⬜ pendente · ➖ N/A neste projeto (não supervisionado / base única)

---

## 1. Entendimento de Negócio

| Item do professor | Status | Onde no projeto |
|---|---|---|
| 1.1 Objetivos de negócio documentados | ✅ | `references/canvas_problema.md`, `docs/entendimento-negocio.md` |
| 1.1 Critérios de sucesso do negócio | ✅ | Canvas + `docs/criterios-sucesso.md` |
| 1.2 Recursos (pessoal, infra) | 🟡 | Ambiente `uv` pronto; equipe/recursos pouco formalizados |
| 1.2 Requisitos técnicos/legais/éticos | 🟡 | Licença ODbL e base sintética citados; ética/LGPD só implícita |
| 1.2 Riscos e contingência | ✅ | Canvas §10 + docs de negócio |
| 1.2 Análise de custo-benefício | ⬜ | Não documentada formalmente |
| 1.3 Metas de sucesso técnico | ✅ | Canvas + `docs/criterios-sucesso.md` |
| 1.3 Resultado técnico esperado (agrupamento) | ✅ | Clusterização + associação |
| 1.4 Tecnologias/ferramentas | ✅ | `pyproject.toml`, README (`uv`, pandas, sklearn…) |
| 1.4 Plano/cronograma CRISP-DM | ✅ | `references/roteiro_trabalho.md`, `docs/metodologia.md` |

**Veredito fase 1:** alinhado ao roteiro; faltam custo-benefício e formalizar recursos/ética.

---

## 2. Entendimento dos Dados

| Item do professor | Status | Onde no projeto |
|---|---|---|
| 2.1 Dados identificados e adquiridos | ✅ | `data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv` |
| 2.1 Dados carregados/acessíveis | ✅ | `notebooks/01_…`, `02_eda.ipynb` |
| 2.1 Permissões/licença | ✅ | ODbL/DbCL documentada em `docs/fonte-dados.md` |
| 2.2 Formato, tamanho, volume | ✅ | 1470×35 em docs e notebooks |
| 2.2 Identidade e tipos de variáveis | ✅ | `references/dicionario_dados.md` |
| 2.2 Relatório inicial de visão geral | ✅ | `docs/entendimento-dados.md`, notebook 01 |
| 2.3 Estatística descritiva (uni/bi/multi) | ✅ | `notebooks/02_eda.ipynb` |
| 2.3 Visualizações | ✅ | `reports/figures/` + `docs/assets/figures/` |
| 2.3 Correlações/relações | ✅ | heatmap + cruzamentos com Attrition |
| 2.4 Missing values | ✅ | nenhum ausente (documentado) |
| 2.4 Outliers / inconsistências | 🟡 | EDA mostra distribuições; sem relatório dedicado de outliers |
| 2.4 Problemas de qualidade documentados | ✅ | constantes, ID, base sintética, multicolinearidade |

**Veredito fase 2:** forte alinhamento; aprofundar outliers se o professor cobrar explicitamente.

---

## 3. Preparação dos Dados

| Item do professor | Status | Onde no projeto |
|---|---|---|
| 3.1 Seleção de dados/variáveis | ✅ | features cluster vs avaliação |
| 3.1 Motivos inclusão/exclusão | ✅ | `references/decisoes_preparacao.md` |
| 3.2 Tratamento de ausentes | ➖/✅ | Sem ausentes; decisão documentada |
| 3.2 Inconsistências corrigidas | ✅ | remoção de colunas constantes |
| 3.2 Tratamento de outliers | ⬜ | ainda não aplicado (pode ser na modelagem) |
| 3.3 Feature engineering | 🟡 | tipologia definida; poucas features derivadas ainda |
| 3.3 Encoding categóricas | 🟡 | one-hot esboço pronto; Gower ainda não |
| 3.4 Integrar múltiplas fontes | ➖ | uma única base |
| 3.5 Tipos ajustados | 🟡 | parcial (object/num ok; Likert como ordinal a tratar no Gower) |
| 3.5 Normalização/padronização | ⬜ | prevista para K-Means (Aula 2) |
| 3.5 Split treino/validação/teste | ➖ | não se aplica da mesma forma a clusterização não supervisionada |

**Veredito fase 3:** início correto e documentado; **fase ainda não fechada** (Gower, scaler, encoding definitivo).

---

## 4. Modelagem

| Item do professor | Status | Nota |
|---|---|---|
| 4.1 Selecionar técnicas | 🟡 | escolhidas no plano (Gower, K-Medoids, Hierárquica, DBSCAN, Apriori); ainda sem notebook |
| 4.1 Justificativa | ✅ | Tema 08 + docs |
| 4.2 Desenho do experimento | ⬜ | |
| 4.2 Métricas técnicas | 🟡 | silhueta/interpretabilidade previstas; não aplicadas |
| 4.3 Construir modelos | ⬜ | |
| 4.4 Avaliar modelos (técnica) | ⬜ | |

**Veredito fase 4:** só planejamento — conforme Aulas 2–3.

---

## 5. Avaliação (negócio)

| Item | Status |
|---|---|
| 5.1 Validar vs critérios de negócio | ⬜ |
| 5.1 Impacto operacional/financeiro | ⬜ |
| 5.1 Aprovação para implantação | ⬜ |
| 5.2 Revisar processo / limitações | ⬜ |
| 5.3 Próximas etapas formais | ⬜ |

---

## 6. Implantação

| Item | Status |
|---|---|
| 6.1 Plano de implantação | ⬜ (há esqueleto Streamlit) |
| 6.2 Monitoramento/manutenção | ⬜ |
| 6.3 Relatório final + apresentação | ⬜ |
| 6.4 Retrospectiva / lições aprendidas | ⬜ |

---

## Conclusão

**Sim — o que foi feito segue o roteiro do professor**, na ordem CRISP-DM:

1. Negócio ✅ (quase completo)
2. Dados ✅ (quase completo)
3. Preparação 🟡 (iniciada corretamente, não fechada)
4–6 ⬜ (ainda não é a hora / próximas aulas)

Estão **adiantados** em relação a uma Aula 1 típica (já entraram na preparação).
Pontos a reforçar para ficar 100% no checklist do PDF:

1. Custo-benefício e recursos/ética um pouco mais explícitos (fase 1)
2. Seção dedicada de outliers (fase 2)
3. Fechar preparação: Gower + padronização (fase 3)
4. Só então modelagem → avaliação → implantação

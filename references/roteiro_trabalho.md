# Roteiro do Trabalho – Tema 08: RH e People Analytics

**Fonte da proposta:** `references/01-temas.pdf`
**Tema escolhido:** 08 – RH e People Analytics
**Pergunta do tema:** *Temos uma política única de carreira e de retenção. Que perfis de colaborador existem, e que trilha de desenvolvimento cabe a cada um?*
**Restrição da diretoria:** no máximo **5 grupos** acionáveis.
**Momento atual:** Aula 1 — Fase 1 fechada, Fase 2 iniciada; ambiente `uv` sincronizado.

---

## Plano por aula (5 encontros ≈ 5 fases)

| Aula | Fase | Foco | Artefatos |
|---|---|---|---|
| **1** | 0 + 1 + início 2 | Canvas, EDA, preparação inicial | `references/`, `notebooks/01–03` |
| **2** | 2 (fechar) + 3 (iniciar) | Gower + primeiros clusters | `notebooks/04_…` |
| **3** | 3 | Clusterização + associação | `04` + `05` |
| **4** | 4 | Avaliação, personas, ações | Cap. VI–VII |
| **5** | 5 | Relatório, pitch, quadros PBL | `reports/`, defesa |

---

## Legenda

- ✅ Pronto
- 🟡 Parcial
- ⬜ Pendente

---

## FASE 0 — Entendimento do problema

| # | O que fazer | Status | Onde |
|---|---|---|---|
| 0.1 | Escolher o tema | ✅ | Tema 08 |
| 0.2 | Obter a base | ✅ | `data/raw/…` |
| 0.3 | Canvas | ✅ | `references/canvas_problema.md` |
| 0.4 | Dicionário | ✅ | `references/dicionario_dados.md` |
| 0.5 | Ambiente (`uv sync`) | ✅ | `.venv` |
| 0.6 | Quadro PBL (fotos) | ⬜ | `docs/pbl/` |

---

## FASE 1 — EDA

| # | Status | Onde |
|---|---|---|
| Exploração inicial | ✅ | `notebooks/01_exploracao_inicial.ipynb` |
| EDA completa | ✅ | `notebooks/02_eda.ipynb` |
| Figuras | ✅ | `reports/figures/` + `docs/assets/figures/` |
| Docs EDA | ✅ | `docs/analise-exploratoria.md` |

---

## FASE 2 — Preparação

| # | Status | Onde |
|---|---|---|
| Remover constantes / separar ID e rótulos | ✅ | `notebooks/03_preparacao.ipynb` |
| Datasets processados | ✅ | `data/processed/` |
| Documentação | ✅ | `docs/preparacao.md` |
| Gower / scaler definitivo | ⬜ | Aula 2 |

---

## FASES 3–5

Modelagem, avaliação e entrega — ver `docs/modelagem.md`, `docs/avaliacao.md`, `docs/implementacao.md` e `docs/status.md`.

---

## Mapa do repositório

```
PeopleCluster-/
├── notebooks/01–03
├── data/raw + processed
├── references/ (canvas, dicionário, roteiro, PDF)
├── reports/figures/
├── docs/ (+ assets/figures para MkDocs)
└── .venv/ (uv)
```

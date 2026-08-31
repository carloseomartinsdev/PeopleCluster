# Roteiro do Trabalho – Tema 08: RH e People Analytics

**Tema:** 08 – RH e People Analytics
**Pergunta:** *Temos uma política única de carreira e de retenção. Que perfis de colaborador existem, e que trilha de desenvolvimento cabe a cada um?*
**Restrição:** no máximo **5** grupos acionáveis.
**Estado:** ciclo CRISP-DM **fechado** (k=2, K-Medoids/Gower).

## Legenda

- Pronto
- Parcial
- Pendente

## FASE 0 — Entendimento do problema

| # | O que fazer | Status | Onde |
|---|---|---|---|
| 0.1 | Escolher o tema | Pronto | Tema 08 |
| 0.2 | Obter a base | Pronto | `data/raw/` |
| 0.3 | Canvas | Pronto | `references/canvas_problema.md`, `docs/pbl/` |
| 0.4 | Dicionário | Pronto | `references/dicionario_dados.md` |
| 0.5 | Ambiente (`uv sync`) | Pronto | `.venv` |
| 0.6 | Quadro PBL (reconstituído, sem fotos) | Pronto | `docs/pbl/quadro-pbl.md` |

## FASES 1–6

| Fase | Status | Onde |
|---|---|---|
| EDA | Pronto | `notebooks/01–02`, `docs/analise-exploratoria.md` |
| Preparação | Pronto | `notebooks/03`, Gower no `04`, experimento de escala |
| Modelagem | Pronto | `notebooks/04` + GMM; bônus `07` |
| Avaliação | Pronto | `notebooks/05` (ARI, associação, SMART, vazamento) |
| Implantação | Pronto | `notebooks/06`, Streamlit, `reports/relatorio-final.md` |

Reprodução: `uv run python scripts/rodar_modelagem.py` · `rodar_avaliacao.py` · `rodar_fechamento.py`.

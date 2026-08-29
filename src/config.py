"""Configuração central do PeopleCluster."""

from __future__ import annotations

from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

DATA = RAIZ / "data"
DATA_RAW = DATA / "raw"
DATA_PROCESSED = DATA / "processed"
DATA_EXTERNAL = DATA / "external"

MODELS = RAIZ / "models"
REPORTS = RAIZ / "reports"
FIGURES = REPORTS / "figures"
TABLES = REPORTS / "tables"
REFERENCES = RAIZ / "references"
DOCS = RAIZ / "docs"
DOCS_FIGURES = DOCS / "assets" / "figures"

SEMENTE = 42
K_MINIMO = 2
K_MAXIMO = 5
SILHUETA_MINIMA = 0.15
RUIDO_MAXIMO = 0.10

PALETA = ["#1B4965", "#EE6C4D", "#74C69D", "#F4D35E", "#8E7DBE", "#2A6F97"]


def garantir_diretorios() -> None:
    for caminho in (
        DATA_RAW,
        DATA_PROCESSED,
        DATA_EXTERNAL,
        MODELS,
        FIGURES,
        TABLES,
        DOCS_FIGURES,
    ):
        caminho.mkdir(parents=True, exist_ok=True)

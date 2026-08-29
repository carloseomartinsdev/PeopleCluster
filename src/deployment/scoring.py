"""Classificação operacional de colaboradores na segmentação publicada."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd

from src import config
from src.model import distancias as dist


def carregar_tipologia() -> dict:
    return json.loads(
        (config.DATA_PROCESSED / "tipologia_variaveis.json").read_text(encoding="utf-8")
    )


def colunas_gower(tipologia: dict) -> tuple[list[str], list[str]]:
    numericas = tipologia["numericas"] + tipologia["likert_clima"] + tipologia["ordinais"]
    nominais = tipologia["categoricas_nominais"]
    return numericas, nominais


def encontrar_medoides(distancias: np.ndarray, rotulos: np.ndarray) -> np.ndarray:
    """Índice do medoide de cada cluster (menor soma de distâncias internas)."""
    medoides = []
    for grupo in sorted(np.unique(rotulos)):
        indices = np.flatnonzero(rotulos == grupo)
        interno = distancias[np.ix_(indices, indices)].sum(axis=1)
        medoides.append(int(indices[int(np.argmin(interno))]))
    return np.array(medoides, dtype=int)


def publicar_pacote(
    features: pd.DataFrame,
    rotulos: np.ndarray,
    avaliacao: pd.DataFrame,
    distancias: np.ndarray,
) -> dict:
    """Monta e grava o pacote operacional da segmentação."""
    config.garantir_diretorios()
    tipologia = carregar_tipologia()
    numericas, nominais = colunas_gower(tipologia)
    medoides_idx = encontrar_medoides(distancias, rotulos)
    catalogo = json.loads((config.MODELS / "catalogo_personas.json").read_text(encoding="utf-8"))

    pacote = {
        "versao": "peoplecluster.segmentacao/1",
        "metodo": "kmedoids_gower",
        "k": int(len(np.unique(rotulos))),
        "colunas": features.columns.tolist(),
        "numericas": numericas,
        "nominais": nominais,
        "medoides_idx": medoides_idx.tolist(),
        "medoides_employee_number": avaliacao.loc[medoides_idx, "EmployeeNumber"]
        .astype(int)
        .tolist(),
        "medoides_registros": features.iloc[medoides_idx].to_dict(orient="records"),
        "catalogo": catalogo,
        "referencia": {
            "n": int(len(features)),
            "attrition_por_cluster": {
                str(int(g)): float((avaliacao.loc[rotulos == g, "Attrition"] == "Yes").mean())
                for g in sorted(np.unique(rotulos))
            },
        },
    }
    caminho = config.MODELS / "pacote_implantacao.json"
    caminho.write_text(json.dumps(pacote, indent=2, ensure_ascii=False), encoding="utf-8")
    return pacote


def _gower_para_medoides(
    registro: pd.DataFrame,
    medoides: pd.DataFrame,
    numericas: list[str],
    nominais: list[str],
) -> np.ndarray:
    """Dissimilaridade Gower do registro a cada medoide (vetor 1×k)."""
    base = pd.concat([registro, medoides], ignore_index=True)
    matriz = dist.gower(base, numericas=numericas, nominais=nominais)
    return matriz[0, 1:]


def classificar_colaborador(
    atributos: dict,
    pacote: dict | None = None,
) -> dict:
    """Classifica um colaborador novo pelo medoide Gower mais próximo."""
    if pacote is None:
        pacote = json.loads((config.MODELS / "pacote_implantacao.json").read_text(encoding="utf-8"))

    colunas = pacote["colunas"]
    faltando = [c for c in colunas if c not in atributos]
    if faltando:
        return {
            "ok": False,
            "erros": [f"atributos ausentes: {faltando}"],
        }

    registro = pd.DataFrame([{c: atributos[c] for c in colunas}])
    medoides = pd.DataFrame(pacote["medoides_registros"])[colunas]
    distancias = _gower_para_medoides(registro, medoides, pacote["numericas"], pacote["nominais"])
    cluster = int(np.argmin(distancias))
    ordenadas = np.sort(distancias)
    margem = float(ordenadas[1] - ordenadas[0]) if len(ordenadas) > 1 else 0.0
    confianca = "alta" if margem >= 0.02 else ("media" if margem >= 0.01 else "baixa")

    persona = next(
        (item for item in pacote["catalogo"] if int(item["cluster"]) == cluster),
        {},
    )
    return {
        "ok": True,
        "cluster": cluster,
        "distancias_medoides": [float(x) for x in distancias],
        "margem": margem,
        "confianca": confianca,
        "persona": persona.get("persona"),
        "acoes": persona.get("acoes"),
        "kpi_monitoramento": persona.get("kpi_monitoramento"),
    }


def classificar_base(
    features: pd.DataFrame,
    pacote: dict | None = None,
) -> pd.DataFrame:
    """Reclassifica a base feature a feature (validação de reprodução)."""
    if pacote is None:
        pacote = json.loads((config.MODELS / "pacote_implantacao.json").read_text(encoding="utf-8"))
    linhas = []
    for _, row in features.iterrows():
        resultado = classificar_colaborador(row.to_dict(), pacote=pacote)
        linhas.append(resultado)
    return pd.DataFrame(linhas)

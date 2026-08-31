"""Regras de associação (Apriori e FP-Growth) sobre a carteira de colaboradores.

Cada transação é um colaborador. Itens vêm de nominais, Likert em faixas,
OverTime e, quando informado, o cluster publicado. Os dois algoritmos do
mlxtend devem devolver os mesmos conjuntos frequentes nos mesmos limiares.
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth

LIKERT = [
    "EnvironmentSatisfaction",
    "JobSatisfaction",
    "RelationshipSatisfaction",
    "JobInvolvement",
    "WorkLifeBalance",
]

NOMINAIS = [
    "BusinessTravel",
    "Department",
    "EducationField",
    "Gender",
    "JobRole",
    "MaritalStatus",
    "OverTime",
]

NUMERICAS_QUARTIL = {
    "MonthlyIncome": "renda",
    "Age": "idade",
    "YearsAtCompany": "tempo_casa",
}


def _faixa_likert(serie: pd.Series, nome: str) -> pd.Series:
    return np.where(serie <= 2, f"{nome}:baixa", f"{nome}:alta")


def montar_transacoes(
    features: pd.DataFrame,
    segmentos: np.ndarray | None = None,
) -> pd.DataFrame:
    """Matriz booleana colaboradores × itens, no formato do mlxtend."""
    itens = pd.DataFrame(index=features.index)

    for coluna in NOMINAIS:
        if coluna not in features.columns:
            continue
        marcadores = pd.get_dummies(features[coluna], prefix=coluna, prefix_sep=":")
        itens = pd.concat([itens, marcadores], axis=1)

    for coluna in LIKERT:
        if coluna not in features.columns:
            continue
        faixa = pd.Series(_faixa_likert(features[coluna], coluna), index=features.index)
        itens = pd.concat([itens, pd.get_dummies(faixa)], axis=1)

    for coluna, prefixo in NUMERICAS_QUARTIL.items():
        if coluna not in features.columns:
            continue
        faixa = pd.qcut(
            features[coluna].rank(method="first"),
            q=4,
            labels=[f"{prefixo}:{q}" for q in ("Q1", "Q2", "Q3", "Q4")],
        )
        itens = pd.concat([itens, pd.get_dummies(faixa)], axis=1)

    if segmentos is not None:
        marcadores = pd.get_dummies(
            pd.Series(segmentos, index=features.index),
            prefix="cluster",
            prefix_sep=":",
        )
        itens = pd.concat([itens, marcadores], axis=1)

    return itens.astype(bool)


def comparar_algoritmos(
    transacoes: pd.DataFrame,
    suporte_minimo: float = 0.12,
    max_tamanho: int = 3,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Roda Apriori e FP-Growth e confere equivalência dos conjuntos."""
    resultados: dict[str, tuple[pd.DataFrame, float]] = {}
    for nome, funcao in (("Apriori", apriori), ("FP-Growth", fpgrowth)):
        inicio = time.perf_counter()
        saida = funcao(
            transacoes,
            min_support=suporte_minimo,
            use_colnames=True,
            max_len=max_tamanho,
        )
        resultados[nome] = (saida, time.perf_counter() - inicio)

    referencia = {frozenset(c) for c in resultados["Apriori"][0]["itemsets"]}
    linhas = []
    for nome, (saida, duracao) in resultados.items():
        conjuntos = {frozenset(c) for c in saida["itemsets"]}
        linhas.append(
            {
                "algoritmo": nome,
                "conjuntos_frequentes": len(saida),
                "tempo_s": round(duracao, 3),
                "identico_ao_apriori": conjuntos == referencia,
            }
        )
    return pd.DataFrame(linhas).set_index("algoritmo"), resultados["Apriori"][0]


def gerar_regras(
    frequentes: pd.DataFrame,
    confianca_minima: float = 0.55,
    lift_minimo: float = 1.10,
) -> pd.DataFrame:
    """Regras com confiança e lift mínimos."""
    if frequentes.empty or (frequentes["itemsets"].map(len) >= 2).sum() == 0:
        return pd.DataFrame()
    regras = association_rules(
        frequentes,
        metric="confidence",
        min_threshold=confianca_minima,
    )
    regras = regras[regras["lift"] >= lift_minimo].copy()
    regras["antecedents"] = regras["antecedents"].map(lambda s: ", ".join(sorted(s)))
    regras["consequents"] = regras["consequents"].map(lambda s: ", ".join(sorted(s)))
    return regras.sort_values(["lift", "confidence"], ascending=False).reset_index(drop=True)


def regras_de_negocio(regras: pd.DataFrame) -> pd.DataFrame:
    """Mantém regras cujo consequente fala de cluster ou de horas extras."""
    if regras.empty:
        return regras
    mask = regras["consequents"].str.contains(r"cluster:|OverTime:", regex=True)
    return regras.loc[mask].reset_index(drop=True)

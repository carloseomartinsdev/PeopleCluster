"""Funções de EDA reutilizáveis (bivariada, discrepantes, PCA exploratório)."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from src import config


def cramer_v(x: pd.Series, y: pd.Series) -> float:
    tabela = pd.crosstab(x, y)
    if tabela.size == 0:
        return float("nan")
    observado = tabela.to_numpy(dtype=float)
    n = observado.sum()
    if n == 0:
        return float("nan")
    linha = observado.sum(axis=1, keepdims=True)
    coluna = observado.sum(axis=0, keepdims=True)
    esperado = linha @ coluna / n
    with np.errstate(divide="ignore", invalid="ignore"):
        chi2 = np.nansum((observado - esperado) ** 2 / np.where(esperado == 0, np.nan, esperado))
    r, k = tabela.shape
    denom = n * (min(r, k) - 1)
    if denom <= 0:
        return float("nan")
    return float(np.sqrt(chi2 / denom))


def pares_spearman(df: pd.DataFrame, colunas: list[str], corte: float = 0.60) -> pd.DataFrame:
    corr = df[colunas].corr(method="spearman")
    pares = (
        corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        .stack()
        .rename("rho")
        .reset_index()
    )
    pares.columns = ["var1", "var2", "rho"]
    pares["abs_rho"] = pares["rho"].abs()
    return pares.sort_values("abs_rho", ascending=False).query("abs_rho >= @corte")


def pares_cramer(df: pd.DataFrame, colunas: list[str], corte: float = 0.30) -> pd.DataFrame:
    linhas = []
    for i, a in enumerate(colunas):
        for b in colunas[i + 1 :]:
            v = cramer_v(df[a], df[b])
            linhas.append({"var1": a, "var2": b, "cramer_v": round(v, 4)})
    tabela = pd.DataFrame(linhas).sort_values("cramer_v", ascending=False)
    return tabela[tabela["cramer_v"] >= corte]


def discrepantes_tukey(df: pd.DataFrame, colunas: list[str], k: float = 1.5) -> pd.DataFrame:
    linhas = []
    n = len(df)
    for coluna in colunas:
        serie = df[coluna].dropna()
        q1, q3 = serie.quantile(0.25), serie.quantile(0.75)
        iqr = q3 - q1
        baixo, alto = q1 - k * iqr, q3 + k * iqr
        mask = (serie < baixo) | (serie > alto)
        linhas.append(
            {
                "coluna": coluna,
                "q1": float(q1),
                "q3": float(q3),
                "iqr": float(iqr),
                "limite_inf": float(baixo),
                "limite_sup": float(alto),
                "n_discrepantes": int(mask.sum()),
                "pct": round(100 * mask.sum() / n, 2),
            }
        )
    return pd.DataFrame(linhas)


def pca_exploratorio(
    df: pd.DataFrame,
    colunas: list[str],
    n_componentes: int = 4,
    semente: int = config.SEMENTE,
) -> tuple[PCA, pd.DataFrame, pd.DataFrame]:
    matriz = StandardScaler().fit_transform(df[colunas].to_numpy(dtype=float))
    pca = PCA(n_components=min(n_componentes, matriz.shape[1]), random_state=semente)
    pca.fit(matriz)
    variancia = pd.DataFrame(
        {
            "componente": [f"CP{i + 1}" for i in range(pca.n_components_)],
            "var_explicada": pca.explained_variance_ratio_,
            "var_acumulada": np.cumsum(pca.explained_variance_ratio_),
        }
    )
    cargas = pd.DataFrame(
        pca.components_.T,
        index=colunas,
        columns=[f"CP{i + 1}" for i in range(pca.n_components_)],
    )
    return pca, variancia, cargas

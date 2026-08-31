"""Modelos de mistura gaussiana (GMM) no espaço euclidiano padronizado.

Comparativo da via K-Means/DBSCAN: o GMM entrega grau de pertencimento.
Não substitui o modelo publicado (K-Medoids / Gower).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture

from src import config
from src.model.particional import metricas_internas

COVARIANCIAS = ("full", "tied", "diag", "spherical")


def varrer_gmm(
    dados: np.ndarray,
    k_minimo: int = 2,
    k_maximo: int = 5,
    covariancias: tuple[str, ...] = COVARIANCIAS,
    semente: int = config.SEMENTE,
) -> pd.DataFrame:
    """Ajusta o GMM para cada combinação de k e tipo de covariância."""
    linhas = []
    for tipo in covariancias:
        for k in range(k_minimo, k_maximo + 1):
            modelo = GaussianMixture(
                n_components=k,
                covariance_type=tipo,
                random_state=semente,
                n_init=5,
                max_iter=500,
            ).fit(dados)
            rotulos = modelo.predict(dados)
            probabilidades = modelo.predict_proba(dados)
            metricas = metricas_internas(dados, rotulos)
            linhas.append(
                {
                    "covariancia": tipo,
                    "k": k,
                    "bic": round(float(modelo.bic(dados)), 1),
                    "aic": round(float(modelo.aic(dados)), 1),
                    "log_verossimilhanca": round(float(modelo.score(dados) * len(dados)), 1),
                    "convergiu": bool(modelo.converged_),
                    "silhueta": round(metricas["silhueta"], 4),
                    "pct_fronteira": round(float((probabilidades.max(axis=1) < 0.60).mean()), 4),
                    "menor_grupo": int(np.bincount(rotulos).min()),
                    "maior_grupo": int(np.bincount(rotulos).max()),
                }
            )
    return pd.DataFrame(linhas)


def ajustar_gmm(
    dados: np.ndarray,
    k: int,
    covariancia: str = "diag",
    semente: int = config.SEMENTE,
) -> tuple[GaussianMixture, np.ndarray, np.ndarray]:
    """Ajusta o GMM e devolve modelo, rótulos e probabilidades."""
    modelo = GaussianMixture(
        n_components=k,
        covariance_type=covariancia,
        random_state=semente,
        n_init=10,
        max_iter=500,
    ).fit(dados)
    return modelo, modelo.predict(dados), modelo.predict_proba(dados)


def classificar_confianca(
    probabilidades: np.ndarray,
    limiar_alto: float = 0.80,
    limiar_baixo: float = 0.60,
) -> pd.Series:
    """Traduz o grau de pertencimento em núcleo / típico / fronteira."""
    maxima = probabilidades.max(axis=1)
    faixas = np.where(
        maxima >= limiar_alto,
        "nucleo",
        np.where(maxima >= limiar_baixo, "tipico", "fronteira"),
    )
    return pd.Series(faixas, name="confianca")


def escolher_configuracao(varredura: pd.DataFrame, k_alvo: int | None = None) -> pd.Series:
    """Menor BIC; se k_alvo for informado, restringe a esse k (comparável ao modelo oficial)."""
    tabela = varredura.copy()
    if k_alvo is not None:
        tabela = tabela[tabela["k"] == k_alvo]
    return tabela.sort_values("bic").iloc[0]

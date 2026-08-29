"""Medidas de distância e dissimilaridade (Gower para dados mistos)."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform


def gower(
    dados: pd.DataFrame,
    numericas: list[str],
    nominais: list[str],
    pesos: dict[str, float] | None = None,
) -> np.ndarray:
    """Matriz n×n de dissimilaridade de Gower no intervalo [0, 1]."""
    pesos = pesos or {}
    n = len(dados)
    acumulado = np.zeros((n, n), dtype=np.float32)
    peso_total = 0.0

    for coluna in numericas:
        valores = dados[coluna].to_numpy(dtype=np.float32)
        amplitude = float(valores.max() - valores.min())
        if amplitude == 0:
            continue
        peso = float(pesos.get(coluna, 1.0))
        acumulado += peso * np.abs(valores[:, None] - valores[None, :]) / amplitude
        peso_total += peso

    for coluna in nominais:
        codigos = pd.factorize(dados[coluna])[0].astype(np.int32)
        peso = float(pesos.get(coluna, 1.0))
        acumulado += peso * (codigos[:, None] != codigos[None, :]).astype(np.float32)
        peso_total += peso

    if peso_total == 0:
        raise ValueError("Nenhuma variável com variância foi informada.")

    matriz = acumulado / peso_total
    np.fill_diagonal(matriz, 0.0)
    return matriz


def matriz_distancia(dados: np.ndarray, metrica: str = "euclidean") -> np.ndarray:
    return squareform(pdist(dados, metric=metrica))

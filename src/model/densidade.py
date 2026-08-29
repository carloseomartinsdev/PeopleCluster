"""Clusterização por densidade: DBSCAN."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

from src.model.particional import metricas_internas


def curva_k_distancia(dados: np.ndarray, k: int) -> np.ndarray:
    vizinhos = NearestNeighbors(n_neighbors=k).fit(dados)
    distancias, _ = vizinhos.kneighbors(dados)
    return np.sort(distancias[:, -1])


def joelho_k_distancia(curva: np.ndarray) -> tuple[int, float]:
    x = np.arange(len(curva), dtype=float)
    x_norm = (x - x.min()) / (x.max() - x.min())
    y_norm = (curva - curva.min()) / (curva.max() - curva.min() + 1e-12)
    inicio = np.array([x_norm[0], y_norm[0]])
    fim = np.array([x_norm[-1], y_norm[-1]])
    vetor = (fim - inicio) / np.linalg.norm(fim - inicio)
    pontos = np.column_stack([x_norm, y_norm]) - inicio
    projecao = np.outer(pontos @ vetor, vetor)
    indice = int(np.argmax(np.linalg.norm(pontos - projecao, axis=1)))
    return indice, float(curva[indice])


def varrer_dbscan(dados: np.ndarray, valores_eps: np.ndarray, min_amostras: int) -> pd.DataFrame:
    linhas = []
    for eps in valores_eps:
        rotulos = DBSCAN(eps=float(eps), min_samples=min_amostras).fit_predict(dados)
        validos = rotulos >= 0
        n_grupos = len(set(rotulos[validos]))
        pct_ruido = float((~validos).mean())
        silhueta = np.nan
        if n_grupos >= 2 and validos.sum() > n_grupos:
            silhueta = metricas_internas(dados[validos], rotulos[validos])["silhueta"]
        linhas.append(
            {
                "eps": round(float(eps), 3),
                "min_amostras": min_amostras,
                "grupos": n_grupos,
                "pct_ruido": round(pct_ruido, 4),
                "silhueta_sem_ruido": round(silhueta, 4) if silhueta == silhueta else np.nan,
            }
        )
    return pd.DataFrame(linhas).set_index("eps")


def aplicar_dbscan(dados: np.ndarray, eps: float, min_amostras: int) -> np.ndarray:
    return DBSCAN(eps=eps, min_samples=min_amostras).fit_predict(dados)

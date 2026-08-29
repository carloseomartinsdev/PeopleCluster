"""Clusterização particional: K-Means, K-Medoids e escolha de k."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_samples,
    silhouette_score,
)

from src.config import SEMENTE


@dataclass
class ResultadoKMedoids:
    rotulos: np.ndarray
    medoides: np.ndarray
    custo: float
    iteracoes: int
    historico_custo: list[float] = field(default_factory=list)


def _inicializar_medoides(
    distancias: np.ndarray, k: int, gerador: np.random.Generator
) -> np.ndarray:
    n = len(distancias)
    medoides = [int(gerador.integers(n))]
    for _ in range(1, k):
        proximidade = distancias[:, medoides].min(axis=1)
        probabilidade = proximidade**2
        soma = probabilidade.sum()
        if soma <= 0:
            candidatos = [i for i in range(n) if i not in medoides]
            medoides.append(int(gerador.choice(candidatos)))
            continue
        medoides.append(int(gerador.choice(n, p=probabilidade / soma)))
    return np.array(medoides)


def kmedoids(
    distancias: np.ndarray,
    k: int,
    reinicios: int = 10,
    max_iteracoes: int = 300,
    semente: int = SEMENTE,
) -> ResultadoKMedoids:
    gerador = np.random.default_rng(semente)
    melhor: ResultadoKMedoids | None = None

    for _ in range(reinicios):
        medoides = _inicializar_medoides(distancias, k, gerador)
        historico: list[float] = []
        rotulos = np.zeros(len(distancias), dtype=int)

        for iteracao in range(max_iteracoes):
            rotulos = np.argmin(distancias[:, medoides], axis=1)
            custo = float(distancias[np.arange(len(distancias)), medoides[rotulos]].sum())
            historico.append(custo)

            novos = medoides.copy()
            for grupo in range(k):
                indices = np.flatnonzero(rotulos == grupo)
                if len(indices) == 0:
                    continue
                interno = distancias[np.ix_(indices, indices)].sum(axis=1)
                novos[grupo] = indices[int(np.argmin(interno))]

            if np.array_equal(np.sort(novos), np.sort(medoides)):
                medoides = novos
                break
            medoides = novos

        rotulos = np.argmin(distancias[:, medoides], axis=1)
        custo = float(distancias[np.arange(len(distancias)), medoides[rotulos]].sum())
        resultado = ResultadoKMedoids(rotulos, medoides, custo, iteracao + 1, historico)
        if melhor is None or resultado.custo < melhor.custo:
            melhor = resultado

    assert melhor is not None
    return melhor


def metricas_internas(
    dados: np.ndarray | None,
    rotulos: np.ndarray,
    distancias: np.ndarray | None = None,
) -> dict[str, float]:
    vazio = {"silhueta": np.nan, "davies_bouldin": np.nan, "calinski_harabasz": np.nan}
    if len(np.unique(rotulos[rotulos >= 0])) < 2:
        return vazio

    if distancias is not None:
        silhueta = float(
            silhouette_score(np.asarray(distancias, dtype=float), rotulos, metric="precomputed")
        )
    else:
        silhueta = float(silhouette_score(dados, rotulos))

    if dados is None:
        return {**vazio, "silhueta": silhueta}

    return {
        "silhueta": silhueta,
        "davies_bouldin": float(davies_bouldin_score(dados, rotulos)),
        "calinski_harabasz": float(calinski_harabasz_score(dados, rotulos)),
    }


def varrer_k(
    dados: np.ndarray,
    k_minimo: int = 2,
    k_maximo: int = 5,
    semente: int = SEMENTE,
) -> pd.DataFrame:
    linhas = []
    for k in range(k_minimo, k_maximo + 1):
        modelo = KMeans(n_clusters=k, init="k-means++", n_init=20, random_state=semente)
        rotulos = modelo.fit_predict(dados)
        metricas = metricas_internas(dados, rotulos)
        linhas.append(
            {
                "k": k,
                "inercia": float(modelo.inertia_),
                **metricas,
                "menor_grupo": int(np.bincount(rotulos).min()),
                "maior_grupo": int(np.bincount(rotulos).max()),
            }
        )
    return pd.DataFrame(linhas).set_index("k")


def varrer_k_gower(
    distancias: np.ndarray,
    k_minimo: int = 2,
    k_maximo: int = 5,
    reinicios: int = 8,
    semente: int = SEMENTE,
) -> pd.DataFrame:
    linhas = []
    for k in range(k_minimo, k_maximo + 1):
        resultado = kmedoids(distancias, k=k, reinicios=reinicios, semente=semente)
        metricas = metricas_internas(None, resultado.rotulos, distancias=distancias)
        contagem = np.bincount(resultado.rotulos)
        linhas.append(
            {
                "k": k,
                "custo": resultado.custo,
                **metricas,
                "menor_grupo": int(contagem.min()),
                "maior_grupo": int(contagem.max()),
            }
        )
    return pd.DataFrame(linhas).set_index("k")


def cotovelo(inercias: pd.Series) -> int:
    x = inercias.index.to_numpy(dtype=float)
    y = inercias.to_numpy(dtype=float)
    x_norm = (x - x.min()) / (x.max() - x.min())
    y_norm = (y - y.min()) / (y.max() - y.min())
    inicio = np.array([x_norm[0], y_norm[0]])
    fim = np.array([x_norm[-1], y_norm[-1]])
    vetor = fim - inicio
    vetor = vetor / np.linalg.norm(vetor)
    pontos = np.column_stack([x_norm, y_norm]) - inicio
    projecao = np.outer(pontos @ vetor, vetor)
    distancias = np.linalg.norm(pontos - projecao, axis=1)
    return int(x[int(np.argmax(distancias))])


def silhueta_por_grupo(
    dados: np.ndarray | None,
    rotulos: np.ndarray,
    distancias: np.ndarray | None = None,
) -> pd.DataFrame:
    if distancias is not None:
        amostras = silhouette_samples(distancias, rotulos, metric="precomputed")
    else:
        amostras = silhouette_samples(dados, rotulos)
    tabela = pd.DataFrame({"grupo": rotulos, "silhueta": amostras})
    resumo = tabela.groupby("grupo")["silhueta"].agg(
        registros="size", media="mean", mediana="median", minimo="min"
    )
    resumo["pct_negativa"] = tabela.groupby("grupo")["silhueta"].apply(lambda s: (s < 0).mean())
    return resumo.round(4)

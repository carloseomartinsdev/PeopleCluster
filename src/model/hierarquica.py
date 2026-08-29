"""Clusterização hierárquica aglomerativa."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import cophenet, dendrogram, fcluster, linkage
from scipy.spatial.distance import squareform

LIGACOES_EUCLIDIANAS = ("ward", "complete", "average", "single")
LIGACOES_GOWER = ("complete", "average", "single")


def matriz_ligacao(
    dados: np.ndarray | None = None,
    ligacao: str = "ward",
    distancias: np.ndarray | None = None,
) -> np.ndarray:
    if distancias is not None:
        if ligacao == "ward":
            raise ValueError(
                "Ward pressupõe espaço euclidiano. Sobre Gower use 'average' ou 'complete'."
            )
        condensada = squareform(distancias, checks=False)
        return linkage(condensada, method=ligacao)
    if dados is None:
        raise ValueError("Informe `dados` ou `distancias`.")
    return linkage(dados, method=ligacao)


def coeficiente_cofenetico(ligacao_matriz: np.ndarray, distancias_condensadas: np.ndarray) -> float:
    return float(cophenet(ligacao_matriz, distancias_condensadas)[0])


def comparar_ligacoes_gower(distancias: np.ndarray, k: int) -> pd.DataFrame:
    condensada = squareform(distancias, checks=False)
    linhas = []
    for ligacao in LIGACOES_GOWER:
        matriz = linkage(condensada, method=ligacao)
        rotulos = fcluster(matriz, t=k, criterion="maxclust")
        tamanhos = np.bincount(rotulos)[1:]
        linhas.append(
            {
                "ligacao": ligacao,
                "cofenetico": round(coeficiente_cofenetico(matriz, condensada), 4),
                "grupos_obtidos": int(len(tamanhos)),
                "menor_grupo": int(tamanhos.min()),
                "maior_grupo": int(tamanhos.max()),
                "razao_maior_menor": round(float(tamanhos.max() / max(tamanhos.min(), 1)), 1),
            }
        )
    return pd.DataFrame(linhas).set_index("ligacao")


def cortar(ligacao_matriz: np.ndarray, k: int) -> np.ndarray:
    return fcluster(ligacao_matriz, t=k, criterion="maxclust") - 1


def desenhar_dendrograma(eixo, ligacao_matriz: np.ndarray, k: int, titulo: str):
    altura_corte = (ligacao_matriz[-k, 2] + ligacao_matriz[-(k - 1), 2]) / 2
    dendrogram(
        ligacao_matriz,
        truncate_mode="lastp",
        p=25,
        ax=eixo,
        color_threshold=altura_corte,
        above_threshold_color="#8A9BA8",
        leaf_rotation=90,
        leaf_font_size=7,
    )
    eixo.axhline(altura_corte, ls="--", lw=1.4, color="#EE6C4D")
    eixo.set_title(titulo)
    eixo.set_xlabel("grupos (últimas 25 fusões)")
    eixo.set_ylabel("altura da fusão")
    return altura_corte

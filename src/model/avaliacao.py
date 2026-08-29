"""Avaliação: estabilidade, concordância entre métodos e perfis de negócio."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_mutual_info_score, adjusted_rand_score

from src.config import SEMENTE
from src.model import particional as part


def matriz_ari(rotulos: dict[str, np.ndarray]) -> pd.DataFrame:
    """ARI pairwise entre partições nomeadas."""
    nomes = list(rotulos.keys())
    matriz = pd.DataFrame(index=nomes, columns=nomes, dtype=float)
    for a in nomes:
        for b in nomes:
            matriz.loc[a, b] = round(float(adjusted_rand_score(rotulos[a], rotulos[b])), 4)
    return matriz


def matriz_ami(rotulos: dict[str, np.ndarray]) -> pd.DataFrame:
    nomes = list(rotulos.keys())
    matriz = pd.DataFrame(index=nomes, columns=nomes, dtype=float)
    for a in nomes:
        for b in nomes:
            matriz.loc[a, b] = round(float(adjusted_mutual_info_score(rotulos[a], rotulos[b])), 4)
    return matriz


def estabilidade_bootstrap_kmeans(
    dados: np.ndarray,
    k: int,
    repeticoes: int = 20,
    fracao: float = 0.80,
    semente: int = SEMENTE,
) -> pd.DataFrame:
    from sklearn.cluster import KMeans

    gerador = np.random.default_rng(semente)
    referencia = KMeans(n_clusters=k, n_init=20, random_state=semente).fit_predict(dados)
    tamanho = int(fracao * len(dados))
    linhas = []
    for repeticao in range(repeticoes):
        indices = gerador.choice(len(dados), size=tamanho, replace=False)
        rotulos = KMeans(
            n_clusters=k, n_init=10, random_state=int(gerador.integers(1_000_000))
        ).fit_predict(dados[indices])
        linhas.append(
            {
                "repeticao": repeticao + 1,
                "ari": round(float(adjusted_rand_score(referencia[indices], rotulos)), 4),
            }
        )
    return pd.DataFrame(linhas).set_index("repeticao")


def estabilidade_bootstrap_kmedoids(
    distancias: np.ndarray,
    k: int,
    repeticoes: int = 15,
    fracao: float = 0.80,
    reinicios: int = 5,
    semente: int = SEMENTE,
) -> pd.DataFrame:
    gerador = np.random.default_rng(semente)
    referencia = part.kmedoids(distancias, k=k, reinicios=reinicios, semente=semente).rotulos
    tamanho = int(fracao * len(distancias))
    linhas = []
    for repeticao in range(repeticoes):
        indices = gerador.choice(len(distancias), size=tamanho, replace=False)
        sub = distancias[np.ix_(indices, indices)]
        rotulos = part.kmedoids(
            sub, k=k, reinicios=reinicios, semente=int(gerador.integers(1_000_000))
        ).rotulos
        linhas.append(
            {
                "repeticao": repeticao + 1,
                "ari": round(float(adjusted_rand_score(referencia[indices], rotulos)), 4),
            }
        )
    return pd.DataFrame(linhas).set_index("repeticao")


def perfil_por_cluster(
    features: pd.DataFrame,
    avaliacao: pd.DataFrame,
    rotulos: np.ndarray,
) -> pd.DataFrame:
    base = features.copy()
    base["cluster"] = rotulos
    base["Attrition"] = avaliacao["Attrition"].values
    base["PerformanceRating"] = avaliacao["PerformanceRating"].values
    return (
        base.groupby("cluster")
        .agg(
            n=("cluster", "size"),
            pct_base=("cluster", lambda s: 100 * len(s) / len(base)),
            pct_attrition=("Attrition", lambda s: (s == "Yes").mean() * 100),
            pct_overtime=("OverTime", lambda s: (s == "Yes").mean() * 100),
            job_satisfaction=("JobSatisfaction", "mean"),
            env_satisfaction=("EnvironmentSatisfaction", "mean"),
            work_life=("WorkLifeBalance", "mean"),
            performance=("PerformanceRating", "mean"),
            monthly_income=("MonthlyIncome", "median"),
            age=("Age", "median"),
            years_company=("YearsAtCompany", "median"),
            job_level=("JobLevel", "median"),
        )
        .round(2)
    )


def mapear_hipoteses_canvas(perfil: pd.DataFrame) -> pd.DataFrame:
    """Confronta clusters com hipóteses do Canvas (não é classificação automática rígida)."""
    linhas = []
    geral_attr = perfil["pct_attrition"].mean()
    geral_renda = perfil["monthly_income"].mean()
    for cluster, row in perfil.iterrows():
        hipoteses = []
        if row["pct_attrition"] < geral_attr and row["monthly_income"] >= geral_renda:
            hipoteses.append("Estáveis e engajados")
        if row["pct_attrition"] > geral_attr and row["monthly_income"] < geral_renda:
            hipoteses.append("Risco de attrition")
        if (
            row["years_company"] <= perfil["years_company"].median()
            and row["age"] <= perfil["age"].median()
        ):
            if "Risco de attrition" in hipoteses or row["pct_attrition"] > geral_attr:
                hipoteses.append("Início de carreira")
        if (
            row["pct_overtime"] > perfil["pct_overtime"].mean() * 1.15
            and row["performance"] >= perfil["performance"].mean()
            and row["monthly_income"] >= geral_renda
            and row["job_level"] >= perfil["job_level"].median()
        ):
            hipoteses.append("Alta performance e alta carga")
        if (
            row["job_satisfaction"] < perfil["job_satisfaction"].mean()
            and row["performance"] < perfil["performance"].mean()
            and row["pct_attrition"] <= geral_attr
        ):
            hipoteses.append("Baixo engajamento")
        linhas.append(
            {
                "cluster": cluster,
                "hipoteses_aproximadas": ", ".join(hipoteses) if hipoteses else "sem match claro",
            }
        )
    return pd.DataFrame(linhas).set_index("cluster")


def catalogo_acoes(perfil: pd.DataFrame) -> pd.DataFrame:
    acoes_por_hipotese = {
        "Estáveis e engajados": [
            "Programas de retenção de longo prazo",
            "Reconhecimento contínuo",
            "Benefícios de permanência",
        ],
        "Risco de attrition": [
            "Revisão salarial",
            "Pesquisa de clima",
            "Acompanhamento próximo do gestor",
        ],
        "Início de carreira": [
            "Mentoria",
            "Trilhas de capacitação",
            "Onboarding estruturado",
        ],
        "Alta performance e alta carga": [
            "Plano de carreira acelerado",
            "Programas de liderança",
            "Prevenção de burnout",
        ],
        "Baixo engajamento": [
            "Feedback estruturado",
            "PDI",
            "Avaliação de fit organizacional",
        ],
    }
    mapa = mapear_hipoteses_canvas(perfil)
    linhas = []
    for cluster, row in perfil.iterrows():
        hips = [h.strip() for h in str(mapa.loc[cluster, "hipoteses_aproximadas"]).split(",")]
        acoes: list[str] = []
        for h in hips:
            acoes.extend(acoes_por_hipotese.get(h, []))
        # dedupe preserving order
        vistas: set[str] = set()
        acoes_u = []
        for a in acoes:
            if a not in vistas:
                vistas.add(a)
                acoes_u.append(a)
        linhas.append(
            {
                "cluster": int(cluster),
                "n": int(row["n"]),
                "pct_attrition": float(row["pct_attrition"]),
                "persona": mapa.loc[cluster, "hipoteses_aproximadas"],
                "acoes": "; ".join(acoes_u)
                if acoes_u
                else "Definir com RH após leitura qualitativa",
                "kpi_monitoramento": "Attrition do segmento; JobSatisfaction; OverTime",
            }
        )
    return pd.DataFrame(linhas).set_index("cluster")

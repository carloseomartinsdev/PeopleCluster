"""Fecha a preparação (Gower + scaler) e executa a modelagem inicial."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src import config
from src.model import densidade as dens
from src.model import distancias as dist
from src.model import hierarquica as hier
from src.model import mistura as mix
from src.model import particional as part

config.garantir_diretorios()

tipologia = json.loads(
    (config.DATA_PROCESSED / "tipologia_variaveis.json").read_text(encoding="utf-8")
)
df = pd.read_csv(config.DATA_PROCESSED / "hr_features_cluster.csv")
avaliacao = pd.read_csv(config.DATA_PROCESSED / "hr_avaliacao.csv")

numericas = tipologia["numericas"] + tipologia["likert_clima"] + tipologia["ordinais"]
nominais = tipologia["categoricas_nominais"]

print("Calculando Gower...")
gower = dist.gower(df, numericas=numericas, nominais=nominais)
np.save(config.DATA_PROCESSED / "matriz_gower.npy", gower)

print("Montando matriz one-hot + StandardScaler...")
df_oh = pd.get_dummies(df, columns=nominais, drop_first=False)
scaler = StandardScaler()
matriz_padronizada = scaler.fit_transform(df_oh.to_numpy(dtype=float))
np.save(config.DATA_PROCESSED / "matriz_kmeans_scaled.npy", matriz_padronizada)
pd.DataFrame(matriz_padronizada, columns=df_oh.columns).to_csv(
    config.DATA_PROCESSED / "hr_kmeans_scaled.csv", index=False
)
pd.Series({"n_features": matriz_padronizada.shape[1]}).to_json(
    config.DATA_PROCESSED / "prep_modelagem_meta.json"
)

print("Varredura K-Medoids (Gower) k=2..5...")
var_gower = part.varrer_k_gower(gower, 2, 5, reinicios=8, semente=config.SEMENTE)
var_gower.to_csv(config.TABLES / "varredura_kmedoids_gower.csv")
print(var_gower.round(4))

print("Varredura K-Means (euclidiano) k=2..5...")
var_kmeans = part.varrer_k(matriz_padronizada, 2, 5, semente=config.SEMENTE)
var_kmeans.to_csv(config.TABLES / "varredura_kmeans.csv")
print(var_kmeans.round(4))

k_gower = int(var_gower["silhueta"].idxmax())
k_kmeans = int(var_kmeans["silhueta"].idxmax())
k = int(np.clip(round((k_gower + k_kmeans) / 2), config.K_MINIMO, config.K_MAXIMO))
# Prefer silhueta Gower as primary for mixed data
k = k_gower
print(f"k escolhido (máx silhueta Gower): {k}")

resultado = part.kmedoids(gower, k=k, reinicios=12, semente=config.SEMENTE)
rotulos = resultado.rotulos

ligacoes = hier.comparar_ligacoes_gower(gower, k)
ligacoes.to_csv(config.TABLES / "comparativo_ligacoes_gower.csv")
melhor_lig = ligacoes["cofenetico"].idxmax()
matriz_lig = hier.matriz_ligacao(distancias=gower, ligacao=melhor_lig)
rotulos_hier = hier.cortar(matriz_lig, k)

min_amostras = 2 * matriz_padronizada.shape[1]
curva = dens.curva_k_distancia(matriz_padronizada, min_amostras)
_, eps = dens.joelho_k_distancia(curva)
rotulos_db = dens.aplicar_dbscan(matriz_padronizada, eps=eps, min_amostras=min_amostras)

pca = PCA(n_components=2, random_state=config.SEMENTE)
proj = pca.fit_transform(matriz_padronizada)

print("Varredura GMM...")
var_gmm = mix.varrer_gmm(matriz_padronizada, 2, 5)
var_gmm.to_csv(config.TABLES / "varredura_gmm.csv", index=False)
escolha_gmm = mix.escolher_configuracao(var_gmm, k_alvo=k)
_, rotulos_gmm, _ = mix.ajustar_gmm(
    matriz_padronizada, k=k, covariancia=str(escolha_gmm["covariancia"])
)

# Perfis
perfil = df.copy()
perfil["cluster"] = rotulos
perfil["Attrition"] = avaliacao["Attrition"].values
perfil["PerformanceRating"] = avaliacao["PerformanceRating"].values

resumo_num = perfil.groupby("cluster")[tipologia["numericas"][:6]].median().round(2)
resumo_cat = (
    perfil.groupby("cluster")
    .agg(
        n=("cluster", "size"),
        pct_attrition=("Attrition", lambda s: (s == "Yes").mean() * 100),
        pct_overtime=("OverTime", lambda s: (s == "Yes").mean() * 100),
        job_satisfaction=("JobSatisfaction", "mean"),
        monthly_income=("MonthlyIncome", "median"),
        age=("Age", "median"),
        years_company=("YearsAtCompany", "median"),
    )
    .round(2)
)
resumo_cat.to_csv(config.TABLES / "perfil_clusters_kmedoids.csv")
print(resumo_cat)

# Figuras
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(var_gower.index, var_gower["silhueta"], marker="o")
axes[0].set_title("Silhueta K-Medoids (Gower)")
axes[0].set_xlabel("k")
axes[1].plot(var_kmeans.index, var_kmeans["silhueta"], marker="o", color="#EE6C4D")
axes[1].set_title("Silhueta K-Means (padronizado)")
axes[1].set_xlabel("k")
plt.tight_layout()
fig.savefig(config.FIGURES / "07_escolha_k.png", dpi=120, bbox_inches="tight")
fig.savefig(config.DOCS_FIGURES / "07_escolha_k.png", dpi=120, bbox_inches="tight")
plt.close()

fig, ax = plt.subplots(figsize=(10, 5))
hier.desenhar_dendrograma(ax, matriz_lig, k, f"Dendrograma Gower ({melhor_lig})")
fig.savefig(config.FIGURES / "08_dendrograma_gower.png", dpi=120, bbox_inches="tight")
fig.savefig(config.DOCS_FIGURES / "08_dendrograma_gower.png", dpi=120, bbox_inches="tight")
plt.close()

fig, ax = plt.subplots(figsize=(7, 5))
for g in sorted(np.unique(rotulos)):
    mask = rotulos == g
    ax.scatter(proj[mask, 0], proj[mask, 1], s=12, label=f"Grupo {g}", alpha=0.7)
ax.set_title("K-Medoids (Gower) projetado em PCA-2D da matriz padronizada")
ax.legend(frameon=False)
fig.savefig(config.FIGURES / "09_pca_clusters.png", dpi=120, bbox_inches="tight")
fig.savefig(config.DOCS_FIGURES / "09_pca_clusters.png", dpi=120, bbox_inches="tight")
plt.close()

pd.DataFrame(
    {
        "EmployeeNumber": avaliacao["EmployeeNumber"],
        "cluster_kmedoids_gower": rotulos,
        "cluster_hierarquico_gower": rotulos_hier,
        "cluster_dbscan": rotulos_db,
        "cluster_kmeans": KMeans(n_clusters=k, n_init=20, random_state=config.SEMENTE).fit_predict(
            matriz_padronizada
        ),
        "cluster_gmm": rotulos_gmm,
    }
).to_csv(config.DATA_PROCESSED / "rotulos_clusters.csv", index=False)

decisao = {
    "k": int(k),
    "k_gower_silhueta": float(var_gower.loc[k, "silhueta"]),
    "k_kmeans_silhueta_max": float(var_kmeans["silhueta"].max()),
    "ligacao_hierarquica": str(melhor_lig),
    "dbscan_eps": float(eps),
    "dbscan_min_amostras": int(min_amostras),
    "dbscan_grupos": int(len(set(rotulos_db[rotulos_db >= 0]))),
    "dbscan_pct_ruido": float((rotulos_db < 0).mean()),
    "pca_var_2d": float(pca.explained_variance_ratio_.sum()),
}
(config.MODELS / "decisao_modelagem.json").write_text(
    json.dumps(decisao, indent=2, ensure_ascii=False), encoding="utf-8"
)
print("Decisão:", decisao)
print("OK")

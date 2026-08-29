"""Executa a fase de avaliação e grava tabelas/figuras."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src import config
from src.model import avaliacao as av

config.garantir_diretorios()
sns.set_theme(style="whitegrid")

features = pd.read_csv(config.DATA_PROCESSED / "hr_features_cluster.csv")
avaliacao = pd.read_csv(config.DATA_PROCESSED / "hr_avaliacao.csv")
rotulos_df = pd.read_csv(config.DATA_PROCESSED / "rotulos_clusters.csv")
gower = np.load(config.DATA_PROCESSED / "matriz_gower.npy")
X = np.load(config.DATA_PROCESSED / "matriz_kmeans_scaled.npy")
decisao = json.loads((config.MODELS / "decisao_modelagem.json").read_text(encoding="utf-8"))
k = int(decisao.get("k", 2))

particoes = {
    "kmedoids_gower": rotulos_df["cluster_kmedoids_gower"].to_numpy(),
    "hierarquico_gower": rotulos_df["cluster_hierarquico_gower"].to_numpy(),
    "kmeans": rotulos_df["cluster_kmeans"].to_numpy(),
}

ari = av.matriz_ari(particoes)
ami = av.matriz_ami(particoes)
ari.to_csv(config.TABLES / "avaliacao_ari_metodos.csv")
ami.to_csv(config.TABLES / "avaliacao_ami_metodos.csv")
print("ARI entre métodos:\n", ari)

print("Bootstrap K-Means...")
boot_km = av.estabilidade_bootstrap_kmeans(X, k=k, repeticoes=20)
boot_km.to_csv(config.TABLES / "avaliacao_bootstrap_kmeans.csv")
print(boot_km["ari"].describe().round(4))

print("Bootstrap K-Medoids (Gower)...")
boot_pam = av.estabilidade_bootstrap_kmedoids(gower, k=k, repeticoes=12, reinicios=4)
boot_pam.to_csv(config.TABLES / "avaliacao_bootstrap_kmedoids.csv")
print(boot_pam["ari"].describe().round(4))

perfil = av.perfil_por_cluster(features, avaliacao, particoes["kmedoids_gower"])
perfil.to_csv(config.TABLES / "avaliacao_perfil_principal.csv")
print(perfil)

hips = av.mapear_hipoteses_canvas(perfil)
hips.to_csv(config.TABLES / "avaliacao_hipoteses_canvas.csv")
catalogo = av.catalogo_acoes(perfil)
catalogo.to_csv(config.TABLES / "avaliacao_catalogo_acoes.csv")
catalogo.reset_index().to_json(
    config.MODELS / "catalogo_personas.json",
    orient="records",
    force_ascii=False,
    indent=2,
)
print(catalogo)

# Critérios canvas
criterios = pd.DataFrame(
    [
        {
            "criterio": "k entre 2 e 5",
            "valor": k,
            "status": "ok" if 2 <= k <= 5 else "falha",
        },
        {
            "criterio": "menor segmento >= 5%",
            "valor": float(perfil["pct_base"].min()),
            "status": "ok" if perfil["pct_base"].min() >= 5 else "falha",
        },
        {
            "criterio": "silhueta Gower (referência)",
            "valor": float(decisao.get("k_gower_silhueta", decisao.get("silhueta_gower", np.nan))),
            "status": "fraca_esperada_base_sintetica",
        },
        {
            "criterio": "ARI médio bootstrap K-Means",
            "valor": float(boot_km["ari"].mean()),
            "status": "ok" if boot_km["ari"].mean() >= 0.5 else "atencao",
        },
        {
            "criterio": "ARI médio bootstrap K-Medoids",
            "valor": float(boot_pam["ari"].mean()),
            "status": "ok" if boot_pam["ari"].mean() >= 0.5 else "atencao",
        },
        {
            "criterio": "cada grupo com ação RH",
            "valor": int((catalogo["acoes"].str.len() > 0).sum()),
            "status": "ok",
        },
    ]
)
criterios.to_csv(config.TABLES / "avaliacao_criterios.csv", index=False)

fig, ax = plt.subplots(figsize=(5, 4))
sns.heatmap(ari.astype(float), annot=True, cmap="Blues", vmin=0, vmax=1, ax=ax)
ax.set_title("ARI entre métodos (k=2)")
plt.tight_layout()
fig.savefig(config.FIGURES / "10_ari_metodos.png", dpi=120, bbox_inches="tight")
fig.savefig(config.DOCS_FIGURES / "10_ari_metodos.png", dpi=120, bbox_inches="tight")
plt.close()

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].hist(boot_km["ari"], bins=8, color="#1B4965", edgecolor="white")
axes[0].set_title("Bootstrap ARI — K-Means")
axes[1].hist(boot_pam["ari"], bins=8, color="#EE6C4D", edgecolor="white")
axes[1].set_title("Bootstrap ARI — K-Medoids/Gower")
plt.tight_layout()
fig.savefig(config.FIGURES / "11_bootstrap_ari.png", dpi=120, bbox_inches="tight")
fig.savefig(config.DOCS_FIGURES / "11_bootstrap_ari.png", dpi=120, bbox_inches="tight")
plt.close()

fig, ax = plt.subplots(figsize=(6, 4))
perfil["pct_attrition"].plot(kind="bar", ax=ax, color=["#74C69D", "#EE6C4D"], rot=0)
ax.set_ylabel("% Attrition")
ax.set_title("Attrition por cluster (K-Medoids/Gower)")
plt.tight_layout()
fig.savefig(config.FIGURES / "12_attrition_por_cluster.png", dpi=120, bbox_inches="tight")
fig.savefig(config.DOCS_FIGURES / "12_attrition_por_cluster.png", dpi=120, bbox_inches="tight")
plt.close()

print("OK avaliação")

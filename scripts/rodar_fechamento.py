"""Gera artefatos do fechamento: EDA extra, escala, GMM, associação e relatório."""

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
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src import config
from src.deployment.relatorio import gravar
from src.eda import exploracao as eda
from src.model import associacao as assoc
from src.model import mistura as mix

config.garantir_diretorios()
sns.set_theme(style="whitegrid")

raw = pd.read_csv(config.DATA_RAW / "WA_Fn-UseC_-HR-Employee-Attrition.csv")
features = pd.read_csv(config.DATA_PROCESSED / "hr_features_cluster.csv")
avaliacao = pd.read_csv(config.DATA_PROCESSED / "hr_avaliacao.csv")
tipologia = json.loads(
    (config.DATA_PROCESSED / "tipologia_variaveis.json").read_text(encoding="utf-8")
)
rotulos_df = pd.read_csv(config.DATA_PROCESSED / "rotulos_clusters.csv")
X = np.load(config.DATA_PROCESSED / "matriz_kmeans_scaled.npy")

numericas = tipologia["numericas"]
nominais = tipologia["categoricas_nominais"]
ordinais = tipologia["ordinais"]
likert = tipologia["likert_clima"]

# --- EDA ---
spearman = eda.pares_spearman(raw, numericas + ordinais, corte=0.60)
spearman.to_csv(config.TABLES / "eda_spearman_pares.csv", index=False)

cramer = eda.pares_cramer(raw, nominais, corte=0.20)
cramer.to_csv(config.TABLES / "eda_cramer_pares.csv", index=False)

outliers = eda.discrepantes_tukey(
    raw, ["MonthlyIncome", "Age", "YearsAtCompany", "TotalWorkingYears"]
)
outliers["decisao"] = "manter — cauda de RH legítima, não erro de cadastro"
outliers.to_csv(config.TABLES / "eda_discrepantes_tukey.csv", index=False)

pca, variancia, cargas = eda.pca_exploratorio(raw, numericas + ordinais + likert, n_componentes=4)
variancia.to_csv(config.TABLES / "eda_pca_variancia.csv", index=False)
cargas.round(3).to_csv(config.TABLES / "eda_pca_cargas.csv")

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(variancia["componente"], variancia["var_acumulada"], marker="o")
ax.set_ylabel("Variância acumulada")
ax.set_title("PCA exploratório — variância acumulada")
plt.tight_layout()
fig.savefig(config.FIGURES / "15_pca_exploratorio.png", dpi=120, bbox_inches="tight")
fig.savefig(config.DOCS_FIGURES / "15_pca_exploratorio.png", dpi=120, bbox_inches="tight")
plt.close()

insights = pd.DataFrame(
    [
        {
            "id": 1,
            "insight": "Taxa de attrition desigual",
            "evidencia": (
                f"{(raw['Attrition'] == 'Yes').mean() * 100:.1f}% geral; "
                f"OverTime Yes "
                f"{(raw.loc[raw['OverTime'] == 'Yes', 'Attrition'] == 'Yes').mean() * 100:.1f}%"
            ),
        },
        {
            "id": 2,
            "insight": "Horas extras elevam risco de saída",
            "evidencia": "OverTime=Yes com attrition bem acima de OverTime=No",
        },
        {
            "id": 3,
            "insight": "Quem sai tem renda e idade médias menores",
            "evidencia": "MonthlyIncome e Age menores no grupo Attrition=Yes",
        },
        {
            "id": 4,
            "insight": "Likert baixa associa-se a mais saída",
            "evidencia": "JobSatisfaction e EnvironmentSatisfaction 1–2 com taxa maior",
        },
        {
            "id": 5,
            "insight": "Multicolinearidade de carreira",
            "evidencia": "JobLevel, MonthlyIncome e TotalWorkingYears com |rho| alto",
        },
        {
            "id": 6,
            "insight": "Constantes e ID não informam cluster",
            "evidencia": "EmployeeCount, StandardHours, Over18; EmployeeNumber é chave",
        },
        {
            "id": 7,
            "insight": "Discrepantes de renda são cauda, não erro",
            "evidencia": "Tukey em MonthlyIncome; decisão: manter",
        },
        {
            "id": 8,
            "insight": "PCA exploratório não é unidimensional",
            "evidencia": "CP1–CP2 concentram porte/carreira; vários CPs para 80%",
        },
    ]
)
insights.to_csv(config.TABLES / "eda_insights.csv", index=False)

# --- Sensibilidade à escala ---
df_oh = pd.get_dummies(features, columns=nominais, drop_first=False).to_numpy(dtype=float)
escaladores = {
    "StandardScaler": StandardScaler(),
    "RobustScaler": RobustScaler(),
    "MinMaxScaler": MinMaxScaler(),
}
rotulos_esc = {}
linhas_esc = []
for nome, esc in escaladores.items():
    matriz = esc.fit_transform(df_oh)
    modelo = KMeans(n_clusters=2, n_init=20, random_state=config.SEMENTE)
    rotulos = modelo.fit_predict(matriz)
    rotulos_esc[nome] = rotulos
    from sklearn.metrics import silhouette_score

    linhas_esc.append(
        {
            "escalador": nome,
            "silhueta": round(float(silhouette_score(matriz, rotulos)), 4),
            "inercia": round(float(modelo.inertia_), 1),
        }
    )
sens = pd.DataFrame(linhas_esc)
nomes = list(rotulos_esc)
ari_esc = pd.DataFrame(index=nomes, columns=nomes, dtype=float)
for a in nomes:
    for b in nomes:
        ari_esc.loc[a, b] = round(float(adjusted_rand_score(rotulos_esc[a], rotulos_esc[b])), 4)
sens.to_csv(config.TABLES / "preparacao_sensibilidade_escala.csv", index=False)
ari_esc.to_csv(config.TABLES / "preparacao_ari_escaladores.csv")

# --- GMM ---
var_gmm = mix.varrer_gmm(X, k_minimo=2, k_maximo=5)
var_gmm.to_csv(config.TABLES / "varredura_gmm.csv", index=False)
escolha = mix.escolher_configuracao(var_gmm, k_alvo=2)
_, rotulos_gmm, _ = mix.ajustar_gmm(X, k=2, covariancia=str(escolha["covariancia"]))
rotulos_df["cluster_gmm"] = rotulos_gmm
rotulos_df.to_csv(config.DATA_PROCESSED / "rotulos_clusters.csv", index=False)
(config.MODELS / "decisao_gmm.json").write_text(
    json.dumps(
        {
            "k": 2,
            "covariancia": str(escolha["covariancia"]),
            "bic": float(escolha["bic"]),
            "silhueta": float(escolha["silhueta"]),
            "pct_fronteira": float(escolha["pct_fronteira"]),
            "papel": "comparativo no espaço one-hot + StandardScaler; não substitui Gower",
        },
        indent=2,
        ensure_ascii=False,
    ),
    encoding="utf-8",
)

# --- Associação ---
transacoes = assoc.montar_transacoes(
    features, segmentos=rotulos_df["cluster_kmedoids_gower"].to_numpy()
)
comparativo, frequentes = assoc.comparar_algoritmos(transacoes, suporte_minimo=0.12, max_tamanho=3)
comparativo.to_csv(config.TABLES / "avaliacao_associacao_algoritmos.csv")
regras = assoc.gerar_regras(frequentes, confianca_minima=0.55, lift_minimo=1.10)
negocio = assoc.regras_de_negocio(regras)
if not negocio.empty:
    negocio.head(25).to_csv(config.TABLES / "avaliacao_regras_associacao.csv", index=False)
else:
    regras.head(25).to_csv(config.TABLES / "avaliacao_regras_associacao.csv", index=False)

# --- SMART + vazamento ---
perfil = pd.read_csv(config.TABLES / "avaliacao_perfil_principal.csv")
smart = pd.DataFrame(
    [
        {
            "pergunta": "Quais perfis emergem?",
            "resposta": "Dois: estáveis (0) e risco/início de carreira (1)",
        },
        {
            "pergunta": "Existe segmento com maior attrition?",
            "resposta": "Sim — cluster 1 com ~21% contra ~11% no 0",
        },
        {
            "pergunta": "O que caracteriza alta performance?",
            "resposta": "PerformanceRating não separou grupo próprio em k=2",
        },
        {
            "pergunta": "Satisfação, remuneração e permanência?",
            "resposta": "Cluster 0: renda e tempo de casa maiores, satisfação um pouco maior",
        },
        {
            "pergunta": "Horas extras e risco de saída?",
            "resposta": "OverTime eleva attrition na EDA; cluster 1 tem overtime um pouco maior",
        },
        {
            "pergunta": "Onde investir em retenção?",
            "resposta": "Prioridade no cluster 1 (mentoria, salário, clima)",
        },
    ]
)
smart.to_csv(config.TABLES / "avaliacao_perguntas_smart.csv", index=False)

proibidas = {"Attrition", "PerformanceRating", "EmployeeNumber"}
vazamento = pd.DataFrame(
    {
        "coluna": sorted(proibidas),
        "esta_nas_features": [c in features.columns for c in sorted(proibidas)],
        "papel": ["rótulo reservado", "rótulo reservado", "identificador"],
    }
)
vazamento.to_csv(config.TABLES / "avaliacao_auditoria_vazamento.csv", index=False)

print("OK fechamento")
print("GMM covariancia:", escolha["covariancia"], "BIC", escolha["bic"])
print("Apriori vs FP-Growth:\n", comparativo)
print("Regras de negócio:", 0 if negocio.empty else len(negocio))

print("Relatório:", gravar())

"""Testes de Gower, GMM, associação e scoring."""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score

from src.model import associacao as assoc
from src.model import distancias as dist
from src.model import mistura as mix


def test_gower_deterministico_e_simetrico():
    dados = pd.DataFrame(
        {
            "idade": [20, 30, 40],
            "area": ["A", "B", "A"],
        }
    )
    a = dist.gower(dados, numericas=["idade"], nominais=["area"])
    b = dist.gower(dados, numericas=["idade"], nominais=["area"])
    assert a.shape == (3, 3)
    np.testing.assert_allclose(a, b)
    np.testing.assert_allclose(a, a.T)
    assert np.allclose(np.diag(a), 0)


def test_gmm_varredura_k():
    rng = np.random.default_rng(42)
    dados = np.vstack([rng.normal(0, 1, size=(40, 4)), rng.normal(3, 1, size=(40, 4))])
    tabela = mix.varrer_gmm(dados, k_minimo=2, k_maximo=3, covariancias=("diag",))
    assert set(tabela["k"]) == {2, 3}
    assert tabela["convergiu"].all()
    escolha = mix.escolher_configuracao(tabela, k_alvo=2)
    _, rotulos, _ = mix.ajustar_gmm(dados, k=2, covariancia=str(escolha["covariancia"]))
    assert len(np.unique(rotulos)) == 2


def test_apriori_equivale_fpgrowth():
    features = pd.DataFrame(
        {
            "OverTime": ["Yes", "No", "Yes", "No"] * 20,
            "Gender": ["Male", "Female"] * 40,
            "Department": ["Sales", "Research & Development"] * 40,
            "JobRole": ["Sales Executive", "Research Scientist"] * 40,
            "BusinessTravel": ["Travel_Rarely"] * 80,
            "EducationField": ["Life Sciences"] * 80,
            "MaritalStatus": ["Married", "Single"] * 40,
            "EnvironmentSatisfaction": [3] * 80,
            "JobSatisfaction": [2, 4] * 40,
            "RelationshipSatisfaction": [3] * 80,
            "JobInvolvement": [3] * 80,
            "WorkLifeBalance": [3] * 80,
            "MonthlyIncome": np.linspace(2000, 9000, 80),
            "Age": np.linspace(22, 55, 80),
            "YearsAtCompany": np.linspace(1, 15, 80),
        }
    )
    transacoes = assoc.montar_transacoes(features, segmentos=np.array([0, 1] * 40))
    comparativo, _ = assoc.comparar_algoritmos(transacoes, suporte_minimo=0.2, max_tamanho=2)
    assert bool(comparativo.loc["FP-Growth", "identico_ao_apriori"])


def test_scoring_reproduz_carteira_treino():
    from src.deployment import scoring

    pacote = json.loads(
        (scoring.config.MODELS / "pacote_implantacao.json").read_text(encoding="utf-8")
    )
    features = pd.read_csv(scoring.config.DATA_PROCESSED / "hr_features_cluster.csv")
    rotulos = pd.read_csv(scoring.config.DATA_PROCESSED / "rotulos_clusters.csv")
    amostra = features.head(30)
    pred = scoring.classificar_base(amostra, pacote=pacote)
    esperado = rotulos["cluster_kmedoids_gower"].head(30).to_numpy()
    ari = adjusted_rand_score(esperado, pred["cluster"].to_numpy())
    assert ari == 1.0
    assert pred["ok"].all()

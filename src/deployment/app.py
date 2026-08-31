"""Aplicação Streamlit — personas, classificação e monitoramento PeopleCluster."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.deployment import scoring

ROOT = Path(__file__).resolve().parents[2]
LIKERT = [
    "EnvironmentSatisfaction",
    "JobSatisfaction",
    "RelationshipSatisfaction",
    "JobInvolvement",
    "WorkLifeBalance",
]
ORDINAIS = ["Education", "JobLevel", "StockOptionLevel"]
NOMINAIS_OPCOES = {
    "BusinessTravel": ["Non-Travel", "Travel_Rarely", "Travel_Frequently"],
    "Department": ["Sales", "Research & Development", "Human Resources"],
    "EducationField": [
        "Life Sciences",
        "Medical",
        "Marketing",
        "Technical Degree",
        "Other",
        "Human Resources",
    ],
    "Gender": ["Male", "Female"],
    "JobRole": [
        "Sales Executive",
        "Research Scientist",
        "Laboratory Technician",
        "Manufacturing Director",
        "Healthcare Representative",
        "Manager",
        "Sales Representative",
        "Research Director",
        "Human Resources",
    ],
    "MaritalStatus": ["Single", "Married", "Divorced"],
    "OverTime": ["Yes", "No"],
}


def _carregar_pacote() -> dict | None:
    caminho = ROOT / "models" / "pacote_implantacao.json"
    if not caminho.exists():
        return None
    return json.loads(caminho.read_text(encoding="utf-8"))


def _campo(col: str, padrao):
    chave = f"campo_{col}"
    if col in NOMINAIS_OPCOES:
        opcoes = NOMINAIS_OPCOES[col]
        idx = opcoes.index(padrao) if padrao in opcoes else 0
        return st.selectbox(col, opcoes, index=idx, key=chave)
    if col in LIKERT:
        return st.slider(col, 1, 4, int(padrao) if pd.notna(padrao) else 3, key=chave)
    if col in ORDINAIS:
        maximo = 5 if col != "StockOptionLevel" else 3
        minimo = 0 if col == "StockOptionLevel" else 1
        return st.slider(col, minimo, maximo, int(padrao), key=chave)
    valor = float(padrao) if pd.notna(padrao) else 0.0
    return st.number_input(col, value=valor, key=chave)


def main() -> None:
    st.set_page_config(page_title="PeopleCluster", layout="wide")
    st.title("PeopleCluster — Segmentação de colaboradores")
    st.caption("Tema 08 · RH e People Analytics · K-Medoids / Gower (k=2)")

    pacote = _carregar_pacote()
    catalogo_path = ROOT / "models" / "catalogo_personas.json"
    perfil_path = ROOT / "reports" / "tables" / "avaliacao_perfil_principal.csv"
    monitor_path = ROOT / "reports" / "tables" / "implantacao_monitoramento.csv"

    aba1, aba2, aba3 = st.tabs(["Personas", "Classificar colaborador", "Monitoramento"])

    with aba1:
        if catalogo_path.exists():
            catalogo = json.loads(catalogo_path.read_text(encoding="utf-8"))
            st.subheader("Personas publicadas")
            st.dataframe(pd.DataFrame(catalogo), use_container_width=True)
        else:
            st.warning("Catálogo ainda não gerado.")
        if perfil_path.exists():
            st.subheader("Perfil quantitativo")
            st.dataframe(pd.read_csv(perfil_path), use_container_width=True)
        if pacote:
            st.caption(
                f"Método {pacote.get('metodo')} · k={pacote.get('k')} · "
                f"medoides {pacote.get('medoides_employee_number')}"
            )

    with aba2:
        if pacote is None:
            st.info("Execute o notebook `06-implantacao.ipynb` para gerar o pacote.")
        else:
            st.subheader("Contrato de entrada")
            st.write("Preencha os atributos. O padrão é o medoide do cluster 0.")
            medoides = pacote["medoides_registros"]
            escolha = st.radio("Partir do medoide", ["cluster 0", "cluster 1"], horizontal=True)
            base = medoides[0 if escolha.endswith("0") else 1]
            atributos = {}
            grupos = [
                (
                    "Contexto",
                    [
                        "Department",
                        "JobRole",
                        "BusinessTravel",
                        "OverTime",
                        "Gender",
                        "MaritalStatus",
                        "EducationField",
                    ],
                ),
                (
                    "Carreira",
                    [
                        "Age",
                        "Education",
                        "JobLevel",
                        "NumCompaniesWorked",
                        "TotalWorkingYears",
                        "TrainingTimesLastYear",
                    ],
                ),
                (
                    "Remuneração",
                    [
                        "DailyRate",
                        "HourlyRate",
                        "MonthlyIncome",
                        "MonthlyRate",
                        "PercentSalaryHike",
                        "StockOptionLevel",
                    ],
                ),
                ("Clima (Likert 1–4)", LIKERT),
                (
                    "Tempo na empresa",
                    [
                        "YearsAtCompany",
                        "YearsInCurrentRole",
                        "YearsSinceLastPromotion",
                        "YearsWithCurrManager",
                        "DistanceFromHome",
                    ],
                ),
            ]
            for titulo, cols in grupos:
                st.markdown(f"**{titulo}**")
                colunas_ui = st.columns(3)
                for i, col in enumerate(cols):
                    if col not in pacote["colunas"]:
                        continue
                    with colunas_ui[i % 3]:
                        atributos[col] = _campo(col, base.get(col))
            if st.button("Classificar", type="primary"):
                resultado = scoring.classificar_colaborador(atributos, pacote=pacote)
                if not resultado.get("ok"):
                    st.error(resultado.get("erros"))
                else:
                    st.success(
                        f"Cluster {resultado['cluster']} · {resultado['persona']} · "
                        f"confiança {resultado['confianca']}"
                    )
                    st.write("Ações:", resultado.get("acoes"))
                    st.write("KPI:", resultado.get("kpi_monitoramento"))
                    st.json(
                        {
                            "distancias_medoides": resultado["distancias_medoides"],
                            "margem": resultado["margem"],
                        }
                    )

    with aba3:
        if monitor_path.exists():
            st.subheader("Plano de monitoramento")
            st.dataframe(pd.read_csv(monitor_path), use_container_width=True)
        else:
            st.info("Tabela de monitoramento ainda não gerada.")
        st.markdown(
            "Reciclagem: reexecutar notebooks 03–05 e republicar `models/pacote_implantacao.json` "
            "a cada 12 meses ou mudança estrutural de headcount."
        )


if __name__ == "__main__":
    main()

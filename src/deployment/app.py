"""Aplicação Streamlit — consulta de personas PeopleCluster."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    st.set_page_config(page_title="PeopleCluster", layout="wide")
    st.title("PeopleCluster — Segmentação de colaboradores")
    st.caption("Tema 08 · RH e People Analytics · partição K-Medoids / Gower (k=2)")

    catalogo_path = ROOT / "models" / "catalogo_personas.json"
    perfil_path = ROOT / "reports" / "tables" / "avaliacao_perfil_principal.csv"
    pacote_path = ROOT / "models" / "pacote_implantacao.json"

    if catalogo_path.exists():
        catalogo = json.loads(catalogo_path.read_text(encoding="utf-8"))
        st.subheader("Personas publicadas")
        st.dataframe(pd.DataFrame(catalogo), use_container_width=True)
    else:
        st.warning("Catálogo ainda não gerado (`models/catalogo_personas.json`).")

    if perfil_path.exists():
        st.subheader("Perfil quantitativo")
        st.dataframe(pd.read_csv(perfil_path), use_container_width=True)

    if pacote_path.exists():
        pacote = json.loads(pacote_path.read_text(encoding="utf-8"))
        st.subheader("Pacote de implantação")
        st.json(
            {
                "versao": pacote.get("versao"),
                "metodo": pacote.get("metodo"),
                "k": pacote.get("k"),
                "medoides_employee_number": pacote.get("medoides_employee_number"),
            }
        )
    else:
        st.info("Execute o notebook `06-implantacao.ipynb` para gerar o pacote.")


if __name__ == "__main__":
    main()

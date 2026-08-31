"""Monta o relatório final a partir dos artefatos persistidos."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src import config


def _ler_csv(nome: str) -> pd.DataFrame:
    return pd.read_csv(config.TABLES / nome)


def _md(df: pd.DataFrame) -> str:
    colunas = [str(c) for c in df.columns]
    linhas = ["| " + " | ".join(colunas) + " |", "| " + " | ".join("---" for _ in colunas) + " |"]
    for _, row in df.iterrows():
        linhas.append("| " + " | ".join(str(v) for v in row.tolist()) + " |")
    return "\n".join(linhas)


def montar_relatorio() -> str:
    perfil = _ler_csv("avaliacao_perfil_principal.csv")
    criterios = _ler_csv("avaliacao_criterios.csv")
    catalogo = _ler_csv("avaliacao_catalogo_acoes.csv")
    smart = _ler_csv("avaliacao_perguntas_smart.csv")
    vazamento = _ler_csv("avaliacao_auditoria_vazamento.csv")
    gmm = json.loads((config.MODELS / "decisao_gmm.json").read_text(encoding="utf-8"))
    decisao = json.loads((config.MODELS / "decisao_modelagem.json").read_text(encoding="utf-8"))
    assoc_alg = _ler_csv("avaliacao_associacao_algoritmos.csv")
    escala = _ler_csv("preparacao_sensibilidade_escala.csv")

    col_cluster = "cluster" if "cluster" in perfil.columns else perfil.columns[0]
    p = perfil.set_index(col_cluster)
    p0, p1 = p.loc[0], p.loc[1]
    k = int(decisao.get("k", 2))
    sil = float(decisao.get("silhueta_gower", decisao.get("k_gower_silhueta", 0)))
    n_conj = int(assoc_alg.iloc[0]["conjuntos_frequentes"])

    return f"""# PeopleCluster — relatório final

**Tema 08 · RH e People Analytics** · K-Medoids/Gower, k = {k}

## I · Sumário executivo

A base IBM HR (1.470 colaboradores) se organiza em **dois perfis acionáveis**:

- **Cluster 0 — estáveis e engajados:** n = {int(p0["n"])}, attrition ≈ {float(p0["pct_attrition"]):.1f}%, renda mediana {float(p0["monthly_income"]):.0f}, {float(p0["years_company"]):.0f} anos de casa.
- **Cluster 1 — risco / início de carreira:** n = {int(p1["n"])}, attrition ≈ {float(p1["pct_attrition"]):.1f}%, renda mediana {float(p1["monthly_income"]):.0f}, {float(p1["years_company"]):.0f} anos de casa.

Silhueta Gower = {sil:.4f} (fraca, esperada na base sintética). O critério decisivo é o **contraste de attrition** (~11% vs ~21%) e o catálogo de ações por persona. O modelo publicado é K-Medoids sobre Gower; GMM e regras de associação são comparativos.

## II · O problema

A organização opera com **política única** de carreira e retenção. Pergunta do Canvas: *que perfis existem, e que trilha cabe a cada um?* Restrição da diretoria: no máximo **cinco** grupos.

## III · Dados e preparação

1.470 × 35 na origem. Sem ausentes nem duplicatas. Removidas três constantes (`EmployeeCount`, `StandardHours`, `Over18`). `EmployeeNumber` é chave. `Attrition` e `PerformanceRating` ficaram **fora** da clusterização.

Dissimilaridade de Gower nas 29 features mistas; via euclidiana = one-hot + StandardScaler. Experimento de escala (k=2 K-Means):

{_md(escala)}

**Decisão:** manter StandardScaler na via euclidiana. RobustScaler sobe a silhueta ao comprimir caudas, mas não é o espaço do modelo oficial (Gower). A matriz `.npy` de Gower é local (gitignore); regenerar com `uv run python scripts/rodar_modelagem.py`.

## IV · Modelagem

| Família | Método | Papel |
|---|---|---|
| Particional | K-Medoids / Gower | **Oficial** (k={k}) |
| Particional | K-Means | Comparativo euclidiano |
| Hierárquica | average / complete / single (Gower) | Comparativo |
| Densidade | DBSCAN | Pouco útil nesta base |
| Mistura | GMM ({gmm["covariancia"]}, k=2) | Comparativo; BIC {gmm["bic"]}; silhueta {gmm["silhueta"]} |
| Associação | Apriori = FP-Growth ({n_conj} conjuntos) | Coocorrência com cluster/OverTime |

GMM opera no espaço one-hot padronizado. Premissa gaussiana é frágil em Likert e nominais; **não substitui** Gower.

## V · Avaliação

{_md(criterios)}

Auditoria de vazamento: nenhuma das colunas reservadas entra nas features.

{_md(vazamento)}

Perguntas SMART:

{_md(smart)}

## VI · Personas e ações

{_md(catalogo)}

## VII · Implantação

Pacote `models/pacote_implantacao.json`: classificação pelo medoide Gower mais próximo, com faixa de confiança. App: `uv run invoke app` (personas, classificar colaborador, monitoramento).

## VIII · Limitações

- Base sintética IBM; padrões podem não se repetir em um RH real.
- Silhueta baixa e ARI entre métodos próximo de zero: as geometrias divergem.
- Bootstrap do K-Medoids é modesto (~0,27).
- Dois grupos fundem hipóteses do Canvas (alta carga e baixo engajamento não emergiram sozinhas).

## IX · Próximos passos

1. Monitorar attrition e OverTime do cluster 1 mensalmente.
2. Reciclar o modelo a cada 12 meses ou mudança estrutural de headcount.
3. Se houver base real, reabrir k e regras de associação com suporte calibrado.
"""


def gravar() -> Path:
    texto = montar_relatorio()
    config.garantir_diretorios()
    destino = config.REPORTS / "relatorio-final.md"
    aviso = (
        "> Cópia montada a partir das tabelas em `reports/` e `models/`. "
        "O texto da banca é `docs/relatorio-final.md`.\n\n"
    )
    destino.write_text(aviso + texto, encoding="utf-8")
    return destino

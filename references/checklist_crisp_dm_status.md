# Checklist CRISP-DM × status do PeopleCluster

**Atualizado em:** 31/08/2026

Legenda: feito · parcial · pendente · N/A

## 1. Entendimento de negócio — feito

Canvas, critérios, riscos, perguntas. Custo-benefício formal permanece leve (projeto acadêmico). Quadro PBL reconstituído em `docs/pbl/quadro-pbl.md` (sem fotos do quadro físico).

## 2. Entendimento dos dados — feito

Base, dicionário, EDA (uni/bi/multi, ausentes, discrepantes Tukey, correlação Spearman/Cramér, PCA exploratório), insights persistidos.

## 3. Preparação — feito

Constantes removidas, rótulos reservados, tipologia, Gower local, StandardScaler, experimento de escala. Outliers mantidos por decisão.

## 4. Modelagem — feito

Técnicas selecionadas e executadas: K-Medoids/Gower (oficial), K-Means, hierárquica, DBSCAN, GMM, PCA. Apriori/FP-Growth na avaliação.

## 5. Avaliação — feito

Critérios de negócio, ARI/bootstrap, personas, SMART, auditoria de vazamento, limitações documentadas.

## 6. Implantação — feito

Pacote, carteira, monitoramento, Streamlit com classificação, relatório final Cap. I–IX.

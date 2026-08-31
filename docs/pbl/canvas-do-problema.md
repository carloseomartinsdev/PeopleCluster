# Canvas do Problema

Fonte operacional: [`references/canvas_problema.md`](../../references/canvas_problema.md).

## Contexto

Política única de carreira e retenção para todos os colaboradores, apesar de perfis distintos de motivação, carga, satisfação e risco de saída.

## Dor

- Rotatividade sem diagnóstico por perfil
- Engajamento desigual
- Trilhas de desenvolvimento genéricas

## Objetivo

Segmentar colaboradores em no máximo **cinco** perfis e definir trilha de desenvolvimento/retenção por grupo.

## Critérios de sucesso (negócio)

Redução de attrition, aumento de engajamento, políticas de RH segmentadas, leitura positiva da gestão.

## Critérios de sucesso (técnico)

Clusters interpretáveis em linguagem de RH, k ∈ [2, 5], coerência a posteriori com Attrition, estabilidade documentada entre métodos. Na base sintética IBM, a **utilidade gerencial** prevalece sobre silhueta máxima.

## Entidade e dados

Funcionário (1 linha = 1 colaborador). IBM HR Analytics Employee Attrition & Performance, 1.470 × 35, ODbL.

## Perguntas orientadas a dados

1. Quais perfis emergem?
2. Existe segmento com maior propensão a sair?
3. O que caracteriza alta performance?
4. Como se relacionam satisfação, remuneração e permanência?
5. Horas extras associam-se a maior risco de saída?
6. Onde concentrar investimento em retenção?

## Resultado do ciclo (k = 2)

| Cluster | Persona | Attrition | Ação |
|---|---|---|---|
| 0 | Estáveis e engajados | ~11% | Retenção de longo prazo |
| 1 | Risco / início de carreira | ~21% | Salário, clima, mentoria |

Hipóteses “alta carga” e “baixo engajamento” **não** emergiram como segmentos próprios em k=2.

## Técnicas executadas

- Oficial: Gower + K-Medoids
- Comparativo: K-Means, hierárquica, DBSCAN, GMM
- Associação: Apriori e FP-Growth (conjuntos equivalentes)
- PCA: diagnóstico, não espaço de produção

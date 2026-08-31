# Entendimento de negócio

## Contexto

A organização aplica a mesma política de carreira e retenção a todos os colaboradores. Perfis distintos de motivação, carga, satisfação e risco de saída recebem o mesmo tratamento, o que reduz o efeito das ações de RH.

## Problema

- Rotatividade sem diagnóstico claro por perfil
- Engajamento desigual entre áreas e cargos
- Política única de RH, sem diferenciar os perfis da base
- Ausência de trilhas de desenvolvimento por grupo

## Objetivo de negócio

Segmentar a base de colaboradores em até **cinco** perfis homogêneos e definir, para cada perfil, uma trilha de desenvolvimento e retenção.

## Meta de mineração de dados

Produzir agrupamentos a partir de atributos demográficos, de carreira, remuneração e clima organizacional (escalas Likert), utilizando distância adequada a dados mistos. Regras de associação (Apriori / FP-Growth) entram na avaliação como evidência de coocorrência, não como substituto da clusterização.

## Perguntas orientadas a dados

- Quais perfis de colaboradores aparecem nos dados?
- Existe segmento com maior propensão a sair?
- Quais atributos caracterizam alta performance nesta base?
- Como se relacionam satisfação, remuneração e permanência?
- Horas extras associam-se a maior risco de saída?
- Quais perfis concentram maior necessidade de investimento em retenção?

## Ações candidatas por perfil

| Perfil | Características esperadas | Ações candidatas |
|---|---|---|
| Alta performance e alta carga | Alto desempenho, overtime, responsabilidade | Carreira acelerada, liderança, prevenção de burnout |
| Estáveis e engajados | Baixo attrition, alta satisfação | Retenção de longo prazo, reconhecimento |
| Risco de attrition | Baixa satisfação, renda abaixo da média | Revisão salarial, clima, acompanhamento |
| Início de carreira | Pouco tempo de casa, faixa etária mais baixa | Mentoria, capacitação, onboarding |
| Baixo engajamento | Baixa satisfação e/ou performance | PDI, feedback, avaliação de fit |

Os perfis acima são hipóteses de negócio a serem confirmadas ou refutadas na modelagem.

## Restrições e riscos

- Base sintética (IBM): padrões podem não refletir uma organização real
- Possível estrutura de clusters fraca
- Mistura de variáveis numéricas, categóricas e Likert
- Limite operacional de cinco grupos
- Risco de superinterpretação de agrupamentos

Canvas completo: [canvas do problema](canvas_problema.md).

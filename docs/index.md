# PeopleCluster

## Introdução

PeopleCluster é um projeto de People Analytics voltado à segmentação de colaboradores e à definição de trilhas de desenvolvimento. A organização opera hoje com uma política única de carreira e retenção; o projeto busca identificar perfis distintos (no máximo cinco) e propor ações diferenciadas por grupo.

A abordagem metodológica é o **CRISP-DM**, com ênfase em aprendizado não supervisionado (clusterização e regras de associação).

## Dados do projeto

| Campo | Valor |
|---|---|
| Nome | PeopleCluster |
| Tema | 08 – RH e People Analytics |
| Entidade de análise | Funcionário (Employee) |
| Base | IBM HR Analytics Employee Attrition & Performance |
| Volume | 1.470 registros × 35 variáveis |
| Licença | ODbL / DbCL 1.0 |
| Restrição operacional | Máximo de 5 grupos acionáveis |
| Stack | Python 3.12, `uv`, pandas, scikit-learn, MkDocs |

### Tipo do projeto

!!! info ""
    - [x] Análise exploratória
    - [ ] Modelo preditivo
    - [ ] Modelo de classificação
    - [x] Modelo de agrupamento
    - [ ] Detecção de anomalias

### Confidencialidade

!!! warning ""
    - [x] Público
    - [ ] Interno
    - [ ] Restrito

### Objetivo de negócio

!!! quote ""
    Identificar perfis distintos de colaboradores e propor trilhas de desenvolvimento específicas para cada grupo, aumentando retenção, satisfação e desempenho organizacional.

## Perguntas orientadoras

1. Quantos grupos existem e por que esse número?
2. O que caracteriza cada grupo em linguagem de negócio?
3. Que padrões de coocorrência sustentam ou contradizem a segmentação?
4. Qual ação diferenciada cada grupo deve receber, e como medir o sucesso?

## Histórico do documento

| Data | Versão | Descrição | Autor |
| :--------- | :----- | :-------- | :---- |
| 07/08/2026 | 1.0 | Estrutura inicial do projeto e Canvas | Carlos E. O. Martins |
| 08/08/2026 | 1.1 | Documentação das fases de negócio, dados e preparação | Carlos E. O. Martins |

## Equipe

- Carlos E. O. Martins ([@carloseomartinsdev](https://github.com/carloseomartinsdev))
- Ana Caroline Amorim ([@amorinana](https://github.com/amorinana))

## Solicitante

Diretoria Executiva (cenário PBL — memorando do Encontro 1).

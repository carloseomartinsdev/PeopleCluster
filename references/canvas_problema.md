# Projeto de People Analytics – Segmentação de Funcionários e Trilhas de Desenvolvimento

## 1. CONTEXTO DE NEGÓCIO

A empresa atualmente adota uma política única de carreira e retenção para todos os colaboradores, independentemente de suas características individuais. No entanto, diferentes perfis de funcionários possuem motivações, comportamentos e expectativas distintas, o que pode impactar diretamente desempenho, engajamento e rotatividade (attrition).

Diante disso, surge a necessidade de segmentar os colaboradores em perfis mais homogêneos para possibilitar estratégias personalizadas de desenvolvimento e retenção.

---

## 2. A DOR

* Alta rotatividade ou dificuldade de retenção sem explicação clara
* Baixo engajamento em determinadas áreas
* Ineficiência de uma política única de RH
* Falta de clareza sobre quais perfis de colaboradores existem
* Ausência de trilhas de carreira personalizadas

---

## 3. OBJETIVO DE NEGÓCIO

Identificar perfis distintos de colaboradores e propor trilhas de desenvolvimento específicas para cada grupo, aumentando retenção, satisfação e desempenho organizacional.

---

## 4. CRITÉRIO DE SUCESSO DO NEGÓCIO

* Redução da taxa de attrition
* Aumento do engajamento dos colaboradores
* Melhoria em métricas de desempenho (PerformanceRating)
* Adoção de políticas segmentadas de RH
* Feedback positivo de gestores e equipe de RH

---

## 5. META DE MINERAÇÃO

Aplicar técnicas de clusterização para identificar grupos de funcionários com características similares, considerando variáveis demográficas, comportamentais e de desempenho.

---

## 6. CRITÉRIO DE SUCESSO TÉCNICO

* Identificação de clusters interpretáveis
* Baixa variabilidade intra-cluster e alta separação entre clusters
* Coerência dos grupos com variáveis de negócio (ex: attrition, performance)
* Redução dimensional eficaz (PCA, se necessário)
* Estabilidade dos clusters entre métodos (K-Medoids, Hierárquico, DBSCAN)

---

## 7. ENTIDADE DE ANÁLISE

Funcionários (Employees)

Cada linha representa um colaborador com atributos como:

* Idade
* Cargo
* Tempo de empresa
* Satisfação no trabalho
* Renda mensal
* Frequência de viagens
* Horas extras
* Performance
* Attrition (se saiu ou não)

---

## 8. FONTE E VOLUME DOS DADOS

* Base: IBM HR Analytics Employee Attrition & Performance
* Origem: Kaggle (pavansubhasht)
* Volume: aproximadamente 1.470 funcionários
* Variáveis: 35 colunas
* Licença: ODbL / DbCL 1.0

Observações:

* Dataset sintético
* Algumas colunas constantes:

  * EmployeeCount
  * StandardHours
  * Over18
    → devem ser removidas (variância zero)

---

## 9. PERGUNTAS ORIENTADAS A DADOS

* Quais perfis de colaboradores existem na empresa?
* Existe um grupo com maior propensão a sair (attrition)?
* Quais características definem colaboradores de alta performance?
* Existe relação entre satisfação, salário e permanência?
* Funcionários com muitas horas extras apresentam maior risco de saída?
* Quais perfis demandam mais investimento em retenção?
* Como idade, tempo de empresa e cargo influenciam comportamento?

---

## 10. RESTRIÇÕES E RISCOS

* Dataset é sintético → padrões podem não refletir a realidade
* Estrutura de clusters pode ser fraca
* Mistura de variáveis:

  * Numéricas
  * Categóricas
  * Likert (satisfação)
* Necessidade de usar distância apropriada (ex: Gower)
* Risco de interpretação incorreta dos clusters
* Possível overfitting conceitual (ver padrões onde não existem)

---

## 11. AÇÕES ESPERADAS POR GRUPO

Após clusterização, espera-se identificar perfis como:

### Grupo 1 – Alta Performance e Alta Carga

Características:

* Alto desempenho
* Muitas horas extras
* Alta responsabilidade

Ações:

* Plano de carreira acelerado
* Programas de liderança
* Prevenção de burnout

---

### Grupo 2 – Estáveis e Engajados

Características:

* Baixo risco de saída
* Satisfação alta
* Performance consistente

Ações:

* Programas de retenção
* Benefícios de longo prazo
* Reconhecimento contínuo

---

### Grupo 3 – Risco de Attrition

Características:

* Baixa satisfação
* Alta rotatividade
* Salário abaixo da média

Ações:

* Revisão salarial
* Pesquisa de clima
* Acompanhamento próximo

---

### Grupo 4 – Início de Carreira

Características:

* Pouco tempo de empresa
* Jovens
* Performance variável

Ações:

* Trilhas de capacitação
* Mentoria
* Onboarding estruturado

---

### Grupo 5 – Baixo Engajamento

Características:

* Baixa satisfação
* Baixa performance
* Pouca evolução

Ações:

* Feedback estruturado
* Plano de desenvolvimento individual (PDI)
* Avaliação de fit organizacional

---

## TÉCNICAS RECOMENDADAS

* Distância: Gower (dados mistos)
* Clusterização:

  * K-Medoids (PAM)
  * Hierárquica
  * DBSCAN
* Redução de dimensionalidade:

  * PCA
* Regras de associação:

  * Apriori
  * FP-Growth

---

## JUSTIFICATIVA DA BASE

A base foi escolhida por:

* Misturar diferentes tipos de variáveis
* Ter tamanho ideal para experimentação
* Permitir uso de múltiplas técnicas
* Simular cenário real de RH

---

## CONCLUSÃO

Este projeto permitirá transformar uma política genérica de RH em uma abordagem orientada a dados, segmentando colaboradores e aplicando estratégias específicas para cada perfil, aumentando eficiência organizacional e reduzindo turnover.

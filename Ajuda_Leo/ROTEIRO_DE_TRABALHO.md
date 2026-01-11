# 📜 Roteiro de Trabalho - Análise TCC (REN 1000 ANEEL)

Este documento define o fluxo de trabalho e os objetivos estratégicos da análise de dados para o TCC.

## 🎯 Objetivo Principal

Gerar **insights quantitativos e qualitativos** que alimentem a argumentação do TCC. O foco é entender como a **REN 1000 da ANEEL (especificamente o Anexo IV)** impactou os grupos de consumidores, as tarifas e as empresas do setor elétrico, traçando comparativos com a norma antiga.

---

## 🚀 O Pipeline de Dados (Passo a Passo)

Para atingir o objetivo, executaremos os seguintes passos técnicos (já implementados nos scripts da pasta):

### 1. Extração de Dados (`1_extracao.py`)

- **Meta**: Obter dados de **2 sites distintos da ANEEL**.
- **Necessidade**: Garantir que as tabelas contenham informações de Consumo, Tarifa e Classificação da Distribuidora.

### 2. Tratamento e Limpeza (`2_limpeza.py`)

- **Meta**: Unificar os dados dos dois sites em uma base sólida.
- **Conformidade**: Os dados devem estar limpos para evitar distorções nas estatísticas (remover nulos, inconsistências de grandezas, etc).

### 3. Clusterização (`3_clusterizacao.py`)

- **Meta**: Agrupar distribuidoras ou consumidores por similaridade.
- **Pergunta Chave**: "Quais grupos se formam naturalmente com a nova regra? Eles mudaram em relação à regra antiga?"

### 4. Análise Estatística (`4_analise.py`)

- **Meta**: Validar as hipóteses do TCC com números.
- **Foco Analítico**:
  - Comparação de médias de tarifas entre os grupos.
  - Identificar se houve mudança significativa no perfil das empresas com a entrada do **Anexo IV da REN 1000**.

---

## 📚 Contexto Normativo (Importante)

Ao analisar os resultados gerados pelos scripts, tenha em mente:

- **Resolução Normativa ANEEL nº 1.000/2021 (REN 1000)**: Consolida as regras de prestação de serviço público de distribuição de energia elétrica.
- **Anexo IV**: Foco especial aqui. Verifique se os clusters encontrados refletem as categorias ou impactos previstos neste anexo.
- **Comparativo**: Tente sempre cruzar os dados atuais com o cenário "pré-REN 1000" para destacar a evolução ou regressão de indicadores.

---

Este roteiro serve como o "cérebro" do projeto. Os scripts Python são os "braços" que executam o trabalho.

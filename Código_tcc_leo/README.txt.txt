# Análise de Dados - TCC (REN 1.000/2021)

Este repositório contém o script em Python utilizado para a análise quantitativa do meu Trabalho de Conclusão de Curso.

**Tema:** Comparativo financeiro e operacional de distribuidoras de energia sob a ótica da REN ANEEL 1.000/2021.

## 📂 Arquivos
* `analise_tcc.py`: Código principal que processa os dados e gera os gráficos.
* `requirements.txt`: Lista de bibliotecas necessárias.

## 🚀 Como executar
Para reproduzir as análises e gerar os gráficos no seu computador:

1.  **Instale as dependências:**
    ```bash
    pip install pandas numpy matplotlib seaborn
    ```

2.  **Execute o script:**
    ```bash
    python analise_tcc.py
    ```

## 📊 Resultados Gerados
Após a execução, o script criará automaticamente na pasta:
* `grafico_eficiencia_financeira.png` (Visualização EBITDA x Margem).
* `grafico_correlacao_regulacao.png` (Regressão CAPEX x Multas).
* `resultados_finais.csv` (Tabela com o ranking de eficiência simulado).

---
**Autor:** [João Pedro Costenaro]
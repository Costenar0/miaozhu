# Análise de Dados - TCC (REN 1.000/2021)

Este repositório contém o script em Python utilizado para a análise quantitativa do meu Trabalho de Conclusão de Curso.

**Tema:** Comparativo financeiro e operacional de distribuidoras de energia sob a ótica da REN ANEEL 1.000/2021.

## 📂 Estrutura de Pastas

* `dados_teste.csv`: Tabela com os dados usados na análise.
* `Código_tcc_leo/`
  * `analise_tcc.py`: Código principal comentado para fácil entendimento.
  * `requirements.txt`: Lista de bibliotecas que precisam ser instaladas.

## 🛠️ Configurando o Ambiente (Leia com atenção!)

Antes de rodar qualquer coisa, é **muito importante** criar um "Ambiente Virtual".

### 🤔 O que é isso e por que usar?

Imagine que o Python do seu computador é uma caixa de ferramentas bagunçada que todos os programas usam. Se instalarmos bibliotecas novas ali, podemos quebrar outros programas que já funcionam.

O **Ambiente Virtual (chamado `.venv`)** é como criar uma **maleta de ferramentas exclusiva** só para este projeto. Tudo que instalarmos fica guardado dentro dessa pastinha e não afeta o resto do seu computador. É mais seguro, organizado e profissional!

### 🚀 Passo a Passo

1. **Abra o terminal** na pasta `TCC_leo`.

2. **Crie a "maleta" (Ambiente Virtual)**:
    Digite este comando e aperte Enter:

    ```bash
    python3 -m venv .venv
    ```

    *Isso vai criar uma pasta invisível chamada `.venv` aí dentro.*

3. **Abra a "maleta" (Ativar o ambiente)**:
    Esse passo diz para o computador: "Agora use as ferramentas desta maleta".
    * **No Linux/Mac:**

        ```bash
        source .venv/bin/activate
        ```

    * **No Windows:**

        ```bash
        .venv\Scripts\activate
        ```

    *💡 Dica: Você saberá que funcionou porque vai aparecer um `(.venv)` escrito no começo da linha do terminal.*

4. **Encha a maleta com as ferramentas (Instalar bibliotecas)**:
    Agora que a maleta está aberta, vamos colocar as bibliotecas que o código precisa (pandas, matplotlib, etc):

    ```bash
    pip install -r Código_tcc_leo/requirements.txt
    ```

5. **Rode o código**:
    Tudo pronto! Agora é só executar:

    ```bash
    python Código_tcc_leo/Analise_tcc.py
    ```

## 🤝 Trabalhando em Conjunto (Git)

Se você tem dúvidas de como mandar suas alterações para o GitHub ou baixar as minhas, leia o guia que preparei:

👉 **[GUIA BÁSICO DE GIT (Clique aqui)](COMO_USAR_GIT.md)** 👈

## 📊 Resultados Gerados

Após a execução, o script criará automaticamente na pasta:

* `grafico_eficiencia_financeira.png` (Visualização EBITDA x Margem).
* `grafico_correlacao_regulacao.png` (Regressão CAPEX x Multas).
* `resultados_finais.csv` (Tabela com o ranking de eficiência simulado).

# ⚡ Projeto de Análise de Dados ANEEL

Bem-vindo! Este guia foi preparado especialmente para você rodar o projeto no seu **Windows**. Vamos construir um **pipeline de dados** (uma sequência de passos) para pegar dados da ANEEL, limpá-los, agrupar consumidores parecidos (clusterização) e analisar os resultados.

Também deixei comentários especiais no código para que, se você usar uma IA (como ChatGPT, Gemini ou Claude), ela consiga entender exatamente o que está acontecendo e te sugerir os próximos passos.

---

## 🪟 Guia Rápido de Windows (Terminal/PowerShell)

Para rodar os comandos, abra o **PowerShell** ou o **CMD** na pasta deste projeto.

- **`dir`** ou **`ls`**: Lista os arquivos da pasta atual ("O que tem aqui?").
- **`cd NOME_DA_PASTA`**: Entra em uma pasta ("Change Directory").
  - `cd ..`: Volta para a pasta anterior (sobe um nível).
- **`python NOME_SCRIPT.py`**: Roda um arquivo Python.
- **`pip install NOME_BIBLIOTECA`**: Instala ferramentas novas.

---

## 1. Configurando o Ambiente

Antes de começar, precisamos instalar as "ferramentas" (bibliotecas) que o Python vai usar.

1. **Abra o Terminal** na pasta deste projeto (`Ajuda_Leo`).
   - Dica: Na pasta, segure `Shift` + clique com botão direito e escolha "Abrir janela do PowerShell aqui" ou "Abrir no Terminal".

2. **Ative o ambiente virtual** (isso isola o projeto para não bagunçar seu sistema).
   - No **PowerShell**:

     ```powershell
     ..\.venv\Scripts\Activate.ps1
     ```

   - Ou no **CMD (Prompt de Comando)**:

     ```cmd
     ..\.venv\Scripts\activate.bat
     ```

   *(Você verá um `(.venv)` aparecer no começo da linha do terminal. Se der erro de permissão no PowerShell, tente: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`)*.

3. **Instale as dependências**:

   ```bash
   pip install -r ..\requirements.txt
   ```

   *(Isso vai baixar pandas, sklearn e outras coisas legais).*

---

## 2. Passo a Passo do Projeto

Rode os scripts na ordem abaixo. Um depende do outro!

### 📥 1. Extração (`1_extracao.py`)

- **Objetivo**: Baixar os dados brutos da internet ou simular dados.
- **Sua Tarefa**:
  1. Abra o arquivo `1_extracao.py` no seu editor de texto (VS Code, Bloco de Notas, etc).
  2. Procure onde diz `URL_ALVO_1`.
  3. Cole o link real da ANEEL que vamos usar (ou deixe como está para testar com dados falsos).
- **Comando**:

  ```bash
  python 1_extracao.py
  ```

### 🧹 2. Limpeza (`2_limpeza.py`)

- **Objetivo**: Arrumar a bagunça. Remove duplicatas e preenche buracos nos dados.
- **Comando**:

  ```bash
  python 2_limpeza.py
  ```

### 🤖 3. Clusterização (`3_clusterizacao.py`)

- **Objetivo**: A Mágica! Usa Inteligência Artificial (algoritmo K-Means) para descobrir grupos de consumidores.
- **O que acontece**: Ele cria uma coluna nova chamada `Cluster` (0, 1, 2...) indicando a qual grupo o consumidor pertence.
- **Comando**:

  ```bash
  python 3_clusterizacao.py
  ```

### 📊 4. Análise (`4_analise.py`)

- **Objetivo**: Entender os grupos. Quem gasta mais? Quem paga mais caro?
- **Comando**:

  ```bash
  python 4_analise.py
  ```

- **Resultado**: Vai aparecer na tela e salvar um arquivo `relatorio_analise.txt`.

---

## 🧠 Seção para Inteligência Artificial (Copie isso para sua IA)

*Se você estiver pedindo ajuda para uma IA continuar este projeto, mostre o texto abaixo para ela:*

> **CONTEXTO DO PROJETO**:
> Estamos criando um pipeline de Data Science para dados de energia (ANEEL).
>
> 1. **Stack**: Python, Pandas, Scikit-learn.
> 2. **Estado Atual**: Temos scripts básicos de Extração (mock/requests), Limpeza (pandas), Clusterização (K-Means) e Análise descritiva.
> 3. **Dados**: Consumidores, Consumo_kWh, Tarifa, Região.
> 4. **Objetivo Futuro**:
>    - Melhorar a clusterização usando "Elbow Method" para definir o K ideal.
>    - Testar outros algoritmos (DBSCAN, Hierarchical).
>    - Criar gráficos avançados (Seaborn/Matplotlib) plotando Consumo x Tarifa coloridos por Cluster.
>    - Automatizar a extração real via scraping de tabelas HTML se necessário.
>
> Por favor, use essas informações para sugerir melhorias no código ou na análise estatística.

---

Boa sorte! Qualquer erro no terminal, copie e me mande.

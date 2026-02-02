TCC Leo - Pipeline de Dados ANEEL
=================================

Este projeto contém um pipeline de dados para análise do impacto da Resolução Normativa 1.000/2021 da ANEEL.

Estrutura de Arquivos
---------------------
/Códigos
  - 1_extracao.py: Extração de dados (ou geração de dados sintéticos para simulação).
  - 2_limpeza.py: Tratamento de dados nulos e formatação.
  - 3_clusterizacao.py: Agrupamento de distribuidoras usando K-Means.
  - 4_analise.py: Geração de indicadores, estatísticas descritivas e gráficos comparativos.

requirements.txt: Lista de dependências Python.
run_pipeline.ps1: Script PowerShell para automação de todo o fluxo.

Como Executar
-------------
1. Certifique-se de ter Python instalado.
2. Abra o terminal na pasta raiz do projeto.
3. Execute o script de automação:
   
   ./run_pipeline.ps1

   Isso irá instalar as dependências e rodar sequencialmente todos os passos, gerando os arquivos CSV e gráficos PNG na raiz.

Arquivos Gerados
----------------
- dados_brutos.csv
- dados_limpos.csv
- dados_clusterizados.csv
- resultados_finais.csv
- *.png (Gráficos de análise)

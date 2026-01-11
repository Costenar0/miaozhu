import requests
import pandas as pd
# import beautifulsoup4 as bs4  # Biblioteca usada para 'ler' sites HTML (scraping)

# ==============================================================================
# 📥 SCRIPT 1: EXTRAÇÃO DE DADOS
# ==============================================================================
# OBJETIVO: Este script é responsável por buscar os dados.
#
# COMO FUNCIONA:
# 1. Definimos as URLs de onde os dados vêm.
# 2. Se tivermos a URL, baixamos.
# 3. Se não tivermos (ainda), criamos dados falsos (MOCK) para testar o resto do projeto.
# ==============================================================================

# --- [ÁREA DE EDIÇÃO DO USUÁRIO] ---
# Coloque aqui as URLs da ANEEL que você vai usar.
# Se for um arquivo CSV direto, melhor ainda!
URL_ALVO_1 = "INSIRA_SUA_URL_AQUI"
URL_ALVO_2 = "INSIRA_OUTRA_URL_AQUI_SE_NECESSARIO"
# -----------------------------------

def extrair_dados():
    print(">>> Iniciando extração de dados...")
    
    # [PARA IA LER]: Aqui estamos preparando o terreno para extração real.
    # Sugestão futura: Implementar tratamento de erro try/except para conexão.
    
    # --- CENÁRIO A: ANEEL fornece um CSV direto linkado ---
    # df = pd.read_csv(URL_ALVO_1, sep=';', encoding='latin1')
    
    # --- CENÁRIO B: Precisamos baixar o site e achar a tabela ---
    # response = requests.get(URL_ALVO_1)
    # if response.status_code == 200:
    #     # Aqui usaríamos BeautifulSoup para achar a <table>...
    #     pass
    
    # ------------------------------------------------------------------
    # --- MOCK / DADOS DE TESTE (Usado enquanto não temos as URLs) ---
    # ------------------------------------------------------------------
    print("⚠️  AVISO: Usando dados de exemplo (MOCK) pois as URLs não foram preenchidas.")
    
    # Criando um "dicionário" (estrutura chave: valor) que vira nossa tabela
    dados = {
        'Consumidor': [
            'Indústria A', 'Comércio B', 'Residencial C', 'Indústria D', 
            'Rural E', 'Comércio F', 'Indústria G', 'Residencial H'
        ],
        'Consumo_kWh': [
            15000, 2300, 450, 45000, 
            3100, 2100, 12000, 500
        ],
        'Regiao': [
            'Norte', 'Sul', 'Norte', 'Sudeste', 
            'Sudeste', 'Sul', 'Centro-Oeste', 'Nordeste'
        ],
        'Tarifa': [
            0.55, 0.60, 0.85, 0.45, 
            0.62, 0.61, 0.50, 0.82
        ]
    }
    
    # Transformando em DataFrame (a tabela do Excel do Python)
    df = pd.DataFrame(dados)
    
    # Visualizando as primeiras linhas para garantir que deu certo
    print("\nVisualização dos Dados Extraídos:")
    print(df.head()) # .head() mostra os 5 primeiros
    # ------------------------------------------------------------------

    # Salvando os dados brutos num arquivo CSV (para o próximo script usar)
    caminho_saida = "dados_brutos.csv"
    df.to_csv(caminho_saida, index=False)
    print(f"\n✅ CONCLUÍDO: Dados extraídos salvos em '{caminho_saida}'")
    print("Agora execute o script: python 2_limpeza.py")

if __name__ == "__main__":
    extrair_dados()

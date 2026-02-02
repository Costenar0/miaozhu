import pandas as pd
import numpy as np
import os

def gerar_dados_simulados(n_linhas=1000):
    """
    Gera um dataset simulado para fallback caso não haja conexão ou arquivos locais.
    Simula Distribuidoras, Datas, DEC, FEC e Tarifas.
    """
    print("Gerando dados sintenticos para simulacao...")
    np.random.seed(42)
    
    # Distribuidoras fictícias
    distribuidoras = [f'Distribuidora_{i}' for i in range(1, 21)]
    
    # Datas entre 2020 e 2023 (cobrindo pré e pós REN 1000)
    datas = pd.date_range(start='2020-01-01', end='2023-12-31', freq='M')
    
    dados = []
    for dist in distribuidoras:
        for data in datas:
            # Simula valores com alguma variância
            dec = np.random.uniform(5, 20)  # Horas
            fec = np.random.uniform(4, 15)  # Vezes
            tarifa = np.random.uniform(0.5, 1.2) # R$/kWh
            
            # Pequena tendência de melhoria (queda) nos indicadores pós 2022 para simulação
            if data.year >= 2022:
                dec *= 0.95
                fec *= 0.95
            
            dados.append({
                'distribuidora': dist,
                'data_referencia': data,
                'dec': dec,
                'fec': fec,
                'tarifa_media': tarifa
            })
            
    df = pd.DataFrame(dados)
    return df

def carregar_dados(url_ou_path):
    """
    Tenta carregar de URL ou Path. Retorna None se falhar.
    """
    try:
        if url_ou_path.endswith('.csv'):
            return pd.read_csv(url_ou_path)
        # Adicionar outros formatos se necessário (excel, json, etc)
    except Exception as e:
        print(f"Erro ao carregar {url_ou_path}: {e}")
        return None

def main():
    # URLs placeholders (Exemplo de onde entrariam links reais da ANEEL/Sosiap)
    url_dados_1 = "http://dados.aneel.gov.br/qq_dataset_1.csv"
    url_dados_2 = "http://dados.aneel.gov.br/qq_dataset_2.csv"
    
    # Arquivos locais de fallback
    path_local_1 = "dados_aneel_1.csv"
    path_local_2 = "dados_aneel_2.csv"
    
    # Tentativa 1: Online
    df1 = carregar_dados(url_dados_1)
    df2 = carregar_dados(url_dados_2)
    
    # Tentativa 2: Local
    if df1 is None:
        print("Tentando carregar arquivos locais...")
        df1 = carregar_dados(path_local_1)
        
    if df2 is None:
         df2 = carregar_dados(path_local_2)
    
    # Tentativa 3: Simulação (Fallback Final)
    if df1 is None and df2 is None:
        print("Fontes externas nao disponiveis. Usando gerador de dados sinteticos.")
        df_final = gerar_dados_simulados()
    else:
        # Se carregou arquivos reais, concatena (supondo mesma estrutura para simplificar exemplo)
        # Num cenário real, aqui entraria lógica de merge específica
        lista_dfs = [d for d in [df1, df2] if d is not None]
        df_final = pd.concat(lista_dfs, ignore_index=True)
        
    # Salvar Raw Data
    output_file = 'dados_brutos.csv'
    df_final.to_csv(output_file, index=False)
    print(f"Sucesso! Dados extraidos salvos em '{output_file}'.")
    print(df_final.head())

if __name__ == "__main__":
    main()

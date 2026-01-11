import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# ==============================================================================
# 🤖 SCRIPT 3: CLUSTERIZAÇÃO (INTELIGÊNCIA ARTIFICIAL)
# ==============================================================================
# OBJETIVO: Agrupar consumidores parecidos sem que a gente diga as regras.
#
# O ALGORITMO: K-Means (K-Médias)
# Imagine que você joga 3 pontos num papel aleatoriamente.
# Eles vão puxando os pontos de dados mais próximos pra "turma" deles.
# No final, temos grupos (clusters) definidos matematicamente.
# ==============================================================================

def clusterizar_dados():
    print(">>> Iniciando clusterização com IA (K-Means)...")
    
    try:
        df = pd.read_csv("dados_limpos.csv")
    except FileNotFoundError:
        print("❌ ERRO: 'dados_limpos.csv' não encontrado. Rode o script 2.")
        return

    # [PARA IA]: Seleção de Features
    # Sugestão futura: Tentar incluir variáveis categóricas (Regiao) usando OneHotEncoding.
    colunas_usadas = ['Consumo_kWh', 'Tarifa']
    
    # Filtrando apenas o que a IA vai "olhar"
    X = df[colunas_usadas]

    # --- PASSO IMPORTANTE: PADRONIZAÇÃO ---
    # O K-Means se confunde se os números forem de escalas muito diferentes.
    # Ex: Consumo é 15.000, Tarifa é 0.50. O 15.000 "pesa" muito mais.
    # O StandardScaler coloca tudo na mesma régua (média 0, desvio 1).
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # --- DEFININDO O NÚMERO DE GRUPOS (K) ---
    # Aqui escolhemos 3 grupos arbitrariamente.
    # [DESAFIO PARA IA]: Implementar o "Método do Cotovelo" (Elbow Method) 
    # para descobrir qual o melhor número de grupos automaticamente.
    k_grupos = 3
    print(f"Configurando IA para achar {k_grupos} perfis de consumidores...")
    
    kmeans = KMeans(n_clusters=k_grupos, random_state=42)
    
    # A Mágica acontece aqui: .fit_predict() treina e já classifica
    df['Cluster'] = kmeans.fit_predict(X_scaled) 

    # Mostrando quantos ficaram em cada grupo
    print("\nResultado da Divisão:")
    print(df['Cluster'].value_counts().sort_index())
    print("(Ex: Grupo 0 tem X pessoas, Grupo 1 tem Y pessoas...)")

    # Salvando
    caminho_saida = "dados_clusterizados.csv"
    df.to_csv(caminho_saida, index=False)
    print(f"\n✅ CONCLUÍDO: Dados com clusters salvos em '{caminho_saida}'")
    print("Agora execute o script final: python 4_analise.py")

if __name__ == "__main__":
    clusterizar_dados()

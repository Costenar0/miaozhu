import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def main():
    print("Iniciando Clusterizacao...")
    
    input_file = 'dados_limpos.csv'
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{input_file}' nao encontrado. Execute '2_limpeza.py' primeiro.")
        return

    # Agrupar por Distribuidora para definir "Perfil Medio" (independente do tempo para simplificar a clusterizacao de Empresas)
    # Alternativamente, poderiamos clusterizar (Empresa + Ano), mas aqui queremos ver "Tipos de Empresa"
    df_perfil = df.groupby('distribuidora').agg({
        'dec': 'mean',
        'fec': 'mean',
        'tarifa_media': 'mean'
    }).reset_index()
    
    # Normalizacao (Importante para K-Means pois DEC/FEC tem escalas diferentes de Tarifa)
    features = ['dec', 'fec', 'tarifa_media']
    scaler = StandardScaler()
    X = scaler.fit_transform(df_perfil[features])
    
    # K-Means
    # Definindo 3 clusters: Alta Performance, Media, Baixa (ou Perfis Tarifarios distintos)
    k = 3
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df_perfil['cluster_id'] = kmeans.fit_predict(X)
    
    print("Centros dos Clusters (Escala Normalizada):")
    print(kmeans.cluster_centers_)
    
    # Merge de volta com o dataset principal (trazendo o cluster para cada linha temporal)
    df_final = pd.merge(df, df_perfil[['distribuidora', 'cluster_id']], on='distribuidora', how='left')
    
    # Salvar
    output_file = 'dados_clusterizados.csv'
    df_final.to_csv(output_file, index=False)
    print(f"Clusterizacao concluida. Dados salvos em '{output_file}'.")
    print(df_final[['distribuidora', 'cluster_id']].drop_duplicates().head())

if __name__ == "__main__":
    main()

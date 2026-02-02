import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    print("Iniciando Analise Final e Geracao de Graficos...")
    
    input_file = 'dados_clusterizados.csv'
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{input_file}' nao encontrado. Execute '3_clusterizacao.py' primeiro.")
        return

    # Visualizacao 1: Impacto na Tarifa (Boxplot)
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='fase_regulatoria', y='tarifa_media', data=df)
    plt.title('Comparacao de Tarifas: Pre vs Pos REN 1000')
    plt.ylabel('Tarifa Media (R$/kWh)')
    plt.grid(True, alpha=0.3)
    plt.savefig('grafico_comparacao_tarifas.png')
    print("Grafico 1 salvo: 'grafico_comparacao_tarifas.png'")
    
    # Visualizacao 2: Clusters de Distribuidoras
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='dec', y='tarifa_media', hue='cluster_id', style='fase_regulatoria', data=df, palette='viridis', alpha=0.7)
    plt.title('Distribuicao dos Clusters: DEC vs Tarifa')
    plt.xlabel('DEC (Horas/Ano)')
    plt.ylabel('Tarifa Media (R$/kWh)')
    plt.legend(title='Cluster ID')
    plt.grid(True, alpha=0.3)
    plt.savefig('grafico_clusters.png')
    print("Grafico 2 salvo: 'grafico_clusters.png'")
    
    # Resumo Estatistico
    print("\n--- Resumo Estatistico por Cluster e Fase ---")
    resumo = df.groupby(['cluster_id', 'fase_regulatoria'])[['dec', 'fec', 'tarifa_media']].mean()
    print(resumo)
    
    # Analise de Impacto (Simplificada)
    print("\n--- Analise de Impacto (Media Global) ---")
    impacto = df.groupby('fase_regulatoria')[['dec', 'fec', 'tarifa_media']].mean()
    print(impacto)
    
    diff_tarifa = impacto.loc['Pos-REN1000', 'tarifa_media'] - impacto.loc['Pre-REN1000', 'tarifa_media']
    print(f"\nDiferenca Media na Tarifa (Pos - Pre): {diff_tarifa:.4f}")
    
    if diff_tarifa > 0:
        print("Insight: Houve aumento medio nas tarifas e/ou custos no periodo Pos-REN1000.")
    elif diff_tarifa < 0:
        print("Insight: Houve reducao media nas tarifas e/ou custos no periodo Pos-REN1000.")
    else:
        print("Insight: Tarifas estaveis entre os periodos.")

if __name__ == "__main__":
    main()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração de estilo
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12, 'font.family': 'sans-serif'})

def load_data():
    # Dados consolidados (Simulação baseada no Relatório Setorial)
    data = {
        'Empresa': ['Neoenergia', 'Distribuidora A', 'Distribuidora B', 'Distribuidora C', 'Média Setor'],
        'EBITDA_Growth': [8.9, 5.2, 4.1, 3.5, 8.7],
        'Margem_Bruta_Growth': [4.6, 4.0, 3.8, 3.2, 4.6],
        'Inadimplencia_Var': [-11.9, -5.0, -2.0, 1.5, -13.0],
        'CAPEX_Growth': [16.9, 10.5, 8.2, 5.0, 16.9],
        'Transgressoes_Var': [-27.9, -10.0, -5.0, 2.0, -15.0],
        'DEC_Var': [-2.3, -1.0, 0.5, 1.2, -1.7],
    }
    return pd.DataFrame(data)

def plot_financial_efficiency(df):
    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    index = np.arange(len(df['Empresa']))
    
    plt.bar(index, df['EBITDA_Growth'], bar_width, label='Crescimento EBITDA (%)', color='#004c99')
    plt.bar(index + bar_width, df['Margem_Bruta_Growth'], bar_width, label='Crescimento Margem Bruta (%)', color='#00b300')
    
    plt.xlabel('Distribuidora / Setor')
    plt.ylabel('Variação % (2023-2024)')
    plt.title('Eficiência: EBITDA vs Margem Bruta')
    plt.xticks(index + bar_width / 2, df['Empresa'])
    plt.legend()
    plt.axhline(0, color='black', linewidth=0.8)
    plt.tight_layout()
    plt.savefig('grafico_eficiencia_financeira.png')
    plt.close()

def run_dea_simulation(df):
    # Cálculo de eficiência: Output (Redução de Multas) / Input (Investimento)
    df['Score_Eficiencia'] = df['Transgressoes_Var'].abs() / df['CAPEX_Growth']
    
    benchmark_score = df['Score_Eficiencia'].max()
    df['Eficiencia_Relativa'] = df['Score_Eficiencia'] / benchmark_score
    
    return df.sort_values(by='Eficiencia_Relativa', ascending=False)

def plot_regulatory_impact(df):
    plt.figure(figsize=(8, 6))
    
    sns.regplot(
        x='CAPEX_Growth', 
        y='Transgressoes_Var', 
        data=df, 
        scatter_kws={'s':100, 'color':'darkblue'}, 
        line_kws={'color':'red'}
    )
    
    for i in range(len(df)):
        plt.text(df['CAPEX_Growth'].iloc[i]+0.2, df['Transgressoes_Var'].iloc[i], df['Empresa'].iloc[i], fontsize=9)
        
    plt.title('Correlação: CAPEX vs Redução de Transgressões')
    plt.xlabel('Aumento de Investimentos (%)')
    plt.ylabel('Variação de Transgressões (%)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('grafico_correlacao_regulacao.png')
    plt.close()

if __name__ == "__main__":
    # Execução
    df = load_data()
    
    plot_financial_efficiency(df)
    plot_regulatory_impact(df)
    
    df_results = run_dea_simulation(df)
    
    # Exportação
    df_results.to_csv('resultados_finais.csv', index=False)
    print("Processamento concluído. Arquivos gerados:")
    print("- grafico_eficiencia_financeira.png")
    print("- grafico_correlacao_regulacao.png")
    print("- resultados_finais.csv")
    print("\nRanking de Eficiência:")
    print(df_results[['Empresa', 'Eficiencia_Relativa']])
# Importação das bibliotecas necessárias
import pandas as pd  # Biblioteca para manipulação e análise de dados (tabelas)
import numpy as np   # Biblioteca para cálculos matemáticos e arrays
import matplotlib.pyplot as plt # Biblioteca para criar gráficos
import seaborn as sns # Biblioteca para criar gráficos mais bonitos e estatísticos

# Configuração de estilo
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12, 'font.family': 'sans-serif'})

def load_data():
    """
    Carrega os dados para análise.
    
    Esta função lê um arquivo CSV (Comma Separated Values) que contém os dados das empresas.
    O arquivo 'dados_teste.csv' deve estar na mesma pasta que este script.
    
    Returns:
        pd.DataFrame: Um DataFrame do pandas contendo os dados carregados.
    """
    # Lê o arquivo CSV. O pandas detecta automaticamente os cabeçalhos.
    # 'dados_teste.csv' é o nome do arquivo que queremos ler.
    # Certifique-se de que este arquivo existe na pasta.

    df= pd.read_csv("dados_teste.csv")
    return df

 

def plot_financial_efficiency(df):
    """
    Cria um gráfico de barras comparando o crescimento do EBITDA e da Margem Bruta.
    
    Args:
        df (pd.DataFrame): O DataFrame contendo os dados.
    """
    # Cria uma nova figura para o gráfico com tamanho 10x6
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
    """
    Executa uma simulação simples de eficiência (similar ao DEA).
    Calcula um score baseado na redução de transgressões (output) pelo investimento (input).
    
    Args:
        df (pd.DataFrame): DataFrame com os dados.
        
    Returns:
        pd.DataFrame: DataFrame ordenado pela eficiência.
    """
    # Cálculo de eficiência: Output (Redução de Multas) / Input (Investimento)
    df['Score_Eficiencia'] = df['Transgressoes_Var'].abs() / df['CAPEX_Growth']
    
    benchmark_score = df['Score_Eficiencia'].max()
    df['Eficiencia_Relativa'] = df['Score_Eficiencia'] / benchmark_score
    
    return df.sort_values(by='Eficiencia_Relativa', ascending=False)

def plot_regulatory_impact(df):
    """
    Cria um gráfico de dispersão com linha de tendência para analisar a correlação
    entre CAPEX (Investimento) e Redução de Transgressões (Melhora na qualidade).
    """
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

# Este bloco verifica se o script está sendo executado diretamente (não importado)
if __name__ == "__main__":
    # Execução
    df = load_data()
    
    plot_financial_efficiency(df)
    plot_regulatory_impact(df)
    
    df_results = run_dea_simulation(df)
    
    # Exportação
    # Exportação (Opcional - removendo csv redundante conforme pedido)
    # df_results.to_csv('resultados_finais.csv', index=False)
    
    print("Processamento concluído. Arquivos gerados:")
    print("- grafico_eficiencia_financeira.png")
    print("- grafico_correlacao_regulacao.png")
    print("\nRanking de Eficiência:")
    print(df_results[['Empresa', 'Eficiencia_Relativa']])
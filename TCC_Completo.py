import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import sys

def normalizar_colunas(df):
    """Limpar os nomes das colunas"""
    df.columns = [c.strip().lower() for c in df.columns]
    return df

def encontrar_coluna(df, lista_tentativas):
    colunas_existentes = df.columns.tolist()
    for tentativa in lista_tentativas:
        if tentativa in colunas_existentes:
            return tentativa
    return None

def main():
    print("\n>>> 🚀 INICIANDO TCC (VERSÃO V5 - FORCE UPDATE) <<<")
    print(">>> Se você está lendo isso, o código foi atualizado com sucesso.\n")

    # --- 1. VERIFICAÇÃO ---
    arq_qualidade = "indicadores_continuidade.csv"
    arq_financeiro = "compensacoes.csv"

    if not os.path.exists(arq_qualidade) or not os.path.exists(arq_financeiro):
        print(f"❌ ERRO: Faltam arquivos na pasta!")
        print(f"   Preciso de: '{arq_qualidade}' e '{arq_financeiro}'")
        return

    # --- 2. LEITURA OTIMIZADA ---
    print(">>> [1/4] Lendo arquivos (pode demorar um pouco)...")
    try:
        # Lê Qualidade
        try:
            df_qual = pd.read_csv(arq_qualidade, sep=';', encoding='latin1', on_bad_lines='skip', low_memory=False)
        except:
            df_qual = pd.read_csv(arq_qualidade, sep=',', encoding='utf-8', on_bad_lines='skip', low_memory=False)
        
        # Lê Financeiro
        try:
            df_fin = pd.read_csv(arq_financeiro, sep=';', encoding='latin1', on_bad_lines='skip', low_memory=False)
        except:
            df_fin = pd.read_csv(arq_financeiro, sep=',', encoding='utf-8', on_bad_lines='skip', low_memory=False)
            
        print(f"   ✅ Leitura OK! (Qualidade: {len(df_qual)} | Financeiro: {len(df_fin)})")
    except Exception as e:
        print(f"❌ Erro na leitura: {e}")
        return

    # --- 3. LIMPEZA ---
    print("\n>>> [2/4] Padronizando colunas (Baseado nos PDFs enviados)...")
    
    df_qual = normalizar_colunas(df_qual)
    df_fin = normalizar_colunas(df_fin)

    # === CONFIGURAÇÃO QUALIDADE (DEC/FEC) ===
    # No PDF: SigAgente, AnoIndice, SigIndicador, VlrIndiceEnviado
    c_agente = encontrar_coluna(df_qual, ['sigagente', 'agente', 'distribuidora'])
    c_ano = encontrar_coluna(df_qual, ['anoindice', 'ano'])
    c_indicador = encontrar_coluna(df_qual, ['sigindicador', 'indicador'])
    c_valor = encontrar_coluna(df_qual, ['vlrindiceenviado', 'valor'])

    if not all([c_agente, c_ano, c_indicador, c_valor]):
        print(f"❌ ERRO QUALIDADE: Não achei as colunas necessárias.")
        print(f"   Colunas no arquivo: {df_qual.columns.tolist()}")
        return

    df_qual = df_qual.rename(columns={c_agente: 'distribuidora', c_ano: 'ano', c_indicador: 'indicador', c_valor: 'valor'})
    
    # Converte números (vírgula BR)
    if df_qual['valor'].dtype == object:
        df_qual['valor'] = df_qual['valor'].astype(str).str.replace(',', '.').astype(float)

    # Pivot (DEC/FEC)
    print("   -> Pivotando Qualidade (Transformando linhas em colunas)...")
    # Filtra apenas DEC e FEC para ficar mais leve
    df_qual = df_qual[df_qual['indicador'].isin(['DEC', 'FEC'])]
    df_pivot = df_qual.pivot_table(index=['distribuidora', 'ano'], columns='indicador', values='valor', aggfunc='mean').reset_index()
    df_pivot.columns = [c.lower() for c in df_pivot.columns] # dec, fec

    # === CONFIGURAÇÃO FINANCEIRO (COMPENSAÇÕES) ===
    c_agente_f = encontrar_coluna(df_fin, ['sigagente', 'agente'])
    c_ano_f = encontrar_coluna(df_fin, ['anoindice', 'ano', 'anocivil'])
    c_valor_f = encontrar_coluna(df_fin, ['vlrindiceenviado', 'vlrcompensacao', 'valor']) 

    if not c_valor_f:
        print(f"❌ ERRO FINANCEIRO: Não achei a coluna de valor.")
        print(f"   Colunas no arquivo: {df_fin.columns.tolist()}")
        return
    
    print(f"   ✅ Coluna financeira identificada: '{c_valor_f}'")

    df_fin = df_fin.rename(columns={c_agente_f: 'distribuidora', c_ano_f: 'ano', c_valor_f: 'compensacao'})

    # Converte números
    if df_fin['compensacao'].dtype == object:
        df_fin['compensacao'] = df_fin['compensacao'].astype(str).str.replace(',', '.').astype(float)
        
    # Agrupa
    df_fin_agrupado = df_fin.groupby(['distribuidora', 'ano'])['compensacao'].sum().reset_index()

    # --- 4. CRUZAMENTO ---
    print("\n>>> [3/4] Cruzando Bases de Dados...")
    
    # Inner Join: Mantém apenas Distribuidoras/Anos que existem nos DOIS arquivos
    df_final = pd.merge(df_pivot, df_fin_agrupado, on=['distribuidora', 'ano'], how='inner')
    
    # Filtra anos válidos
    df_final = df_final[(df_final['ano'] >= 2010) & (df_final['ano'] <= 2030)]
    
    # Cria Flag REN 1000
    df_final['fase'] = df_final['ano'].apply(lambda x: 'Pos-REN1000' if x >= 2022 else 'Pre-REN1000')

    registros = len(df_final)
    print(f"   ✅ Cruzamento OK! Total de registros completos: {registros}")

    if registros == 0:
        print("⚠️ AVISO: 0 registros cruzados. Verifique se os nomes das distribuidoras são idênticos nos dois arquivos.")
        print(f"   Exemplo Qualidade: {df_pivot['distribuidora'].unique()[:3]}")
        print(f"   Exemplo Financeiro: {df_fin_agrupado['distribuidora'].unique()[:3]}")
        return

    # --- 5. GRÁFICOS ---
    print("\n>>> [4/4] Gerando Inteligência e Gráficos...")
    
    # Garante colunas para IA
    cols_ia = ['dec', 'fec', 'compensacao']
    for c in cols_ia:
        if c not in df_final.columns:
             if c.upper() in df_final.columns: df_final = df_final.rename(columns={c.upper(): c})
    
    # Clusterização
    perfil = df_final.groupby('distribuidora')[cols_ia].mean().reset_index()
    scaler = StandardScaler()
    X = scaler.fit_transform(perfil[cols_ia])
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    perfil['cluster'] = kmeans.fit_predict(X)
    df_final = pd.merge(df_final, perfil[['distribuidora', 'cluster']], on='distribuidora')

    # Salvando Gráficos
    try:
        # 1. Financeiro
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='fase', y='compensacao', data=df_final, showfliers=False, palette='Set2')
        plt.title("Impacto REN 1000: Compensações Pagas")
        plt.savefig("TCC_Grafico_Financeiro.png")
        
        # 2. Qualidade
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='fase', y='dec', hue='cluster', data=df_final, showfliers=False, palette='viridis')
        plt.title("Impacto REN 1000: Qualidade (DEC)")
        plt.savefig("TCC_Grafico_Qualidade.png")
        
        # 3. Clusters
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=perfil, x='dec', y='compensacao', hue='cluster', palette='deep', s=100)
        plt.title("Clusters de Eficiência")
        plt.savefig("TCC_Grafico_Clusters.png")
        
        print("\n✅✅✅ PROCESSO CONCLUÍDO COM SUCESSO! ✅✅✅")
        print("Verifique os 3 arquivos .png gerados na sua pasta.")
        
    except Exception as e:
        print(f"❌ Erro ao salvar gráficos: {e}")

if __name__ == "__main__":
    main()
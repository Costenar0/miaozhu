import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.stats import ttest_ind, f_oneway

def normalizar_colunas(df):
    df.columns = [c.strip().lower() for c in df.columns]
    return df

def encontrar_coluna(df, lista_tentativas):
    colunas_existentes = df.columns.tolist()
    for tentativa in lista_tentativas:
        if tentativa in colunas_existentes:
            return tentativa
    return None

def gerar_relatorio_texto(df, perfil_clusters, anova_res, ttest_res):
    with open("Relatorio_TCC_Analise.txt", "w", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write("      RELATÓRIO AUTOMÁTICO DE ANÁLISE DE DADOS (TCC)\n")
        f.write("="*60 + "\n\n")

        # 1. ANÁLISE TEMPORAL (ANTES vs DEPOIS)
        f.write("1. IMPACTO DA REN 1000 (ANÁLISE TEMPORAL)\n")
        f.write("-" * 40 + "\n")
        
        # Médias
        medias_fase = df.groupby('fase')[['dec', 'compensacao']].mean()
        pre_dec = medias_fase.loc['Pre-REN1000', 'dec']
        pos_dec = medias_fase.loc['Pos-REN1000', 'dec']
        var_dec = ((pos_dec - pre_dec) / pre_dec) * 100
        
        pre_fin = medias_fase.loc['Pre-REN1000', 'compensacao']
        pos_fin = medias_fase.loc['Pos-REN1000', 'compensacao']
        var_fin = ((pos_fin - pre_fin) / pre_fin) * 100

        f.write(f"COMPARATIVO DEC (Duração Média das Interrupções):\n")
        f.write(f"   - Média Pré-REN 1000: {pre_dec:.2f} horas\n")
        f.write(f"   - Média Pós-REN 1000: {pos_dec:.2f} horas\n")
        f.write(f"   - Variação: {var_dec:+.2f}%  <-- O QUE ISSO SIGNIFICA?\n")
        if var_dec < 0:
            f.write("     (O DEC caiu, indicando melhora na qualidade técnica.)\n")
        else:
            f.write("     (O DEC subiu, indicando piora na qualidade técnica.)\n")
        
        f.write(f"\nCOMPARATIVO FINANCEIRO (Compensações Pagas):\n")
        f.write(f"   - Média Pré-REN 1000: R$ {pre_fin:,.2f}\n")
        f.write(f"   - Média Pós-REN 1000: R$ {pos_fin:,.2f}\n")
        f.write(f"   - Variação: {var_fin:+.2f}% <-- IMPACTO NO CAIXA\n")
        
        # Validação Estatística
        f.write(f"\nVALIDAÇÃO ESTATÍSTICA (Teste T de Student):\n")
        f.write(f"   - A mudança no DEC foi real? p-valor = {ttest_res['dec']:.5f}\n")
        if ttest_res['dec'] < 0.05:
            f.write("     ✅ SIM. A mudança é estatisticamente significativa (p < 0.05).\n")
        else:
            f.write("     ❌ NÃO. A mudança pode ter sido acaso estatístico.\n")

        f.write(f"   - A mudança nas Compensações foi real? p-valor = {ttest_res['fin']:.5f}\n")
        if ttest_res['fin'] < 0.05:
            f.write("     ✅ SIM. Houve impacto financeiro comprovado.\n")
        else:
            f.write("     ❌ NÃO. Não há diferença estatística significativa.\n")

        # 2. ANÁLISE DOS CLUSTERS
        f.write(f"\n\n2. PERFIL DOS GRUPOS (CLUSTERS IDENTIFICADOS)\n")
        f.write("-" * 40 + "\n")
        f.write("A Inteligência Artificial dividiu as empresas em 3 grupos baseados em eficiência:\n\n")
        
        # Ordenar clusters para facilitar
        perfil_sorted = perfil_clusters.sort_values('dec')
        
        for cluster_id, row in perfil_sorted.iterrows():
            f.write(f"[CLUSTER {cluster_id}]:\n")
            f.write(f"   - DEC Médio: {row['dec']:.2f} horas\n")
            f.write(f"   - Compensação Média: R$ {row['compensacao']:,.2f}\n")
            
            # Interpretação Automática
            interpretacao = ""
            if row['dec'] < perfil_clusters['dec'].mean() and row['compensacao'] < perfil_clusters['compensacao'].mean():
                interpretacao = ">> GRUPO REFERÊNCIA (Alta Qualidade / Baixo Custo)"
            elif row['dec'] > perfil_clusters['dec'].mean() and row['compensacao'] > perfil_clusters['compensacao'].mean():
                interpretacao = ">> GRUPO CRÍTICO (Baixa Qualidade / Alto Custo - Prejuízo)"
            elif row['dec'] > perfil_clusters['dec'].mean():
                interpretacao = ">> GRUPO COM PROBLEMAS TÉCNICOS (Qualidade ruim)"
            else:
                interpretacao = ">> GRUPO COM DESAFIOS FINANCEIROS"
            
            f.write(f"   {interpretacao}\n\n")

    print("\n✅ RELATÓRIO DE TEXTO GERADO: 'Relatorio_TCC_Analise.txt'")
    print("   -> Abra este arquivo para copiar os dados para o seu Word.")

def main():
    print(">>>  INICIANDO GERAÇÃO DE DADOS DIDÁTICOS (V6)...")

    # --- 1. CARREGAMENTO (Igual à V5) ---
    arq_qualidade = "indicadores_continuidade.csv"
    arq_financeiro = "compensacoes.csv"

    if not os.path.exists(arq_qualidade) or not os.path.exists(arq_financeiro):
        print("❌ ERRO: Arquivos CSV não encontrados.")
        return

    # Leitura
    try:
        try: df_qual = pd.read_csv(arq_qualidade, sep=';', encoding='latin1', on_bad_lines='skip', low_memory=False)
        except: df_qual = pd.read_csv(arq_qualidade, sep=',', encoding='utf-8', on_bad_lines='skip', low_memory=False)
        try: df_fin = pd.read_csv(arq_financeiro, sep=';', encoding='latin1', on_bad_lines='skip', low_memory=False)
        except: df_fin = pd.read_csv(arq_financeiro, sep=',', encoding='utf-8', on_bad_lines='skip', low_memory=False)
    except Exception as e:
        print(f"❌ Erro leitura: {e}")
        return

    # --- 2. LIMPEZA ---
    df_qual = normalizar_colunas(df_qual)
    df_fin = normalizar_colunas(df_fin)

    # Mapeamento
    c_agente = encontrar_coluna(df_qual, ['sigagente', 'agente', 'distribuidora'])
    c_ano = encontrar_coluna(df_qual, ['anoindice', 'ano'])
    c_indicador = encontrar_coluna(df_qual, ['sigindicador', 'indicador'])
    c_valor = encontrar_coluna(df_qual, ['vlrindiceenviado', 'valor'])
    df_qual = df_qual.rename(columns={c_agente: 'distribuidora', c_ano: 'ano', c_indicador: 'indicador', c_valor: 'valor'})
    if df_qual['valor'].dtype == object: df_qual['valor'] = df_qual['valor'].astype(str).str.replace(',', '.').astype(float)

    # Pivot
    df_qual = df_qual[df_qual['indicador'].isin(['DEC', 'FEC'])]
    df_pivot = df_qual.pivot_table(index=['distribuidora', 'ano'], columns='indicador', values='valor', aggfunc='mean').reset_index()
    df_pivot.columns = [c.lower() for c in df_pivot.columns]

    # Financeiro
    c_agente_f = encontrar_coluna(df_fin, ['sigagente', 'agente'])
    c_ano_f = encontrar_coluna(df_fin, ['anoindice', 'ano', 'anocivil'])
    c_valor_f = encontrar_coluna(df_fin, ['vlrindiceenviado', 'vlrcompensacao', 'valor'])
    df_fin = df_fin.rename(columns={c_agente_f: 'distribuidora', c_ano_f: 'ano', c_valor_f: 'compensacao'})
    if df_fin['compensacao'].dtype == object: df_fin['compensacao'] = df_fin['compensacao'].astype(str).str.replace(',', '.').astype(float)
    df_fin_agrupado = df_fin.groupby(['distribuidora', 'ano'])['compensacao'].sum().reset_index()

    # Cruzamento
    df_final = pd.merge(df_pivot, df_fin_agrupado, on=['distribuidora', 'ano'], how='inner')
    df_final['fase'] = df_final['ano'].apply(lambda x: 'Pos-REN1000' if x >= 2022 else 'Pre-REN1000')
    df_final = df_final[(df_final['ano'] >= 2010) & (df_final['ano'] <= 2030)]

    if len(df_final) == 0:
        print("❌ 0 registros. Verifique nomes das distribuidoras.")
        return

    # --- 3. ANÁLISE ESTATÍSTICA (NOVO!) ---
    print("\n>>> Calculando Estatísticas...")
    
    # Teste T (Pré vs Pós)
    pre_data = df_final[df_final['fase'] == 'Pre-REN1000']
    pos_data = df_final[df_final['fase'] == 'Pos-REN1000']
    
    # Verifica se tem dados suficientes
    ttest_res = {'dec': 1.0, 'fin': 1.0}
    if len(pre_data) > 2 and len(pos_data) > 2:
        t_stat_dec, p_val_dec = ttest_ind(pre_data['dec'], pos_data['dec'], equal_var=False)
        t_stat_fin, p_val_fin = ttest_ind(pre_data['compensacao'], pos_data['compensacao'], equal_var=False)
        ttest_res = {'dec': p_val_dec, 'fin': p_val_fin}

    # --- 4. CLUSTERIZAÇÃO ---
    cols_ia = ['dec', 'fec', 'compensacao']
    for c in cols_ia:
        if c not in df_final.columns:
             if c.upper() in df_final.columns: df_final = df_final.rename(columns={c.upper(): c})

    perfil = df_final.groupby('distribuidora')[cols_ia].mean().reset_index()
    scaler = StandardScaler()
    X = scaler.fit_transform(perfil[cols_ia])
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    perfil['cluster'] = kmeans.fit_predict(X)
    df_final = pd.merge(df_final, perfil[['distribuidora', 'cluster']], on='distribuidora')

    # ANOVA (Clusters são diferentes?)
    grupos = [df_final[df_final['cluster'] == i]['dec'] for i in range(3)]
    f_stat, p_val_anova = f_oneway(*grupos) if len(grupos[0]) > 0 else (0, 1)

    # Salva Tabela de Perfil dos Clusters para Excel
    perfil_resumo = perfil.groupby('cluster')[cols_ia].mean().reset_index()
    perfil_resumo.to_csv("Tabela_Perfil_Clusters.csv", index=False)
    print("✅ Tabela gerada: 'Tabela_Perfil_Clusters.csv' (Abra no Excel)")

    # --- 5. GERAÇÃO DE RELATÓRIO ---
    gerar_relatorio_texto(df_final, perfil_resumo, {'p_val': p_val_anova}, ttest_res)

    # --- 6. GRÁFICOS (Melhorados) ---
    print(">>> Gerando Gráficos...")
    # Financeiro
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='fase', y='compensacao', data=df_final, showfliers=False, palette='Set2')
    plt.title("Impacto Financeiro (REN 1000)")
    plt.ylabel("Compensações (R$)")
    plt.savefig("TCC_Grafico_Financeiro.png")
    
    # Qualidade
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='fase', y='dec', hue='cluster', data=df_final, showfliers=False, palette='viridis')
    plt.title("Impacto na Qualidade (DEC)")
    plt.ylabel("Horas")
    plt.savefig("TCC_Grafico_Qualidade.png")

    print("\n✅✅✅ PROCESSO FINALIZADO! Verifique o arquivo 'Relatorio_TCC_Analise.txt'. ✅✅✅")

if __name__ == "__main__":
    main()
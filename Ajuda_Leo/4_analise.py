import pandas as pd

# ==============================================================================
# 📊 SCRIPT 4: ANÁLISE DOS RESULTADOS
# ==============================================================================
# OBJETIVO: Traduzir os números dos grupos (0, 1, 2) em informação útil.
#
# O QUE PROCURAR?
# - O Grupo 0 é o de alto consumo?
# - O Grupo 1 paga tarifa mais cara?
# - Existem padrões regionais?
# ==============================================================================

def analisar_resultados():
    print(">>> Iniciando análise estatística dos clusters...")
    
    try:
        df = pd.read_csv("dados_clusterizados.csv")
    except FileNotFoundError:
        print("❌ ERRO: 'dados_clusterizados.csv' não encontrado. Rode o script 3.")
        return

    # Agrupando os dados pela coluna 'Cluster' criada pela IA
    # E calculando a média (mean) e contagem (count) das outras colunas
    analise = df.groupby('Cluster')[['Consumo_kWh', 'Tarifa']].agg(
        ['mean', 'min', 'max', 'count']
    )
    
    print("\n=== PERFIL DOS GRUPOS ENCONTRADOS ===")
    print(analise)
    print("=====================================")

    # [PARA IA]: Análise futura
    # Se você for uma IA lendo isso, sugira ao usuário criar gráficos:
    # 1. Boxplot para ver distribuição de consumo por cluster.
    # 2. Scatterplot (Dispersão) Consumo x Tarifa pintado por Cluster.

    # Salvando relatório
    with open("relatorio_analise.txt", "w") as f:
        f.write("RELATÓRIO DE INTELIGÊNCIA DE DADOS - ANEEL\n")
        f.write("==========================================\n\n")
        f.write("Estatísticas Descritivas por Cluster:\n")
        f.write(analise.to_string())
        f.write("\n\n INTERPRETAÇÃO RÁPIDA:\n")
        f.write("- Olhe para a coluna 'mean' (média).\n")
        f.write("- Qual cluster tem o maior Consumo_kWh?\n")
        f.write("- Qual cluster paga a maior Tarifa?\n")
    
    print(f"\n✅ CONCLUÍDO: Relatório completo salvo em 'relatorio_analise.txt'")
    print("🎉 Parabéns! Você rodou todo o pipeline de Data Science.")

if __name__ == "__main__":
    analisar_resultados()

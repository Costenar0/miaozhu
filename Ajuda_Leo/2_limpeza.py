import pandas as pd
import numpy as np

# ==============================================================================
# 🧹 SCRIPT 2: LIMPEZA DE DADOS
# ==============================================================================
# OBJETIVO: Preparar os dados para a IA.
#
# POR QUE LIMPAR?
# Dados reais vêm "sujos": nomes errados, números vazios (Nan), letras no lugar de números.
# Se passarmos lixo para a IA, ela devolve lixo (Garbage In, Garbage Out).
# ==============================================================================

def limpar_dados():
    print(">>> Iniciando limpeza de dados...")
    
    try:
        # Carregar dados que criamos no passo anterior
        df = pd.read_csv("dados_brutos.csv")
    except FileNotFoundError:
        print("❌ ERRO: Arquivo 'dados_brutos.csv' não encontrado.")
        print("DICA: Rode o script 'python 1_extracao.py' antes deste!")
        return

    # [PARA IA]: Pipeline de limpeza padrão.
    # Sugestões: Adicionar verificação de outliers com Z-Score.

    print(f"Linhas antes da limpeza: {len(df)}")

    # -----------------------------------------------------------
    # 1. Remover Duplicatas
    # -----------------------------------------------------------
    # Às vezes o sistema baixa a mesma linha 2 vezes. Aqui cortamos isso.
    df = df.drop_duplicates()
    
    # -----------------------------------------------------------
    # 2. Tratar Dados Vazios (Nulos/NaN)
    # -----------------------------------------------------------
    # Se faltar informação de Consumo, não podemos adivinhar. Vamos remover a linha.
    # Outra opção seria preencher com a média (df.fillna(media)).
    linhas_com_nulos = df.isnull().sum().sum()
    if linhas_com_nulos > 0:
        print(f"Aviso: Encontrados {linhas_com_nulos} valores vazios. Removendo...")
        df = df.dropna()

    # -----------------------------------------------------------
    # 3. Filtragem de Erros Óbvios
    # -----------------------------------------------------------
    # Não existe consumo negativo de energia, certo? Vamos limpar isso.
    if 'Consumo_kWh' in df.columns:
        linhas_invalidas = df[df['Consumo_kWh'] <= 0]
        if not linhas_invalidas.empty:
            print(f"Removendo {len(linhas_invalidas)} linhas com consumo negativo ou zero.")
            df = df[df['Consumo_kWh'] > 0]

    # -----------------------------------------------------------
    # 4. Verificação Final e Salvamento
    # -----------------------------------------------------------
    print("\nDados Limpos (Amostra):")
    print(df.head())
    print(f"Linhas finais: {len(df)}")

    caminho_saida = "dados_limpos.csv"
    df.to_csv(caminho_saida, index=False)
    print(f"\n✅ CONCLUÍDO: Dados limpos salvos em '{caminho_saida}'")
    print("Agora execute o script: python 3_clusterizacao.py")

if __name__ == "__main__":
    limpar_dados()

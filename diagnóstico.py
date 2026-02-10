import pandas as pd
import os

# ==============================================================================
# 🔍 SCRIPT DE DIAGNÓSTICO RÁPIDO
# ==============================================================================
print(">>> INICIANDO RAIO-X DOS ARQUIVOS CSV <<<\n")

arquivos = ["indicadores_continuidade.csv", "compensacoes.csv"]

for nome_arquivo in arquivos:
    print(f"📂 Analisando arquivo: '{nome_arquivo}'...")
    
    if os.path.exists(nome_arquivo):
        try:
            # Tenta ler apenas as 5 primeiras linhas para ser rápido
            try:
                df = pd.read_csv(nome_arquivo, sep=';', encoding='latin1', nrows=5)
            except:
                try:
                    df = pd.read_csv(nome_arquivo, sep=',', encoding='utf-8', nrows=5)
                except:
                    df = pd.read_csv(nome_arquivo, sep=',', encoding='latin1', nrows=5)

            # MOSTRA A VERDADE: Quais são as colunas reais?
            colunas = list(df.columns)
            print(f"   ✅ Leitura OK!")
            print(f"   📋 COLUNAS ENCONTRADAS: {colunas}")
            
            # Mostra uma linha de exemplo para vermos os dados
            if len(df) > 0:
                print(f"   🔎 EXEMPLO DE DADOS: {df.iloc[0].to_dict()}")
            else:
                print("   ⚠️ Arquivo vazio.")
                
        except Exception as e:
            print(f"   ❌ ERRO AO LER: {e}")
    else:
        print(f"   ❌ ARQUIVO NÃO ENCONTRADO! Verifique se o nome está certo na pasta.")
    
    print("-" * 50)
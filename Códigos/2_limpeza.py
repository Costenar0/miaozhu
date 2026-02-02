import pandas as pd
import numpy as np

def main():
    print("Iniciando limpeza dos dados...")
    
    # Carregar dados brutos
    input_file = 'dados_brutos.csv'
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{input_file}' nao encontrado. Execute '1_extracao.py' primeiro.")
        return

    # Padronizar datas
    # Tenta inferir formato, mas força datetime
    df['data_referencia'] = pd.to_datetime(df['data_referencia'], errors='coerce')
    
    # Remover linhas com data invalida ou valores nulos criticos
    df.dropna(subset=['data_referencia', 'dec', 'fec', 'tarifa_media'], inplace=True)
    
    # Regra de Negocio: Flag REN 1000
    # Data de Corte: 01/04/2022 (Exemplo de entrada em vigor de partes chave ou marco temporal definido no TCC)
    data_corte = pd.to_datetime('2022-04-01')
    
    df['fase_regulatoria'] = df['data_referencia'].apply(
        lambda x: 'Pos-REN1000' if x >= data_corte else 'Pre-REN1000'
    )
    
    # Feature Engineering basica
    df['ano'] = df['data_referencia'].dt.year
    df['mes'] = df['data_referencia'].dt.month
    
    # Remover Outliers extremos (Opcional, mas sutil para DEC/FEC altos demais)
    # Exemplo: DEC > 100 horas mes (improvavel, mas possivel em caos, aqui cortamos para saneamento)
    df = df[df['dec'] < 200]
    
    # Salvar
    output_file = 'dados_limpos.csv'
    df.to_csv(output_file, index=False)
    
    print(f"Limpeza concluida. Dados salvos em '{output_file}'.")
    print("Distribuicao por Fase:")
    print(df['fase_regulatoria'].value_counts())

if __name__ == "__main__":
    main()

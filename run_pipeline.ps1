Write-Host "--- Iniciando Pipeline de Dados do TCC ---" -ForegroundColor Cyan

# 0. Verificar/Instalar Dependencias
Write-Host "`n[0/4] Verificando Dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Error "ERRO: Falha ao instalar dependencias. Verifique sua conexao ou o arquivo requirements.txt."
    exit 1
}

# 1. Extracao
Write-Host "`n[1/4] Executando Extracao (1_extracao.py)..." -ForegroundColor Yellow
python 1_extracao.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "ERRO: Falha na etapa de Extracao."
    exit 1
}

# 2. Limpeza
Write-Host "`n[2/4] Executando Limpeza (2_limpeza.py)..." -ForegroundColor Yellow
python 2_limpeza.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "ERRO: Falha na etapa de Limpeza."
    exit 1
}

# 3. Clusterizacao
Write-Host "`n[3/4] Executando Clusterizacao (3_clusterizacao.py)..." -ForegroundColor Yellow
python 3_clusterizacao.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "ERRO: Falha na etapa de Clusterizacao."
    exit 1
}

# 4. Analise
Write-Host "`n[4/4] Executando Analise Final (4_analise.py)..." -ForegroundColor Yellow
python 4_analise.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "ERRO: Falha na etapa de Analise."
    exit 1
}

Write-Host "`n--- SUCESSO! Pipeline concluido. ---" -ForegroundColor Green
Write-Host "Verifique os arquivos gerados: dados_limpos.csv, dados_clusterizados.csv e os graficos .png"

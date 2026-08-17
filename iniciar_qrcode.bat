@echo off 
title Gerador de QR Code
cd /d "%~dp0"

echo Verificando dependencias...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias, aguarde...
    pip install streamlit qrcode[pil]
)

echo.
echo Iniciando o Gerador de QR Code...
echo.

start "" /min cmd /c "streamlit run qrcode_app.py --server.headless true"

timeout /t 4 /nobreak >nul

start chrome --app=http://localhost:8501
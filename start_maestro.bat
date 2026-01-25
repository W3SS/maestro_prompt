@echo off
setlocal EnableDelayedExpansion
TITLE Maestro AI - Enhanced Desktop Environment
COLOR 0A

echo ========================================================
echo      MAESTRO AI - ENHANCED DESKTOP CONTROLLER
echo      (Ollama Generation + Brave Automation)
echo ========================================================
echo.

:: 0. Fast Start Check (Bypass)
IF EXIST "venv" (
    IF EXIST "data\vocal_profiles_enhanced.json" (
        IF EXIST "data\genre_fusion_matrix_enhanced.json" (
            echo [*] Ambiente ja configurado. Pulando setup...
            call venv\Scripts\activate
            GOTO EXECUTION
        )
    )
)

:: 1. Verificação do Ollama e Modelo
echo [*] Verificando Sistema de IA Local...

:: 1.1 Tenta Ollama Nativo (CLI)
ollama -v >nul 2>&1
IF !ERRORLEVEL! EQU 0 (
    echo     Ollama nativo detectado.
    echo [*] Verificando conexao com o servidor...
    ollama list >nul 2>&1
    IF !ERRORLEVEL! NEQ 0 (
        echo [X] O servidor do Ollama nao esta respondendo!
        echo     Certifique-se de que o aplicativo Ollama esta rodando.
        pause
        exit
    )
    echo     Servidor online. Garantindo modelo mistral-nemo:12b...
    ollama pull mistral-nemo:12b
    GOTO PYTHON_SETUP
)

:: 1.2 Tenta Ollama via Docker (Fallback)
echo     Ollama CLI nao encontrado. Verificando Docker...
docker --version >nul 2>&1
IF !ERRORLEVEL! EQU 0 (
    echo     Docker detectado. Verificando container Ollama...
    docker ps -q -f name=ollama >nul 2>&1
    IF !ERRORLEVEL! EQU 0 (
        echo     Container Ollama rodando!
        echo     Garantindo modelo mistral-nemo:12b via Docker exec...
        docker exec ollama ollama pull mistral-nemo:12b
        GOTO PYTHON_SETUP
    ) ELSE (
        echo [X] Docker detectado, mas container 'ollama' nao esta rodando.
        echo     Iniciando container...
        docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
        echo     Aguardando inicializacao...
        timeout /t 5
        docker exec ollama ollama pull mistral-nemo:12b
        GOTO PYTHON_SETUP
    )
)

:: 1.3 Falha Total
echo [X] NEM OLLAMA NATIVO NEM DOCKER FORAM ENCONTRADOS!
echo     Por favor instale o Ollama (ollama.com) OU Docker Desktop.
pause
exit

:PYTHON_SETUP

:: 2. Configuração Python
echo.
echo [*] Configurando Ambiente Python...
IF NOT EXIST "venv" (
    echo     Criando ambiente virtual ^(venv^)...
    python -m venv venv
)
call venv\Scripts\activate

:: 3. Instalação de Dependências
echo [*] Verificando dependencias...
pip install -r requirements.txt >nul 2>&1

:: 4. Inicialização de Dados Enhanced
echo.
echo [*] Verificando Base de Dados Musical (Enhanced)...

IF NOT EXIST "data\vocal_profiles_enhanced.json" (
    echo     [!] Gerando perfis vocais expandidos ^(60+ generos^)...
    python create_enhanced_profiles.py
)

IF NOT EXIST "data\genre_fusion_matrix_enhanced.json" (
    echo     [!] Gerando matriz de fusao aprimorada...
    python create_enhanced_fusion_matrix.py
)

:EXECUTION
:: 5. Execução do Maestro (Geração)
echo.
echo ========================================================
echo    ETAPA 1: COMPOSICAO NEURAL (OLLAMA Local)
echo ========================================================
echo.
python maestro_ollama_enhanced.py

:: 6. Execução do Automator (Opcional)
echo.
echo ========================================================
echo    ETAPA 2: AUTOMACAO DE BROWSER (Suno.com)
echo ========================================================
echo.
set /p RUN_BRAVE="Deseja iniciar a injecao no Brave agora? (S/N): "
IF /I "%RUN_BRAVE%"=="S" (
    python maestro_brave_automator.py
)

echo.
echo [!] Processo finalizado.
pause
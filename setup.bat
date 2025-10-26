@echo off
echo ====================================
echo Email Optimizer - Setup Automatico
echo ====================================
echo.

REM Check Python
echo Verifico Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python non trovato. Installalo prima di continuare.
    pause
    exit /b 1
)
echo [OK] Python trovato

REM Crea virtual environment
echo.
echo Creo ambiente virtuale...
if exist venv (
    echo [WARNING] Directory venv esistente, la elimino...
    rmdir /s /q venv
)
python -m venv venv
echo [OK] Ambiente virtuale creato

REM Attiva venv
echo.
echo Attivo ambiente virtuale...
call venv\Scripts\activate.bat
echo [OK] Ambiente attivato

REM Aggiorna pip
echo.
echo Aggiorno pip...
python -m pip install --upgrade pip --quiet
echo [OK] Pip aggiornato

REM Installa dipendenze
echo.
echo Installo dipendenze...
echo (questo potrebbe richiedere qualche minuto)
pip install -r requirements.txt --quiet
echo [OK] Dipendenze installate

REM Crea directories
echo.
echo Creo directories necessarie...
if not exist logs mkdir logs
if not exist credentials mkdir credentials
if not exist cache mkdir cache
echo [OK] Directory create

REM Crea .env
if not exist .env (
    echo.
    echo Creo file di configurazione...
    copy .env.example .env
    echo [OK] File .env creato
    echo [WARNING] IMPORTANTE: Modifica il file .env con le tue credenziali!
) else (
    echo.
    echo [WARNING] File .env gia esistente, non sovrascritto
)

REM Summary
echo.
echo ====================================
echo Setup completato con successo!
echo ====================================
echo.
echo PROSSIMI PASSI:
echo.
echo 1. Ottieni API Key Claude:
echo    https://console.anthropic.com/
echo.
echo 2. Configura email (Gmail App Password):
echo    https://myaccount.google.com/security
echo.
echo 3. Modifica file .env:
echo    notepad .env
echo.
echo 4. Esegui l'applicazione:
echo    venv\Scripts\activate
echo    python main.py
echo.
echo Documentazione:
echo    - README.md
echo    - QUICKSTART.md
echo    - TUTORIAL.md
echo.
pause

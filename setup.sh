#!/bin/bash

echo "🤖 Email Optimizer - Setup Automatico"
echo "======================================"
echo ""

# Colori
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python
echo "🔍 Verifico Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 non trovato. Installalo prima di continuare.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION trovato"

# Crea virtual environment
echo ""
echo "📦 Creo ambiente virtuale..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠${NC} Directory venv già esistente, la elimino..."
    rm -rf venv
fi

python3 -m venv venv
echo -e "${GREEN}✓${NC} Ambiente virtuale creato"

# Attiva venv
echo ""
echo "⚡ Attivo ambiente virtuale..."
source venv/bin/activate
echo -e "${GREEN}✓${NC} Ambiente attivato"

# Aggiorna pip
echo ""
echo "⬆️  Aggiorno pip..."
pip install --upgrade pip --quiet
echo -e "${GREEN}✓${NC} Pip aggiornato"

# Installa dipendenze
echo ""
echo "📥 Installo dipendenze..."
echo "   (questo potrebbe richiedere qualche minuto)"
pip install -r requirements.txt --quiet
echo -e "${GREEN}✓${NC} Dipendenze installate"

# Crea directories
echo ""
echo "📁 Creo directories necessarie..."
mkdir -p logs
mkdir -p credentials
mkdir -p cache
echo -e "${GREEN}✓${NC} Directory create"

# Crea .env se non esiste
if [ ! -f ".env" ]; then
    echo ""
    echo "⚙️  Creo file di configurazione..."
    cp .env.example .env
    echo -e "${GREEN}✓${NC} File .env creato da .env.example"
    echo -e "${YELLOW}⚠${NC}  IMPORTANTE: Modifica il file .env con le tue credenziali!"
else
    echo ""
    echo -e "${YELLOW}⚠${NC}  File .env già esistente, non sovrascritto"
fi

# Test import
echo ""
echo "🧪 Verifico installazione..."
if python -c "import anthropic, pydantic, dotenv" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Tutti i moduli importati correttamente"
else
    echo -e "${RED}❌ Errore nell'importazione dei moduli${NC}"
    exit 1
fi

# Summary
echo ""
echo "======================================"
echo -e "${GREEN}✅ Setup completato con successo!${NC}"
echo "======================================"
echo ""
echo "📝 PROSSIMI PASSI:"
echo ""
echo "1. Ottieni API Key Claude:"
echo "   https://console.anthropic.com/"
echo ""
echo "2. Configura email (Gmail App Password):"
echo "   https://myaccount.google.com/security"
echo ""
echo "3. Modifica file .env:"
echo "   nano .env"
echo ""
echo "4. Esegui l'applicazione:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "📚 Documentazione:"
echo "   - README.md - Panoramica completa"
echo "   - QUICKSTART.md - Guida rapida"
echo "   - TUTORIAL.md - Tutorial dettagliato"
echo ""
echo "🆘 Supporto:"
echo "   - Logs: logs/email_optimizer.log"
echo "   - Issues: GitHub repository"
echo ""

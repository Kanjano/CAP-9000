#!/bin/bash
# CAP 9000 - Script di Avvio Unificato
# Controlla prerequisiti, avvia servizi e lancia l'applicazione

set -e

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Directory progetto
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# PID files
OLLAMA_PID_FILE="/tmp/cap9000_ollama.pid"
BACKEND_PID_FILE="/tmp/cap9000_backend.pid"
FRONTEND_PID_FILE="/tmp/cap9000_frontend.pid"

# Logo HAL 9000
show_logo() {
    echo -e "${RED}"
    cat << "EOF"
    ╔═══════════════════════════════════════╗
    ║                                       ║
    ║          ⬤  CAP 9000  ⬤              ║
    ║                                       ║
    ║    Cognitive Assistance Program       ║
    ║                                       ║
    ╚═══════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}Arresto servizi...${NC}"
    
    # Stop frontend
    if [ -f "$FRONTEND_PID_FILE" ]; then
        FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            kill $FRONTEND_PID 2>/dev/null || true
            echo -e "${GREEN}✓${NC} Frontend arrestato"
        fi
        rm -f "$FRONTEND_PID_FILE"
    fi
    
    # Stop backend
    if [ -f "$BACKEND_PID_FILE" ]; then
        BACKEND_PID=$(cat "$BACKEND_PID_FILE")
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            kill $BACKEND_PID 2>/dev/null || true
            echo -e "${GREEN}✓${NC} Backend arrestato"
        fi
        rm -f "$BACKEND_PID_FILE"
    fi
    
    # Note: Non arrestiamo Ollama perché potrebbe essere usato da altre app
    
    echo -e "${CYAN}CAP 9000 arrestato.${NC}"
    exit 0
}

# Trap CTRL+C
trap cleanup SIGINT SIGTERM

# Header
clear
show_logo
echo -e "${CYAN}Avvio CAP 9000...${NC}\n"

# ============================================
# STEP 1: Verifica Prerequisiti
# ============================================
echo -e "${YELLOW}[1/5] Verifica prerequisiti...${NC}"

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 non trovato${NC}"
    echo -e "${YELLOW}Installa Python da: https://www.python.org/downloads/${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION"

# Verifica pip
if ! python3 -m pip --version &> /dev/null; then
    echo -e "${RED}✗ pip non trovato${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} pip disponibile"

# Verifica Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}✗ Node.js non trovato${NC}"
    echo -e "${YELLOW}Installa Node.js da: https://nodejs.org/${NC}"
    exit 1
fi
NODE_VERSION=$(node --version)
echo -e "${GREEN}✓${NC} Node.js $NODE_VERSION"

# Verifica npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}✗ npm non trovato${NC}"
    exit 1
fi
NPM_VERSION=$(npm --version)
echo -e "${GREEN}✓${NC} npm $NPM_VERSION"

# Verifica Ollama
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}✗ Ollama non trovato${NC}"
    echo -e "${YELLOW}Installa Ollama: curl -fsSL https://ollama.ai/install.sh | sh${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} Ollama installato"

echo ""

# ============================================
# STEP 2: Verifica Dipendenze Python
# ============================================
echo -e "${YELLOW}[2/5] Verifica dipendenze Python...${NC}"

if [ -f "requirements.txt" ]; then
    # Verifica se le dipendenze sono installate
    if ! python3 -c "import flask" &> /dev/null; then
        echo -e "${CYAN}Installazione dipendenze Python...${NC}"
        python3 -m pip install -q -r requirements.txt
        echo -e "${GREEN}✓${NC} Dipendenze Python installate"
    else
        echo -e "${GREEN}✓${NC} Dipendenze Python già installate"
    fi
else
    echo -e "${YELLOW}⚠${NC} requirements.txt non trovato"
fi

echo ""

# ============================================
# STEP 3: Avvia Ollama
# ============================================
echo -e "${YELLOW}[3/5] Avvio Ollama...${NC}"

# Verifica se Ollama è già in esecuzione
if pgrep -x "ollama" > /dev/null; then
    echo -e "${GREEN}✓${NC} Ollama già in esecuzione"
else
    echo -e "${CYAN}Avvio servizio Ollama...${NC}"
    nohup ollama serve > /tmp/cap9000_ollama.log 2>&1 &
    OLLAMA_PID=$!
    echo $OLLAMA_PID > "$OLLAMA_PID_FILE"
    
    # Attendi che Ollama sia pronto
    echo -e "${CYAN}Attesa avvio Ollama...${NC}"
    for i in {1..10}; do
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            echo -e "${GREEN}✓${NC} Ollama avviato (PID: $OLLAMA_PID)"
            break
        fi
        sleep 1
    done
    
    # Verifica finale
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${RED}✗ Ollama non risponde${NC}"
        exit 1
    fi
fi

# Verifica modello CodeLlama
echo -e "${CYAN}Verifica modello CodeLlama...${NC}"
if ollama list | grep -q "codellama"; then
    echo -e "${GREEN}✓${NC} CodeLlama disponibile"
else
    echo -e "${YELLOW}⚠ CodeLlama non trovato${NC}"
    echo -e "${CYAN}Download CodeLlama (3.8 GB)...${NC}"
    ollama pull codellama
    echo -e "${GREEN}✓${NC} CodeLlama scaricato"
fi

echo ""

# ============================================
# STEP 4: Avvia Backend Flask
# ============================================
echo -e "${YELLOW}[4/5] Avvio backend Flask...${NC}"

# Verifica se backend è già in esecuzione
if lsof -i:5001 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Porta 5001 già in uso, arresto processo...${NC}"
    pkill -f "python.*app.py" || true
    sleep 2
fi

# Avvia backend
echo -e "${CYAN}Avvio Flask su porta 5001...${NC}"
nohup python3 app.py > /tmp/cap9000_backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "$BACKEND_PID_FILE"

# Attendi che Flask sia pronto
echo -e "${CYAN}Attesa avvio Flask...${NC}"
for i in {1..15}; do
    if curl -s http://localhost:5001/api/languages > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Backend Flask avviato (PID: $BACKEND_PID)"
        break
    fi
    sleep 1
done

# Verifica finale
if ! curl -s http://localhost:5001/api/languages > /dev/null 2>&1; then
    echo -e "${RED}✗ Backend non risponde${NC}"
    echo -e "${YELLOW}Controlla log: tail -f /tmp/cap9000_backend.log${NC}"
    exit 1
fi

echo ""

# ============================================
# STEP 5: Avvia Frontend (se in dev mode)
# ============================================
echo -e "${YELLOW}[5/5] Verifica frontend...${NC}"

if [ -d "frontend/dist" ]; then
    echo -e "${GREEN}✓${NC} Frontend già buildato (dist/ presente)"
    echo -e "${CYAN}Frontend servito da Flask su http://localhost:5001${NC}"
else
    echo -e "${YELLOW}⚠ Frontend non buildato${NC}"
    if [ -d "frontend" ]; then
        echo -e "${CYAN}Build frontend...${NC}"
        cd frontend
        
        # Installa dipendenze se necessario
        if [ ! -d "node_modules" ]; then
            echo -e "${CYAN}Installazione dipendenze npm...${NC}"
            npm install
        fi
        
        # Build
        npm run build
        cd ..
        echo -e "${GREEN}✓${NC} Frontend buildato"
    else
        echo -e "${RED}✗ Directory frontend non trovata${NC}"
        exit 1
    fi
fi

echo ""

# ============================================
# Riepilogo e Apertura Browser
# ============================================
echo -e "${GREEN}╔═══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                       ║${NC}"
echo -e "${GREEN}║   ✓ CAP 9000 AVVIATO CON SUCCESSO!   ║${NC}"
echo -e "${GREEN}║                                       ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Servizi attivi:${NC}"
echo -e "  ${GREEN}✓${NC} Ollama        → http://localhost:11434"
echo -e "  ${GREEN}✓${NC} Backend Flask → http://localhost:5001"
echo -e "  ${GREEN}✓${NC} Frontend      → http://localhost:5001"
echo ""
echo -e "${CYAN}Modello AI:${NC}"
echo -e "  ${GREEN}✓${NC} CodeLlama (specializzato programmazione)"
echo ""
echo -e "${CYAN}Log files:${NC}"
echo -e "  • Ollama:  /tmp/cap9000_ollama.log"
echo -e "  • Backend: /tmp/cap9000_backend.log"
echo ""
echo -e "${YELLOW}Apertura browser...${NC}"

# Apri browser
sleep 2
if command -v open &> /dev/null; then
    open http://localhost:5001
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:5001
else
    echo -e "${CYAN}Apri manualmente: http://localhost:5001${NC}"
fi

echo ""
echo -e "${RED}\"I am putting myself to the fullest possible use.\"${NC}"
echo -e "${RED}                                        - HAL 9000${NC}"
echo ""
echo -e "${YELLOW}Premi CTRL+C per arrestare CAP 9000${NC}"
echo ""

# Mantieni script in esecuzione
while true; do
    sleep 1
done

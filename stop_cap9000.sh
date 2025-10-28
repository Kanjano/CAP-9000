#!/bin/bash
# CAP 9000 - Script di Arresto

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# PID files
BACKEND_PID_FILE="/tmp/cap9000_backend.pid"
FRONTEND_PID_FILE="/tmp/cap9000_frontend.pid"
OLLAMA_PID_FILE="/tmp/cap9000_ollama.pid"

echo -e "${CYAN}Arresto CAP 9000...${NC}\n"

# Stop frontend
if [ -f "$FRONTEND_PID_FILE" ]; then
    FRONTEND_PID=$(cat "$FRONTEND_PID_FILE")
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        kill $FRONTEND_PID 2>/dev/null || true
        echo -e "${GREEN}✓${NC} Frontend arrestato"
    fi
    rm -f "$FRONTEND_PID_FILE"
fi

# Stop Electron app
if pgrep -f "electron" > /dev/null; then
    pkill -f "electron" 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Applicazione Electron arrestata"
fi

# Stop backend (gestito da Electron, ma cleanup per sicurezza)
if [ -f "$BACKEND_PID_FILE" ]; then
    BACKEND_PID=$(cat "$BACKEND_PID_FILE")
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    rm -f "$BACKEND_PID_FILE"
fi

# Stop any remaining Python processes
pkill -f "python.*app.py" 2>/dev/null || true

# Verifica porta 5001 libera
if lsof -i:5001 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Porta 5001 ancora occupata, forzatura...${NC}"
    lsof -ti:5001 | xargs kill -9 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Porta 5001 liberata"
fi

# Note: Non arrestiamo Ollama perché potrebbe essere usato da altre app
# Se vuoi arrestare anche Ollama, decommenta:
# if [ -f "$OLLAMA_PID_FILE" ]; then
#     OLLAMA_PID=$(cat "$OLLAMA_PID_FILE")
#     if ps -p $OLLAMA_PID > /dev/null 2>&1; then
#         kill $OLLAMA_PID 2>/dev/null || true
#         echo -e "${GREEN}✓${NC} Ollama arrestato"
#     fi
#     rm -f "$OLLAMA_PID_FILE"
# fi

echo ""
echo -e "${CYAN}CAP 9000 arrestato con successo.${NC}"
echo -e "${RED}\"I'm sorry, Dave. I'm afraid I can't do that.\"${NC}"
echo ""

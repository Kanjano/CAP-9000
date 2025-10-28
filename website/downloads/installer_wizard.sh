#!/bin/bash
# CAP 9000 - Installation Wizard
# Installer completo con download automatico LLM e documentazioni

set -e

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ASCII Art HAL 9000
show_hal_logo() {
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

# Progress bar
show_progress() {
    local current=$1
    local total=$2
    local width=50
    local percentage=$((current * 100 / total))
    local completed=$((width * current / total))
    local remaining=$((width - completed))
    
    printf "\r${CYAN}["
    printf "%${completed}s" | tr ' ' '█'
    printf "%${remaining}s" | tr ' ' '░'
    printf "] ${percentage}%%${NC}"
}

# Verifica requisiti
check_requirements() {
    echo -e "${YELLOW}[1/7] Verifica requisiti sistema...${NC}"
    
    # Verifica Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}✗ Python 3 non trovato${NC}"
        echo -e "${YELLOW}Installa Python da: https://www.python.org/downloads/${NC}"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ Python $PYTHON_VERSION trovato${NC}"
    
    # Verifica spazio disco
    AVAILABLE_SPACE=$(df -h . | awk 'NR==2 {print $4}' | sed 's/Gi//')
    if [ "${AVAILABLE_SPACE%.*}" -lt 5 ]; then
        echo -e "${RED}✗ Spazio disco insufficiente (richiesto: 5GB, disponibile: ${AVAILABLE_SPACE}GB)${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Spazio disco sufficiente (${AVAILABLE_SPACE}GB disponibili)${NC}"
    
    # Verifica RAM
    TOTAL_RAM=$(sysctl -n hw.memsize | awk '{print int($1/1024/1024/1024)}')
    if [ "$TOTAL_RAM" -lt 8 ]; then
        echo -e "${YELLOW}⚠ RAM limitata (${TOTAL_RAM}GB). Raccomandati 8GB+${NC}"
    else
        echo -e "${GREEN}✓ RAM sufficiente (${TOTAL_RAM}GB)${NC}"
    fi
    
    echo ""
}

# Installa dipendenze Python
install_python_deps() {
    echo -e "${YELLOW}[2/7] Installazione dipendenze Python...${NC}"
    
    if [ -f "requirements.txt" ]; then
        python3 -m pip install --user -q -r requirements.txt
        echo -e "${GREEN}✓ Dipendenze Python installate${NC}"
    else
        echo -e "${YELLOW}⚠ requirements.txt non trovato, skip${NC}"
    fi
    
    echo ""
}

# Installa Ollama
install_ollama() {
    echo -e "${YELLOW}[3/7] Installazione Ollama...${NC}"
    
    if command -v ollama &> /dev/null; then
        echo -e "${GREEN}✓ Ollama già installato${NC}"
    else
        echo -e "${CYAN}Scaricamento Ollama...${NC}"
        curl -fsSL https://ollama.ai/install.sh | sh
        echo -e "${GREEN}✓ Ollama installato${NC}"
    fi
    
    # Avvia Ollama
    if ! pgrep -x "ollama" > /dev/null; then
        echo -e "${CYAN}Avvio servizio Ollama...${NC}"
        nohup ollama serve > /tmp/ollama.log 2>&1 &
        sleep 3
        echo -e "${GREEN}✓ Ollama avviato${NC}"
    else
        echo -e "${GREEN}✓ Ollama già in esecuzione${NC}"
    fi
    
    echo ""
}

# Scarica modello CodeLlama
download_codellama() {
    echo -e "${YELLOW}[4/7] Download modello CodeLlama (3.8 GB)...${NC}"
    echo -e "${CYAN}Questo richiederà 5-15 minuti in base alla connessione${NC}"
    
    # Verifica se già scaricato
    if ollama list | grep -q "codellama"; then
        echo -e "${GREEN}✓ CodeLlama già scaricato${NC}"
    else
        echo -e "${CYAN}Download in corso...${NC}"
        ollama pull codellama 2>&1 | while IFS= read -r line; do
            if [[ $line =~ ([0-9]+)% ]]; then
                percentage="${BASH_REMATCH[1]}"
                show_progress "$percentage" 100
            fi
        done
        echo ""
        echo -e "${GREEN}✓ CodeLlama scaricato${NC}"
    fi
    
    echo ""
}

# Scarica documentazioni
download_docs() {
    echo -e "${YELLOW}[5/7] Download documentazioni ufficiali (50 MB)...${NC}"
    
    if [ -d "local_docs" ] && [ "$(ls -A local_docs 2>/dev/null)" ]; then
        echo -e "${GREEN}✓ Documentazioni già scaricate${NC}"
    else
        if [ -f "download_docs.py" ]; then
            echo -e "${CYAN}Download in corso...${NC}"
            python3 download_docs.py
            echo -e "${GREEN}✓ Documentazioni scaricate${NC}"
        else
            echo -e "${YELLOW}⚠ Script download_docs.py non trovato, skip${NC}"
        fi
    fi
    
    echo ""
}

# Build frontend
build_frontend() {
    echo -e "${YELLOW}[6/7] Build frontend React...${NC}"
    
    if [ -d "frontend" ]; then
        cd frontend
        
        if [ ! -d "node_modules" ]; then
            echo -e "${CYAN}Installazione dipendenze npm...${NC}"
            npm install --silent
        fi
        
        echo -e "${CYAN}Build in corso...${NC}"
        npm run build --silent
        cd ..
        echo -e "${GREEN}✓ Frontend buildato${NC}"
    else
        echo -e "${YELLOW}⚠ Directory frontend non trovata, skip${NC}"
    fi
    
    echo ""
}

# Configura avvio automatico
setup_autostart() {
    echo -e "${YELLOW}[7/7] Configurazione avvio automatico...${NC}"
    
    # Crea LaunchAgent per Ollama
    PLIST_PATH="$HOME/Library/LaunchAgents/com.ollama.server.plist"
    
    cat > "$PLIST_PATH" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ollama.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/ollama</string>
        <string>serve</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/ollama.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/ollama.error.log</string>
</dict>
</plist>
EOF
    
    launchctl load "$PLIST_PATH" 2>/dev/null || true
    echo -e "${GREEN}✓ Avvio automatico Ollama configurato${NC}"
    
    # Crea alias per avvio rapido
    INSTALL_DIR="$(pwd)"
    ALIAS_FILE="$HOME/.zshrc"
    
    if ! grep -q "alias cap9000" "$ALIAS_FILE" 2>/dev/null; then
        echo "" >> "$ALIAS_FILE"
        echo "# CAP 9000 Alias" >> "$ALIAS_FILE"
        echo "alias cap9000='cd \"$INSTALL_DIR\" && ./run.sh'" >> "$ALIAS_FILE"
        echo -e "${GREEN}✓ Alias 'cap9000' creato${NC}"
    fi
    
    echo ""
}

# Riepilogo installazione
show_summary() {
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                       ║${NC}"
    echo -e "${GREEN}║   ✓ INSTALLAZIONE COMPLETATA!        ║${NC}"
    echo -e "${GREEN}║                                       ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${CYAN}Componenti installati:${NC}"
    echo -e "  ${GREEN}✓${NC} CAP 9000 Application"
    echo -e "  ${GREEN}✓${NC} Ollama LLM Engine"
    echo -e "  ${GREEN}✓${NC} CodeLlama Model (3.8 GB)"
    echo -e "  ${GREEN}✓${NC} Documentazioni Ufficiali"
    echo -e "  ${GREEN}✓${NC} Frontend React"
    echo ""
    echo -e "${CYAN}Per avviare CAP 9000:${NC}"
    echo -e "  ${YELLOW}1.${NC} Apri Terminale"
    echo -e "  ${YELLOW}2.${NC} Digita: ${MAGENTA}cap9000${NC}"
    echo -e "  ${YELLOW}3.${NC} Oppure: ${MAGENTA}cd \"$INSTALL_DIR\" && ./run.sh${NC}"
    echo ""
    echo -e "${CYAN}Supporto:${NC}"
    echo -e "  Email: ${BLUE}antonio.web2music@gmail.com${NC}"
    echo ""
    echo -e "${RED}\"I am putting myself to the fullest possible use.\"${NC}"
    echo -e "${RED}                                        - HAL 9000${NC}"
    echo ""
}

# Main
main() {
    clear
    show_hal_logo
    
    echo -e "${CYAN}Benvenuto nell'installer di CAP 9000${NC}"
    echo -e "${CYAN}Questo wizard installerà tutti i componenti necessari.${NC}"
    echo ""
    echo -e "${YELLOW}Spazio richiesto: ~5 GB${NC}"
    echo -e "${YELLOW}Tempo stimato: 10-20 minuti${NC}"
    echo ""
    
    read -p "Premere INVIO per continuare o CTRL+C per annullare..."
    echo ""
    
    check_requirements
    install_python_deps
    install_ollama
    download_codellama
    download_docs
    build_frontend
    setup_autostart
    show_summary
}

# Esegui
main

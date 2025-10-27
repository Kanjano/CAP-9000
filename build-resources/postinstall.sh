#!/bin/bash
# CAP 9000 Post-Installation Script for macOS
# Installa Ollama e scarica documentazioni

set -e

echo "========================================"
echo "CAP 9000 Post-Installation Setup"
echo "========================================"
echo ""

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directory installazione
INSTALL_DIR="/Applications/CAP 9000.app/Contents/Resources"
APP_DIR="/Applications/CAP 9000.app"

# Funzione per mostrare progress
show_progress() {
    echo -e "${GREEN}[✓]${NC} $1"
}

show_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

show_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Calcola spazio richiesto
echo "Spazio su disco richiesto:"
echo "  • CAP 9000 Application: ~200 MB"
echo "  • Ollama LLM Engine: ~500 MB"
echo "  • CodeLlama AI Model: ~3.8 GB"
echo "  • Official Documentation: ~50 MB"
echo "  ────────────────────────────────"
echo "  TOTALE: ~4.5 GB"
echo ""

# Chiedi conferma
read -p "Vuoi installare Ollama e scaricare le documentazioni? (s/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[SsYy]$ ]]; then
    show_warning "Installazione componenti saltata."
    show_warning "CAP 9000 funzionerà in modalità limitata."
    echo ""
    echo "Per installare Ollama manualmente:"
    echo "  curl -fsSL https://ollama.ai/install.sh | sh"
    echo "  ollama pull codellama"
    echo ""
    echo "Per scaricare documentazioni:"
    echo "  cd \"$INSTALL_DIR\""
    echo "  python3 download_docs.py"
    exit 0
fi

# 1. Verifica se Ollama è già installato
echo ""
echo "Verifico installazione Ollama..."

if command -v ollama &> /dev/null; then
    show_progress "Ollama già installato"
    OLLAMA_INSTALLED=true
else
    show_warning "Ollama non trovato, procedo con l'installazione..."
    OLLAMA_INSTALLED=false
fi

# 2. Installa Ollama se necessario
if [ "$OLLAMA_INSTALLED" = false ]; then
    echo ""
    echo "Scarico e installo Ollama..."
    echo "Questo richiederà ~500 MB e potrebbe richiedere alcuni minuti..."
    
    # Download e installa Ollama
    if curl -fsSL https://ollama.ai/install.sh | sh; then
        show_progress "Ollama installato con successo"
    else
        show_error "Errore durante l'installazione di Ollama"
        show_warning "Puoi installarlo manualmente da: https://ollama.ai"
        exit 1
    fi
fi

# 3. Avvia Ollama
echo ""
echo "Avvio servizio Ollama..."

# Verifica se Ollama è già in esecuzione
if pgrep -x "ollama" > /dev/null; then
    show_progress "Ollama già in esecuzione"
else
    # Avvia Ollama in background
    nohup ollama serve > /dev/null 2>&1 &
    sleep 3
    show_progress "Ollama avviato"
fi

# 4. Scarica modello CodeLlama
echo ""
echo "Scarico modello CodeLlama..."
echo "Questo richiederà ~3.8 GB e potrebbe richiedere 10-30 minuti..."
echo "Attendere prego..."

if ollama pull codellama; then
    show_progress "CodeLlama scaricato con successo"
else
    show_error "Errore durante il download di CodeLlama"
    show_warning "Puoi scaricarlo manualmente con: ollama pull codellama"
fi

# 5. Verifica Python
echo ""
echo "Verifico Python..."

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    show_progress "Python3 trovato"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    show_progress "Python trovato"
else
    show_error "Python non trovato"
    show_warning "Installa Python da: https://www.python.org/downloads/"
    show_warning "Le documentazioni non saranno scaricate"
    PYTHON_CMD=""
fi

# 6. Installa dipendenze Python
if [ -n "$PYTHON_CMD" ]; then
    echo ""
    echo "Installo dipendenze Python..."
    
    if $PYTHON_CMD -m pip install --user beautifulsoup4 requests; then
        show_progress "Dipendenze installate"
    else
        show_warning "Errore installazione dipendenze"
    fi
fi

# 7. Scarica documentazioni
if [ -n "$PYTHON_CMD" ]; then
    echo ""
    echo "Scarico documentazioni ufficiali..."
    echo "Questo richiederà ~50 MB e alcuni minuti..."
    
    cd "$INSTALL_DIR"
    
    if [ -f "download_docs.py" ]; then
        if $PYTHON_CMD download_docs.py; then
            show_progress "Documentazioni scaricate con successo"
        else
            show_warning "Errore durante il download delle documentazioni"
            show_warning "Puoi scaricarle manualmente con:"
            show_warning "  cd \"$INSTALL_DIR\" && python3 download_docs.py"
        fi
    else
        show_warning "Script download_docs.py non trovato"
    fi
fi

# 8. Configura avvio automatico Ollama (opzionale)
echo ""
read -p "Vuoi avviare Ollama automaticamente all'avvio? (s/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[SsYy]$ ]]; then
    # Crea LaunchAgent per avvio automatico
    PLIST_PATH="$HOME/Library/LaunchAgents/com.ollama.server.plist"
    
    cat > "$PLIST_PATH" << EOF
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
    
    launchctl load "$PLIST_PATH"
    show_progress "Ollama configurato per avvio automatico"
fi

# 9. Riepilogo
echo ""
echo "========================================"
echo "Installazione completata!"
echo "========================================"
echo ""
show_progress "CAP 9000 installato in: $APP_DIR"
show_progress "Ollama installato e configurato"
show_progress "CodeLlama model pronto"

if [ -d "$INSTALL_DIR/local_docs" ]; then
    show_progress "Documentazioni ufficiali scaricate"
else
    show_warning "Documentazioni non scaricate (CAP 9000 userà fallback)"
fi

echo ""
echo "Puoi avviare CAP 9000 da:"
echo "  • Spotlight: cerca 'CAP 9000'"
echo "  • Finder: Applicazioni > CAP 9000"
echo "  • Launchpad: icona CAP 9000"
echo ""
echo "Per supporto: antonio.web2music@gmail.com"
echo ""

exit 0

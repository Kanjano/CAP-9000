#!/bin/bash

# 🔧 Fix macOS Security Block per CAP 9000
# Rimuove la quarantena dall'app per permettere l'esecuzione

echo "🔐 CAP 9000 - Fix macOS Security"
echo "================================"
echo ""

APP_PATH="/Applications/CAP 9000 Code Assistant.app"

# Controlla se l'app esiste
if [ ! -d "$APP_PATH" ]; then
    echo "❌ App non trovata in: $APP_PATH"
    echo ""
    echo "Possibili soluzioni:"
    echo "1. Assicurati di aver installato l'app in /Applications"
    echo "2. Oppure specifica il path: $0 /path/to/app"
    exit 1
fi

# Usa path custom se fornito
if [ ! -z "$1" ]; then
    APP_PATH="$1"
fi

echo "📍 App trovata: $APP_PATH"
echo ""

# Rimuovi attributi di quarantena
echo "🔓 Rimozione attributi di quarantena..."
xattr -cr "$APP_PATH"

if [ $? -eq 0 ]; then
    echo "✅ Successo! L'app può ora essere aperta."
    echo ""
    echo "Puoi avviare CAP 9000 normalmente."
else
    echo "❌ Errore durante la rimozione degli attributi."
    echo ""
    echo "Prova manualmente:"
    echo "  xattr -cr \"$APP_PATH\""
    exit 1
fi

echo ""
echo "🚀 Vuoi avviare CAP 9000 ora? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    open "$APP_PATH"
    echo "✅ CAP 9000 avviato!"
fi

#!/bin/bash

# Script per verificare e avviare Ollama se necessario

echo "🔍 Verifica stato Ollama..."

# Funzione per verificare se Ollama è in esecuzione
check_ollama() {
    curl -s http://localhost:11434/api/tags > /dev/null 2>&1
    return $?
}

# Verifica se Ollama è già in esecuzione
if check_ollama; then
    echo "✅ Ollama è già in esecuzione"
    exit 0
fi

echo "⚠️  Ollama non è in esecuzione. Tentativo di avvio..."

# Verifica se Ollama è installato
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama non è installato!"
    echo ""
    echo "Per installare Ollama:"
    echo "1. Visita: https://ollama.ai"
    echo "2. Scarica e installa Ollama per macOS"
    echo "3. Esegui: ollama pull qwen2.5-coder:3b   (modello di default, veloce)"
    echo ""
    exit 1
fi

# Avvia Ollama in background
echo "🚀 Avvio Ollama in background..."
ollama serve > /dev/null 2>&1 &
OLLAMA_PID=$!

# Attendi che Ollama sia pronto (max 10 secondi)
echo "⏳ Attendo che Ollama sia pronto..."
for i in {1..20}; do
    sleep 0.5
    if check_ollama; then
        echo "✅ Ollama avviato con successo (PID: $OLLAMA_PID)"
        
        # Verifica modello: default qwen2.5-coder:3b, fallback codellama
        if ollama list | grep -q "qwen2.5-coder"; then
            echo "✅ Modello qwen2.5-coder disponibile (default)"
        elif ollama list | grep -q "codellama"; then
            echo "✅ Modello codellama disponibile (fallback)"
        else
            echo "⚠️  Nessun modello di codice trovato"
            echo "📥 Download consigliato: ollama pull qwen2.5-coder:3b"
        fi
        
        exit 0
    fi
    echo -n "."
done

echo ""
echo "❌ Timeout: Ollama non risponde dopo 10 secondi"
echo "Prova ad avviarlo manualmente: ollama serve"
exit 1

# 🤖 Setup LLM Locale per HAL 9000

HAL 9000 può usare modelli LLM locali tramite **Ollama** per risposte intelligenti e contestuali.

## 📥 Installazione Ollama

### macOS
```bash
# Scarica e installa da
https://ollama.ai/download

# Oppure con Homebrew
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows
Scarica l'installer da: https://ollama.ai/download

## 🚀 Avvio Ollama

```bash
# Avvia il servizio Ollama
ollama serve
```

Il servizio sarà disponibile su `http://localhost:11434`

## 📦 Download Modelli

### Modelli Consigliati per Programmazione

#### 1. CodeLlama (Consigliato) - 7B
```bash
ollama pull codellama
```
- Ottimizzato specificamente per codice
- Buon equilibrio velocità/qualità
- ~4GB di spazio

#### 2. DeepSeek Coder - 6.7B
```bash
ollama pull deepseek-coder
```
- Eccellente per programmazione
- Supporta molti linguaggi
- ~3.8GB di spazio

#### 3. CodeLlama 13B (Più potente)
```bash
ollama pull codellama:13b
```
- Migliore qualità ma più lento
- Richiede più RAM
- ~7.3GB di spazio

#### 4. Phi (Veloce e leggero) - 2.7B
```bash
ollama pull phi
```
- Molto veloce
- Buono per domande semplici
- ~1.6GB di spazio

#### 5. Mistral (General Purpose) - 7B
```bash
ollama pull mistral
```
- Buon modello general purpose
- Funziona bene anche per codice
- ~4.1GB di spazio

## ⚙️ Configurazione HAL 9000

### Cambiare Modello

Modifica `app.py`:

```python
# Usa CodeLlama (default)
llm = LLMHandler(model="codellama")

# Oppure usa DeepSeek Coder
llm = LLMHandler(model="deepseek-coder")

# Oppure usa Phi (più veloce)
llm = LLMHandler(model="phi")
```

### Verificare Modelli Disponibili

```bash
ollama list
```

## 🔄 Modalità di Funzionamento

HAL 9000 usa una strategia a cascata:

1. **LLM Locale (Ollama)** - Se disponibile, genera risposte intelligenti
2. **Knowledge Base** - Fallback con risposte predefinite
3. **Risposta Generica** - Se nessuna delle precedenti funziona

## 🧪 Test

### Verifica che Ollama funzioni:

```bash
curl http://localhost:11434/api/tags
```

Dovresti vedere la lista dei modelli installati.

### Test con HAL 9000:

1. Avvia Ollama: `ollama serve`
2. Avvia HAL 9000
3. Chiedi qualcosa come: "Spiegami le list comprehension in Python"

Se vedi "Using LLM for query" nei log, sta funzionando! 🎉

## 📊 Confronto Modelli

| Modello | Dimensione | Velocità | Qualità Codice | RAM Richiesta |
|---------|-----------|----------|----------------|---------------|
| phi | 2.7B | ⚡⚡⚡⚡⚡ | ⭐⭐⭐ | 4GB |
| codellama | 7B | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 8GB |
| deepseek-coder | 6.7B | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ | 8GB |
| mistral | 7B | ⚡⚡⚡ | ⭐⭐⭐⭐ | 8GB |
| codellama:13b | 13B | ⚡⚡ | ⭐⭐⭐⭐⭐ | 16GB |

## 🔧 Troubleshooting

### Ollama non si avvia
```bash
# Verifica che non ci siano altri processi
ps aux | grep ollama

# Riavvia il servizio
killall ollama
ollama serve
```

### Modello troppo lento
- Usa un modello più piccolo (phi o codellama base)
- Chiudi altre applicazioni per liberare RAM
- Considera di usare la knowledge base invece dell'LLM

### Errore "model not found"
```bash
# Scarica il modello
ollama pull codellama
```

### HAL usa sempre la knowledge base
- Verifica che Ollama sia in esecuzione: `curl http://localhost:11434`
- Controlla i log di Flask per vedere "Ollama available: True"
- Assicurati di aver scaricato almeno un modello

## 🎯 Vantaggi LLM Locale

✅ **Privacy** - Tutto rimane sul tuo computer
✅ **Offline** - Funziona senza internet
✅ **Veloce** - Nessuna latenza di rete
✅ **Gratuito** - Nessun costo API
✅ **Personalizzabile** - Puoi scegliere il modello

## 📝 Note

- Il primo avvio di un modello può richiedere qualche secondo
- I modelli vengono memorizzati in `~/.ollama/models`
- Puoi avere più modelli installati e switchare tra loro
- HAL 9000 funziona anche senza Ollama (usa la knowledge base)

## 🔗 Risorse

- Ollama: https://ollama.ai
- Modelli disponibili: https://ollama.ai/library
- CodeLlama: https://ollama.ai/library/codellama
- DeepSeek Coder: https://ollama.ai/library/deepseek-coder

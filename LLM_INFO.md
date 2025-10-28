# 🤖 CAP 9000 - Modello AI: CodeLlama

## 📊 Architettura

### **CAP 9000 usa esclusivamente CodeLlama**

**IMPORTANTE:** CAP 9000 è specializzato per programmazione e usa solo CodeLlama:

```
┌─────────────────────────────────────┐
│         OLLAMA                      │
│  (Server/Engine LLM)                │
│  - Gestisce modelli                 │
│  - API REST localhost:11434         │
│  - Runtime per inferenza            │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│       CODELLAMA                     │
│  (Modello AI specifico)             │
│  - Model file ~3.8 GB               │
│  - Specializzato per coding         │
│  - Eseguito da Ollama               │
└─────────────────────────────────────┘
```

### **Analogia:**

```
Ollama : CodeLlama = Docker : Container Image

- Ollama è il RUNTIME (come Docker)
- CodeLlama è il MODELLO (come un'immagine Docker)
```

## 🔍 Configurazione Attuale

### **File: `app.py` (linea 17)**

```python
# Initialize LLM handler (prova prima codellama, poi altri modelli)
llm = LLMHandler(model="codellama")
```

✅ **CORRETTO** - Stiamo usando **CodeLlama** come modello

### **File: `llm_handler.py` (linea 11)**

```python
def __init__(self, model="codellama", ollama_url="http://localhost:11434"):
    """
    Inizializza l'handler LLM
    
    Args:
        model: Nome del modello Ollama (codellama, llama2, mistral, ecc.)
        ollama_url: URL del server Ollama
    """
    self.model = model
    self.ollama_url = ollama_url
```

✅ **CORRETTO** - Default è **CodeLlama**, Ollama è solo il server

## 📝 Come Funziona

### **1. Avvio Ollama (Server)**

```bash
ollama serve
# Avvia server su localhost:11434
```

### **2. Download Modello CodeLlama**

```bash
ollama pull codellama
# Scarica model file ~3.8 GB
# Salvato in ~/.ollama/models/
```

### **3. CAP 9000 Usa CodeLlama**

```python
# CAP 9000 si connette a Ollama
llm = LLMHandler(model="codellama")

# Ollama carica CodeLlama
# Ollama esegue inferenza
# CAP 9000 riceve risposta
```

## 🎯 Modello Utilizzato

### **CodeLlama 7B - Specializzato per Programmazione**

| Caratteristica | Dettaglio |
|----------------|-----------|
| **Nome** | CodeLlama |
| **Versione** | 7B (7 miliardi parametri) |
| **Dimensione** | 3.8 GB |
| **Sviluppatore** | Meta AI |
| **Specializzazione** | Programmazione |
| **Qualità** | ⭐⭐⭐⭐ |
| **Velocità** | ⚡⚡⚡⚡ |
| **RAM Richiesta** | 8 GB |
| **Lingue Supportate** | Python, Java, JavaScript, C, C++, Go, e altri |

### **Perché Solo CodeLlama?**

✅ **Specializzato per coding** - Addestrato specificamente su codice  
✅ **Ottimo equilibrio** - Qualità/velocità/dimensione  
✅ **Affidabile** - Sviluppato da Meta AI  
✅ **Efficiente** - Funziona bene su hardware consumer  
✅ **Completo** - Supporta tutti i linguaggi principali  
✅ **Consistente** - Risposte uniformi e prevedibili

## ⚙️ Configurazione

### **CAP 9000 è pre-configurato con CodeLlama**

Non è necessario configurare il modello. CAP 9000 usa automaticamente CodeLlama.

**Installazione CodeLlama:**

```bash
# Scarica il modello (una volta sola)
ollama pull codellama

# Verifica installazione
ollama list
```

**Configurazione avanzata (opzionale):**

```python
# llm_handler.py - Modifica URL Ollama se necessario
def __init__(self, ollama_url="http://localhost:11434"):
    # Cambia porta se Ollama usa porta diversa
    pass
```

## 🧪 Test Modello Attuale

### **Verifica quale modello è attivo:**

```bash
# Lista modelli installati
ollama list

# Output:
# NAME              ID           SIZE    MODIFIED
# codellama:latest  8fdf8f752f6e 3.8 GB  2 days ago
```

### **Test risposta:**

```bash
# Test diretto con Ollama
ollama run codellama "Write a Python hello world"

# Test via CAP 9000
# Apri app e chiedi: "Write a Python hello world"
```

## 📊 Performance CodeLlama

### **Prestazioni Tipiche**

| Metrica | Valore |
|---------|--------|
| **Velocità** | 4-8 token/sec |
| **Latenza Prima Risposta** | 1-2 secondi |
| **RAM Utilizzata** | 6-8 GB |
| **Qualità Codice** | ⭐⭐⭐⭐ |
| **Accuratezza** | 85-90% |
| **Lingue Supportate** | 15+ linguaggi |

### **Punti di Forza**

✅ **Generazione Codice** - Produce codice pulito e funzionante  
✅ **Debugging** - Identifica e corregge errori efficacemente  
✅ **Spiegazioni** - Spiega concetti in modo chiaro  
✅ **Best Practices** - Suggerisce pattern e convenzioni  
✅ **Multi-lingua** - Supporta tutti i linguaggi principali  
✅ **Velocità** - Risposte rapide anche su hardware consumer

### **Ottimizzazioni CAP 9000**

CAP 9000 migliora CodeLlama con:

- 🔍 **RAG System** - Documentazioni ufficiali integrate
- 📚 **Best Practices** - Database pattern hardcoded
- 🌍 **Multi-lingua** - Risposte in 8 lingue
- 💾 **Caching** - Ottimizzazione memoria
- ⚡ **Streaming** - Output progressivo real-time

## 🔧 Troubleshooting

### **Problema: "Ollama not available"**

```bash
# Verifica Ollama running
ps aux | grep ollama

# Se non running, avvia
ollama serve
```

### **Problema: "Model not found"**

```bash
# Scarica model
ollama pull codellama

# Verifica installato
ollama list
```

### **Problema: "Out of memory"**

```bash
# Usa model più piccolo
ollama pull phi3

# Modifica app.py
llm = LLMHandler(model="phi3")
```

## 📝 Conclusione

**Stato Attuale:**
- ✅ Ollama: Server LLM (runtime)
- ✅ CodeLlama: Modello AI (coding specialist)
- ✅ Configurazione corretta
- ✅ Nessuna modifica necessaria

**Ollama NON è un modello, è il server che esegue CodeLlama!**

---

**Per domande:** antonio.web2music@gmail.com

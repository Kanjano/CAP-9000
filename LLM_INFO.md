# 🤖 CAP 9000 - Informazioni LLM

## 📊 Architettura Attuale

### **Ollama vs CodeLlama: Chiarimento**

**IMPORTANTE:** Non c'è confusione! L'architettura è corretta:

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

## 🎯 Modelli Disponibili

### **Modelli Coding (Raccomandati)**

| Modello | Dimensione | Qualità | Velocità | Uso RAM |
|---------|------------|---------|----------|---------|
| **codellama** | 3.8 GB | ⭐⭐⭐⭐ | ⚡⚡⚡⚡ | 8 GB |
| codellama:13b | 7.0 GB | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | 16 GB |
| codellama:34b | 19 GB | ⭐⭐⭐⭐⭐ | ⚡⚡ | 32 GB |
| qwen2.5-coder:7b | 4.5 GB | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⭐ | 10 GB |
| deepseek-coder:6.7b | 3.8 GB | ⭐⭐⭐⭐ | ⚡⚡⚡⚡ | 8 GB |

### **Modelli General Purpose**

| Modello | Dimensione | Qualità | Velocità |
|---------|------------|---------|----------|
| llama2 | 3.8 GB | ⭐⭐⭐ | ⚡⚡⚡⚡ |
| mistral | 4.1 GB | ⭐⭐⭐⭐ | ⚡⚡⚡ |
| phi3 | 2.3 GB | ⭐⭐⭐ | ⚡⚡⚡⚡⚡ |

## 🔄 Cambiare Modello

### **Metodo 1: Modifica Codice**

```python
# app.py linea 17
llm = LLMHandler(model="qwen2.5-coder:7b")  # Cambia qui
```

### **Metodo 2: Variabile Ambiente**

```bash
export CAP9000_MODEL="qwen2.5-coder:7b"
```

```python
# app.py
import os
model = os.getenv('CAP9000_MODEL', 'codellama')
llm = LLMHandler(model=model)
```

### **Metodo 3: Config File**

```json
// config.json
{
  "llm": {
    "model": "qwen2.5-coder:7b",
    "ollama_url": "http://localhost:11434"
  }
}
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

## 📊 Performance Comparison

### **CodeLlama 7B (Attuale)**

```
✅ Pros:
- Ottimizzato per coding
- Veloce (4-8 token/sec)
- RAM moderata (8 GB)
- Buona qualità risposte

⚠️ Cons:
- Meno generale di GPT
- Limitato a coding tasks
```

### **Qwen2.5-Coder 7B (Alternativa)**

```
✅ Pros:
- Migliore qualità coding
- Più aggiornato
- Supporta più linguaggi
- Veloce

⚠️ Cons:
- Dimensione maggiore (4.5 GB)
- RAM maggiore (10 GB)
```

## 🎯 Raccomandazioni

### **Per Sviluppo Normale:**
```
✅ CodeLlama 7B (attuale)
- Perfetto equilibrio
- Veloce e accurato
- RAM accessibile
```

### **Per Qualità Massima:**
```
⭐ Qwen2.5-Coder 7B
- Migliori risposte
- Più aggiornato
- Vale la RAM extra
```

### **Per Hardware Limitato:**
```
💡 Phi-3 3.8B
- Solo 2.3 GB
- Velocissimo
- Qualità accettabile
```

### **Per Professionisti:**
```
🚀 CodeLlama 34B
- Qualità eccezionale
- Richiede 32 GB RAM
- Più lento
```

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

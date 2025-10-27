# 📚 CAP 9000 - Local Documentation Setup

## Overview

CAP 9000 supporta **documentazioni ufficiali locali** per funzionamento completamente offline con risposte più accurate e dettagliate.

## 🎯 Come Funziona

### **Sistema a 3 Livelli:**

1. **Documentazione Locale** (Priorità 1)
   - Docs ufficiali scaricate in locale
   - Snippet rilevanti estratti automaticamente
   - ~2000 caratteri per risposta
   - ✅ Massima accuratezza

2. **Best Practices Hardcoded** (Priorità 2)
   - 60+ best practices integrate
   - 30+ code patterns comuni
   - ✅ Sempre disponibili

3. **Fallback Generico** (Priorità 3)
   - Risposta base se tutto fallisce
   - ✅ Garantisce sempre una risposta

## 📥 Download Documentazioni

### **Setup Iniziale (Una Tantum):**

```bash
# 1. Installa dipendenze
pip install beautifulsoup4

# 2. Scarica documentazioni ufficiali
python download_docs.py
```

### **Cosa Viene Scaricato:**

- **Python**: Tutorial, Library, Reference, PEP 8
- **Java**: Tutorial, API Reference
- **JavaScript**: MDN Guide, Reference
- **C++**: Language, Containers, Algorithms
- **Go**: Effective Go, Tour

### **Dimensioni:**
- ~5-10 MB per linguaggio
- ~30-50 MB totali
- Scaricamento: ~5-10 minuti

## 🚀 Utilizzo

### **Con Documentazioni Locali:**

```bash
# Avvia normalmente
./run.sh

# Output:
# ✓ Local documentation found in local_docs
#   → Loaded 5 language docs
```

### **Senza Documentazioni Locali:**

```bash
# Avvia normalmente
./run.sh

# Output:
# ⚠ No local docs found. Using hardcoded fallback.
#   Run 'python download_docs.py' to download docs for offline use.
```

**Funziona comunque!** Usa best practices hardcoded.

## 📊 Vantaggi Docs Locali

### **Con Docs Locali:**
- ✅ Risposte più accurate
- ✅ Snippet da docs ufficiali
- ✅ Contesto più ricco
- ✅ 100% offline
- ✅ Zero latenza
- ✅ Privacy totale

### **Senza Docs Locali:**
- ✅ Funziona comunque
- ✅ Best practices disponibili
- ✅ Code patterns disponibili
- ⚠️ Meno dettagliato

## 🔍 Esempio Confronto

### **Query:** "Come leggere un file in Python?"

#### **Con Docs Locali:**
```
=== OFFICIAL PYTHON DOCUMENTATION (LOCAL) ===
The with statement simplifies exception handling by encapsulating
common preparation and cleanup tasks. In addition, it will
automatically close the file. The with statement provides a way
for ensuring that a clean-up code is always executed...

[2000 caratteri di docs ufficiali]

=== BEST PRACTICES FOR PYTHON ===
• Use context managers (with statement) for resource management
• Handle exceptions specifically, avoid bare except
...
```

#### **Senza Docs Locali:**
```
=== BEST PRACTICES FOR PYTHON ===
• Use context managers (with statement) for resource management
• Handle exceptions specifically, avoid bare except
...

=== RELEVANT CODE PATTERNS ===
File Reading:
```python
with open(file) as f: content = f.read()
```

=== OFFICIAL DOCUMENTATION ===
Reference: https://docs.python.org/3/
```

## 🗂️ Struttura File

```
windsurf-project/
├── download_docs.py          # Script download
├── rag_system.py             # Sistema RAG aggiornato
└── local_docs/               # Docs scaricate
    ├── index.json            # Indice
    ├── python/
    │   ├── tutorial.txt
    │   ├── library.txt
    │   ├── reference.txt
    │   └── pep8.txt
    ├── java/
    │   ├── tutorial.txt
    │   └── api.txt
    ├── javascript/
    │   ├── guide.txt
    │   └── reference.txt
    ├── cpp/
    │   ├── language.txt
    │   ├── container.txt
    │   └── algorithm.txt
    └── go/
        ├── effective_go.txt
        └── tour.txt
```

## 🔧 Aggiornamento Docs

```bash
# Ri-scarica docs aggiornate
rm -rf local_docs/
python download_docs.py
```

## ⚙️ Configurazione

### **Modifica Dimensione Snippet:**

In `rag_system.py`:
```python
# Linea 65: Cambia 5000 per più/meno contesto
content = f.read(5000)  # Caratteri per file

# Linea 299: Cambia 2000 per snippet più/meno lunghi
return content[:2000]  # Caratteri per snippet
```

### **Aggiungi Nuove Docs:**

In `download_docs.py`:
```python
def download_rust_docs(self):
    rust_docs = {
        'book': 'https://doc.rust-lang.org/book/',
        'reference': 'https://doc.rust-lang.org/reference/',
    }
    # ... implementazione
```

## 🎯 Best Practices

1. **Scarica docs una volta** durante setup
2. **Aggiorna periodicamente** (ogni 3-6 mesi)
3. **Verifica spazio disco** (~50 MB)
4. **Backup local_docs/** se importante

## 🐛 Troubleshooting

### **Errore durante download:**
```bash
# Riprova con timeout più lungo
# Modifica download_docs.py linea timeout=30 -> timeout=60
```

### **Docs non vengono usate:**
```bash
# Verifica presenza
ls local_docs/index.json

# Se manca, ri-scarica
python download_docs.py
```

### **Errore lettura docs:**
```bash
# Verifica permessi
chmod -R 755 local_docs/
```

## 📈 Performance

- **Caricamento docs**: ~100ms (una volta all'avvio)
- **Lettura snippet**: ~10ms per query
- **Overhead totale**: ~10-20ms per risposta
- **Beneficio**: Risposte molto più accurate

## 🔒 Privacy

- ✅ Download una tantum (con internet)
- ✅ Uso completamente offline
- ✅ Nessun tracking
- ✅ Docs sul tuo computer
- ✅ Zero telemetria

## 📝 Note

- Docs scaricate sono **testo puro** (no HTML)
- **Rate limiting** durante download (1s tra richieste)
- **Fallback automatico** se docs non disponibili
- **Compatibile** con versione precedente

## ✅ Conclusione

Il sistema è **completamente opzionale**:
- ✅ Con docs: Risposte migliori
- ✅ Senza docs: Funziona comunque

**Raccomandato:** Scarica docs per esperienza ottimale offline!

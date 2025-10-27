# 🔴 HAL 9000 Code Assistant

Un assistente di programmazione desktop standalone ispirato a HAL 9000 di "2001: Odissea nello Spazio".

![HAL 9000](https://img.shields.io/badge/HAL-9000-red?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge)
![Electron](https://img.shields.io/badge/Electron-Latest-47848F?style=for-the-badge)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge)

## ✨ Caratteristiche

### 🖥️ **Applicazione Desktop Standalone**
- Nessun browser richiesto
- Funziona completamente offline
- Cross-platform (macOS, Windows, Linux)
- Backend Flask integrato

### 🤖 **Intelligenza Artificiale**
- **LLM Locale** via Ollama (CodeLlama, DeepSeek Coder, ecc.)
- **Knowledge Base** integrata come fallback
- Risposte contestuali e intelligenti
- Privacy totale - tutto rimane sul tuo computer

### 🌍 **Multilingua**
Interfaccia disponibile in 8 lingue europee:
- 🇬🇧 English
- 🇮🇹 Italiano
- 🇫🇷 Français
- 🇩🇪 Deutsch
- 🇪🇸 Español
- 🇵🇹 Português
- 🇳🇱 Nederlands
- 🇵🇱 Polski

### 💻 **Linguaggi di Programmazione Supportati**
- Python
- Java
- JavaScript
- C
- C++
- Go

### 🎨 **Design HAL 9000**
- Occhio rosso iconico pulsante
- Tema scuro con effetti glow
- Interfaccia chat moderna
- Citazioni dal film

## 🚀 Installazione Rapida

### Prerequisiti
- **Python 3.9+**
- **Node.js 16+**
- **Ollama** (opzionale, per LLM locale)

### 1. Clona il Repository
```bash
git clone <your-repo>
cd windsurf-project
```

### 2. Installa Dipendenze Python
```bash
pip3 install flask flask-cors requests
```

### 3. Installa Dipendenze Node.js
```bash
cd frontend
npm install
```

### 4. Build Frontend
```bash
npm run build
```

### 5. Avvia l'Applicazione
```bash
npm run electron:dev
```

## 🤖 Setup LLM Locale (Consigliato)

Per risposte intelligenti, installa Ollama:

### Installa Ollama
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: scarica da https://ollama.ai
```

### Scarica un Modello
```bash
# CodeLlama (consigliato per programmazione)
ollama pull codellama

# Oppure DeepSeek Coder
ollama pull deepseek-coder

# Oppure Phi (veloce e leggero)
ollama pull phi
```

### Avvia Ollama
```bash
ollama serve
```

**Vedi [SETUP_LLM.md](SETUP_LLM.md) per dettagli completi**

## 📦 Creazione Pacchetto Installabile

### macOS
```bash
cd frontend
npm run package:mac
```
Genera: `frontend/release/HAL 9000 Code Assistant.dmg`

### Windows
```bash
npm run package:win
```
Genera: `frontend/release/HAL 9000 Code Assistant Setup.exe`

### Linux
```bash
npm run package:linux
```
Genera: `frontend/release/HAL 9000 Code Assistant.AppImage`

## 🎯 Utilizzo

1. **Avvia l'app** - Doppio click sull'icona o `npm run electron:dev`
2. **Seleziona lingua interfaccia** - Clicca sull'icona 🌍
3. **Seleziona linguaggio programmazione** - Python, Java, JavaScript, ecc.
4. **Fai una domanda** - "Spiegami le list comprehension in Python"
5. **Ricevi risposta intelligente** - HAL 9000 ti risponderà con esempi di codice

### Esempi di Domande

**Python:**
- "Spiegami le variabili in Python"
- "Come funzionano le funzioni lambda?"
- "Cosa sono le list comprehension?"

**JavaScript:**
- "Differenza tra let e const"
- "Come funziona async/await?"
- "Spiegami le arrow functions"

**Java:**
- "Come si dichiarano le variabili?"
- "Cosa sono le classi in Java?"
- "Spiegami i metodi"

## 🏗️ Architettura

```
windsurf-project/
├── main.py              # CodeAssistant core
├── languages.py         # Linguaggi supportati
├── app.py              # Backend Flask API
├── llm_handler.py      # Handler LLM locale
├── knowledge_base.py   # Database risposte predefinite
├── frontend/
│   ├── electron/
│   │   ├── main.js     # Processo principale Electron
│   │   └── preload.js  # Script preload IPC
│   ├── src/
│   │   ├── App.jsx     # Componente React principale
│   │   ├── i18n/
│   │   │   └── translations.js  # Traduzioni
│   │   └── index.css   # Stili globali
│   └── dist/           # Build production
└── README.md
```

## 🔄 Modalità di Funzionamento

HAL 9000 usa una strategia intelligente a cascata:

1. **LLM Locale (Ollama)** ⚡
   - Se disponibile, genera risposte contestuali
   - Usa modelli come CodeLlama o DeepSeek Coder
   - Privacy totale, tutto offline

2. **Knowledge Base** 📚
   - Fallback con risposte predefinite
   - Copre argomenti comuni di programmazione
   - Veloce e affidabile

3. **Risposta Generica** 💬
   - Se nessuna delle precedenti funziona
   - Suggerisce argomenti disponibili

## 🛠️ Sviluppo

### Struttura Comandi

```bash
# Sviluppo frontend (con hot reload)
cd frontend
npm run dev

# Sviluppo Electron
npm run electron:dev

# Build production
npm run build

# Package per distribuzione
npm run package:mac    # macOS
npm run package:win    # Windows
npm run package:linux  # Linux
```

### Modificare il Modello LLM

Modifica `app.py`:

```python
# Cambia modello
llm = LLMHandler(model="deepseek-coder")  # invece di codellama
```

### Aggiungere una Lingua

1. Modifica `frontend/src/i18n/translations.js`
2. Aggiungi le traduzioni nel formato esistente
3. Rebuild: `npm run build`

### Aggiungere un Linguaggio di Programmazione

1. Modifica `languages.py`
2. Aggiungi risposte in `knowledge_base.py` (opzionale)
3. Riavvia l'app

## 📊 Requisiti di Sistema

### Minimi
- **RAM**: 4GB
- **Spazio**: 2GB (senza LLM)
- **CPU**: Dual-core

### Consigliati (con LLM)
- **RAM**: 8GB+
- **Spazio**: 8GB (include modelli LLM)
- **CPU**: Quad-core

## 🔧 Troubleshooting

### L'app non si avvia
```bash
# Verifica Python
python3 --version

# Verifica Flask
pip3 list | grep -i flask

# Reinstalla dipendenze
cd frontend && npm install
```

### Ollama non funziona
```bash
# Verifica servizio
curl http://localhost:11434/api/tags

# Riavvia Ollama
killall ollama
ollama serve
```

### Porta 5001 occupata
Modifica `app.py`:
```python
app.run(debug=True, port=5002)  # Cambia porta
```

E `frontend/electron/main.js`:
```javascript
const response = await fetch('http://127.0.0.1:5002/api/query', {
```

## 📝 Documentazione

- **[GUIDA_RAPIDA.md](GUIDA_RAPIDA.md)** - Guida rapida in italiano
- **[SETUP_LLM.md](SETUP_LLM.md)** - Setup completo LLM locale
- **[README_DESKTOP.md](README_DESKTOP.md)** - Documentazione app desktop

## 🎬 Citazioni HAL 9000

> "Good afternoon. I am HAL 9000, your code assistant. How may I help you?"

> "This mission is too important for me to allow you to jeopardize it."

> "I'm afraid I can't do that, Dave." (in caso di errori)

## 🤝 Contributi

Contributi benvenuti! Aree di miglioramento:
- Nuovi linguaggi di programmazione
- Più traduzioni
- Miglioramenti UI/UX
- Ottimizzazioni performance
- Nuovi modelli LLM

## 📄 Licenza

Progetto educativo ispirato a "2001: A Space Odyssey" di Stanley Kubrick.

## 🙏 Ringraziamenti

- Stanley Kubrick per HAL 9000
- Ollama per i modelli LLM locali
- Electron per il framework desktop
- React e TailwindCSS per l'UI

---

**Fatto con ❤️ e ispirato da 🔴 HAL 9000**

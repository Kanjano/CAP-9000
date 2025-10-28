# 🔴 CAP 9000 - Cognitive Assistance Program

> *"I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do."* - HAL 9000

Un assistente di programmazione AI desktop standalone ispirato a HAL 9000 di "2001: Odissea nello Spazio".

![HAL 9000](https://img.shields.io/badge/HAL-9000-red?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge)
![Electron](https://img.shields.io/badge/Electron-Latest-47848F?style=for-the-badge)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge)
![CodeLlama](https://img.shields.io/badge/CodeLlama-7B-orange?style=for-the-badge)
![Mistral](https://img.shields.io/badge/Mistral-NLU-purple?style=for-the-badge)

## ✨ Caratteristiche

### 🖥️ **Applicazione Desktop Standalone**
- Nessun browser richiesto
- Funziona completamente offline
- Cross-platform (macOS, Windows, Linux)
- Backend Flask integrato

### 🤖 **Intelligenza Artificiale Dual-Model**
- **CodeLlama 7B** - Specializzato per generazione codice
- **Mistral** - Comprensione linguaggio naturale (NLU)
- **Sistema RAG** - Documentazioni ufficiali integrate
- **Query Enhancement** - Migliora comprensione domande
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

**Metodo Semplice (Raccomandato):**
```bash
./scripts/start_cap9000.sh
```

Lo script unificato:
- ✅ Verifica tutti i prerequisiti (Python, Node.js, Ollama)
- ✅ Installa dipendenze mancanti
- ✅ Avvia Ollama se necessario
- ✅ Scarica CodeLlama se non presente
- ✅ Avvia backend Flask
- ✅ Serve frontend
- ✅ Apre browser automaticamente

**Arresto:**
```bash
./scripts/stop_cap9000.sh
# Oppure CTRL+C nello script di avvio
```

**Metodo Manuale (per sviluppatori):**
```bash
# Terminal 1: Backend
python3 app.py

# Terminal 2: Frontend dev (opzionale)
cd frontend
npm run dev
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

Tutta la documentazione è organizzata nella cartella **[`docs/`](docs/)**:

### 🚀 Guide Utente
- **[Avvio Rapido](docs/guides/AVVIO_RAPIDO.md)** - Start qui!
- **[Guida Completa](docs/guides/GUIDA_RAPIDA.md)** - Tutorial dettagliato
- **[App Desktop](docs/guides/README_DESKTOP.md)** - Guida desktop
- **[Tema HAL 9000](docs/guides/README_HAL9000.md)** - Design e citazioni

### ⚙️ Setup
- **[Configurazione Ollama](docs/setup/CONFIGURAZIONE_OLLAMA.md)** - Setup Ollama
- **[Setup LLM](docs/setup/SETUP_LLM.md)** - Configurazione modelli
- **[Info Modelli](docs/setup/LLM_INFO.md)** - CodeLlama & Mistral

### 🚀 Deployment
- **[Hosting Guide](docs/deployment/HOSTING_GUIDE.md)** - Deploy website
- **[Netlify](docs/deployment/NETLIFY_DEPLOY.md)** - Deploy su Netlify
- **[Installer](docs/deployment/INSTALLER_README.md)** - Creare installer

### 🔧 Tecnica
- **[Sistema RAG](docs/technical/RAG_DOCUMENTATION.md)** - Documentazione RAG
- **[Architettura](docs/technical/README_COMPLETE.md)** - Doc completa

## 📁 Struttura Progetto

```
CAP-9000/
├── 📄 README.md                    # Questo file
├── 📄 CHANGELOG.md                 # Storia modifiche
├── 📄 LICENSE                      # Licenza MIT
│
├── 📂 docs/                        # 📚 Documentazione
│   ├── guides/                     # Guide utente
│   ├── setup/                      # Setup e configurazione
│   ├── deployment/                 # Deploy e distribuzione
│   └── technical/                  # Documentazione tecnica
│
├── 📂 scripts/                     # 🔧 Script utility
│   ├── start_cap9000.sh           # Avvio applicazione
│   ├── stop_cap9000.sh            # Stop applicazione
│   ├── create_installers.sh       # Crea installer
│   └── installer_wizard.sh        # Wizard installazione
│
├── 📂 frontend/                    # ⚛️ Frontend React + Electron
│   ├── src/                       # Codice sorgente
│   ├── electron/                  # Electron main process
│   └── dist/                      # Build production
│
├── 📂 website/                     # 🌐 Landing page
│   ├── index.html                 # Landing page
│   ├── downloads/                 # Installer scaricabili
│   └── netlify.toml              # Config Netlify
│
├── 📂 build-resources/            # 🎨 Risorse build
│   └── icons/                     # Icone applicazione
│
├── 🐍 Backend Python
│   ├── app.py                     # Flask server
│   ├── llm_handler.py            # Gestione LLM
│   ├── query_enhancer.py         # Query enhancement (NLU)
│   ├── rag_system.py             # Sistema RAG
│   ├── knowledge_base.py         # Knowledge base
│   ├── language_detector.py      # Rilevamento lingua
│   └── requirements.txt          # Dipendenze Python
│
└── 📦 Configurazione
    ├── package.json              # Dipendenze Node.js
    └── .gitignore               # Git ignore
```

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

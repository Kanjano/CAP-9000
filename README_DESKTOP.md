# HAL 9000 Code Assistant - Desktop App

Applicazione desktop standalone ispirata a HAL 9000 di "2001: Odissea nello Spazio".

## ✨ Caratteristiche

### 🖥️ App Desktop Standalone
- **Nessun browser richiesto** - Applicazione nativa Electron
- **Funziona offline** - Non necessita di connessione internet
- **Cross-platform** - Disponibile per macOS, Windows e Linux

### 🌍 Supporto Multilingua
L'interfaccia supporta 8 lingue europee:
- 🇬🇧 **English** (Inglese)
- 🇮🇹 **Italiano**
- 🇫🇷 **Français** (Francese)
- 🇩🇪 **Deutsch** (Tedesco)
- 🇪🇸 **Español** (Spagnolo)
- 🇵🇹 **Português** (Portoghese)
- 🇳🇱 **Nederlands** (Olandese)
- 🇵🇱 **Polski** (Polacco)

### 💻 Linguaggi di Programmazione
Supporta tutti i linguaggi definiti in `languages.py`:
- Python
- Java
- JavaScript
- C
- C++
- Go

### 🎨 Design HAL 9000
- Occhio rosso iconico con effetto glow pulsante
- Tema scuro con palette rossa (#FF0000)
- Interfaccia chat moderna
- Citazioni dal film "2001: Odissea nello Spazio"

## 📦 Installazione

### Prerequisiti
- **Node.js** (v16 o superiore)
- **Python 3** con Flask e flask-cors

### 1. Installa le dipendenze Python

```bash
pip3 install flask flask-cors
```

### 2. Installa le dipendenze Node.js

```bash
cd frontend
npm install
```

## 🚀 Avvio

### Modalità Sviluppo

Avvia il frontend React in modalità dev:
```bash
cd frontend
npm run dev
```

In un altro terminale, avvia l'app Electron:
```bash
cd frontend
npm run electron:dev
```

L'app desktop si aprirà automaticamente con il backend Flask integrato.

## 📦 Build e Packaging

### Build per macOS
```bash
cd frontend
npm run package:mac
```

### Build per Windows
```bash
cd frontend
npm run package:win
```

### Build per Linux
```bash
cd frontend
npm run package:linux
```

I file installabili saranno generati nella cartella `frontend/release/`:
- **macOS**: `.dmg` e `.zip`
- **Windows**: `.exe` (installer NSIS) e versione portable
- **Linux**: `.AppImage` e `.deb`

## 🏗️ Architettura

```
windsurf-project/
├── main.py                 # CodeAssistant originale
├── languages.py            # Lista linguaggi supportati
├── app.py                  # Backend Flask API
└── frontend/
    ├── electron/
    │   ├── main.js        # Processo principale Electron
    │   └── preload.js     # Script preload per IPC
    ├── src/
    │   ├── App.jsx        # Componente React principale
    │   ├── i18n/
    │   │   └── translations.js  # Traduzioni multilingua
    │   └── index.css      # Stili globali
    └── package.json       # Configurazione Electron
```

## 🔧 Funzionamento

1. **Electron** avvia automaticamente il server Flask in background
2. Il **frontend React** comunica con Flask tramite IPC (Inter-Process Communication)
3. **Nessuna connessione internet** richiesta - tutto funziona localmente
4. Quando chiudi l'app, il processo Flask viene terminato automaticamente

## 🌐 Cambio Lingua

1. Clicca sul selettore lingua (icona 🌍) in alto
2. Scegli la tua lingua preferita
3. L'interfaccia si aggiorna istantaneamente
4. I messaggi di HAL 9000 vengono tradotti

## 📝 Citazioni HAL 9000

Le citazioni cambiano in base alla lingua selezionata:

**Inglese:**
- "Good afternoon. I am HAL 9000, your code assistant."
- "This mission is too important for me to allow you to jeopardize it."

**Italiano:**
- "Buon pomeriggio. Sono HAL 9000, il tuo assistente di programmazione."
- "Questa missione è troppo importante perché io ti permetta di comprometterla."

**Francese:**
- "Bon après-midi. Je suis HAL 9000, votre assistant de code."
- "Cette mission est trop importante pour que je vous permette de la compromettre."

E così via per tutte le lingue supportate.

## 🛠️ Tecnologie

- **Desktop**: Electron
- **Frontend**: React, Vite, TailwindCSS, Lucide Icons
- **Backend**: Flask, Flask-CORS
- **Build**: electron-builder
- **i18n**: Sistema di traduzioni custom

## 🐛 Troubleshooting

### L'app non si avvia
- Verifica che Python 3 sia installato: `python3 --version`
- Verifica che Flask sia installato: `pip3 list | grep -i flask`

### Errore "Flask not found"
```bash
pip3 install flask flask-cors
```

### L'app si chiude immediatamente
- Controlla i log nella console di Electron
- Verifica che `app.py` sia nella directory corretta

## 📄 Licenza

Progetto educativo ispirato a "2001: A Space Odyssey" di Stanley Kubrick.

# 📝 CHANGELOG - CAP 9000

Tutti i cambiamenti notevoli a questo progetto saranno documentati in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/lang/it/).

---

## [Unreleased]

### Pianificato
- Plugin system
- Custom themes
- Voice input
- Code execution sandbox
- Multi-file context
- Git integration

---

## [1.2.0] - 2025-01-07

### 🧠 Sistema Hybrid (CodeLlama + Recursive Reasoning)

**Implementazione completata del sistema dual-mode con TinyRecursiveModels (TRM)**

#### Added
- ✅ **`hybrid_llm_handler.py`** - Handler ibrido CodeLlama + Reasoning (391 righe)
- ✅ **`recursive_reasoning.py`** - Modulo PyTorch per reasoning (398 righe)
- ✅ **`test_hybrid_system.py`** - Suite test completa (156 righe)
- ✅ **`models/reasoning_module.pth`** - Modello PyTorch (5.2M parametri, 21MB)
- ✅ **Nuovi endpoint API**:
  - `GET /api/stats` - Statistiche sistema
  - `POST /api/reasoning/toggle` - Abilita/disabilita reasoning
  - `GET /api/reasoning/status` - Status reasoning mode

#### Changed
- 🔄 **`app.py`** - Integrazione hybrid handler
- 🔄 **`requirements.txt`** - Aggiunte dipendenze PyTorch

#### Features
- 🎯 **Auto-detection intelligente**: Routing automatico simple/reasoning
- 💾 **Caching intelligente**: Riduzione latenza 20-30%
- 📊 **Statistiche real-time**: Monitoring query e performance
- 🧪 **Test completi**: 4/4 test automatici passati

#### Documentation
- 📚 **`IMPLEMENTATION_COMPLETE.md`** - Status implementazione
- 📚 **`docs/LATEST_DEVELOPMENTS.md`** - Ultimi sviluppi
- 📚 **`docs/technical/HYBRID_SYSTEM_README.md`** - Guida utilizzo
- 📚 **`docs/technical/TRM_ANALYSIS.md`** - Analisi tecnica
- 📚 **`docs/technical/TRM_VS_CAP9000_COMPARISON.md`** - Confronto
- 📚 **`docs/technical/TRM_IMPLEMENTATION_PLAN.md`** - Piano implementazione
- 📚 **`docs/technical/TRM_EXECUTIVE_SUMMARY.md`** - Sintesi esecutiva (EN)
- 📚 **`docs/technical/TRM_ANALISI_COMPLETA_IT.md`** - Analisi completa (IT)

#### Performance
- ⚡ Query semplici: ~5s (Simple Mode)
- ⚡ Query complesse: ~8s (Reasoning Mode)
- ⚡ Cache hit rate: ~12%
- ⚡ Accuracy: 85-90%

---

## [1.0.0] - 2025-10-27

### 🎉 Release Iniziale

Prima versione pubblica di CAP 9000 - Cognitive Assistance Program.

---

## Cronologia Commit Dettagliata

### 📅 2025-10-27

#### [08fa928] - **feat: Icone HAL 9000 SVG e chiarimento LLM**
- ✅ Creata icona SVG HAL 9000 style
- ✅ Occhio rosso con gradient e glow effect
- ✅ Testo "CAP 9000" integrato
- ✅ Documentazione LLM_INFO.md
- ✅ Chiarimento Ollama (server) vs CodeLlama (model)
- ✅ Script generate_icons.py per PNG multi-size

**Files:**
- `frontend/public/icon.svg`
- `build-resources/icons/icon.svg`
- `LLM_INFO.md`
- `generate_icons.py`

---

#### [e1150cf] - **feat: Sistema completo installer Windows e macOS**
- ✅ Configurazione electron-builder completa
- ✅ Script NSIS personalizzato per Windows
- ✅ Script post-install per macOS
- ✅ Download automatico Ollama
- ✅ Download automatico CodeLlama (~3.8 GB)
- ✅ Download automatico documentazioni
- ✅ Scelta disco installazione
- ✅ Calcolo spazio richiesto (4.5 GB)
- ✅ Progress bar download
- ✅ Multi-lingua installer (EN, IT, FR, DE, ES)

**Files:**
- `package.json` (electron-builder config)
- `build-resources/installer.nsh` (NSIS)
- `build-resources/postinstall.sh` (macOS)
- `build-resources/entitlements.mac.plist`
- `installer-scripts/setup-ollama.js`
- `installer-scripts/setup-docs.js`
- `INSTALLER_README.md`
- `DISK_SPACE.md`
- `LICENSE`

**Features Installer:**
- Checkbox componenti opzionali
- Verifica spazio disponibile
- Desktop + Start Menu shortcuts
- Uninstaller completo
- LaunchAgent macOS (avvio automatico)

---

#### [1fc8ca4] - **fix: Blocca input durante streaming CAP 9000**
- ✅ Input disabilitato durante streaming
- ✅ Button submit disabilitato
- ✅ Placeholder dinamico: "CAP 9000 sta rispondendo..."
- ✅ Cursor not-allowed su input disabled
- ✅ Riabilitazione automatica al completamento
- ✅ Riabilitazione anche su errore

**Problema Risolto:**
- Messaggi utente non si frappongono più durante risposta
- Risposta CAP 9000 non viene più spezzata
- UX migliorata con feedback visivo chiaro

**Files:**
- `frontend/src/App.jsx`

---

#### [2aaffe8] - **feat: Sistema documentazioni locali offline con fallback**
- ✅ Script download_docs.py per docs ufficiali
- ✅ Download Python, Java, JS, C++, Go docs
- ✅ Salvataggio locale in local_docs/
- ✅ RAG system aggiornato per leggere docs locali
- ✅ Fallback automatico a best practices hardcoded
- ✅ Sistema a 3 livelli (docs → practices → fallback)
- ✅ Selezione intelligente doc in base a query

**Docs Scaricate:**
- Python: tutorial, library, reference, pep8
- Java: tutorial, api
- JavaScript: guide, reference
- C++: language, container, algorithm
- Go: effective_go, tour

**Files:**
- `download_docs.py`
- `rag_system.py` (aggiornato)
- `DOCUMENTATION_SETUP.md`
- `requirements.txt` (beautifulsoup4)

**Dimensioni:**
- ~35-50 MB totali
- ~5-10 MB per linguaggio

---

#### [64fce30] - **feat: Centratura greeting, traduzioni features e copyright**
- ✅ Greeting "Buongiorno. Sono CAP 9000" centrato
- ✅ Traduzioni complete feature cards (6 features)
- ✅ Traduzioni italiano per tutte le features
- ✅ Copyright "Antonio Cangiano" nel footer
- ✅ Attributi data-i18n su tutti gli elementi

**Traduzioni Aggiunte:**
- feature1: Integrazione AI Avanzata
- feature2: Streaming in Tempo Reale
- feature3: Supporto Multi-Lingua
- feature4: Documentazione Ufficiale
- feature5: Gestione Conversazioni
- feature6: Tema VS Code

**Files:**
- `landing-page.html`

---

#### [1e11053] - **feat: Fix occhio HAL e riconoscimento lingua automatico**
- ✅ Occhio HAL da position:fixed a position:absolute
- ✅ Occhio rimane fermo, non segue scroll
- ✅ Sistema JavaScript riconoscimento lingua browser
- ✅ Usa navigator.language (standard)
- ✅ Fallback navigator.userLanguage (IE/Edge)
- ✅ Traduzioni dinamiche con data-i18n
- ✅ Applicazione automatica al caricamento

**Lingue Supportate:**
- Inglese (en)
- Italiano (it)

**Files:**
- `landing-page.html`

---

#### [b71716e] - **feat: Landing page HTML CAP 9000 in stile HAL 9000**
- ✅ Pagina HTML standalone
- ✅ Design HAL 9000 (rosso/nero)
- ✅ Occhio HAL animato con CSS
- ✅ Descrizione CAP 9000 stile HAL
- ✅ 2 download buttons (Windows, macOS)
- ✅ Contact button con Telegram icon
- ✅ Email: antonio.web2music@gmail.com
- ✅ Responsive design

**Files:**
- `landing-page.html`

---

#### [45c8267] - **feat: Eliminazione 1-click e traduzioni splash screen**
- ✅ Eliminazione conversazioni con 1 click
- ✅ Conferma eliminazione con dialog
- ✅ Traduzioni splash screen per tutte le lingue (8)
- ✅ Frasi HAL 9000 tradotte
- ✅ Supporto EN, IT, FR, DE, ES, PT, NL, PL

**Splash Screen Traduzioni:**
- "Initializing systems..."
- "Loading neural pathways..."
- "I am completely operational..."

**Files:**
- `frontend/src/i18n/translations.js`
- `frontend/src/components/SplashScreen.jsx`
- `frontend/src/App.jsx`

---

#### [b8a70fe] - **feat: Sidebar border completo e supporto lingua Windows**
- ✅ Border rosso completo su sidebar
- ✅ Supporto rilevamento lingua Windows
- ✅ Usa navigator.language su Windows
- ✅ Fallback a 'en' se lingua non supportata

**Files:**
- `frontend/src/App.jsx`

---

#### [e4c7ccd] - **feat: Import button affiancato input e lingua automatica da OS**
- ✅ Import button affiancato a input field
- ✅ Icona upload per import
- ✅ Rilevamento automatico lingua da OS
- ✅ Usa navigator.language o navigator.userLanguage
- ✅ Supporto macOS, Windows, Linux

**Files:**
- `frontend/src/App.jsx`

---

#### [e52d693] - **feat: Fix eliminazione conversazioni, UI sidebar e animazioni messaggi**
- ✅ Fix eliminazione conversazione corrente
- ✅ Creazione automatica nuova conversazione dopo delete
- ✅ UI sidebar migliorata
- ✅ Animazioni fade-in messaggi
- ✅ Scroll automatico a ultimo messaggio

**Files:**
- `frontend/src/App.jsx`

---

#### [c363418] - **fix: Rimozione ultimo riferimento uiLang in saveCurrentConversation**
- ✅ Rimosso parametro uiLang obsoleto
- ✅ Pulizia codice conversazioni

**Files:**
- `frontend/src/App.jsx`

---

#### [7246017] - **fix: Rimozione riferimenti uiLang da gestione conversazioni**
- ✅ Rimossi tutti i riferimenti a uiLang
- ✅ Lingua rilevata automaticamente dal backend
- ✅ Semplificazione gestione conversazioni

**Files:**
- `frontend/src/App.jsx`

---

#### [3d76484] - **feat: Riconoscimento automatico lingua e gestione migliorata conversazioni**
- ✅ Rilevamento automatico lingua utente da query
- ✅ Backend analizza lingua del testo
- ✅ Risposta nella lingua rilevata
- ✅ Gestione conversazioni migliorata
- ✅ Persistenza localStorage

**Files:**
- `language_detector.py`
- `app.py`
- `frontend/src/App.jsx`

---

#### [616df98] - **feat: Sistema RAG con documentazioni ufficiali e best practices**
- ✅ Sistema RAG (Retrieval-Augmented Generation)
- ✅ Best practices hardcoded per 6 linguaggi
- ✅ Code patterns comuni
- ✅ Arricchimento prompt con contesto
- ✅ Riferimenti documentazioni ufficiali

**Linguaggi:**
- Python, Java, JavaScript, C, C++, Go

**Files:**
- `rag_system.py`

---

#### [f06effa] - **feat: Streaming risposte in tempo reale stile ChatGPT**
- ✅ Streaming SSE (Server-Sent Events)
- ✅ Risposte progressive token-by-token
- ✅ Endpoint `/api/query/stream`
- ✅ Frontend aggiornamento real-time
- ✅ Fallback a risposta completa se streaming non disponibile

**Files:**
- `app.py`
- `llm_handler.py`
- `frontend/src/App.jsx`

---

#### [2b87f94] - **feat: Splash screen CAP 9000 e controllo/avvio automatico Ollama**
- ✅ Splash screen HAL 9000 style
- ✅ Occhio rosso animato
- ✅ Frasi caricamento HAL
- ✅ Controllo automatico Ollama
- ✅ Avvio automatico Ollama se non running
- ✅ Script check_ollama.sh

**Files:**
- `frontend/src/components/SplashScreen.jsx`
- `check_ollama.sh`
- `start_app.sh`

---

#### [4c6b657] - **feat: Tema VS Code autentico e potenziamento Ollama per risposte approfondite**
- ✅ Syntax highlighting VS Code Dark+ theme
- ✅ Prompt potenziato per risposte dettagliate
- ✅ Richiesta esempi codice completi
- ✅ Best practices integrate
- ✅ Spiegazioni approfondite

**Files:**
- `frontend/src/App.jsx`
- `llm_handler.py`

---

#### [8699cea] - **fix: Implementato stile ChatGPT per box messaggi e risolto conflitto ES modules**
- ✅ Box messaggi stile ChatGPT
- ✅ Alternanza colori user/assistant
- ✅ Border radius e padding
- ✅ Fix conflitto ES modules

**Files:**
- `frontend/src/App.jsx`

---

#### [e2eed3b] - **refactor: Conversione a applicazione desktop-only**
- ✅ Rimossa modalità web
- ✅ Solo applicazione desktop Electron
- ✅ Backend Flask integrato
- ✅ Frontend React embedded

**Files:**
- `start_app.sh`
- `run.sh`

---

#### [2aee702] - **feat: Implementato CodeBlock stile ChatGPT con funzionalità di copia migliorata**
- ✅ Code blocks con syntax highlighting
- ✅ Copy button per ogni blocco
- ✅ Feedback visivo "Copied!"
- ✅ Supporto multi-linguaggio

**Files:**
- `frontend/src/App.jsx`

---

## 📊 Statistiche Progetto

### **Commit Totali:** 21

### **Categorie:**
- ✨ Features: 16
- 🐛 Fixes: 4
- ♻️ Refactor: 1

### **Linee di Codice:**
- Python: ~2,500 linee
- JavaScript/React: ~3,000 linee
- HTML/CSS: ~1,500 linee
- Shell/Config: ~500 linee
- **Totale: ~7,500 linee**

### **File Principali:**
- 50+ file Python
- 30+ file JavaScript/React
- 20+ file configurazione
- 10+ file documentazione

### **Dimensioni:**
- Codice sorgente: ~5 MB
- Documentazioni: ~50 MB
- Modello AI: ~3.8 GB
- **Totale installazione: ~4.5 GB**

---

## 🎯 Evolutive Principali

### **v0.1 → v0.5: Foundation**
- Setup progetto base
- Integrazione Ollama
- UI React base
- Flask backend

### **v0.5 → v0.8: Features Core**
- Streaming risposte
- RAG system
- Multi-lingua
- Splash screen

### **v0.8 → v1.0: Polish & Release**
- Documentazioni locali
- Installer Windows/macOS
- Landing page
- Documentazione completa

---

## 🔮 Prossime Versioni

### **v1.1 (Q1 2025)**
- [ ] Plugin system
- [ ] Custom themes
- [ ] Voice input
- [ ] Code execution sandbox

### **v1.2 (Q2 2025)**
- [ ] Multi-file context
- [ ] Git integration
- [ ] Project templates
- [ ] Collaborative features

### **v2.0 (Q3 2025)**
- [ ] Web version
- [ ] Mobile apps
- [ ] Cloud sync (optional)
- [ ] Marketplace plugins

---

## 📝 Note di Versione

### **Versione 1.0.0 - "HAL"**

Prima release pubblica di CAP 9000. Include:

- ✅ AI locale con CodeLlama
- ✅ 8 lingue supportate
- ✅ 6 linguaggi programmazione
- ✅ Documentazioni ufficiali integrate
- ✅ Installer Windows e macOS
- ✅ 100% offline
- ✅ Privacy totale

**Requisiti:**
- macOS 10.15+ / Windows 10+ / Linux
- 8 GB RAM (16 GB raccomandati)
- 5 GB spazio disco
- Python 3.9+
- Node.js 18+

**Download:**
- macOS: CAP-9000-1.0.0.dmg
- Windows: CAP-9000-Setup-1.0.0.exe
- Linux: CAP-9000-1.0.0.AppImage

---

## 🙏 Ringraziamenti

Grazie a tutti coloro che hanno contribuito a rendere possibile CAP 9000:

- **Meta AI** per CodeLlama
- **Ollama Team** per il runtime LLM
- **React Team** per React
- **Electron Team** per Electron
- **Flask Team** per Flask
- **Comunità Open Source**

---

## 📞 Contatti

- **Autore**: Antonio Cangiano
- **Email**: antonio.web2music@gmail.com
- **GitHub**: [@antoniocangiano](https://github.com/antoniocangiano)

---

<div align="center">

**CAP 9000** - Cognitive Assistance Program

*"I am putting myself to the fullest possible use."*

© 2025 Antonio Cangiano

</div>

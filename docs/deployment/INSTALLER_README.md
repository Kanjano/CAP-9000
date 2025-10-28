# 📦 CAP 9000 - Installer Build Guide

## Overview

Questa guida spiega come creare gli installer per **Windows** e **macOS** di CAP 9000, completi di:
- ✅ Download automatico Ollama
- ✅ Download modello CodeLlama
- ✅ Download documentazioni ufficiali
- ✅ Scelta disco installazione
- ✅ Calcolo spazio richiesto
- ✅ Icone e grafica HAL 9000 style

## 🎨 Step 1: Generare Icone

### **Genera icone HAL 9000:**

```bash
# Apri il generatore di icone
open build-resources/icon-generator.html
```

**Nel browser:**
1. Click "Generate All Icons"
2. Download ogni icona con il nome esatto mostrato
3. Salva in `build-resources/icons/`

### **Icone richieste:**

**Windows (.ico):**
- `icon.ico` - Tutte le dimensioni embedded (16, 32, 48, 64, 128, 256)

**macOS (.icns):**
- `icon.icns` - Tutte le dimensioni embedded (16, 32, 128, 256, 512, 1024)

**Singole (.png):**
- `icon-16x16.png`
- `icon-32x32.png`
- `icon-48x48.png`
- `icon-64x64.png`
- `icon-128x128.png`
- `icon-256x256.png`
- `icon-512x512.png`
- `icon-1024x1024.png`

### **Converti PNG in ICO/ICNS:**

**Per Windows (.ico):**
```bash
# Usa ImageMagick
convert icon-16x16.png icon-32x32.png icon-48x48.png icon-64x64.png icon-128x128.png icon-256x256.png icon.ico
```

**Per macOS (.icns):**
```bash
# Crea iconset
mkdir icon.iconset
cp icon-16x16.png icon.iconset/icon_16x16.png
cp icon-32x32.png icon.iconset/icon_16x16@2x.png
cp icon-32x32.png icon.iconset/icon_32x32.png
cp icon-64x64.png icon.iconset/icon_32x32@2x.png
cp icon-128x128.png icon.iconset/icon_128x128.png
cp icon-256x256.png icon.iconset/icon_128x128@2x.png
cp icon-256x256.png icon.iconset/icon_256x256.png
cp icon-512x512.png icon.iconset/icon_256x256@2x.png
cp icon-512x512.png icon.iconset/icon_512x512.png
cp icon-1024x1024.png icon.iconset/icon_512x512@2x.png

# Converti in icns
iconutil -c icns icon.iconset
```

## 🖼️ Step 2: Creare Background DMG (macOS)

### **Crea immagine background per installer macOS:**

```bash
# Dimensioni: 540x380 px
# Stile: HAL 9000 (nero, rosso, occhio)
```

**Salva come:** `build-resources/dmg-background.png`

**Contenuto suggerito:**
- Background nero
- Occhio HAL 9000 al centro
- Testo "CAP 9000" in rosso
- Istruzioni "Trascina l'icona in Applications"

## 📋 Step 3: Preparare Build

### **Installa dipendenze:**

```bash
# Root del progetto
npm install

# Installa electron-builder
npm install --save-dev electron-builder
```

### **Verifica struttura file:**

```
windsurf-project/
├── package.json                    ✅
├── main.js                         ✅
├── preload.js                      ✅
├── app.py                          ✅
├── download_docs.py                ✅
├── requirements.txt                ✅
├── frontend/
│   └── dist/                       ✅ (npm run build)
├── build-resources/
│   ├── icons/
│   │   ├── icon.ico               ✅
│   │   ├── icon.icns              ✅
│   │   └── *.png                  ✅
│   ├── dmg-background.png         ✅
│   ├── installer.nsh              ✅
│   ├── entitlements.mac.plist     ✅
│   └── postinstall.sh             ✅
└── installer-scripts/
    ├── setup-ollama.js            ✅
    └── setup-docs.js              ✅
```

## 🏗️ Step 4: Build Installer

### **Windows Installer:**

```bash
# Build per Windows (da macOS con Wine o da Windows)
npm run build:win

# Output:
# dist/CAP 9000-Setup-1.0.0.exe
# dist/CAP 9000-1.0.0-portable.exe
```

**Caratteristiche installer Windows:**
- ✅ NSIS installer personalizzato
- ✅ Scelta directory installazione
- ✅ Calcolo spazio disco (4.5 GB)
- ✅ Checkbox opzionali:
  - Installa Ollama + CodeLlama
  - Scarica documentazioni
- ✅ Progress bar download
- ✅ Desktop shortcut
- ✅ Start Menu shortcut
- ✅ Uninstaller incluso

### **macOS Installer:**

```bash
# Build per macOS
npm run build:mac

# Output:
# dist/CAP 9000-1.0.0.dmg
# dist/CAP 9000-1.0.0-mac.zip
```

**Caratteristiche installer macOS:**
- ✅ DMG con background personalizzato
- ✅ Drag & Drop in Applications
- ✅ Script post-install automatico
- ✅ Download Ollama via curl
- ✅ Download CodeLlama via ollama
- ✅ Download documentazioni via Python
- ✅ Configurazione LaunchAgent opzionale

### **Build per tutte le piattaforme:**

```bash
# Build Windows + macOS + Linux
npm run build:all

# Output:
# dist/CAP 9000-Setup-1.0.0.exe       (Windows)
# dist/CAP 9000-1.0.0.dmg             (macOS)
# dist/CAP 9000-1.0.0.AppImage        (Linux)
# dist/CAP 9000-1.0.0.deb             (Debian/Ubuntu)
# dist/CAP 9000-1.0.0.rpm             (RedHat/Fedora)
```

## 📊 Spazio Disco Richiesto

### **Breakdown completo:**

| Componente | Dimensione | Obbligatorio |
|------------|------------|--------------|
| CAP 9000 App | ~200 MB | ✅ Sì |
| Ollama Engine | ~450-500 MB | ⚠️ Raccomandato |
| CodeLlama Model | ~3.8 GB | ⚠️ Raccomandato |
| Documentazioni | ~50 MB | 💡 Opzionale |
| **TOTALE** | **~4.5 GB** | |

### **Modalità installazione:**

**Completa (Raccomandato):**
- ✅ Tutti i componenti
- ✅ Funzionalità complete
- 💾 4.5 GB

**Base:**
- ✅ Solo CAP 9000
- ⚠️ Funzionalità limitate
- 💾 200 MB

**Personalizzata:**
- ✅ Scegli componenti
- 💾 200 MB - 4.5 GB

## 🎯 Processo Installazione

### **Windows:**

```
1. Esegui CAP 9000-Setup-1.0.0.exe
2. Accetta licenza
3. Scegli directory (default: C:\Program Files\CAP 9000)
4. Verifica spazio disponibile
5. Seleziona componenti:
   ☑ Installa Ollama + CodeLlama
   ☑ Scarica documentazioni
6. Click "Installa"
7. Progress bar:
   - Copia file CAP 9000 (10%)
   - Download Ollama (20%)
   - Installa Ollama (30%)
   - Avvia Ollama (40%)
   - Download CodeLlama (80%)
   - Download documentazioni (95%)
   - Finalizza (100%)
8. Click "Fine"
9. CAP 9000 si avvia automaticamente
```

### **macOS:**

```
1. Apri CAP 9000-1.0.0.dmg
2. Trascina CAP 9000 in Applications
3. Chiudi DMG
4. Apri CAP 9000 da Applications
5. Primo avvio: script post-install
6. Conferma installazione componenti (s/n)
7. Progress:
   - Verifica Ollama
   - Download Ollama (se necessario)
   - Avvia Ollama
   - Download CodeLlama (~10-30 min)
   - Verifica Python
   - Download documentazioni
   - Configurazione avvio automatico (opzionale)
8. Installazione completata
9. CAP 9000 pronto all'uso
```

## 🧪 Testing Installer

### **Test Windows:**

```bash
# VM Windows o Wine
wine dist/CAP\ 9000-Setup-1.0.0.exe

# Verifica:
# - Installazione in C:\Program Files\CAP 9000
# - Shortcut desktop
# - Shortcut Start Menu
# - Ollama installato
# - CodeLlama scaricato
# - Documentazioni presenti
# - App si avvia correttamente
```

### **Test macOS:**

```bash
# Monta DMG
open dist/CAP\ 9000-1.0.0.dmg

# Verifica:
# - Background DMG corretto
# - Drag & Drop funziona
# - App in /Applications
# - Post-install eseguito
# - Ollama installato
# - CodeLlama scaricato
# - Documentazioni presenti
# - App si avvia correttamente
```

## 🐛 Troubleshooting

### **Errore: "Icone non trovate"**
```bash
# Verifica presenza icone
ls -la build-resources/icons/

# Rigenera icone
open build-resources/icon-generator.html
```

### **Errore: "electron-builder not found"**
```bash
npm install --save-dev electron-builder
```

### **Errore: "Frontend dist non trovato"**
```bash
cd frontend
npm run build
cd ..
```

### **Errore Windows: "NSIS error"**
```bash
# Verifica installer.nsh
cat build-resources/installer.nsh

# Rimuovi build cache
rm -rf dist/
npm run build:win
```

### **Errore macOS: "Code signing failed"**
```bash
# Disabilita code signing per test
export CSC_IDENTITY_AUTO_DISCOVERY=false
npm run build:mac
```

## 📝 Note Importanti

### **Code Signing:**

**Windows:**
- Richiede certificato Authenticode
- Senza: warning "Publisher unknown"
- Acquista da: DigiCert, Sectigo, etc.

**macOS:**
- Richiede Apple Developer Account ($99/anno)
- Senza: warning "App da sviluppatore non identificato"
- Soluzione temporanea: `xattr -cr /Applications/CAP\ 9000.app`

### **Notarization (macOS):**

```bash
# Dopo code signing
xcrun notarytool submit dist/CAP\ 9000-1.0.0.dmg \
  --apple-id "your@email.com" \
  --password "app-specific-password" \
  --team-id "TEAM_ID" \
  --wait
```

### **Distribuzione:**

**Windows:**
- Upload su sito web
- Microsoft Store (opzionale)
- Winget package (opzionale)

**macOS:**
- Upload su sito web
- Mac App Store (richiede modifiche)
- Homebrew Cask (opzionale)

## ✅ Checklist Pre-Release

- [ ] Icone generate (tutte le dimensioni)
- [ ] Background DMG creato
- [ ] Frontend buildato (`npm run build`)
- [ ] Versione aggiornata in `package.json`
- [ ] LICENSE file presente
- [ ] README.md aggiornato
- [ ] Test installer Windows
- [ ] Test installer macOS
- [ ] Verifica download Ollama
- [ ] Verifica download CodeLlama
- [ ] Verifica download documentazioni
- [ ] Test funzionalità app
- [ ] Screenshot per landing page
- [ ] Video demo (opzionale)

## 🚀 Release

```bash
# 1. Tag versione
git tag v1.0.0
git push origin v1.0.0

# 2. Build release
npm run build:all

# 3. Upload su GitHub Releases
# - CAP 9000-Setup-1.0.0.exe (Windows)
# - CAP 9000-1.0.0.dmg (macOS Intel)
# - CAP 9000-1.0.0-arm64.dmg (macOS Apple Silicon)
# - CAP 9000-1.0.0.AppImage (Linux)

# 4. Update landing page
# - Link download
# - Release notes
# - Screenshots
```

## 📧 Support

Per problemi o domande:
- Email: antonio.web2music@gmail.com
- GitHub Issues: [repository]/issues

---

**CAP 9000** - Cognitive Assistance Program
© 2025 Antonio Cangiano

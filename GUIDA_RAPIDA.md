# 🔴 HAL 9000 Code Assistant - Guida Rapida

## 🚀 Avvio Rapido

### Metodo 1: Script Automatico (Consigliato)

```bash
./start_app.sh
```

Lo script controllerà automaticamente:
- ✅ Python 3 installato
- ✅ Flask installato
- ✅ Node.js installato
- ✅ Dipendenze installate
- ✅ Frontend compilato

### Metodo 2: Manuale

1. **Installa dipendenze Python** (solo la prima volta):
```bash
pip3 install flask flask-cors
```

2. **Installa dipendenze Node.js** (solo la prima volta):
```bash
cd frontend
npm install
```

3. **Compila il frontend** (solo la prima volta):
```bash
npm run build
```

4. **Avvia l'applicazione**:
```bash
npm run electron:dev
```

## 🌍 Lingue Supportate

L'interfaccia è disponibile in **8 lingue europee**:

| Lingua | Codice | Emoji |
|--------|--------|-------|
| English | en | 🇬🇧 |
| Italiano | it | 🇮🇹 |
| Français | fr | 🇫🇷 |
| Deutsch | de | 🇩🇪 |
| Español | es | 🇪🇸 |
| Português | pt | 🇵🇹 |
| Nederlands | nl | 🇳🇱 |
| Polski | pl | 🇵🇱 |

Per cambiare lingua, clicca sull'icona 🌍 in alto nell'interfaccia.

## 💻 Linguaggi di Programmazione

Supporta i seguenti linguaggi:
- Python
- Java
- JavaScript
- C
- C++
- Go

## 📦 Creare Pacchetto Installabile

### Per macOS:
```bash
cd frontend
npm run package:mac
```
Genera: `frontend/release/HAL 9000 Code Assistant.dmg`

### Per Windows:
```bash
cd frontend
npm run package:win
```
Genera: `frontend/release/HAL 9000 Code Assistant Setup.exe`

### Per Linux:
```bash
cd frontend
npm run package:linux
```
Genera: `frontend/release/HAL 9000 Code Assistant.AppImage`

## 🎯 Caratteristiche Principali

### ✅ Standalone
- **Nessun browser** richiesto
- **Nessuna connessione internet** necessaria
- Tutto funziona **localmente**

### ✅ Multilingua
- Interfaccia tradotta in 8 lingue
- Cambio lingua istantaneo
- Messaggi HAL tradotti

### ✅ Cross-Platform
- macOS (Intel e Apple Silicon)
- Windows (64-bit)
- Linux (AppImage e .deb)

## 🔧 Risoluzione Problemi

### Porta 5001 già in uso

Su macOS, AirPlay Receiver usa la porta 5000. L'app usa la porta 5001.

Se anche questa è occupata, modifica `app.py`:
```python
app.run(debug=True, port=5002)  # Cambia porta
```

E `frontend/electron/main.js`:
```javascript
const response = await fetch('http://127.0.0.1:5002/api/query', {
```

### L'app non si avvia

1. Verifica Python:
```bash
python3 --version
```

2. Verifica Flask:
```bash
python3 -c "import flask; print(flask.__version__)"
```

3. Verifica Node.js:
```bash
node --version
```

### Errore "Cannot find module"

Reinstalla le dipendenze:
```bash
cd frontend
rm -rf node_modules
npm install
```

## 📝 Esempi di Utilizzo

1. **Seleziona la lingua dell'interfaccia** (es. Italiano)
2. **Seleziona il linguaggio di programmazione** (es. Python)
3. **Digita la tua domanda**: "Come creare una funzione?"
4. **HAL 9000 risponderà** nella lingua selezionata

## 🎬 Citazioni HAL 9000

Le citazioni iconiche dal film cambiano in base alla lingua:

**Italiano:**
> "Buon pomeriggio. Sono HAL 9000, il tuo assistente di programmazione."

**Francese:**
> "Bon après-midi. Je suis HAL 9000, votre assistant de code."

**Tedesco:**
> "Guten Tag. Ich bin HAL 9000, Ihr Code-Assistent."

## 📞 Supporto

Per problemi o domande, controlla:
- `README_DESKTOP.md` - Documentazione completa
- `README_HAL9000.md` - Documentazione originale web

## 🎨 Personalizzazione

### Aggiungere una nuova lingua

1. Modifica `frontend/src/i18n/translations.js`
2. Aggiungi le traduzioni nel formato:
```javascript
cs: {  // Ceco
  greeting: "Dobré odpoledne. Jsem HAL 9000...",
  // ... altre traduzioni
}
```

### Aggiungere un linguaggio di programmazione

Modifica `languages.py`:
```python
languages = [
    'Python',
    'Java',
    'JavaScript',
    'C',
    'C++',
    'Go',
    'Rust',  # Nuovo linguaggio
]
```

L'app si aggiornerà automaticamente!

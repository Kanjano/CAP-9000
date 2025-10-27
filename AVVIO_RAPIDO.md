# 🚀 Avvio Rapido CAP 9000 Desktop

## Avvio con un solo comando

Per avviare l'applicazione desktop CAP 9000, esegui semplicemente:

```bash
./run.sh
```

Oppure:

```bash
./start_app.sh
```

## Requisiti

- **Python 3** (per il backend Flask)
- **Node.js** (per l'applicazione Electron)

## Cosa fa lo script

1. Verifica la presenza di Python 3 e Node.js
2. Installa le dipendenze se necessario
3. Builda l'applicazione frontend
4. Avvia l'applicazione desktop Electron

## Note

- **Questa è un'applicazione DESKTOP-ONLY**
- Non è necessario aprire un browser
- L'applicazione si avvia automaticamente in una finestra dedicata
- Il backend Flask viene avviato automaticamente da Electron

## Modalità Sviluppo

Per avviare in modalità sviluppo con DevTools:

```bash
cd frontend
npm run dev
```

## Packaging

Per creare un pacchetto distribuibile:

**macOS:**
```bash
cd frontend
npm run package:mac
```

**Windows:**
```bash
cd frontend
npm run package:win
```

**Linux:**
```bash
cd frontend
npm run package:linux
```

# HAL 9000 Code Assistant

Un'interfaccia web ispirata a HAL 9000 di "2001: Odissea nello Spazio" per il Code Assistant.

## Caratteristiche

- 🔴 Design iconico con l'occhio rosso di HAL 9000
- 💬 Interfaccia chat stile ChatGPT
- 🎨 Tema scuro con effetti glow rossi
- 🌐 Supporto per tutti i linguaggi definiti in `languages.py`
- ⚡ Backend Flask + Frontend React

## Struttura

```
windsurf-project/
├── main.py              # CodeAssistant originale
├── languages.py         # Lista linguaggi supportati
├── app.py              # Backend Flask API
├── requirements.txt    # Dipendenze Python
└── frontend/           # Applicazione React
    ├── src/
    │   ├── App.jsx     # Componente principale HAL 9000
    │   ├── main.jsx
    │   └── index.css
    └── package.json
```

## Installazione

### Backend (Python)

```bash
# Installa le dipendenze Python
pip install flask flask-cors
```

### Frontend (React)

```bash
cd frontend
npm install
```

## Avvio

### 1. Avvia il Backend Flask

```bash
python app.py
```

Il server sarà disponibile su `http://localhost:5000`

### 2. Avvia il Frontend React

In un nuovo terminale:

```bash
cd frontend
npm run dev
```

L'interfaccia sarà disponibile su `http://localhost:3000`

## Utilizzo

1. Apri il browser su `http://localhost:3000`
2. Seleziona il linguaggio di programmazione dal menu a tendina
3. Digita la tua domanda nella chat
4. HAL 9000 risponderà con il suo stile caratteristico

## API Endpoints

- `POST /api/query` - Invia una query al Code Assistant
  ```json
  {
    "query": "Come creo una funzione?",
    "language": "Python"
  }
  ```

- `GET /api/languages` - Ottieni la lista dei linguaggi supportati

## Citazioni HAL 9000

L'interfaccia include citazioni iconiche dal film:
- "Good afternoon. I am HAL 9000, your code assistant."
- "This mission is too important for me to allow you to jeopardize it."
- "I'm afraid I can't do that." (in caso di errori)

## Tecnologie

- **Frontend**: React, Vite, TailwindCSS, Lucide Icons
- **Backend**: Flask, Flask-CORS
- **Linguaggi**: Python, Java, JavaScript, C, C++, Go

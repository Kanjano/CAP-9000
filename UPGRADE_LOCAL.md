# CAP 9000 — Upgrade per esecuzione locale veloce

Questo documento riassume l'upgrade dello stack tecnologico e le modifiche
architetturali fatte per ottimizzare i **tempi di risposta in locale**
(obiettivo: ogni risposta sotto gli **8 secondi**), senza toccare il frontend.

## TL;DR

- **Modello di default cambiato**: da `codellama` (7B, lento) a
  **`qwen2.5-coder`** (modello di codice più recente e veloce), con fallback
  automatico a `codellama` se non installato.
- **Eliminata la pre-call NLU** (`mistral`) che raddoppiava la latenza.
- **Prompt di sistema ridotto**: niente più output "production-ready" enormi
  per ogni domanda → risposte più corte = molto più veloci.
- **`num_predict` tarato** sui benchmark locali per restare sotto gli 8s.
- **Modello tenuto caldo in RAM** (`keep_alive`) → niente cold-start.
- **`torch` reso opzionale** (import lazy) e dipendenze inutili rimosse.
- **Configurazione centralizzata** in `config.py`, tutto sovrascrivibile via
  variabili d'ambiente.

Il **frontend (Electron/React) non è stato modificato**: il contratto JSON
(`response`, `language`, `error`, `source`, `reasoning_used`) è invariato.

---

## Analisi: dov'era la lentezza

| # | Problema | Impatto |
|---|----------|---------|
| 1 | `query_enhancer.py` faceva una **seconda chiamata LLM** (`mistral`) prima di ogni risposta | ~+5–15s per query |
| 2 | Il prompt di sistema chiedeva codice "production-ready" completo (controller, service, repository, DTO, test…) per **ogni** domanda | output 1000+ token → latenza alta |
| 3 | `recursive_reasoning.py` importava **torch** all'avvio anche se la rete neurale non è mai usata nel percorso di risposta | startup lento + dipendenza pesante |
| 4 | "Reasoning mode" anteponeva un template multi-step ("mostra tutto il processo") | output ancora più lungo |
| 5 | Modello `codellama` 7B a ~38 tok/s su M2 Pro | baseline ~10s solo per query semplici |
| 6 | Nessun `keep_alive` → il modello veniva ricaricato (cold-start) | secondi extra sulla prima query |
| 7 | `requirements.txt` con tensorflow/numpy/pandas/sklearn/langdetect **mai importati** | ambiente inutilmente pesante |

## Ricerca: modelli alternativi valutati

Tutti testati localmente su **Apple M2 Pro / 16 GB** via Ollama:

| Modello | Dimensione | Qualità codice | Velocità | Note |
|---------|-----------|----------------|----------|------|
| codellama 7B | 3.8 GB | buona | lenta (~38 tok/s) | baseline originale |
| **qwen2.5-coder:3b** | 1.9 GB | **ottima** | veloce | **default scelto** |
| qwen2.5-coder:1.5b | 1.0 GB | buona | molto veloce | opzione ultra-veloce |
| deepseek-coder / codegemma / starcoder2 | varie | buone | — | alternative valide, non default |

`qwen2.5-coder` è attualmente tra i migliori modelli di codice open per il
rapporto qualità/dimensione, nettamente più veloce di codellama a parità di
hardware.

---

## Come si esegue in locale

### 1. Prerequisiti
```bash
# Ollama (runtime del modello)
brew install ollama          # macOS
ollama serve                 # avvia il server (in un terminale dedicato)

# Modello di default (veloce)
ollama pull qwen2.5-coder:3b
# (opzionale) fallback
ollama pull codellama
```

### 2. Dipendenze Python
```bash
pip install -r requirements.txt
```

### 3. Avvio backend
```bash
# Opzione A: API Flask
python app.py            # http://localhost:5001

# Opzione B: bridge stdin/stdout usato dall'app Electron
python python_bridge.py
```

### 4. Benchmark dei tempi di risposta
```bash
python benchmark.py          # 100 query, verifica obiettivo < 8s
python benchmark.py 30       # run più breve
```
Il report viene salvato in `benchmark_results.json`.

---

## Configurazione (variabili d'ambiente)

Tutto in `config.py`, sovrascrivibile senza toccare il codice:

| Variabile | Default | Descrizione |
|-----------|---------|-------------|
| `CAP9000_MODEL` | `qwen2.5-coder:3b` | Modello primario |
| `CAP9000_FALLBACK_MODEL` | `codellama` | Fallback se il primario manca |
| `CAP9000_NUM_PREDICT` | `320` | Max token generati (leva principale sulla latenza) |
| `CAP9000_NUM_CTX` | `2048` | Context window |
| `CAP9000_KEEP_ALIVE` | `30m` | Tempo di permanenza del modello in RAM |
| `CAP9000_ENABLE_RAG` | `1` | Arricchimento con best practice |
| `CAP9000_ENABLE_ENHANCER` | `0` | Pre-call NLU (lento, off di default) |
| `CAP9000_ENABLE_REASONING` | `1` | Reasoning leggero per query complesse |

Esempio — privilegiare la **velocità massima**:
```bash
CAP9000_MODEL=qwen2.5-coder:1.5b CAP9000_NUM_PREDICT=320 python app.py
```
Esempio — privilegiare la **qualità** (risposte più lunghe):
```bash
CAP9000_NUM_PREDICT=512 python app.py
```

---

## File modificati / aggiunti

- **nuovo** `config.py` — configurazione centralizzata
- **nuovo** `benchmark.py` — suite di test dei tempi di risposta
- `llm_handler.py` — modello configurabile, fallback, warm-up `keep_alive`,
  prompt conciso, enhancer opzionale, opzioni da `config`
- `hybrid_llm_handler.py` — reasoning leggero, passaggio corretto del `context`
- `recursive_reasoning.py` — `torch` importato in modo lazy (rete prototipo non
  usata a runtime)
- `requirements.txt` — ridotto alle dipendenze realmente usate
- `query_enhancer.py` — invariato, ma istanziato solo se abilitato
- script di setup (`scripts/check_ollama.sh`, `installer-scripts/setup-ollama.js`)
  — modello di default aggiornato

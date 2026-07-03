"""
Configurazione centralizzata CAP 9000 (esecuzione locale, offline)

CAP 9000 gira interamente in locale su un endpoint OpenAI-compatibile.
Di default usa Ollama (che espone /v1 OpenAI-compatible) con il modello
Mistral. CodeLlama e' stato rimosso: il modello e' Mistral 7B Instruct
in locale (dev) e Devstral Small 2 24B sul target EliteBook.

Tutti i parametri performance-critical sono qui e sovrascrivibili via
variabili d'ambiente, cosi' da poter calibrare la velocita' senza
toccare il codice.

Variabili d'ambiente principali:
    CAP9000_MODEL        Modello da usare (default: mistral:7b-instruct-q4_K_M)
    CAP9000_API_BASE     Endpoint OpenAI-compatible (default: http://localhost:11434/v1)
    CAP9000_API_KEY      API key (non necessaria in locale, default: not-needed)
    CAP9000_OLLAMA_URL   URL server Ollama nativo (default: http://localhost:11434)
    CAP9000_NUM_PREDICT  Max token generati (default: 320, tarato per < 8s)
    CAP9000_MAX_TOKENS   Alias OpenAI di NUM_PREDICT (spec Mistral: 1024)
    CAP9000_NUM_CTX      Context window (default: 2048)
    CAP9000_KEEP_ALIVE   Tempo mantenimento modello in RAM (default: 30m)
    CAP9000_ENABLE_RAG   Abilita arricchimento RAG (default: 1)
    CAP9000_ENABLE_ENHANCER  Abilita pre-call NLU enhancer (default: 0)
    CAP9000_ENABLE_REASONING Abilita reasoning prompt (default: 1)
"""

import os


def _env_bool(name: str, default: bool) -> bool:
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


# --- Modello e connessione -------------------------------------------------
# Mistral 7B Instruct (Q4_K_M): compromesso qualita'/velocita' su hardware
# locale a 16GB (Ollama). Sul target EliteBook (>=24GB) usare Devstral Small 2
# via CAP9000_MODEL. Fallback alla famiglia 'mistral' se il tag non e' presente.
MODEL = os.environ.get("CAP9000_MODEL", "mistral:7b-instruct-q4_K_M")
FALLBACK_MODEL = os.environ.get("CAP9000_FALLBACK_MODEL", "mistral")
OLLAMA_URL = os.environ.get("CAP9000_OLLAMA_URL", "http://localhost:11434")

# Endpoint OpenAI-compatibile. Ollama espone /v1 (chat.completions, models).
# Centralizza qui per puntare a vLLM / llama.cpp / Mistral CLI senza toccare il codice.
API_BASE = os.environ.get("CAP9000_API_BASE", f"{OLLAMA_URL}/v1")
API_KEY = os.environ.get("CAP9000_API_KEY", "not-needed")

# Mantiene il modello caricato in RAM tra una richiesta e l'altra:
# elimina il cold-start (caricamento pesi) dalla latenza percepita.
KEEP_ALIVE = os.environ.get("CAP9000_KEEP_ALIVE", "30m")

# --- Parametri di generazione (tarati per latenza < 8s) --------------------
# 320 token: cap tarato sui benchmark locali (M2 Pro). Mantiene TUTTE le
# risposte (incluse quelle in reasoning mode) sotto gli 8s con margine,
# restando complete (~1000+ caratteri). Alzare per risposte piu' lunghe.
NUM_PREDICT = _env_int("CAP9000_NUM_PREDICT", 320)
# Spec Mistral consiglia max_tokens=1024. In locale (mistral 7B su CPU) 1024
# token superano gli 8s: NUM_PREDICT resta il cap effettivo per la latenza.
# MAX_TOKENS e' esposto per il target EliteBook dove 1024 e' raggiungibile.
MAX_TOKENS = _env_int("CAP9000_MAX_TOKENS", NUM_PREDICT)
NUM_CTX = _env_int("CAP9000_NUM_CTX", 2048)
NUM_THREAD = _env_int("CAP9000_NUM_THREAD", 0)  # 0 = auto (Ollama sceglie)
TEMPERATURE = float(os.environ.get("CAP9000_TEMPERATURE", "0.3"))
TOP_P = float(os.environ.get("CAP9000_TOP_P", "0.9"))
TOP_K = _env_int("CAP9000_TOP_K", 40)

# --- Feature toggles -------------------------------------------------------
# RAG: arricchisce il prompt con best practice. NB: gonfia il prompt di
# sistema e aumenta il tempo di prompt-eval (misurato: +2-3s/query su 3b),
# spingendo alcune query oltre gli 8s. Disabilitato di default: il prompt
# conciso gia' istruisce a seguire le best practice del linguaggio.
# Riabilitabile con CAP9000_ENABLE_RAG=1 (consigliato con num_predict piu' basso).
ENABLE_RAG = _env_bool("CAP9000_ENABLE_RAG", False)
# Enhancer: pre-call a un secondo LLM (mistral). Raddoppia la latenza.
# Disabilitato di default per esecuzione locale veloce.
ENABLE_ENHANCER = _env_bool("CAP9000_ENABLE_ENHANCER", False)
# Reasoning: aggiunge istruzioni di ragionamento al prompt per query complesse.
ENABLE_REASONING = _env_bool("CAP9000_ENABLE_REASONING", True)
ENABLE_CACHE = _env_bool("CAP9000_ENABLE_CACHE", True)


def generation_options(num_predict: int = None) -> dict:
    """Opzioni di generazione Ollama centralizzate."""
    opts = {
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "top_k": TOP_K,
        "num_predict": num_predict if num_predict is not None else NUM_PREDICT,
        "num_ctx": NUM_CTX,
    }
    if NUM_THREAD > 0:
        opts["num_thread"] = NUM_THREAD
    return opts


def chat_params(max_tokens: int = None) -> dict:
    """Parametri per l'endpoint OpenAI-compatible (chat.completions)."""
    return {
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": max_tokens if max_tokens is not None else MAX_TOKENS,
    }

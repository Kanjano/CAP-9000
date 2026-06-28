"""
LLM Handler per CAP 9000 Code Assistant

CAP 9000 usa Mistral in modalita' offline locale tramite un endpoint
OpenAI-compatibile (Ollama espone /v1; in alternativa vLLM o llama.cpp).
CodeLlama e' stato rimosso.

Mistral e' ottimizzato per:
- Generazione di codice di alta qualita'
- Debugging e analisi codice
- Spiegazioni tecniche dettagliate
- Best practices e pattern
- Supporto multi-linguaggio

Integrato con sistema RAG per documentazioni ufficiali.
"""

import json
import time

from openai import OpenAI

import config
from rag_system import get_rag_system
from query_enhancer import get_query_enhancer


class LLMHandler:
    def __init__(self, ollama_url=None):
        """
        Inizializza l'handler LLM su endpoint OpenAI-compatibile.

        Il modello e' configurabile (config.MODEL, default mistral:7b-instruct-q4_K_M),
        con fallback automatico a config.FALLBACK_MODEL (famiglia mistral) se il
        modello primario non e' installato.

        Args:
            ollama_url: URL del server Ollama nativo (default: config.OLLAMA_URL).
                        L'endpoint OpenAI usato e' config.API_BASE.
        """
        self.ollama_url = ollama_url or config.OLLAMA_URL
        self.api_base = config.API_BASE
        # Client OpenAI puntato all'endpoint locale (Ollama /v1).
        self.client = OpenAI(base_url=self.api_base, api_key=config.API_KEY)
        self.available = self.check_available()
        # Seleziona modello disponibile (primario o fallback)
        self.model = self._select_model()
        self.rag = get_rag_system()  # Sistema RAG per documentazioni
        # Enhancer NLU: pre-call a un secondo LLM. Costoso (raddoppia latenza),
        # disabilitato di default per esecuzione locale veloce (config.ENABLE_ENHANCER).
        self.enhancer = get_query_enhancer() if config.ENABLE_ENHANCER else None
        # Pre-carica il modello in RAM per azzerare il cold-start sulla 1a query.
        if self.available:
            self._warmup()

    def _list_models(self):
        """Ritorna la lista dei modelli serviti dall'endpoint OpenAI."""
        try:
            return [m.id for m in self.client.models.list().data]
        except Exception:
            return []

    def _select_model(self):
        """Sceglie il modello primario se presente, altrimenti il fallback."""
        if not self.available:
            return config.MODEL
        installed = self._list_models()

        def is_installed(name):
            # match esatto (es. "mistral:7b-instruct-q4_K_M") o per famiglia ("mistral")
            return name in installed or any(
                m == name or m.split(':')[0] == name.split(':')[0] for m in installed)

        if is_installed(config.MODEL):
            return config.MODEL
        if is_installed(config.FALLBACK_MODEL):
            print(f"[MODEL] '{config.MODEL}' non trovato, uso fallback '{config.FALLBACK_MODEL}'")
            return config.FALLBACK_MODEL
        print(f"[MODEL] Ne' '{config.MODEL}' ne' '{config.FALLBACK_MODEL}' installati. "
              f"Eseguire: ollama pull {config.MODEL}")
        return config.MODEL

    def _warmup(self):
        """Carica il modello in RAM (keep_alive) per eliminare il cold-start."""
        try:
            self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=1,
                extra_body={"keep_alive": config.KEEP_ALIVE},
            )
            print(f"[WARMUP] Modello '{self.model}' caricato in RAM (keep_alive={config.KEEP_ALIVE})")
        except Exception as e:
            print(f"[WARMUP] Skipped: {e}")

    def check_available(self):
        """Verifica se l'endpoint OpenAI-compatibile (Mistral) e' raggiungibile."""
        try:
            self.client.models.list()
            return True
        except Exception:
            return False

    # Compat: alcuni moduli chiamano check_ollama_available().
    def check_ollama_available(self):
        return self.check_available()

    def health_check(self):
        """
        Healthcheck dell'endpoint Mistral locale.

        Returns:
            dict: {available, api_base, model, models, error}
        """
        try:
            models = self._list_models()
            return {
                "available": True,
                "api_base": self.api_base,
                "model": self.model,
                "models": models,
                "error": None,
            }
        except Exception as e:
            return {
                "available": False,
                "api_base": self.api_base,
                "model": config.MODEL,
                "models": [],
                "error": str(e),
            }

    def _build_system_prompt(self, language, response_language):
        """
        Prompt di sistema CONCISO.

        Punta a risposte corrette, idiomatiche e direttamente utili, con codice
        solo quando serve -> output piu' corto = molto piu' veloce, senza perdere
        qualita' per le domande tecniche tipiche.
        """
        return (
            f"You are CAP 9000, an expert programming assistant.\n"
            f"Answer the {language} question clearly and correctly in {response_language}.\n"
            f"Guidelines:\n"
            f"- Be concise and direct; no filler or boilerplate.\n"
            f"- Provide a short, correct, idiomatic code example when it helps.\n"
            f"- Follow {language} best practices; handle obvious edge cases.\n"
            f"- Briefly explain the key idea; skip exhaustive theory.\n"
            f"- Only expand into full project structure if the user explicitly asks.\n"
            f"Respond entirely in {response_language}."
        )

    _LANGUAGE_NAMES = {
        'en': 'English', 'it': 'Italian', 'fr': 'French', 'de': 'German',
        'es': 'Spanish', 'pt': 'Portuguese', 'nl': 'Dutch', 'pl': 'Polish',
    }

    def _build_messages(self, query, language, response_language, context):
        """Costruisce system+user message per chat.completions, con RAG opzionale."""
        enhanced_query = query
        if self.enhancer is not None:
            start_enhance = time.time()
            enhanced_query = self.enhancer.enhance_query(query, language, response_language)
            print(f"[TIMING] Query enhancement took: {time.time() - start_enhance:.2f}s", flush=True)

        system_prompt = self._build_system_prompt(language, response_language)
        if config.ENABLE_RAG:
            system_prompt = self.rag.enrich_prompt(system_prompt, language, enhanced_query)

        user_prompt = f"[Respond in {response_language}] Question about {language}: {enhanced_query}"
        if context:
            user_prompt = f"{context}\n\n{user_prompt}"

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def generate_response(self, query, language, ui_language='en', context=None):
        """
        Genera una risposta usando il modello Mistral (non-streaming).

        Args:
            query: Domanda dell'utente
            language: Linguaggio di programmazione
            ui_language: Lingua dell'interfaccia (en, it, fr, de, es, pt, nl, pl)
            context: Contesto aggiuntivo (opzionale)

        Returns:
            str | None: Risposta generata, o None se l'endpoint non e' disponibile.
        """
        if not self.available:
            return None

        response_language = self._LANGUAGE_NAMES.get(ui_language, 'English')
        print(f"Generating response in {response_language} (UI language: {ui_language})")

        messages = self._build_messages(query, language, response_language, context)

        try:
            print(f"[TIMING] Starting Mistral API call (non-streaming, model={self.model})...", flush=True)
            start = time.time()

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False,
                extra_body={"keep_alive": config.KEEP_ALIVE},
                **config.chat_params(),
            )

            elapsed = time.time() - start
            print(f"[TIMING] Mistral API call took: {elapsed:.2f}s", flush=True)
            print(f"[TIMING] ===== TOTAL TIME: {elapsed:.2f}s =====", flush=True)
            return (completion.choices[0].message.content or "").strip()

        except Exception as e:
            print(f"Error calling Mistral endpoint: {e}")
            return None

    def generate_response_streaming(self, query, language, ui_language='en', context=None):
        """
        Genera una risposta in streaming per visualizzazione progressiva.

        Yields:
            str: Chunks della risposta
        """
        if not self.available:
            return

        response_language = self._LANGUAGE_NAMES.get(ui_language, 'English')
        messages = self._build_messages(query, language, response_language, context)

        print(f"[TIMING] Starting Mistral API call (streaming, model={self.model})...", flush=True)
        start = time.time()
        first_token_time = None

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                extra_body={"keep_alive": config.KEEP_ALIVE},
                **config.chat_params(),
            )

            for chunk in stream:
                delta = chunk.choices[0].delta.content if chunk.choices else None
                if delta:
                    if first_token_time is None:
                        first_token_time = time.time() - start
                        print(f"[TIMING] First token received after: {first_token_time:.2f}s", flush=True)
                    yield delta

        except Exception as e:
            print(f"Error in streaming: {e}")
            return

    def get_model_info(self):
        """Restituisce informazioni sul modello attivo (configurabile)."""
        descriptions = {
            'mistral': 'Modello Mistral 7B Instruct (Mistral AI), generalista e veloce',
            'devstral': 'Modello Devstral Small 2 (Mistral AI), specializzato per code tasks',
        }
        family = self.model.split(':')[0]
        version = self.model.split(':')[1] if ':' in self.model else 'latest'
        return {
            'name': self.model,
            'version': version,
            'description': descriptions.get(family, f'Modello Mistral locale: {self.model}'),
            'api_base': self.api_base,
            'languages': ['Python', 'Java', 'JavaScript', 'C', 'C++', 'Go', 'e altri'],
            'features': [
                'Generazione codice',
                'Debugging',
                'Spiegazioni tecniche',
                'Best practices',
                'Refactoring'
            ]
        }


def get_fallback_response(language, query):
    """Risposta di fallback se l'endpoint Mistral locale non e' disponibile."""
    return f"""I apologize, but I cannot access my neural network at this moment.
The local Mistral service (OpenAI-compatible endpoint) appears to be offline.

To enable intelligent responses:
1. Install Ollama: https://ollama.com
2. Run: ollama pull mistral:7b-instruct-q4_K_M
3. Start the Ollama service (it exposes the OpenAI-compatible /v1 API)

Your query about {language}: "{query}" will be processed once the service is available.

In the meantime, I can confirm this is a valid {language} programming question."""

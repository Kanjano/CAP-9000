"""
LLM Handler per CAP 9000 Code Assistant

CAP 9000 usa esclusivamente CodeLlama, un modello AI specializzato
per programmazione sviluppato da Meta AI.

CodeLlama è ottimizzato per:
- Generazione di codice di alta qualità
- Debugging e analisi codice
- Spiegazioni tecniche dettagliate
- Best practices e pattern
- Supporto multi-linguaggio

Integrato con sistema RAG per documentazioni ufficiali.
"""

import requests
import json
import time
import config
from rag_system import get_rag_system
from query_enhancer import get_query_enhancer

class LLMHandler:
    def __init__(self, ollama_url=None):
        """
        Inizializza l'handler LLM.

        Il modello e' configurabile (config.MODEL, default qwen2.5-coder:3b),
        con fallback automatico a config.FALLBACK_MODEL (codellama) se il
        modello primario non e' installato in Ollama.

        Args:
            ollama_url: URL del server Ollama (default: config.OLLAMA_URL)
        """
        self.ollama_url = ollama_url or config.OLLAMA_URL
        self.available = self.check_ollama_available()
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
        """Ritorna la lista dei tag modello installati in Ollama."""
        try:
            r = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if r.status_code == 200:
                return [m.get('name', '') for m in r.json().get('models', [])]
        except Exception:
            pass
        return []

    def _select_model(self):
        """Sceglie il modello primario se presente, altrimenti il fallback."""
        if not self.available:
            return config.MODEL
        installed = self._list_models()

        def is_installed(name):
            # match esatto (es. "qwen2.5-coder:3b") o per famiglia ("codellama")
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
            requests.post(
                f"{self.ollama_url}/api/generate",
                json={"model": self.model, "prompt": "hi", "stream": False,
                      "keep_alive": config.KEEP_ALIVE, "options": {"num_predict": 1}},
                timeout=120,
            )
            print(f"[WARMUP] Modello '{self.model}' caricato in RAM (keep_alive={config.KEEP_ALIVE})")
        except Exception as e:
            print(f"[WARMUP] Skipped: {e}")

    def check_ollama_available(self):
        """Verifica se Ollama è disponibile"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def _build_system_prompt(self, language, response_language):
        """
        Prompt di sistema CONCISO.

        Il vecchio prompt imponeva output "production-ready" enormi (controller,
        service, repository, DTO, test...) per OGNI domanda, gonfiando la
        risposta a 1000+ token e quindi la latenza. Questo prompt punta a
        risposte corrette, idiomatiche e direttamente utili, con codice solo
        quando serve -> output piu' corto = molto piu' veloce, senza perdere
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

    def generate_response(self, query, language, ui_language='en', context=None):
        """
        Genera una risposta usando il modello LLM
        
        Args:
            query: Domanda dell'utente
            language: Linguaggio di programmazione
            ui_language: Lingua dell'interfaccia utente (en, it, fr, de, es, pt, nl, pl)
            context: Contesto aggiuntivo (opzionale)
        
        Returns:
            str: Risposta generata dal modello
        """
        if not self.available:
            return None
        
        # Mappa delle lingue
        language_names = {
            'en': 'English',
            'it': 'Italian',
            'fr': 'French',
            'de': 'German',
            'es': 'Spanish',
            'pt': 'Portuguese',
            'nl': 'Dutch',
            'pl': 'Polish'
        }
        
        response_language = language_names.get(ui_language, 'English')
        print(f"Generating response in {response_language} (UI language: {ui_language})")

        # Enhancer NLU opzionale (pre-call costoso). Disabilitato di default.
        enhanced_query = query
        if self.enhancer is not None:
            start_enhance = time.time()
            enhanced_query = self.enhancer.enhance_query(query, language, ui_language)
            print(f"[TIMING] Query enhancement took: {time.time() - start_enhance:.2f}s", flush=True)

        # Prompt di sistema conciso (vedi _build_system_prompt): risposte
        # corrette e idiomatiche ma SENZA over-engineering -> output piu' corto
        # = latenza molto piu' bassa.
        system_prompt = self._build_system_prompt(language, response_language)

        # Arricchisci con contesto RAG (best practice) solo se abilitato.
        if config.ENABLE_RAG:
            enriched_system_prompt = self.rag.enrich_prompt(system_prompt, language, enhanced_query)
        else:
            enriched_system_prompt = system_prompt

        user_prompt = f"[Respond in {response_language}] Question about {language}: {enhanced_query}"
        if context:
            user_prompt = f"{context}\n\n{user_prompt}"

        try:
            print(f"[TIMING] Starting Ollama API call (non-streaming, model={self.model})...", flush=True)
            start_ollama = time.time()

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": user_prompt,
                    "system": enriched_system_prompt,
                    "stream": False,
                    "keep_alive": config.KEEP_ALIVE,
                    "options": config.generation_options(),
                },
                timeout=120,
            )
            
            ollama_time = time.time() - start_ollama
            print(f"[TIMING] Ollama API call took: {ollama_time:.2f}s", flush=True)
            
            if response.status_code == 200:
                result = response.json()
                print(f"[TIMING] ===== TOTAL TIME: {time.time() - start_ollama:.2f}s =====", flush=True)
                return result.get('response', '').strip()
            else:
                print(f"[ERROR] Ollama returned status code: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return None
    
    def generate_response_streaming(self, query, language, ui_language='en', context=None):
        """
        Genera una risposta in streaming per visualizzazione progressiva
        
        Args:
            query: Domanda dell'utente
            language: Linguaggio di programmazione
            ui_language: Lingua dell'interfaccia
            context: Contesto conversazionale (opzionale)
        
        Yields:
            str: Chunks della risposta
        """
        if not self.available:
            return
        
        # Mappa delle lingue
        language_names = {
            'en': 'English',
            'it': 'Italian',
            'fr': 'French',
            'de': 'German',
            'es': 'Spanish',
            'pt': 'Portuguese',
            'nl': 'Dutch',
            'pl': 'Polish'
        }
        
        response_language = language_names.get(ui_language, 'English')

        # Stesso prompt conciso della versione non-streaming.
        system_prompt = self._build_system_prompt(language, response_language)

        if config.ENABLE_RAG:
            enriched_system_prompt = self.rag.enrich_prompt(system_prompt, language, query)
        else:
            enriched_system_prompt = system_prompt

        user_prompt = f"[Respond in {response_language}] Question about {language}: {query}"
        if context:
            user_prompt = f"{context}\n\n{user_prompt}"

        print(f"[TIMING] Starting Ollama API call (streaming, model={self.model})...", flush=True)
        start_ollama = time.time()
        first_token_time = None

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": user_prompt,
                    "system": enriched_system_prompt,
                    "stream": True,
                    "keep_alive": config.KEEP_ALIVE,
                    "options": config.generation_options(),
                },
                stream=True,
                timeout=120,
            )
            
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if 'response' in chunk and chunk['response']:
                            if first_token_time is None:
                                first_token_time = time.time() - start_ollama
                                print(f"[TIMING] First token received after: {first_token_time:.2f}s", flush=True)
                            yield chunk['response']
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            print(f"Error in streaming: {e}")
            return

    def get_model_info(self):
        """Restituisce informazioni sul modello attivo (configurabile)."""
        descriptions = {
            'qwen2.5-coder': 'Modello di codice Qwen2.5-Coder (Alibaba), veloce e idiomatico',
            'codellama': 'Modello specializzato per programmazione sviluppato da Meta AI',
        }
        family = self.model.split(':')[0]
        version = self.model.split(':')[1] if ':' in self.model else 'latest'
        return {
            'name': self.model,
            'version': version,
            'description': descriptions.get(family, f'Modello Ollama: {self.model}'),
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
    """Risposta di fallback se Ollama non è disponibile"""
    return f"""I apologize, but I cannot access my neural network at this moment. 
The local LLM service (Ollama) appears to be offline.

To enable intelligent responses:
1. Install Ollama: https://ollama.ai
2. Run: ollama pull codellama
3. Start Ollama service

Your query about {language}: "{query}" will be processed once the service is available.

In the meantime, I can confirm this is a valid {language} programming question."""

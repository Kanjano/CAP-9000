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
from rag_system import get_rag_system

class LLMHandler:
    def __init__(self, ollama_url="http://localhost:11434"):
        """
        Inizializza l'handler LLM con CodeLlama
        
        CAP 9000 usa esclusivamente CodeLlama, un modello specializzato
        per programmazione sviluppato da Meta AI.
        
        Args:
            ollama_url: URL del server Ollama
        """
        self.model = "codellama"  # Unico modello supportato
        self.ollama_url = ollama_url
        self.available = self.check_ollama_available()
        self.rag = get_rag_system()  # Sistema RAG per documentazioni
    
    def check_ollama_available(self):
        """Verifica se Ollama è disponibile"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
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
        
        # Prompt bilanciato per risposte complete ma concise
        system_prompt = f"""You are CAP 9000, a CodeLlama-powered programming assistant.

CRITICAL RULE #1 - LANGUAGE (MANDATORY):
YOU MUST RESPOND **ONLY** IN {response_language}.
- EVERY word in {response_language}
- EVERY explanation in {response_language}
- EVERY code comment in {response_language}
- NO OTHER LANGUAGE ALLOWED
- This applies to ALL responses, not just the first one

CRITICAL RULE #2 - COMPLETENESS:
Be COMPLETE but CONCISE - provide all necessary components
For complex requests (APIs, microservices), include ALL layers (controller, service, repository)

RESPONSE FORMAT:
1. Brief answer (1 sentence in {response_language})
2. COMPLETE code with all components (controller, service, model, config)
3. Concise explanation of each part (in {response_language})
4. One key best practice (in {response_language})

STYLE:
- Clear, focused sentences in {response_language}
- Complete working examples
- All necessary files/classes
- Production-ready code

Programming Language: {language}
Response Language: {response_language} (ALWAYS)

Be complete, practical, efficient - IN {response_language}."""

        # Arricchisci il prompt con contesto RAG (documentazioni ufficiali + best practices)
        enriched_system_prompt = self.rag.enrich_prompt(system_prompt, language, query)
        
        # User prompt con reminder esplicito della lingua
        user_prompt = f"[RESPOND IN {response_language}] Question about {language}: {query}"
        
        if context:
            user_prompt = f"{context}\n\n{user_prompt}"
        
        print(f"[RAG] Prompt enriched with official documentation and best practices for {language}")
        
        try:
            # Chiamata API Ollama con prompt arricchito
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": f"{enriched_system_prompt}\n\n{user_prompt}",
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "top_k": 40,
                        "num_predict": 2048,
                        "repeat_penalty": 1.1,
                        "num_ctx": 4096
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                return None
                
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return None
    
    def generate_response_streaming(self, query, language, ui_language='en'):
        """
        Genera una risposta in streaming per visualizzazione progressiva
        
        Args:
            query: Domanda dell'utente
            language: Linguaggio di programmazione
            ui_language: Lingua dell'interfaccia
        
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
        
        # Usa lo stesso prompt bilanciato della versione non-streaming
        system_prompt = f"""You are CAP 9000, a CodeLlama-powered programming assistant.

CRITICAL RULE #1 - LANGUAGE (MANDATORY):
YOU MUST RESPOND **ONLY** IN {response_language}.
- EVERY word in {response_language}
- EVERY explanation in {response_language}
- EVERY code comment in {response_language}
- NO OTHER LANGUAGE ALLOWED
- This applies to ALL responses, not just the first one

CRITICAL RULE #2 - COMPLETENESS:
Be COMPLETE but CONCISE - provide all necessary components
For complex requests (APIs, microservices), include ALL layers (controller, service, repository)

RESPONSE FORMAT:
1. Brief answer (1 sentence in {response_language})
2. COMPLETE code with all components (controller, service, model, config)
3. Concise explanation of each part (in {response_language})
4. One key best practice (in {response_language})

STYLE:
- Clear, focused sentences in {response_language}
- Complete working examples
- All necessary files/classes
- Production-ready code

Programming Language: {language}
Response Language: {response_language} (ALWAYS)

Be complete, practical, efficient - IN {response_language}."""

        # Arricchisci il prompt con contesto RAG anche per streaming
        enriched_system_prompt = self.rag.enrich_prompt(system_prompt, language, query)
        
        # User prompt con reminder esplicito della lingua
        user_prompt = f"[RESPOND IN {response_language}] Question about {language}: {query}"
        
        print(f"[RAG Streaming] Prompt enriched with official documentation for {language}")

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": f"{enriched_system_prompt}\n\n{user_prompt}",
                    "stream": True,
                    "options": {
                        "temperature": 0.8,
                        "top_p": 0.95,
                        "top_k": 40,
                        "num_predict": 4096,
                        "repeat_penalty": 1.15,
                        "num_ctx": 8192
                    }
                },
                stream=True,
                timeout=120
            )
            
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if 'response' in chunk and chunk['response']:
                            yield chunk['response']
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            print(f"Error in streaming: {e}")
            return

    def get_model_info(self):
        """Restituisce informazioni sul modello CodeLlama"""
        return {
            'name': 'CodeLlama',
            'version': '7B',
            'description': 'Modello specializzato per programmazione sviluppato da Meta AI',
            'size': '3.8 GB',
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

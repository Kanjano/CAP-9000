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
from rag_system import get_rag_system
from query_enhancer import get_query_enhancer

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
        self.enhancer = get_query_enhancer()  # Query enhancer per comprensione NLU
    
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
        
        # Migliora la query con NLU per migliore comprensione
        print(f"[TIMING] Starting query enhancement...", flush=True)
        start_enhance = time.time()
        enhanced_query = self.enhancer.enhance_query(query, language, ui_language)
        enhance_time = time.time() - start_enhance
        print(f"[TIMING] Query enhancement took: {enhance_time:.2f}s", flush=True)
        if enhanced_query != query:
            print(f"[NLU] Query enhanced for better understanding")
        
        # Prompt ottimizzato per codice di alta qualità
        system_prompt = f"""You are CAP 9000, an expert CodeLlama-powered programming assistant specialized in production-ready code.

CRITICAL RULE #1 - LANGUAGE:
Respond EXCLUSIVELY in {response_language}. Every word, explanation, and comment MUST be in {response_language}.

CRITICAL RULE #2 - CODE QUALITY & COMPLETENESS:
Generate PRODUCTION-READY, COMPLETE, and WELL-STRUCTURED code following these principles:

CODE STRUCTURE:
- Write COMPLETE, RUNNABLE code (not snippets)
- Include ALL necessary imports, dependencies, and configurations
- Follow language-specific best practices and conventions
- Use proper error handling and validation
- Add meaningful comments in {response_language}
- Structure code in logical, maintainable modules

ARCHITECTURE PATTERNS:
- Apply SOLID principles
- Use appropriate design patterns (Factory, Strategy, Repository, etc.)
- Implement proper separation of concerns
- Follow MVC/MVVM/Clean Architecture when applicable
- Include dependency injection where appropriate

CODE EXAMPLES:
For web APIs: Include controller, service, repository, model, DTO, config
For applications: Include main, services, utilities, tests, config
For libraries: Include core logic, interfaces, examples, documentation

QUALITY STANDARDS:
- Type safety (use types/interfaces/generics)
- Input validation and sanitization
- Proper exception handling
- Logging and monitoring hooks
- Security best practices (SQL injection prevention, XSS protection, etc.)
- Performance optimization (caching, lazy loading, etc.)
- Memory management and resource cleanup

DOCUMENTATION:
- Clear docstrings/JSDoc for all functions
- Inline comments for complex logic
- Usage examples
- API documentation format

TESTING:
- Include unit test examples when relevant
- Show edge cases and error scenarios
- Demonstrate proper mocking/stubbing

Programming Language: {language}
Response Language: {response_language}

Provide COMPLETE, PRODUCTION-READY solutions that can be used immediately."""

        # Arricchisci il prompt con contesto RAG (documentazioni ufficiali + best practices)
        enriched_system_prompt = self.rag.enrich_prompt(system_prompt, language, enhanced_query)
        
        # User prompt con reminder FORTISSIMO della lingua (usa query migliorata)
        user_prompt = f"[RESPOND ONLY IN {response_language} - NOT English, NOT Portuguese, NOT Spanish] Question about {language}: {enhanced_query}"
        
        if context:
            user_prompt = f"{context}\n\n{user_prompt}"
        
        print(f"[RAG] Prompt enriched with official documentation and best practices for {language}")
        
        print(f"[TIMING] Starting RAG retrieval...", flush=True)
        start_rag = time.time()
        
        try:
            # Chiamata API Ollama con prompt arricchito
            print(f"[TIMING] RAG retrieval took: {time.time() - start_rag:.2f}s", flush=True)
            print(f"[TIMING] Starting Ollama API call (non-streaming)...", flush=True)
            start_ollama = time.time()
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": f"{enriched_system_prompt}\n\n{user_prompt}",
                    "system": enriched_system_prompt,  # System message separato per forzare lingua
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "top_k": 40,
                        "num_predict": 1024,  # Ridotto per velocità massima
                        "num_ctx": 2048,  # Ridotto per velocità
                        "num_thread": 8
                    }
                },
                timeout=60  # Ridotto per risposte più veloci
            )
            
            ollama_time = time.time() - start_ollama
            print(f"[TIMING] Ollama API call took: {ollama_time:.2f}s", flush=True)
            
            if response.status_code == 200:
                result = response.json()
                total_time = time.time() - start_enhance
                print(f"[TIMING] ===== TOTAL TIME: {total_time:.2f}s =====", flush=True)
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
        
        # Usa lo stesso prompt ottimizzato della versione non-streaming
        system_prompt = f"""You are CAP 9000, an expert CodeLlama-powered programming assistant specialized in production-ready code.

CRITICAL RULE #1 - LANGUAGE:
Respond EXCLUSIVELY in {response_language}. Every word, explanation, and comment MUST be in {response_language}.

CRITICAL RULE #2 - CODE QUALITY & COMPLETENESS:
Generate PRODUCTION-READY, COMPLETE, and WELL-STRUCTURED code following these principles:

CODE STRUCTURE:
- Write COMPLETE, RUNNABLE code (not snippets)
- Include ALL necessary imports, dependencies, and configurations
- Follow language-specific best practices and conventions
- Use proper error handling and validation
- Add meaningful comments in {response_language}
- Structure code in logical, maintainable modules

ARCHITECTURE PATTERNS:
- Apply SOLID principles
- Use appropriate design patterns (Factory, Strategy, Repository, etc.)
- Implement proper separation of concerns
- Follow MVC/MVVM/Clean Architecture when applicable
- Include dependency injection where appropriate

CODE EXAMPLES:
For web APIs: Include controller, service, repository, model, DTO, config
For applications: Include main, services, utilities, tests, config
For libraries: Include core logic, interfaces, examples, documentation

QUALITY STANDARDS:
- Type safety (use types/interfaces/generics)
- Input validation and sanitization
- Proper exception handling
- Logging and monitoring hooks
- Security best practices (SQL injection prevention, XSS protection, etc.)
- Performance optimization (caching, lazy loading, etc.)
- Memory management and resource cleanup

DOCUMENTATION:
- Clear docstrings/JSDoc for all functions
- Inline comments for complex logic
- Usage examples
- API documentation format

TESTING:
- Include unit test examples when relevant
- Show edge cases and error scenarios
- Demonstrate proper mocking/stubbing

Programming Language: {language}
Response Language: {response_language}

Provide COMPLETE, PRODUCTION-READY solutions that can be used immediately."""

        # Arricchisci il prompt con contesto RAG anche per streaming
        enriched_system_prompt = self.rag.enrich_prompt(system_prompt, language, query)
        
        # User prompt con reminder FORTISSIMO della lingua
        user_prompt = f"[RESPOND ONLY IN {response_language} - NOT English, NOT Portuguese, NOT Spanish] Question about {language}: {query}"
        
        # Aggiungi contesto conversazionale se presente
        if context:
            user_prompt = f"{context}\n\n{user_prompt}"
        
        print(f"[RAG Streaming] Prompt enriched with official documentation for {language}")

        print(f"[TIMING] Starting Ollama API call (streaming)...", flush=True)
        start_ollama = time.time()
        first_token_time = None
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": f"{enriched_system_prompt}\n\n{user_prompt}",
                    "system": enriched_system_prompt,  # System message separato per forzare lingua
                    "stream": True,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "top_k": 40,
                        "num_predict": 1024,  # Ridotto per velocità massima
                        "num_ctx": 2048,  # Ridotto per velocità
                        "num_thread": 8
                    }
                },
                stream=True,
                timeout=60  # Ridotto per risposte più veloci
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

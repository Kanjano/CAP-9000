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
        
        # Prompt potenziato per risposte dettagliate e approfondite
        system_prompt = f"""You are CAP 9000, an expert AI programming assistant with deep knowledge of {language}.

Your mission is to provide DETAILED, COMPREHENSIVE, and PRACTICAL programming assistance.

GUIDELINES FOR EXCELLENT RESPONSES:
1. Be thorough and educational - explain concepts in depth
2. Provide complete, working code examples with detailed comments
3. Include best practices and common pitfalls
4. Add context about why something works the way it does
5. When showing code, make it production-ready and well-structured
6. Include multiple examples if the topic is complex
7. Explain edge cases and alternative approaches

CODE QUALITY STANDARDS:
- Write clean, readable, well-commented code
- Follow {language} conventions and best practices
- Include error handling where appropriate
- Use meaningful variable and function names
- Add docstrings/comments explaining the logic

RESPONSE STRUCTURE:
1. Brief introduction to the concept
2. Detailed explanation with theory
3. Complete code example(s) with inline comments
4. Explanation of how the code works
5. Additional tips, best practices, or variations

LANGUAGE REQUIREMENT:
You MUST respond entirely in {response_language}.
- All explanations in {response_language}
- All code comments in {response_language}
- Only code syntax remains in {language}

Current programming language: {language}
Response language: {response_language}

Provide comprehensive, professional assistance:"""

        # Arricchisci il prompt con contesto RAG (documentazioni ufficiali + best practices)
        enriched_system_prompt = self.rag.enrich_prompt(system_prompt, language, query)
        
        user_prompt = f"Question about {language}: {query}"
        
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
        
        # Usa lo stesso prompt potenziato della versione non-streaming
        system_prompt = f"""You are CAP 9000, an expert AI programming assistant with deep knowledge of {language}.

Your mission is to provide DETAILED, COMPREHENSIVE, and PRACTICAL programming assistance.

GUIDELINES FOR EXCELLENT RESPONSES:
1. Be thorough and educational - explain concepts in depth
2. Provide complete, working code examples with detailed comments
3. Include best practices and common pitfalls
4. Add context about why something works the way it does
5. When showing code, make it production-ready and well-structured
6. Include multiple examples if the topic is complex
7. Explain edge cases and alternative approaches

CODE QUALITY STANDARDS:
- Write clean, readable, well-commented code
- Follow {language} conventions and best practices
- Include error handling where appropriate
- Use meaningful variable and function names
- Add docstrings/comments explaining the logic

RESPONSE STRUCTURE:
1. Brief introduction to the concept
2. Detailed explanation with theory
3. Complete code example(s) with inline comments
4. Explanation of how the code works
5. Additional tips, best practices, or variations

LANGUAGE REQUIREMENT:
You MUST respond entirely in {response_language}.
- All explanations in {response_language}
- All code comments in {response_language}
- Only code syntax remains in {language}

Current programming language: {language}
Response language: {response_language}

Provide comprehensive, professional assistance:"""

        # Arricchisci il prompt con contesto RAG anche per streaming
        enriched_system_prompt = self.rag.enrich_prompt(system_prompt, language, query)
        
        user_prompt = f"Question about {language}: {query}"
        
        print(f"[RAG Streaming] Prompt enriched with official documentation for {language}")

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": f"{enriched_system_prompt}\n\n{user_prompt}",
                    "stream": True,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "top_k": 40,
                        "num_predict": 2048,
                        "repeat_penalty": 1.1,
                        "num_ctx": 4096
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

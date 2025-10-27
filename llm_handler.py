"""
LLM Handler per CAP 9000 Code Assistant
Supporta Ollama per modelli locali
"""

import requests
import json

class LLMHandler:
    def __init__(self, model="codellama", ollama_url="http://localhost:11434"):
        """
        Inizializza l'handler LLM
        
        Args:
            model: Nome del modello Ollama (codellama, llama2, mistral, ecc.)
            ollama_url: URL del server Ollama
        """
        self.model = model
        self.ollama_url = ollama_url
        self.available = self.check_ollama_available()
    
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

        user_prompt = f"Question about {language}: {query}"
        
        if context:
            user_prompt = f"{context}\n\n{user_prompt}"
        
        try:
            # Chiamata API Ollama
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": f"{system_prompt}\n\n{user_prompt}",
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

        user_prompt = f"Question about {language}: {query}"

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": f"{system_prompt}\n\n{user_prompt}",
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

    def list_available_models(self):
        """Lista i modelli disponibili in Ollama"""
        if not self.available:
            return []
        
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except:
            return []


# Modelli consigliati per coding (ordinati per qualità)
RECOMMENDED_MODELS = {
    'qwen2.5-coder:32b': 'Qwen2.5 Coder 32B - MIGLIORE per coding (richiede GPU potente)',
    'deepseek-coder:33b': 'DeepSeek Coder 33B - Eccellente qualità, risposte dettagliate',
    'codellama:34b': 'CodeLlama 34B - Molto potente per programmazione',
    'qwen2.5-coder:14b': 'Qwen2.5 Coder 14B - Ottimo compromesso qualità/velocità',
    'deepseek-coder:6.7b': 'DeepSeek Coder 6.7B - Veloce e accurato',
    'codellama:13b': 'CodeLlama 13B - Buon equilibrio',
    'codellama': 'CodeLlama 7B - Base, veloce ma meno dettagliato',
    'mistral': 'Mistral 7B - General purpose, buono per spiegazioni',
    'phi3:14b': 'Phi-3 14B - Compatto ma potente',
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

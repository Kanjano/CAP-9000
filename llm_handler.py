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
        
        # Costruisci il prompt in stile CAP 9000
        system_prompt = f"""You are CAP 9000, an advanced AI code assistant. You provide clear, concise, and accurate programming help.
You are knowledgeable about {language} programming.
Always respond in a professional but slightly formal tone, like CAP 9000 from "2001: A Space Odyssey".
Provide code examples when relevant.
Keep responses focused and practical.

IMPORTANT: You MUST respond in {response_language}. This is not optional.
All explanations, comments, and text MUST be in {response_language}.
Only code examples should remain in {language} syntax.

If you are asked to respond in a specific language, you MUST respect that request.

Current response language: {response_language}

Example of how to respond in {response_language}:
""" + (
    """
    Ecco un esempio di come dovresti rispondere in italiano:
    - Spiegazioni in italiano
    - Commenti nel codice in italiano
    - Solo la sintassi del codice in {language}
    """ if ui_language == 'it' else
    """
    Here's an example of how you should respond in English:
    - Explanations in English
    - Code comments in English
    - Only code syntax in {language}
    """
)

# Inizia la tua risposta in {response_language} qui sotto:"""

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
                        "top_p": 0.9,
                        "max_tokens": 500
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                return None
                
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return None
    
    def generate_response_streaming(self, query, language):
        """
        Genera una risposta in streaming (per future implementazioni)
        
        Args:
            query: Domanda dell'utente
            language: Linguaggio di programmazione
        
        Yields:
            str: Chunks della risposta
        """
        if not self.available:
            return
        
        system_prompt = f"""You are CAP 9000, an advanced AI code assistant for {language} programming.
Respond professionally and provide code examples when relevant."""

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": f"{system_prompt}\n\nQuestion: {query}",
                    "stream": True
                },
                stream=True,
                timeout=30
            )
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if 'response' in chunk:
                        yield chunk['response']
                        
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


# Modelli consigliati per coding
RECOMMENDED_MODELS = {
    'codellama': 'CodeLlama - Ottimizzato per programmazione (7B)',
    'codellama:13b': 'CodeLlama 13B - Più potente ma più lento',
    'deepseek-coder': 'DeepSeek Coder - Eccellente per codice',
    'mistral': 'Mistral - Buon equilibrio qualità/velocità',
    'llama2': 'Llama 2 - Modello general purpose',
    'phi': 'Phi - Piccolo e veloce (2.7B)',
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

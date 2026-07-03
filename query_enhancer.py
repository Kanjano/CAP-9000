"""
Query Enhancer per CAP 9000

Migliora la comprensione delle domande usando un modello NLU
prima di passarle a Mistral per la generazione del codice.

Strategia: Usa un modello generale (Mistral/Llama2) per:
1. Comprendere l'intento della domanda
2. Estrarre dettagli tecnici
3. Riformulare in modo più chiaro per Mistral
"""

import requests
import json


class QueryEnhancer:
    def __init__(self, ollama_url="http://localhost:11434"):
        """
        Inizializza il Query Enhancer
        
        Args:
            ollama_url: URL del server Ollama
        """
        self.ollama_url = ollama_url
        self.nlu_model = "mistral"  # Modello per comprensione linguaggio naturale
        
    def check_nlu_model_available(self):
        """Verifica se il modello NLU è disponibile"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get('models', [])
                return any(self.nlu_model in model['name'] for model in models)
            return False
        except:
            return False
    
    def enhance_query(self, query, language, ui_language='it'):
        """
        Migliora la query per una migliore comprensione da parte di Mistral
        
        Args:
            query: Domanda originale dell'utente
            language: Linguaggio di programmazione
            ui_language: Lingua dell'interfaccia
            
        Returns:
            str: Query migliorata e più dettagliata
        """
        # Se il modello NLU non è disponibile, ritorna la query originale
        if not self.check_nlu_model_available():
            print(f"[Query Enhancer] {self.nlu_model} not available, using original query")
            return query
        
        # Mappa lingue
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
        
        # Prompt per il modello NLU
        enhancement_prompt = f"""You are a technical query analyzer. 

Your task: Analyze this programming question and extract key technical details.

Original question (in {response_language}): "{query}"
Programming language: {language}

Extract and list:
1. Main intent (what the user wants to do)
2. Technical components needed (classes, functions, libraries)
3. Specific requirements mentioned
4. Missing details that should be included

Respond in {response_language} with a clear, detailed technical description.
Be concise but complete. Focus on technical specifics."""

        try:
            # Chiamata al modello NLU
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.nlu_model,
                    "prompt": enhancement_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,  # Più deterministico
                        "num_predict": 512,  # Risposta breve
                        "num_ctx": 2048
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                enhanced = result.get('response', '').strip()
                
                # Combina query originale con enhancement
                if enhanced:
                    print(f"[Query Enhancer] Query enhanced with {self.nlu_model}")
                    # Ritorna query arricchita
                    return f"{query}\n\nTechnical details: {enhanced}"
                
        except Exception as e:
            print(f"[Query Enhancer] Error: {e}")
        
        # Fallback: ritorna query originale
        return query
    
    def extract_intent(self, query, language):
        """
        Estrae l'intento principale dalla query
        
        Args:
            query: Domanda dell'utente
            language: Linguaggio di programmazione
            
        Returns:
            dict: Intento e dettagli estratti
        """
        if not self.check_nlu_model_available():
            return {
                'intent': 'code_generation',
                'components': [],
                'details': query
            }
        
        intent_prompt = f"""Analyze this programming question and extract:
1. Intent (create, explain, debug, optimize, refactor)
2. Components (API, microservice, function, class, etc.)
3. Key requirements

Question: "{query}"
Language: {language}

Respond in JSON format:
{{"intent": "...", "components": [...], "requirements": [...]}}"""

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.nlu_model,
                    "prompt": intent_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2,
                        "num_predict": 256,
                        "num_ctx": 1024
                    }
                },
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                intent_text = result.get('response', '').strip()
                
                # Prova a parsare JSON
                try:
                    return json.loads(intent_text)
                except:
                    pass
                    
        except Exception as e:
            print(f"[Intent Extraction] Error: {e}")
        
        # Fallback
        return {
            'intent': 'code_generation',
            'components': [],
            'details': query
        }


# Singleton instance
_enhancer_instance = None

def get_query_enhancer():
    """Ottieni istanza singleton del Query Enhancer"""
    global _enhancer_instance
    if _enhancer_instance is None:
        _enhancer_instance = QueryEnhancer()
    return _enhancer_instance

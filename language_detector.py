"""
Sistema di riconoscimento automatico della lingua dell'utente
Rileva la lingua del testo e CAP 9000 risponde nella stessa lingua
"""

import re
from typing import Optional

class LanguageDetector:
    """Rileva automaticamente la lingua del testo dell'utente"""
    
    def __init__(self):
        # Pattern e parole chiave per ogni lingua
        self.language_patterns = {
            'it': {
                'keywords': [
                    'come', 'cosa', 'perché', 'quando', 'dove', 'chi', 'quale',
                    'ciao', 'grazie', 'prego', 'scusa', 'aiuto', 'esempio',
                    'funziona', 'fare', 'creare', 'usare', 'implementare',
                    'spiegare', 'mostrare', 'voglio', 'posso', 'devo',
                    'mi', 'ti', 'lo', 'la', 'gli', 'le', 'sono', 'è',
                    'un', 'una', 'il', 'dello', 'della', 'degli', 'delle'
                ],
                'patterns': [
                    r'\b(è|perché|così|più)\b',
                    r'\b(mi|ti|ci|vi|si)\s+\w+',
                    r'\b\w+are\b',  # verbi infinito -are
                    r'\b\w+zione\b',  # sostantivi -zione
                ]
            },
            'en': {
                'keywords': [
                    'how', 'what', 'why', 'when', 'where', 'who', 'which',
                    'hello', 'thanks', 'please', 'sorry', 'help', 'example',
                    'works', 'make', 'create', 'use', 'implement',
                    'explain', 'show', 'want', 'can', 'should', 'need',
                    'the', 'a', 'an', 'is', 'are', 'was', 'were',
                    'do', 'does', 'did', 'have', 'has', 'had'
                ],
                'patterns': [
                    r'\b(the|a|an)\s+\w+',
                    r'\b\w+ing\b',  # gerundi
                    r'\b\w+ed\b',   # past tense
                    r'\b(is|are|was|were)\s+\w+',
                ]
            },
            'fr': {
                'keywords': [
                    'comment', 'quoi', 'pourquoi', 'quand', 'où', 'qui', 'quel',
                    'bonjour', 'merci', 's\'il vous plaît', 'désolé', 'aide',
                    'fonctionne', 'faire', 'créer', 'utiliser', 'implémenter',
                    'expliquer', 'montrer', 'veux', 'peux', 'dois',
                    'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de',
                    'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils'
                ],
                'patterns': [
                    r'\b(le|la|les|un|une|des)\s+\w+',
                    r'\b\w+tion\b',
                    r'\b(est|sont|était|étaient)\s+\w+',
                ]
            },
            'de': {
                'keywords': [
                    'wie', 'was', 'warum', 'wann', 'wo', 'wer', 'welche',
                    'hallo', 'danke', 'bitte', 'entschuldigung', 'hilfe',
                    'funktioniert', 'machen', 'erstellen', 'verwenden',
                    'erklären', 'zeigen', 'will', 'kann', 'soll',
                    'der', 'die', 'das', 'ein', 'eine', 'den', 'dem',
                    'ich', 'du', 'er', 'sie', 'wir', 'ihr'
                ],
                'patterns': [
                    r'\b(der|die|das|ein|eine)\s+\w+',
                    r'\b\w+ung\b',
                    r'\b(ist|sind|war|waren)\s+\w+',
                ]
            },
            'es': {
                'keywords': [
                    'cómo', 'qué', 'por qué', 'cuándo', 'dónde', 'quién', 'cuál',
                    'hola', 'gracias', 'por favor', 'perdón', 'ayuda',
                    'funciona', 'hacer', 'crear', 'usar', 'implementar',
                    'explicar', 'mostrar', 'quiero', 'puedo', 'debo',
                    'el', 'la', 'los', 'las', 'un', 'una', 'del', 'de',
                    'yo', 'tú', 'él', 'ella', 'nosotros', 'vosotros'
                ],
                'patterns': [
                    r'\b(el|la|los|las|un|una)\s+\w+',
                    r'\b\w+ción\b',
                    r'\b(es|son|era|eran)\s+\w+',
                ]
            },
            'pt': {
                'keywords': [
                    'como', 'o que', 'por que', 'quando', 'onde', 'quem', 'qual',
                    'olá', 'obrigado', 'por favor', 'desculpe', 'ajuda',
                    'funciona', 'fazer', 'criar', 'usar', 'implementar',
                    'explicar', 'mostrar', 'quero', 'posso', 'devo',
                    'o', 'a', 'os', 'as', 'um', 'uma', 'do', 'da',
                    'eu', 'tu', 'ele', 'ela', 'nós', 'vós'
                ],
                'patterns': [
                    r'\b(o|a|os|as|um|uma)\s+\w+',
                    r'\b\w+ção\b',
                    r'\b(é|são|era|eram)\s+\w+',
                ]
            },
            'nl': {
                'keywords': [
                    'hoe', 'wat', 'waarom', 'wanneer', 'waar', 'wie', 'welke',
                    'hallo', 'dank je', 'alsjeblieft', 'sorry', 'hulp',
                    'werkt', 'maken', 'creëren', 'gebruiken', 'implementeren',
                    'uitleggen', 'tonen', 'wil', 'kan', 'moet',
                    'de', 'het', 'een', 'van', 'voor', 'op',
                    'ik', 'jij', 'hij', 'zij', 'wij', 'jullie'
                ],
                'patterns': [
                    r'\b(de|het|een)\s+\w+',
                    r'\b\w+ing\b',
                    r'\b(is|zijn|was|waren)\s+\w+',
                ]
            },
            'pl': {
                'keywords': [
                    'jak', 'co', 'dlaczego', 'kiedy', 'gdzie', 'kto', 'który',
                    'cześć', 'dziękuję', 'proszę', 'przepraszam', 'pomoc',
                    'działa', 'zrobić', 'stworzyć', 'użyć', 'zaimplementować',
                    'wyjaśnić', 'pokazać', 'chcę', 'mogę', 'powinienem',
                    'jest', 'są', 'był', 'byli', 'w', 'na', 'do'
                ],
                'patterns': [
                    r'\b(jest|są|był|byli)\s+\w+',
                    r'\b\w+ować\b',
                    r'\b\w+acja\b',
                ]
            }
        }
    
    def detect_language(self, text: str) -> str:
        """
        Rileva la lingua del testo
        
        Args:
            text: Testo da analizzare
        
        Returns:
            Codice lingua (it, en, fr, de, es, pt, nl, pl) - default 'en'
        """
        if not text or len(text.strip()) < 3:
            return 'en'  # Default inglese
        
        text_lower = text.lower()
        scores = {}
        
        # Calcola score per ogni lingua
        for lang_code, lang_data in self.language_patterns.items():
            score = 0
            
            # Score da keywords
            for keyword in lang_data['keywords']:
                if keyword in text_lower:
                    # Keyword esatta vale di più
                    if f' {keyword} ' in f' {text_lower} ':
                        score += 3
                    else:
                        score += 1
            
            # Score da pattern regex
            for pattern in lang_data['patterns']:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                score += len(matches) * 2
            
            scores[lang_code] = score
        
        # Trova lingua con score più alto
        if not scores or max(scores.values()) == 0:
            return 'en'  # Default se nessun match
        
        detected_lang = max(scores, key=scores.get)
        
        # Log per debug
        print(f"[Language Detection] Text: '{text[:50]}...' -> Detected: {detected_lang} (scores: {scores})")
        
        return detected_lang


# Singleton instance
_detector_instance = None

def get_language_detector() -> LanguageDetector:
    """Ottiene l'istanza singleton del detector"""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = LanguageDetector()
    return _detector_instance

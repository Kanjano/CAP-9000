#!/usr/bin/env python3
"""
Python Bridge per Electron
Comunicazione diretta via stdin/stdout con JSON
Elimina overhead HTTP Flask
"""

import sys
import json
import traceback
import io

# CRITICAL: Redirect all print() to stderr to avoid polluting stdout (used for JSON)
# Save original stdout for JSON responses
_original_stdout = sys.stdout
sys.stdout = sys.stderr

from hybrid_llm_handler import get_hybrid_handler
from language_detector import LanguageDetector

# Inizializza handler
print("Initializing Hybrid LLM Handler...", file=sys.stderr, flush=True)
llm = get_hybrid_handler(
    enable_reasoning=True,
    enable_cache=True,
    num_recursions=3
)

detector = LanguageDetector()
print("Python Bridge ready", file=sys.stderr, flush=True)

def process_query(request_id, data, streaming=False):
    """Processa una query e ritorna risposta (con supporto streaming e contesto)"""
    try:
        query = data.get('query', '')
        language = data.get('language', 'Python')
        ui_language = data.get('ui_language', 'en')
        context = data.get('context', [])
        
        print(f"Processing query: {query[:50]}... (streaming={streaming}, context_msgs={len(context)})", file=sys.stderr, flush=True)
        
        # Auto-detect UI language se non specificato
        if not ui_language or ui_language == 'auto':
            ui_language = detector.detect_language(query)
        
        # Costruisci contesto conversazionale
        context_str = ""
        if context and len(context) > 0:
            context_str = "\n\nPREVIOUS CONVERSATION:\n"
            for msg in context:
                role = "User" if msg.get('role') == 'user' else "Assistant"
                content = msg.get('content', '')[:200]  # Limita lunghezza
                context_str += f"{role}: {content}\n"
            context_str += "\nCurrent question (consider the conversation above):\n"
        
        if streaming:
            # Streaming mode - invia chunks progressivamente
            try:
                for chunk in llm.generate_response_streaming(query, language, ui_language, context_str):
                    chunk_response = {
                        'id': request_id,
                        'type': 'chunk',
                        'data': {
                            'content': chunk,
                            'done': False
                        }
                    }
                    print(json.dumps(chunk_response), file=_original_stdout, flush=True)
                
                # Segnala completamento
                final_response = {
                    'id': request_id,
                    'type': 'chunk',
                    'data': {
                        'content': '',
                        'done': True,
                        'language': language,
                        'source': 'hybrid_llm'
                    }
                }
                print(json.dumps(final_response), file=_original_stdout, flush=True)
                return None  # Non ritornare nulla, già inviato via streaming
                
            except Exception as e:
                print(f"Streaming error: {e}", file=sys.stderr, flush=True)
                traceback.print_exc(file=sys.stderr)
                return {
                    'id': request_id,
                    'data': {
                        'response': f"I apologize, but an error occurred: {str(e)}",
                        'error': True,
                        'source': 'error'
                    }
                }
        else:
            # Non-streaming mode - risposta completa
            response = llm.generate_response(query, language, ui_language, context_str)
            
            # Determina se reasoning è stato usato
            stats = llm.get_stats()
            reasoning_used = stats.get('queries', {}).get('reasoning', 0) > 0
            
            # Ritorna risultato
            return {
                'id': request_id,
                'data': {
                    'response': response if response else "I apologize, but I cannot process this request at the moment.",
                    'language': language,
                    'error': False if response else True,
                    'source': 'hybrid_llm',
                    'reasoning_used': reasoning_used
                }
            }
    except Exception as e:
        print(f"Error processing query: {e}", file=sys.stderr, flush=True)
        traceback.print_exc(file=sys.stderr)
        return {
            'id': request_id,
            'data': {
                'response': f"I apologize, but an error occurred: {str(e)}",
                'error': True,
                'source': 'error'
            }
        }

def process_stats(request_id):
    """Ritorna statistiche sistema"""
    try:
        stats = llm.get_stats()
        return {
            'id': request_id,
            'data': stats
        }
    except Exception as e:
        return {
            'id': request_id,
            'data': {
                'error': True,
                'message': str(e)
            }
        }

def main():
    """Main loop - legge da stdin, scrive su stdout"""
    # Segnala ready (usa original stdout per JSON)
    print(json.dumps({'status': 'ready'}), file=_original_stdout, flush=True)
    
    try:
        for line in sys.stdin:
            try:
                line = line.strip()
                if not line:
                    continue
                    
                request = json.loads(line)
                request_id = request.get('id')
                request_type = request.get('type')
                request_data = request.get('data', {})
                
                if request_type == 'query':
                    streaming = request_data.get('streaming', False)
                    result = process_query(request_id, request_data, streaming=streaming)
                    if result:  # Solo se non streaming (streaming invia chunks direttamente)
                        print(json.dumps(result), file=_original_stdout, flush=True)
                elif request_type == 'stats':
                    result = process_stats(request_id)
                    print(json.dumps(result), file=_original_stdout, flush=True)
                elif request_type == 'exit':
                    print(json.dumps({'id': request_id, 'data': {'status': 'exiting'}}), file=_original_stdout, flush=True)
                    break
                    
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}", file=sys.stderr, flush=True)
                error_response = {
                    'id': 0,
                    'data': {
                        'error': True,
                        'message': f'Invalid JSON: {str(e)}'
                    }
                }
                print(json.dumps(error_response), file=_original_stdout, flush=True)
            except Exception as e:
                print(f"Error processing request: {e}", file=sys.stderr, flush=True)
                traceback.print_exc(file=sys.stderr)
                error_response = {
                    'id': request.get('id', 0) if 'request' in locals() else 0,
                    'data': {
                        'error': True,
                        'message': str(e)
                    }
                }
                print(json.dumps(error_response), file=_original_stdout, flush=True)
    except KeyboardInterrupt:
        print("Python Bridge interrupted", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr, flush=True)
        traceback.print_exc(file=sys.stderr)

if __name__ == '__main__':
    main()

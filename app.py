from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from main import CodeAssistant
from languages import languages
from knowledge_base import find_answer
from llm_handler import LLMHandler, get_fallback_response
from language_detector import get_language_detector
import json

app = Flask(__name__)
CORS(app)

# Initialize the assistant
assistant = CodeAssistant()

# Initialize LLM handler con CodeLlama
llm = LLMHandler()
print(f"CodeLlama (via Ollama) available: {llm.available}")
if llm.available:
    model_info = llm.get_model_info()
    print(f"Model: {model_info['name']} {model_info['version']}")
    print(f"Specialized for: {', '.join(model_info['features'])}")

# Initialize language detector
lang_detector = get_language_detector()
print("Language detector initialized")

@app.route('/api/query', methods=['POST'])
def handle_query():
    data = request.json
    query = data.get('query', '')
    language = data.get('language', 'Python')
    
    # Rileva automaticamente la lingua dell'utente dal testo
    ui_language = lang_detector.detect_language(query)
    print(f"Received request - Query: '{query}', Language: '{language}', Auto-detected UI Language: '{ui_language}'")
    
    # Set the language
    assistant.set_language(language)
    
    # Check if language is supported
    if language not in languages:
        return jsonify({
            'response': f"I'm afraid I cannot process {language}. Supported languages are: {', '.join(languages)}",
            'error': True
        })
    
    # Try LLM first (if available)
    if llm.available:
        print(f"Using LLM for query: '{query}' in language: '{language}' with UI language: '{ui_language}'", flush=True)
        print(f"[DEBUG] About to call llm.generate_response()...", flush=True)
        llm_response = llm.generate_response(query, language, ui_language)
        print(f"[DEBUG] llm.generate_response() returned", flush=True)
        print(f"LLM response language: {llm_response[:100]}..." if llm_response else "No response from LLM", flush=True)
        
        if llm_response:
            response = llm_response
            return jsonify({
                'response': response,
                'language': language,
                'error': False,
                'source': 'llm'
            })
    
    # Fallback to knowledge base
    print(f"Using knowledge base for query: {query}")
    answer = find_answer(language, query)
    
    if answer:
        # CAP found a specific answer in knowledge base
        response = f"Here is what I know about {language}:\n\n{answer}\n\nThis information should address your query regarding: '{query}'"
        source = 'knowledge_base'
    else:
        # Last resort: generic response
        if not llm.available:
            response = get_fallback_response(language, query)
            source = 'fallback_ollama_offline'
        else:
            response = f"I have received your {language} query: '{query}'. While I have this in my database, I need more specific information to provide a detailed answer. Try asking about: variables, functions, loops, classes, or other specific programming concepts."
            source = 'fallback_generic'
    
    return jsonify({
        'response': response,
        'language': language,
        'error': False,
        'source': source
    })

@app.route('/api/query/stream', methods=['POST'])
def handle_query_stream():
    """Endpoint per streaming delle risposte in tempo reale"""
    data = request.json
    query = data.get('query', '')
    language = data.get('language', 'Python')
    
    # Rileva automaticamente la lingua dell'utente dal testo
    ui_language = lang_detector.detect_language(query)
    print(f"Streaming request - Query: '{query}', Language: '{language}', Auto-detected UI Language: '{ui_language}'")
    
    def generate():
        # Set the language
        assistant.set_language(language)
        
        # Check if language is supported
        if language not in languages:
            yield f"data: {json.dumps({'error': True, 'content': f'Language {language} not supported'})}\n\n"
            return
        
        # Try LLM streaming
        if llm.available:
            try:
                for chunk in llm.generate_response_streaming(query, language, ui_language):
                    if chunk:
                        yield f"data: {json.dumps({'content': chunk, 'done': False})}\n\n"
                
                # Segnala fine stream
                yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
            except Exception as e:
                print(f"Streaming error: {e}")
                yield f"data: {json.dumps({'error': True, 'content': str(e)})}\n\n"
        else:
            # Fallback senza streaming
            answer = find_answer(language, query)
            if answer:
                response = f"Here is what I know about {language}:\n\n{answer}"
            else:
                response = get_fallback_response(language, query)
            
            # Simula streaming per consistenza
            for char in response:
                yield f"data: {json.dumps({'content': char, 'done': False})}\n\n"
            yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )

@app.route('/api/languages', methods=['GET'])
def get_languages():
    return jsonify({
        'languages': languages
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001, threaded=True)

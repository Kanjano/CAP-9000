"""
Sistema RAG (Retrieval-Augmented Generation) per CAP 9000
Integra documentazioni ufficiali e best practices nei prompt di Ollama
Supporta documentazioni locali scaricate + fallback hardcoded
"""

import requests
import json
import os
from pathlib import Path
from typing import List, Dict, Optional

class DocumentationRAG:
    """Sistema RAG per arricchire le risposte con documentazione ufficiale"""
    
    def __init__(self):
        self.docs_cache = {}
        self.local_docs_dir = Path("local_docs")
        self.local_docs_available = self.check_local_docs()
        self.load_documentation_sources()
        
        if self.local_docs_available:
            print(f"✓ Local documentation found in {self.local_docs_dir}")
            self.load_local_docs_index()
        else:
            print("⚠ No local docs found. Using hardcoded fallback.")
            print(f"  Run 'python download_docs.py' to download docs for offline use.")
    
    def check_local_docs(self) -> bool:
        """Verifica se esistono documentazioni locali"""
        return self.local_docs_dir.exists() and (self.local_docs_dir / "index.json").exists()
    
    def load_local_docs_index(self):
        """Carica l'indice delle documentazioni locali"""
        try:
            index_file = self.local_docs_dir / "index.json"
            with open(index_file, 'r', encoding='utf-8') as f:
                self.local_docs_index = json.load(f)
                print(f"  → Loaded {len(self.local_docs_index.get('languages', {}))} language docs")
        except Exception as e:
            print(f"  ✗ Error loading local docs index: {e}")
            self.local_docs_available = False
    
    def read_local_doc(self, language: str, doc_name: str) -> Optional[str]:
        """Legge una documentazione locale"""
        if not self.local_docs_available:
            return None
        
        # Mappa nomi linguaggi
        lang_map = {
            'Python': 'python',
            'Java': 'java',
            'JavaScript': 'javascript',
            'C': 'c',
            'C++': 'cpp',
            'Go': 'go'
        }
        
        lang_dir = lang_map.get(language, language.lower())
        doc_path = self.local_docs_dir / lang_dir / f"{doc_name}.txt"
        
        if doc_path.exists():
            try:
                # Leggi solo i primi 5000 caratteri per non sovraccaricare il prompt
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read(5000)
                return content
            except Exception as e:
                print(f"  ✗ Error reading {doc_path}: {e}")
                return None
        
        return None
    
    def load_documentation_sources(self):
        """Carica le fonti di documentazione ufficiale per ogni linguaggio"""
        self.documentation_sources = {
            'Python': {
                'official_docs': 'https://docs.python.org/3/',
                'pep8': 'https://peps.python.org/pep-0008/',
                'best_practices': [
                    'Use list comprehensions for simple transformations',
                    'Prefer f-strings for string formatting',
                    'Use context managers (with statement) for resource management',
                    'Follow PEP 8 style guide',
                    'Use type hints for better code documentation',
                    'Prefer pathlib over os.path for file operations',
                    'Use dataclasses for data containers',
                    'Handle exceptions specifically, avoid bare except',
                    'Use virtual environments for project isolation',
                    'Write docstrings for all public functions and classes'
                ],
                'common_patterns': {
                    'file_reading': 'with open(file) as f: content = f.read()',
                    'list_comprehension': '[x for x in items if condition]',
                    'dictionary_comprehension': '{k: v for k, v in items.items()}',
                    'error_handling': 'try: ... except SpecificError as e: ...',
                    'class_definition': 'class MyClass:\n    def __init__(self, param): ...'
                }
            },
            'Java': {
                'official_docs': 'https://docs.oracle.com/en/java/',
                'best_practices': [
                    'Follow Java naming conventions (camelCase for methods, PascalCase for classes)',
                    'Use interfaces for abstraction',
                    'Prefer composition over inheritance',
                    'Use try-with-resources for automatic resource management',
                    'Make classes immutable when possible',
                    'Override equals() and hashCode() together',
                    'Use StringBuilder for string concatenation in loops',
                    'Prefer EnumSet over bit fields',
                    'Use Optional to avoid null pointer exceptions',
                    'Follow SOLID principles'
                ],
                'common_patterns': {
                    'class_definition': 'public class MyClass { ... }',
                    'interface': 'public interface MyInterface { ... }',
                    'try_with_resources': 'try (Resource r = new Resource()) { ... }',
                    'singleton': 'private static final MyClass INSTANCE = new MyClass();',
                    'builder_pattern': 'MyClass.builder().field(value).build()'
                }
            },
            'JavaScript': {
                'official_docs': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
                'best_practices': [
                    'Use const by default, let when reassignment needed, avoid var',
                    'Prefer arrow functions for callbacks',
                    'Use async/await instead of promise chains',
                    'Destructure objects and arrays',
                    'Use template literals for string interpolation',
                    'Avoid callback hell with promises or async/await',
                    'Use strict equality (===) instead of loose equality (==)',
                    'Handle errors in async functions with try/catch',
                    'Use modern ES6+ features',
                    'Prefer map, filter, reduce over for loops'
                ],
                'common_patterns': {
                    'arrow_function': 'const func = (param) => { ... }',
                    'async_await': 'async function fetchData() { const data = await fetch(url); }',
                    'destructuring': 'const { name, age } = person;',
                    'spread_operator': 'const newArray = [...oldArray, newItem];',
                    'promise': 'fetch(url).then(response => response.json()).catch(error => ...)'
                }
            },
            'C': {
                'official_docs': 'https://en.cppreference.com/w/c',
                'best_practices': [
                    'Always initialize variables',
                    'Check return values of functions',
                    'Free all allocated memory',
                    'Use const for read-only pointers',
                    'Avoid magic numbers, use named constants',
                    'Check array bounds manually',
                    'Use size_t for array indices and sizes',
                    'Prefer snprintf over sprintf',
                    'Initialize pointers to NULL',
                    'Use header guards in .h files'
                ],
                'common_patterns': {
                    'memory_allocation': 'int *ptr = (int*)malloc(size * sizeof(int));',
                    'string_copy': 'strncpy(dest, src, sizeof(dest) - 1);',
                    'file_operations': 'FILE *fp = fopen(filename, "r"); ... fclose(fp);',
                    'struct_definition': 'typedef struct { ... } MyStruct;',
                    'header_guard': '#ifndef HEADER_H\n#define HEADER_H\n...\n#endif'
                }
            },
            'C++': {
                'official_docs': 'https://en.cppreference.com/w/cpp',
                'best_practices': [
                    'Use RAII for resource management',
                    'Prefer smart pointers over raw pointers',
                    'Use const correctness',
                    'Prefer std::vector over arrays',
                    'Use auto for type deduction when appropriate',
                    'Prefer range-based for loops',
                    'Use nullptr instead of NULL',
                    'Follow the Rule of Five for resource-managing classes',
                    'Use move semantics for efficiency',
                    'Prefer std::string over C-style strings'
                ],
                'common_patterns': {
                    'smart_pointer': 'std::unique_ptr<Type> ptr = std::make_unique<Type>();',
                    'range_for': 'for (const auto& item : container) { ... }',
                    'lambda': 'auto lambda = [](int x) { return x * 2; };',
                    'class_definition': 'class MyClass { public: ... private: ... };',
                    'move_semantics': 'MyClass(MyClass&& other) noexcept : data(std::move(other.data)) {}'
                }
            },
            'Go': {
                'official_docs': 'https://go.dev/doc/',
                'best_practices': [
                    'Use gofmt for code formatting',
                    'Handle errors explicitly, don\'t ignore them',
                    'Use defer for cleanup operations',
                    'Prefer composition over inheritance',
                    'Use goroutines for concurrency',
                    'Use channels for communication between goroutines',
                    'Keep interfaces small',
                    'Use context for cancellation and timeouts',
                    'Follow effective Go guidelines',
                    'Use table-driven tests'
                ],
                'common_patterns': {
                    'error_handling': 'if err != nil { return err }',
                    'defer': 'defer file.Close()',
                    'goroutine': 'go func() { ... }()',
                    'channel': 'ch := make(chan int)',
                    'struct_definition': 'type MyStruct struct { Field string }'
                }
            }
        }
    
    def get_relevant_context(self, language: str, query: str) -> str:
        """
        Recupera contesto rilevante dalla documentazione per arricchire il prompt
        Usa docs locali se disponibili, altrimenti fallback a hardcoded
        
        Args:
            language: Linguaggio di programmazione
            query: Query dell'utente
        
        Returns:
            Contesto rilevante da aggiungere al prompt
        """
        if language not in self.documentation_sources:
            return ""
        
        docs = self.documentation_sources[language]
        context_parts = []
        
        # PRIORITÀ 1: Documentazione locale (se disponibile)
        if self.local_docs_available:
            local_content = self.get_local_doc_snippet(language, query)
            if local_content:
                context_parts.append(f"\n=== OFFICIAL {language.upper()} DOCUMENTATION (LOCAL) ===")
                context_parts.append(local_content)
                context_parts.append("")  # Linea vuota
        
        # PRIORITÀ 2: Best practices (sempre disponibili - hardcoded)
        context_parts.append(f"\n=== BEST PRACTICES FOR {language.upper()} ===")
        for practice in docs['best_practices'][:5]:  # Prime 5 best practices
            context_parts.append(f"• {practice}")
        
        # PRIORITÀ 3: Pattern comuni se rilevanti (hardcoded)
        query_lower = query.lower()
        relevant_patterns = []
        
        for pattern_name, pattern_code in docs.get('common_patterns', {}).items():
            if any(keyword in query_lower for keyword in pattern_name.split('_')):
                relevant_patterns.append(f"\n{pattern_name.replace('_', ' ').title()}:\n```{language.lower()}\n{pattern_code}\n```")
        
        if relevant_patterns:
            context_parts.append("\n=== RELEVANT CODE PATTERNS ===")
            context_parts.extend(relevant_patterns[:3])  # Max 3 pattern
        
        # Riferimento documentazione
        if not self.local_docs_available:
            context_parts.append(f"\n=== OFFICIAL DOCUMENTATION ===")
            context_parts.append(f"Reference: {docs['official_docs']}")
        
        return "\n".join(context_parts)
    
    def get_local_doc_snippet(self, language: str, query: str) -> Optional[str]:
        """
        Cerca snippet rilevante nelle docs locali basandosi sulla query
        
        Args:
            language: Linguaggio di programmazione
            query: Query dell'utente
        
        Returns:
            Snippet di documentazione rilevante o None
        """
        if not self.local_docs_available:
            return None
        
        # Determina quale doc leggere in base alla query
        query_lower = query.lower()
        
        # Mappa keywords a docs
        doc_map = {
            'tutorial': ['tutorial', 'guide', 'learn', 'start', 'begin', 'intro'],
            'reference': ['reference', 'api', 'function', 'method', 'class'],
            'library': ['library', 'module', 'package', 'import'],
            'pep8': ['style', 'format', 'convention', 'pep8'],
            'effective_go': ['best', 'practice', 'effective', 'idiomatic'],
        }
        
        # Trova doc più rilevante
        selected_doc = 'tutorial'  # Default
        for doc_name, keywords in doc_map.items():
            if any(kw in query_lower for kw in keywords):
                selected_doc = doc_name
                break
        
        # Leggi doc locale
        content = self.read_local_doc(language, selected_doc)
        if content:
            # Ritorna snippet (primi 2000 caratteri)
            return content[:2000] + "\n..." if len(content) > 2000 else content
        
        return None
    
    def enrich_prompt(self, base_prompt: str, language: str, query: str) -> str:
        """
        Arricchisce il prompt base con contesto dalla documentazione
        
        Args:
            base_prompt: Prompt base
            language: Linguaggio di programmazione
            query: Query dell'utente
        
        Returns:
            Prompt arricchito con contesto
        """
        context = self.get_relevant_context(language, query)
        
        if not context:
            return base_prompt
        
        enriched_prompt = f"""{base_prompt}

{context}

IMPORTANT: Use the above best practices and patterns in your response.
Ensure your code examples follow these guidelines and explain why they are considered best practices.
"""
        
        return enriched_prompt
    
    def get_language_specific_tips(self, language: str) -> List[str]:
        """Ottiene suggerimenti specifici per il linguaggio"""
        if language not in self.documentation_sources:
            return []
        
        return self.documentation_sources[language]['best_practices']


# Singleton instance
_rag_instance = None

def get_rag_system() -> DocumentationRAG:
    """Ottiene l'istanza singleton del sistema RAG"""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = DocumentationRAG()
    return _rag_instance

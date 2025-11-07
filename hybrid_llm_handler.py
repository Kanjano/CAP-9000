"""
Hybrid LLM Handler per CAP 9000
Combina CodeLlama + Recursive Reasoning Module

Modalità:
1. Simple Mode: Solo CodeLlama (query semplici)
2. Reasoning Mode: CodeLlama + Recursive Reasoning (query complesse)
"""

import time
from typing import Optional, Dict, Any
from llm_handler import LLMHandler
from recursive_reasoning import (
    ReasoningAnalyzer,
    get_reasoning_cache
)


class HybridLLMHandler:
    """
    Handler ibrido che combina CodeLlama con Recursive Reasoning
    
    Funzionamento:
    - Analizza la query per determinare complessità
    - Query semplici → Solo CodeLlama (veloce)
    - Query complesse → CodeLlama con prompt enhancement (reasoning)
    
    Nota: Questa è la versione prototipo che usa prompt enhancement.
    In futuro potrà integrare direttamente gli embeddings di Ollama.
    """
    
    def __init__(
        self,
        ollama_url: str = "http://localhost:11434",
        enable_reasoning: bool = True,
        enable_cache: bool = True,
        num_recursions: int = 3
    ):
        """
        Inizializza hybrid handler
        
        Args:
            ollama_url: URL del server Ollama
            enable_reasoning: Abilita reasoning mode
            enable_cache: Abilita caching
            num_recursions: Numero di ricorsioni (3-5 raccomandato)
        """
        # Base CodeLlama handler
        self.codellama = LLMHandler(ollama_url)
        
        # Reasoning configuration
        self.enable_reasoning = enable_reasoning
        self.num_recursions = num_recursions
        
        # Cache
        self.cache = get_reasoning_cache() if enable_cache else None
        
        # Statistics
        self.stats = {
            'total_queries': 0,
            'simple_queries': 0,
            'reasoning_queries': 0,
            'cache_hits': 0,
            'total_time': 0.0
        }
        
        # Log initialization
        mode = "HYBRID" if enable_reasoning else "SIMPLE"
        print(f"\n{'='*60}")
        print(f"  CAP 9000 - {mode} MODE INITIALIZED")
        print(f"{'='*60}")
        print(f"✓ CodeLlama: {'Available' if self.codellama.available else 'Unavailable'}")
        print(f"✓ Reasoning: {'Enabled' if enable_reasoning else 'Disabled'}")
        print(f"✓ Cache: {'Enabled' if enable_cache else 'Disabled'}")
        print(f"✓ Recursions: {num_recursions}")
        print(f"{'='*60}\n")
    
    def should_use_reasoning(self, query: str) -> bool:
        """
        Decide se usare recursive reasoning
        
        Args:
            query: User query
        
        Returns:
            True se serve reasoning, False altrimenti
        """
        if not self.enable_reasoning:
            return False
        
        return ReasoningAnalyzer.should_use_reasoning(query)
    
    def _enhance_prompt_with_reasoning(
        self,
        query: str,
        language: str,
        num_recursions: int
    ) -> str:
        """
        Enhance prompt per simulare recursive reasoning
        
        Questa funzione crea un prompt che incoraggia il modello a:
        1. Analizzare il problema in profondità
        2. Considerare multiple prospettive
        3. Iterare sulla soluzione
        
        Args:
            query: Original query
            language: Programming language
            num_recursions: Number of reasoning steps
        
        Returns:
            Enhanced prompt
        """
        enhanced_prompt = f"""[🧠 RECURSIVE REASONING MODE - {num_recursions} STEPS]

You are CAP 9000 with enhanced recursive reasoning capabilities.
For this complex task, you will reason through {num_recursions} iterative steps:

STEP 1 - INITIAL ANALYSIS:
- Understand the core problem
- Identify key components
- Consider edge cases

STEP 2 - DEEP REASONING:
- Analyze patterns and relationships
- Consider multiple approaches
- Evaluate trade-offs

STEP 3 - SOLUTION REFINEMENT:
- Synthesize insights from previous steps
- Optimize the solution
- Ensure completeness and correctness

Original Query: {query}
Programming Language: {language}

Now, apply recursive reasoning to provide a comprehensive, well-thought-out solution.
Show your reasoning process and explain your decisions."""

        return enhanced_prompt
    
    def generate_response(
        self,
        query: str,
        language: str,
        ui_language: str = 'en',
        use_reasoning: Optional[bool] = None,
        num_recursions: Optional[int] = None
    ) -> str:
        """
        Generate response con modalità ibrida
        
        Args:
            query: User query
            language: Programming language
            ui_language: UI language
            use_reasoning: Force reasoning on/off (None = auto)
            num_recursions: Number of recursive steps (None = default)
        
        Returns:
            Generated response
        """
        start_time = time.time()
        self.stats['total_queries'] += 1
        
        # Decide reasoning mode
        if use_reasoning is None:
            use_reasoning = self.should_use_reasoning(query)
        
        if num_recursions is None:
            num_recursions = self.num_recursions
        
        # Check cache
        if self.cache and use_reasoning:
            query_hash = ReasoningAnalyzer.get_query_hash(query, language)
            cached = self.cache.get(query_hash)
            if cached is not None:
                self.stats['cache_hits'] += 1
                elapsed = time.time() - start_time
                self.stats['total_time'] += elapsed
                print(f"[CACHE] ✓ Hit! Returning cached response ({elapsed:.2f}s)")
                return cached.get('response', '')
        
        # Simple mode: direct CodeLlama
        if not use_reasoning or not self.enable_reasoning:
            self.stats['simple_queries'] += 1
            print(f"\n[MODE] 🔵 SIMPLE (CodeLlama only)")
            
            response = self.codellama.generate_response(
                query, language, ui_language
            )
            
            elapsed = time.time() - start_time
            self.stats['total_time'] += elapsed
            print(f"[TIMING] Simple mode: {elapsed:.2f}s")
            
            return response
        
        # Reasoning mode: CodeLlama + Recursive Reasoning
        self.stats['reasoning_queries'] += 1
        print(f"\n[MODE] 🧠 REASONING (CodeLlama + {num_recursions} recursions)")
        
        # Enhance prompt with reasoning
        enhanced_query = self._enhance_prompt_with_reasoning(
            query, language, num_recursions
        )
        
        # Generate with CodeLlama
        response = self.codellama.generate_response(
            enhanced_query,
            language,
            ui_language
        )
        
        # Cache result
        if self.cache:
            query_hash = ReasoningAnalyzer.get_query_hash(query, language)
            self.cache.set(query_hash, {'response': response})
        
        elapsed = time.time() - start_time
        self.stats['total_time'] += elapsed
        print(f"[TIMING] Reasoning mode: {elapsed:.2f}s")
        
        return response
    
    def generate_response_streaming(
        self,
        query: str,
        language: str,
        ui_language: str = 'en',
        use_reasoning: Optional[bool] = None
    ):
        """
        Generate response in streaming mode
        
        Args:
            query: User query
            language: Programming language
            ui_language: UI language
            use_reasoning: Force reasoning on/off (None = auto)
        
        Yields:
            Response chunks
        """
        # Decide reasoning mode
        if use_reasoning is None:
            use_reasoning = self.should_use_reasoning(query)
        
        # Enhance prompt if reasoning mode
        if use_reasoning and self.enable_reasoning:
            print(f"\n[MODE] 🧠 REASONING STREAMING ({self.num_recursions} recursions)")
            query = self._enhance_prompt_with_reasoning(
                query, language, self.num_recursions
            )
        else:
            print(f"\n[MODE] 🔵 SIMPLE STREAMING")
        
        # Stream from CodeLlama
        for chunk in self.codellama.generate_response_streaming(
            query, language, ui_language
        ):
            yield chunk
    
    def get_stats(self) -> Dict[str, Any]:
        """Get handler statistics"""
        stats = {
            'mode': 'hybrid' if self.enable_reasoning else 'simple',
            'codellama_available': self.codellama.available,
            'reasoning_enabled': self.enable_reasoning,
            'cache_enabled': self.cache is not None,
            'num_recursions': self.num_recursions,
            'queries': {
                'total': self.stats['total_queries'],
                'simple': self.stats['simple_queries'],
                'reasoning': self.stats['reasoning_queries'],
                'cache_hits': self.stats['cache_hits']
            },
            'performance': {
                'total_time': f"{self.stats['total_time']:.2f}s",
                'avg_time': f"{self.stats['total_time'] / max(1, self.stats['total_queries']):.2f}s"
            }
        }
        
        if self.cache:
            stats['cache'] = self.cache.get_stats()
        
        # Calculate percentages
        total = self.stats['total_queries']
        if total > 0:
            stats['queries']['simple_pct'] = f"{self.stats['simple_queries'] / total * 100:.1f}%"
            stats['queries']['reasoning_pct'] = f"{self.stats['reasoning_queries'] / total * 100:.1f}%"
        
        return stats
    
    def print_stats(self):
        """Print statistics in a nice format"""
        stats = self.get_stats()
        
        print(f"\n{'='*60}")
        print(f"  CAP 9000 - HYBRID HANDLER STATISTICS")
        print(f"{'='*60}")
        print(f"Mode: {stats['mode'].upper()}")
        print(f"CodeLlama: {'✓ Available' if stats['codellama_available'] else '✗ Unavailable'}")
        print(f"Reasoning: {'✓ Enabled' if stats['reasoning_enabled'] else '✗ Disabled'}")
        print(f"Cache: {'✓ Enabled' if stats['cache_enabled'] else '✗ Disabled'}")
        print(f"\nQueries:")
        print(f"  Total: {stats['queries']['total']}")
        print(f"  Simple: {stats['queries']['simple']} ({stats['queries'].get('simple_pct', 'N/A')})")
        print(f"  Reasoning: {stats['queries']['reasoning']} ({stats['queries'].get('reasoning_pct', 'N/A')})")
        print(f"  Cache Hits: {stats['queries']['cache_hits']}")
        print(f"\nPerformance:")
        print(f"  Total Time: {stats['performance']['total_time']}")
        print(f"  Avg Time: {stats['performance']['avg_time']}")
        
        if 'cache' in stats:
            print(f"\nCache:")
            print(f"  Size: {stats['cache']['size']}/{stats['cache']['max_size']}")
            print(f"  Hit Rate: {stats['cache']['hit_rate']}")
        
        print(f"{'='*60}\n")
    
    def get_model_info(self):
        """Get model information"""
        info = self.codellama.get_model_info()
        info['hybrid_mode'] = self.enable_reasoning
        info['reasoning_recursions'] = self.num_recursions
        return info


# Singleton instance
_hybrid_handler = None


def get_hybrid_handler(
    enable_reasoning: bool = True,
    enable_cache: bool = True,
    num_recursions: int = 3
) -> HybridLLMHandler:
    """
    Get singleton instance of hybrid handler
    
    Args:
        enable_reasoning: Enable reasoning mode
        enable_cache: Enable caching
        num_recursions: Number of recursive steps
    
    Returns:
        HybridLLMHandler instance
    """
    global _hybrid_handler
    
    if _hybrid_handler is None:
        _hybrid_handler = HybridLLMHandler(
            enable_reasoning=enable_reasoning,
            enable_cache=enable_cache,
            num_recursions=num_recursions
        )
    
    return _hybrid_handler


# Test function
def test_hybrid_handler():
    """Test the hybrid handler"""
    print("\n=== Testing HybridLLMHandler ===\n")
    
    # Create handler
    handler = HybridLLMHandler(enable_reasoning=True, enable_cache=True)
    
    # Test queries
    test_queries = [
        ("What is a variable in Python?", "Python", False),  # Simple
        ("Debug this complex code and refactor it following SOLID principles", "Python", True),  # Complex
    ]
    
    print("\nTesting query analysis...")
    for query, lang, expected_reasoning in test_queries:
        should_reason = handler.should_use_reasoning(query)
        status = "✓" if should_reason == expected_reasoning else "✗"
        print(f"{status} '{query[:50]}...' → Reasoning: {should_reason}")
    
    # Print stats
    handler.print_stats()
    
    print("\n=== Test completed! ===\n")


if __name__ == "__main__":
    test_hybrid_handler()

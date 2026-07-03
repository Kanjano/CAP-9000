"""
Recursive Reasoning Module ispirato a TinyRecursiveModels (Samsung SAIL)
Implementa recursive reasoning per potenziare Mistral in CAP 9000

Paper: "Less is More: Recursive Reasoning with Tiny Networks"
GitHub: https://github.com/SamsungSAILMontreal/TinyRecursiveModels
"""

from typing import Optional, Tuple, Dict, Any
import json
from pathlib import Path
import hashlib

# NOTE: torch e' importato in modo lazy (solo se si usa effettivamente la rete
# neurale prototipo). Il percorso di risposta runtime NON usa torch: sfrutta
# solo ReasoningAnalyzer e ReasoningCache (puro Python). Cosi' lo startup
# dell'app non paga il costo di caricamento di torch (~1-2s) ne' lo richiede
# come dipendenza obbligatoria.
torch = None
nn = None


def _require_torch():
    """Importa torch on-demand. Sollevato ImportError chiaro se assente."""
    global torch, nn
    if torch is None:
        try:
            import torch as _torch
            import torch.nn as _nn
        except ImportError as exc:  # pragma: no cover - percorso opzionale
            raise ImportError(
                "torch non installato. La rete RecursiveReasoningModule e' "
                "opzionale e non serve al runtime. Per usarla: pip install torch"
            ) from exc
        torch, nn = _torch, _nn
    return torch, nn


def _build_module_class():
    """
    Costruisce la classe nn.Module solo quando torch e' disponibile.

    La definizione e' annidata perche' eredita da nn.Module, che esiste solo
    dopo l'import di torch. Mantiene intatta l'architettura prototipo TRM.
    """
    _torch, _nn = _require_torch()

    class _RecursiveReasoningModule(_nn.Module):
        def __init__(self, input_dim=4096, hidden_dim=512, num_layers=2,
                     num_recursions=3, dropout=0.1):
            super().__init__()
            self.input_dim = input_dim
            self.hidden_dim = hidden_dim
            self.num_recursions = num_recursions

            self.input_projection = _nn.Linear(input_dim, hidden_dim)
            self.latent_projection = _nn.Linear(hidden_dim, hidden_dim)
            self.reasoning_net = _nn.Sequential(
                _nn.Linear(input_dim + hidden_dim, hidden_dim),
                _nn.LayerNorm(hidden_dim),
                _nn.ReLU(),
                _nn.Dropout(dropout),
                _nn.Linear(hidden_dim, hidden_dim),
                _nn.LayerNorm(hidden_dim),
                _nn.ReLU(),
            )
            self.output_projection = _nn.Linear(hidden_dim, hidden_dim)
            self._init_weights()

            print("✓ RecursiveReasoningModule initialized:")
            print(f"  - Input dim: {input_dim}")
            print(f"  - Hidden dim: {hidden_dim}")
            print(f"  - Num recursions: {num_recursions}")
            print(f"  - Total parameters: {self.count_parameters():,}")

        def _init_weights(self):
            for module in self.modules():
                if isinstance(module, _nn.Linear):
                    _nn.init.xavier_uniform_(module.weight)
                    if module.bias is not None:
                        _nn.init.zeros_(module.bias)

        def count_parameters(self):
            return sum(p.numel() for p in self.parameters() if p.requires_grad)

        def forward(self, embedding, num_recursions=None):
            if num_recursions is None:
                num_recursions = self.num_recursions
            batch_size = embedding.shape[0]
            latent = _torch.zeros(batch_size, self.hidden_dim, device=embedding.device)
            for _ in range(num_recursions):
                combined = _torch.cat([embedding, latent], dim=-1)
                latent = latent + self.reasoning_net(combined)
            enhanced_latent = self.output_projection(latent)
            enhanced_embedding = _torch.cat([embedding, enhanced_latent], dim=-1)
            return enhanced_embedding, latent

        def save(self, path):
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            _torch.save({
                'state_dict': self.state_dict(),
                'config': {
                    'input_dim': self.input_dim,
                    'hidden_dim': self.hidden_dim,
                    'num_recursions': self.num_recursions,
                },
            }, path)
            print(f"✓ Model saved to {path}")

        def load(self, path):
            checkpoint = _torch.load(path, map_location='cpu')
            self.load_state_dict(checkpoint['state_dict'])
            print(f"✓ Model loaded from {path}")
            return checkpoint['config']

    return _RecursiveReasoningModule


def RecursiveReasoningModule(*args, **kwargs):
    """
    Factory compatibile con l'API originale: ``RecursiveReasoningModule(...)``.

    Prototipo NON usato nel percorso di risposta runtime (vedi nota in testa
    al file). Costruisce la rete torch solo on-demand.
    """
    cls = _build_module_class()
    return cls(*args, **kwargs)


class ReasoningCache:
    """
    Cache per embeddings e latent states
    Migliora performance evitando di ricalcolare reasoning per query simili
    """
    
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, query_hash: str) -> Optional[Dict[str, Any]]:
        """Get cached reasoning result"""
        result = self.cache.get(query_hash)
        if result:
            self.hits += 1
        else:
            self.misses += 1
        return result
    
    def set(self, query_hash: str, data: Dict[str, Any]):
        """Cache reasoning result"""
        if len(self.cache) >= self.max_size:
            # Remove oldest entry (FIFO)
            self.cache.pop(next(iter(self.cache)))
        self.cache[query_hash] = data
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{hit_rate:.1f}%"
        }


class ReasoningAnalyzer:
    """
    Analizza query per decidere se serve recursive reasoning
    """
    
    # Keywords che indicano necessità di reasoning
    REASONING_KEYWORDS = [
        # Debugging
        'debug', 'fix', 'error', 'bug', 'issue', 'problem', 'wrong',
        'crash', 'exception', 'traceback', 'stack trace',
        
        # Refactoring
        'refactor', 'improve', 'optimize', 'clean', 'restructure',
        'reorganize', 'simplify', 'modularize',
        
        # Analysis
        'analyze', 'review', 'check', 'inspect', 'examine', 'evaluate',
        'assess', 'audit', 'investigate',
        
        # Patterns
        'pattern', 'anti-pattern', 'design pattern', 'architecture',
        'best practice', 'code smell',
        
        # Complex tasks
        'complex', 'multi-step', 'advanced', 'difficult', 'sophisticated',
        'comprehensive', 'detailed', 'in-depth'
    ]
    
    @staticmethod
    def should_use_reasoning(query: str) -> bool:
        """
        Decide se usare recursive reasoning basandosi sulla query
        
        Args:
            query: User query
        
        Returns:
            True se serve reasoning, False altrimenti
        """
        query_lower = query.lower()
        
        # Check for reasoning keywords
        for keyword in ReasoningAnalyzer.REASONING_KEYWORDS:
            if keyword in query_lower:
                return True
        
        # Check query length (query lunghe spesso sono complesse)
        if len(query.split()) > 20:
            return True
        
        # Check for multiple questions (indica complessità)
        if query.count('?') > 1:
            return True
        
        return False
    
    @staticmethod
    def get_query_hash(query: str, language: str) -> str:
        """Generate hash for caching"""
        content = f"{query}_{language}"
        return hashlib.md5(content.encode()).hexdigest()


# Singleton instances
_reasoning_module = None
_reasoning_cache = None


def get_reasoning_module(
    model_path: Optional[str] = None,
    device: str = 'cpu'
) -> RecursiveReasoningModule:
    """
    Get singleton instance of reasoning module
    
    Args:
        model_path: Path to saved model weights (optional)
        device: Device to use ('cpu' or 'cuda')
    
    Returns:
        RecursiveReasoningModule instance
    """
    global _reasoning_module
    
    if _reasoning_module is None:
        _reasoning_module = RecursiveReasoningModule()
        
        if model_path and Path(model_path).exists():
            _reasoning_module.load(model_path)
        
        _reasoning_module.to(device)
        _reasoning_module.eval()  # Set to evaluation mode
        
        print(f"✓ Reasoning module ready on {device}")
    
    return _reasoning_module


def get_reasoning_cache() -> ReasoningCache:
    """Get singleton instance of reasoning cache"""
    global _reasoning_cache
    
    if _reasoning_cache is None:
        _reasoning_cache = ReasoningCache()
        print("✓ Reasoning cache initialized")
    
    return _reasoning_cache


# Test function
def test_reasoning_module():
    """Test the reasoning module"""
    print("\n=== Testing RecursiveReasoningModule ===\n")
    
    # Create module
    module = RecursiveReasoningModule(
        input_dim=4096,
        hidden_dim=512,
        num_recursions=3
    )
    
    # Test forward pass
    print("\nTesting forward pass...")
    batch_size = 2
    embedding = torch.randn(batch_size, 4096)
    
    enhanced, latent = module(embedding)
    
    print(f"✓ Input shape: {embedding.shape}")
    print(f"✓ Enhanced shape: {enhanced.shape}")
    print(f"✓ Latent shape: {latent.shape}")
    
    # Test save/load
    print("\nTesting save/load...")
    test_path = "models/test_reasoning.pth"
    module.save(test_path)
    
    module2 = RecursiveReasoningModule()
    module2.load(test_path)
    print("✓ Save/load successful")
    
    # Test analyzer
    print("\nTesting ReasoningAnalyzer...")
    test_queries = [
        "What is a variable?",  # Simple
        "Debug this complex code and refactor it",  # Complex
        "How do I fix this error in my Python script?"  # Complex
    ]
    
    for query in test_queries:
        should_reason = ReasoningAnalyzer.should_use_reasoning(query)
        print(f"  '{query[:50]}...' → Reasoning: {should_reason}")
    
    # Test cache
    print("\nTesting ReasoningCache...")
    cache = ReasoningCache(max_size=3)
    
    cache.set("hash1", {"result": "test1"})
    cache.set("hash2", {"result": "test2"})
    
    result = cache.get("hash1")
    print(f"✓ Cache hit: {result}")
    
    result = cache.get("hash3")
    print(f"✓ Cache miss: {result}")
    
    print(f"✓ Cache stats: {cache.get_stats()}")
    
    print("\n=== All tests passed! ===\n")


if __name__ == "__main__":
    test_reasoning_module()

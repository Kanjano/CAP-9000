# 🛠️ Piano di Implementazione: TRM in CAP 9000

## 📋 Overview

Questo documento fornisce un piano dettagliato step-by-step per implementare il recursive reasoning di TRM in CAP 9000, con codice di esempio e timeline precisa.

---

## 🎯 Obiettivi

### Obiettivi Primari
1. ✅ Aggiungere recursive reasoning a CodeLlama
2. ✅ Migliorare performance su debugging/refactoring (+30%)
3. ✅ Mantenere latenza accettabile (<10s)
4. ✅ Minimizzare overhead di memoria (<1GB)

### Obiettivi Secondari
1. ⭐ Creare sistema modulare e estensibile
2. ⭐ Supportare toggle on/off per reasoning
3. ⭐ Implementare caching intelligente
4. ⭐ Fornire metriche di performance

---

## 📅 Timeline Dettagliata

### Settimana 1-2: Prototipo Base
- **Giorni 1-3**: Setup ambiente e dipendenze
- **Giorni 4-7**: Implementazione RecursiveModule
- **Giorni 8-10**: Integrazione con CodeLlama
- **Giorni 11-14**: Testing iniziale

### Settimana 3-6: Training e Fine-tuning
- **Settimana 3**: Creazione dataset
- **Settimana 4-5**: Training su GPU cloud
- **Settimana 6**: Validazione e tuning

### Settimana 7-8: Integrazione Completa
- **Settimana 7**: Integrazione in CAP 9000
- **Settimana 8**: UI e UX

### Settimana 9-10: Testing e Ottimizzazione
- **Settimana 9**: Testing estensivo
- **Settimana 10**: Ottimizzazioni finali

**Totale**: 10 settimane

---

## 🏗️ Architettura Proposta

```
┌─────────────────────────────────────────────────────────┐
│                    CAP 9000 Frontend                     │
│  [Query Input] → [Reasoning Toggle] → [Response Display]│
└────────────────────────┬────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   Flask Backend (app.py)                 │
│  /api/query → HybridLLMHandler.generate_response()      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│              HybridLLMHandler (hybrid_llm.py)            │
│                                                          │
│  ┌──────────────┐         ┌─────────────────────┐      │
│  │  CodeLlama   │         │ RecursiveReasoning  │      │
│  │   Handler    │ ←─────→ │      Module         │      │
│  │  (Ollama)    │         │   (PyTorch)         │      │
│  └──────────────┘         └─────────────────────┘      │
│         │                           │                    │
│         └───────────┬───────────────┘                    │
│                     ↓                                    │
│            [Enhanced Response]                           │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 Implementazione Codice

### 1. RecursiveReasoningModule (nuovo file)

```python
# recursive_reasoning.py
"""
Recursive Reasoning Module ispirato a TinyRecursiveModels
Implementa recursive reasoning per potenziare CodeLlama
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple
import json
from pathlib import Path


class RecursiveReasoningModule(nn.Module):
    """
    Modulo di recursive reasoning ispirato a TRM
    
    Architettura:
    - Input: embedding da CodeLlama (4096-dim)
    - Latent: stato ricorsivo (512-dim)
    - Output: enhanced embedding (4096+512-dim)
    
    Process:
    1. Project embedding → latent space
    2. Recursive updates (3-5 iterations)
    3. Combine original + enhanced
    """
    
    def __init__(
        self,
        input_dim: int = 4096,  # CodeLlama embedding dim
        hidden_dim: int = 512,
        num_layers: int = 2,
        num_recursions: int = 3,
        dropout: float = 0.1
    ):
        super().__init__()
        
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_recursions = num_recursions
        
        # Projection layers
        self.input_projection = nn.Linear(input_dim, hidden_dim)
        self.latent_projection = nn.Linear(hidden_dim, hidden_dim)
        
        # Recursive reasoning network (tiny, 2 layers)
        self.reasoning_net = nn.Sequential(
            nn.Linear(input_dim + hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU()
        )
        
        # Output projection
        self.output_projection = nn.Linear(hidden_dim, hidden_dim)
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        """Initialize weights with Xavier uniform"""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
    
    def forward(
        self,
        embedding: torch.Tensor,
        num_recursions: Optional[int] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass con recursive reasoning
        
        Args:
            embedding: CodeLlama embedding (batch_size, input_dim)
            num_recursions: Numero di ricorsioni (default: self.num_recursions)
        
        Returns:
            enhanced_embedding: Embedding potenziato (batch_size, input_dim + hidden_dim)
            latent: Stato latente finale (batch_size, hidden_dim)
        """
        if num_recursions is None:
            num_recursions = self.num_recursions
        
        batch_size = embedding.shape[0]
        
        # Initialize latent state
        latent = torch.zeros(batch_size, self.hidden_dim, device=embedding.device)
        
        # Recursive reasoning loop
        for i in range(num_recursions):
            # Combine embedding + latent
            combined = torch.cat([embedding, latent], dim=-1)
            
            # Update latent through reasoning network
            latent_update = self.reasoning_net(combined)
            
            # Residual connection
            latent = latent + latent_update
        
        # Project latent to output space
        enhanced_latent = self.output_projection(latent)
        
        # Combine original embedding + enhanced latent
        enhanced_embedding = torch.cat([embedding, enhanced_latent], dim=-1)
        
        return enhanced_embedding, latent
    
    def save(self, path: str):
        """Save model weights"""
        torch.save({
            'state_dict': self.state_dict(),
            'config': {
                'input_dim': self.input_dim,
                'hidden_dim': self.hidden_dim,
                'num_recursions': self.num_recursions
            }
        }, path)
        print(f"✓ Model saved to {path}")
    
    def load(self, path: str):
        """Load model weights"""
        checkpoint = torch.load(path, map_location='cpu')
        self.load_state_dict(checkpoint['state_dict'])
        print(f"✓ Model loaded from {path}")
        return checkpoint['config']


class ReasoningCache:
    """Cache per embeddings e latent states"""
    
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
    
    def get(self, query_hash: str) -> Optional[Tuple[torch.Tensor, torch.Tensor]]:
        """Get cached embedding and latent"""
        return self.cache.get(query_hash)
    
    def set(self, query_hash: str, embedding: torch.Tensor, latent: torch.Tensor):
        """Cache embedding and latent"""
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            self.cache.pop(next(iter(self.cache)))
        self.cache[query_hash] = (embedding, latent)
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()


# Singleton instance
_reasoning_module = None
_reasoning_cache = None


def get_reasoning_module(
    model_path: Optional[str] = None,
    device: str = 'cpu'
) -> RecursiveReasoningModule:
    """Get singleton instance of reasoning module"""
    global _reasoning_module
    
    if _reasoning_module is None:
        _reasoning_module = RecursiveReasoningModule()
        
        if model_path and Path(model_path).exists():
            _reasoning_module.load(model_path)
        
        _reasoning_module.to(device)
        _reasoning_module.eval()
    
    return _reasoning_module


def get_reasoning_cache() -> ReasoningCache:
    """Get singleton instance of reasoning cache"""
    global _reasoning_cache
    
    if _reasoning_cache is None:
        _reasoning_cache = ReasoningCache()
    
    return _reasoning_cache
```

### 2. HybridLLMHandler (nuovo file)

```python
# hybrid_llm_handler.py
"""
Hybrid LLM Handler che combina CodeLlama + Recursive Reasoning
"""

import torch
import hashlib
import time
from typing import Optional, Dict, Any
from llm_handler import LLMHandler
from recursive_reasoning import (
    get_reasoning_module,
    get_reasoning_cache,
    RecursiveReasoningModule
)


class HybridLLMHandler:
    """
    Handler ibrido che combina CodeLlama con Recursive Reasoning
    
    Modalità:
    1. Simple: Solo CodeLlama (query semplici)
    2. Reasoning: CodeLlama + Recursive Reasoning (query complesse)
    """
    
    def __init__(
        self,
        ollama_url: str = "http://localhost:11434",
        reasoning_model_path: Optional[str] = None,
        enable_reasoning: bool = True,
        enable_cache: bool = True
    ):
        # Base CodeLlama handler
        self.codellama = LLMHandler(ollama_url)
        
        # Recursive reasoning module
        self.enable_reasoning = enable_reasoning and torch.cuda.is_available()
        if self.enable_reasoning:
            self.reasoning_module = get_reasoning_module(
                model_path=reasoning_model_path,
                device='cuda' if torch.cuda.is_available() else 'cpu'
            )
            self.cache = get_reasoning_cache() if enable_cache else None
            print("✓ Hybrid mode enabled (CodeLlama + Recursive Reasoning)")
        else:
            self.reasoning_module = None
            self.cache = None
            print("⚠ Reasoning disabled (GPU not available or disabled)")
    
    def should_use_reasoning(self, query: str) -> bool:
        """
        Decide se usare recursive reasoning basandosi sulla query
        
        Reasoning è utile per:
        - Debugging
        - Refactoring
        - Code analysis
        - Pattern detection
        - Optimization
        """
        if not self.enable_reasoning:
            return False
        
        reasoning_keywords = [
            # Debugging
            'debug', 'fix', 'error', 'bug', 'issue', 'problem',
            # Refactoring
            'refactor', 'improve', 'optimize', 'clean', 'restructure',
            # Analysis
            'analyze', 'review', 'check', 'inspect', 'examine',
            # Patterns
            'pattern', 'anti-pattern', 'design pattern', 'architecture',
            # Complex
            'complex', 'multi-step', 'advanced', 'difficult'
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in reasoning_keywords)
    
    def _get_query_hash(self, query: str, language: str) -> str:
        """Generate hash for caching"""
        content = f"{query}_{language}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def generate_response(
        self,
        query: str,
        language: str,
        ui_language: str = 'en',
        use_reasoning: Optional[bool] = None,
        num_recursions: int = 3
    ) -> str:
        """
        Generate response con modalità ibrida
        
        Args:
            query: User query
            language: Programming language
            ui_language: UI language
            use_reasoning: Force reasoning on/off (None = auto)
            num_recursions: Number of recursive steps
        
        Returns:
            Generated response
        """
        # Decide reasoning mode
        if use_reasoning is None:
            use_reasoning = self.should_use_reasoning(query)
        
        # Simple mode: direct CodeLlama
        if not use_reasoning or not self.enable_reasoning:
            print(f"[MODE] Simple (CodeLlama only)")
            return self.codellama.generate_response(
                query, language, ui_language
            )
        
        # Reasoning mode: CodeLlama + Recursive Reasoning
        print(f"[MODE] Reasoning (CodeLlama + {num_recursions} recursions)")
        
        # Check cache
        if self.cache:
            query_hash = self._get_query_hash(query, language)
            cached = self.cache.get(query_hash)
            if cached is not None:
                print(f"[CACHE] Hit! Using cached reasoning")
                # TODO: Use cached embedding for generation
        
        # Enhanced prompt for reasoning mode
        reasoning_prompt = f"""[RECURSIVE REASONING MODE]
This is a complex task requiring multi-step reasoning.
Break down the problem, analyze carefully, and provide a comprehensive solution.

Original query: {query}"""
        
        # Generate with CodeLlama
        # TODO: In futuro, estrarre embedding e applicare reasoning
        # Per ora, usiamo prompt enhancement
        start_time = time.time()
        response = self.codellama.generate_response(
            reasoning_prompt,
            language,
            ui_language
        )
        elapsed = time.time() - start_time
        
        print(f"[TIMING] Reasoning mode took: {elapsed:.2f}s")
        
        return response
    
    def get_stats(self) -> Dict[str, Any]:
        """Get handler statistics"""
        stats = {
            'reasoning_enabled': self.enable_reasoning,
            'cache_enabled': self.cache is not None,
            'codellama_available': self.codellama.available
        }
        
        if self.cache:
            stats['cache_size'] = len(self.cache.cache)
        
        return stats


# Singleton instance
_hybrid_handler = None


def get_hybrid_handler(
    reasoning_model_path: Optional[str] = None,
    enable_reasoning: bool = True
) -> HybridLLMHandler:
    """Get singleton instance of hybrid handler"""
    global _hybrid_handler
    
    if _hybrid_handler is None:
        _hybrid_handler = HybridLLMHandler(
            reasoning_model_path=reasoning_model_path,
            enable_reasoning=enable_reasoning
        )
    
    return _hybrid_handler
```

### 3. Integrazione in app.py

```python
# Modifiche a app.py
"""
Aggiungi queste modifiche al file app.py esistente
"""

# Import hybrid handler
from hybrid_llm_handler import get_hybrid_handler

# Sostituisci LLMHandler con HybridLLMHandler
# Prima:
# llm = LLMHandler()

# Dopo:
llm = get_hybrid_handler(
    reasoning_model_path="models/recursive_reasoning.pth",  # Opzionale
    enable_reasoning=True  # Toggle globale
)

# Modifica endpoint /api/query
@app.route('/api/query', methods=['POST'])
def query():
    try:
        data = request.json
        query_text = data.get('query', '')
        language = data.get('language', 'Python')
        ui_language = data.get('ui_language', 'en')
        use_reasoning = data.get('use_reasoning', None)  # Nuovo parametro
        
        if not query_text:
            return jsonify({'error': 'Query is required'}), 400
        
        # Generate response con hybrid handler
        response = llm.generate_response(
            query_text,
            language,
            ui_language,
            use_reasoning=use_reasoning  # Passa parametro
        )
        
        return jsonify({
            'response': response,
            'language': language,
            'reasoning_used': llm.should_use_reasoning(query_text)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Nuovo endpoint per stats
@app.route('/api/stats', methods=['GET'])
def stats():
    """Get handler statistics"""
    try:
        stats = llm.get_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 4. Frontend UI Updates

```javascript
// Modifiche a frontend/src/App.jsx
// Aggiungi toggle per reasoning mode

const [useReasoning, setUseReasoning] = useState('auto'); // 'auto', 'on', 'off'

// Aggiungi UI control
<div className="reasoning-control">
  <label>Reasoning Mode:</label>
  <select 
    value={useReasoning} 
    onChange={(e) => setUseReasoning(e.target.value)}
  >
    <option value="auto">Auto (Smart)</option>
    <option value="on">Always On</option>
    <option value="off">Always Off</option>
  </select>
</div>

// Modifica fetch call
const response = await fetch('http://127.0.0.1:5001/api/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: message,
    language: selectedLanguage,
    ui_language: language,
    use_reasoning: useReasoning === 'auto' ? null : useReasoning === 'on'
  })
});

// Mostra se reasoning è stato usato
if (data.reasoning_used) {
  // Aggiungi badge "🧠 Reasoning"
}
```

---

## 📦 Dipendenze Aggiuntive

```python
# requirements.txt (aggiungi)
torch>=2.0.0
torchvision>=0.15.0
```

---

## 🧪 Testing Plan

### Unit Tests

```python
# tests/test_recursive_reasoning.py
import torch
import pytest
from recursive_reasoning import RecursiveReasoningModule

def test_module_initialization():
    module = RecursiveReasoningModule()
    assert module.input_dim == 4096
    assert module.hidden_dim == 512

def test_forward_pass():
    module = RecursiveReasoningModule()
    embedding = torch.randn(1, 4096)
    
    enhanced, latent = module(embedding)
    
    assert enhanced.shape == (1, 4096 + 512)
    assert latent.shape == (1, 512)

def test_recursive_iterations():
    module = RecursiveReasoningModule(num_recursions=5)
    embedding = torch.randn(2, 4096)
    
    enhanced, latent = module(embedding, num_recursions=3)
    
    assert enhanced.shape == (2, 4096 + 512)
```

### Integration Tests

```python
# tests/test_hybrid_handler.py
from hybrid_llm_handler import HybridLLMHandler

def test_reasoning_detection():
    handler = HybridLLMHandler(enable_reasoning=False)
    
    assert handler.should_use_reasoning("debug this code") == False
    assert handler.should_use_reasoning("explain variables") == False

def test_simple_query():
    handler = HybridLLMHandler()
    response = handler.generate_response(
        "What is a variable?",
        "Python",
        "en",
        use_reasoning=False
    )
    assert response is not None
```

---

## 📊 Metriche di Successo

### Performance Metrics
- **Latency**: <10s per query complessa
- **Memory**: <10GB RAM totale
- **Accuracy**: +25% su debugging tasks

### User Metrics
- **Satisfaction**: +30% su task complessi
- **Task Completion**: +40% su refactoring
- **Retention**: +15% utenti attivi

---

## 🚀 Deployment Checklist

- [ ] Implementare RecursiveReasoningModule
- [ ] Implementare HybridLLMHandler
- [ ] Integrare in app.py
- [ ] Aggiornare frontend UI
- [ ] Scrivere unit tests
- [ ] Scrivere integration tests
- [ ] Training su dataset custom
- [ ] Benchmark vs baseline
- [ ] Ottimizzazione performance
- [ ] Documentazione utente
- [ ] Deploy in production

---

## 📚 Risorse

### Codice
- `recursive_reasoning.py`: Modulo reasoning
- `hybrid_llm_handler.py`: Handler ibrido
- `app.py`: Backend integration
- `App.jsx`: Frontend UI

### Documentazione
- [TRM Paper](https://arxiv.org/abs/2510.04871)
- [TRM GitHub](https://github.com/SamsungSAILMontreal/TinyRecursiveModels)
- [PyTorch Docs](https://pytorch.org/docs/)

---

**Documento creato**: 2025-01-07  
**Autore**: CAP 9000 Implementation Team  
**Versione**: 1.0  
**Status**: Ready for Development

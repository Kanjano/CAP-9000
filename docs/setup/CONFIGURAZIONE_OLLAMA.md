# 🚀 Configurazione Ollama per Risposte Migliori

## 📊 Modelli Consigliati (dal migliore al più veloce)

### 🏆 MIGLIORI (Risposte più dettagliate e accurate)

**Qwen2.5 Coder 32B** - Il migliore in assoluto
```bash
ollama pull qwen2.5-coder:32b
```
- Risposte estremamente dettagliate
- Codice production-ready
- Richiede GPU potente (16GB+ VRAM)

**DeepSeek Coder 33B** - Eccellente qualità
```bash
ollama pull deepseek-coder:33b
```
- Spiegazioni approfondite
- Best practices incluse
- Richiede GPU potente

**CodeLlama 34B** - Molto potente
```bash
ollama pull codellama:34b
```
- Ottimo per programmazione complessa
- Richiede GPU potente

### ⚖️ BILANCIATI (Ottimo compromesso)

**Qwen2.5 Coder 14B** - CONSIGLIATO per la maggior parte
```bash
ollama pull qwen2.5-coder:14b
```
- Eccellente qualità
- Velocità accettabile
- Funziona su GPU medie (8GB VRAM)

**DeepSeek Coder 6.7B** - Veloce e accurato
```bash
ollama pull deepseek-coder:6.7b
```
- Buona qualità
- Veloce
- Funziona su GPU entry-level

**CodeLlama 13B** - Equilibrato
```bash
ollama pull codellama:13b
```
- Buon compromesso
- Ampiamente testato

### ⚡ VELOCI (Per risposte rapide)

**CodeLlama 7B** - Attualmente in uso
```bash
ollama pull codellama
```
- Veloce ma risposte meno dettagliate
- Funziona anche su CPU

## 🔧 Come Cambiare Modello

### Opzione 1: Modifica app.py
Apri `/app.py` e cambia la riga 15:

```python
# Da:
llm = LLMHandler(model="codellama")

# A (esempio con modello migliore):
llm = LLMHandler(model="qwen2.5-coder:14b")
```

### Opzione 2: Variabile d'ambiente
```bash
export OLLAMA_MODEL="qwen2.5-coder:14b"
```

## 📈 Miglioramenti Implementati

### 1. **Prompt Potenziato**
- Istruzioni dettagliate per risposte approfondite
- Richiesta di esempi multipli
- Best practices obbligatorie
- Spiegazione di edge cases

### 2. **Parametri Ottimizzati**
- `num_predict: 2048` - Risposte fino a 2048 token (molto più lunghe)
- `num_ctx: 4096` - Contesto esteso per conversazioni complesse
- `top_p: 0.95` - Maggiore creatività nelle risposte
- `repeat_penalty: 1.1` - Evita ripetizioni

### 3. **Timeout Aumentato**
- 60 secondi invece di 30 per risposte dettagliate

## 🎨 Tema Syntax Highlighting

Implementato **VS Code Dark+ autentico** con:
- Colori IDE realistici
- Syntax highlighting professionale
- Font monospace ottimizzati (Fira Code, Cascadia Code, JetBrains Mono)

### Colori principali:
- **Keywords**: `#569cd6` (blu)
- **Strings**: `#ce9178` (arancione)
- **Functions**: `#dcdcaa` (giallo)
- **Comments**: `#6a9955` (verde)
- **Numbers**: `#b5cea8` (verde chiaro)
- **Classes**: `#4ec9b0` (turchese)

## 💡 Suggerimenti per Risposte Migliori

1. **Sii specifico** nelle domande
   - ❌ "Come funziona Java?"
   - ✅ "Spiegami l'ereditarietà in Java con esempi di classi astratte"

2. **Chiedi esempi pratici**
   - "Mostrami un esempio completo di..."
   - "Dammi un caso d'uso reale per..."

3. **Richiedi best practices**
   - "Quali sono le best practices per..."
   - "Come dovrei gestire gli errori in..."

4. **Usa il modello giusto**
   - Codice complesso → Modelli 13B+
   - Domande veloci → Modelli 7B
   - Progetti production → Modelli 30B+

## 🔍 Verifica Modello Attivo

Controlla quale modello stai usando:
```bash
ollama list
```

Verifica che Ollama sia in esecuzione:
```bash
curl http://localhost:11434/api/tags
```

## 📝 Note

- Modelli più grandi = risposte migliori ma più lente
- Richiedi GPU con VRAM adeguata per modelli 13B+
- Il modello può essere cambiato senza riavviare l'app (riavvia solo il backend Flask)

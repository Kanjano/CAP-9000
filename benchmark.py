"""
Benchmark dei tempi di risposta CAP 9000 (esecuzione locale).

Esegue ~100 query reali attraverso lo stack completo (HybridLLMHandler ->
LLMHandler -> Ollama), misura la latenza end-to-end e verifica l'obiettivo:
TUTTE le risposte sotto gli 8 secondi.

Uso:
    python benchmark.py            # 100 query
    python benchmark.py 50         # N query
    CAP9000_MODEL=qwen2.5-coder:1.5b python benchmark.py
"""

import sys
import time
import json
import statistics
from datetime import datetime

from hybrid_llm_handler import get_hybrid_handler
from language_detector import get_language_detector

TARGET_SECONDS = 8.0

# Pool di domande tecniche realistiche (mix semplici + complesse, multi-lingua).
QUERY_POOL = [
    ("Python", "How do I read a file line by line?"),
    ("Python", "What is a list comprehension and when should I use it?"),
    ("Python", "How do I handle exceptions properly?"),
    ("Python", "Write a function to reverse a linked list"),
    ("Python", "How do I use a context manager?"),
    ("Python", "Explain the difference between a list and a tuple"),
    ("Python", "How do I make an HTTP GET request?"),
    ("Python", "Debug a recursion that causes a stack overflow"),
    ("Python", "How do decorators work?"),
    ("Python", "How do I parse JSON from a string?"),
    ("JavaScript", "How to debounce a function?"),
    ("JavaScript", "Explain async/await vs promises"),
    ("JavaScript", "How do I deep clone an object?"),
    ("JavaScript", "What is the difference between == and ===?"),
    ("JavaScript", "How do I fix a 'cannot read property of undefined' error?"),
    ("JavaScript", "How does event delegation work?"),
    ("JavaScript", "How to remove duplicates from an array?"),
    ("JavaScript", "Explain closures with an example"),
    ("Java", "How to use streams to filter a list?"),
    ("Java", "Explain the difference between an interface and an abstract class"),
    ("Java", "How do I handle a NullPointerException?"),
    ("Java", "How does the try-with-resources statement work?"),
    ("Java", "What is the difference between HashMap and TreeMap?"),
    ("Java", "How do I create an immutable class?"),
    ("Go", "How to handle errors idiomatically?"),
    ("Go", "Explain goroutines and channels"),
    ("Go", "How do I use defer for cleanup?"),
    ("Go", "How do I read a file in Go?"),
    ("Go", "What is a struct and how do I define methods on it?"),
    ("C", "How do I allocate and free memory safely?"),
    ("C", "What is a segmentation fault and how do I debug it?"),
    ("C", "How do I copy a string safely?"),
    ("C++", "When should I use smart pointers?"),
    ("C++", "Explain move semantics with an example"),
    ("C++", "What is RAII and why does it matter?"),
    ("C++", "How do range-based for loops work?"),
    # Query in altre lingue (test del language detector + risposta multilingua)
    ("Python", "Come leggo un file riga per riga in Python?"),
    ("Python", "Come gestisco le eccezioni in modo corretto?"),
    ("JavaScript", "Comment fonctionne async/await en JavaScript?"),
    ("Java", "Wie verwende ich Streams zum Filtern einer Liste?"),
    ("Python", "¿Cómo hago una petición HTTP en Python?"),
]


def build_queries(n):
    """Genera n query ciclando sul pool, mantenendo varieta'."""
    out = []
    i = 0
    while len(out) < n:
        out.append(QUERY_POOL[i % len(QUERY_POOL)])
        i += 1
    return out


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    print(f"\n{'='*64}\n  CAP 9000 - RESPONSE TIME BENCHMARK ({n} query, target < {TARGET_SECONDS}s)\n{'='*64}")

    llm = get_hybrid_handler()
    if not llm.codellama.available:
        print("ERRORE: Ollama non disponibile. Avviare 'ollama serve'.")
        sys.exit(2)
    print(f"Modello attivo: {llm.codellama.model}\n")

    detector = get_language_detector()
    queries = build_queries(n)
    times = []
    over = []  # query sopra il target

    for idx, (lang, q) in enumerate(queries, 1):
        ui_lang = detector.detect_language(q)  # rileva lingua come fa il backend
        t = time.time()
        resp = llm.generate_response(q, lang, ui_language=ui_lang)
        elapsed = time.time() - t
        times.append(elapsed)
        flag = "" if elapsed < TARGET_SECONDS else "  <-- OVER TARGET"
        if elapsed >= TARGET_SECONDS:
            over.append((idx, lang, q, elapsed))
        chars = len(resp) if resp else 0
        print(f"[{idx:3d}/{n}] {elapsed:5.2f}s  {chars:5d} ch  {lang:11s} {q[:42]}{flag}")

    times_sorted = sorted(times)
    p50 = statistics.median(times)
    p95 = times_sorted[int(len(times_sorted) * 0.95) - 1]

    print(f"\n{'='*64}\n  RESULTS\n{'='*64}")
    print(f"  Queries:   {len(times)}")
    print(f"  Min:       {min(times):.2f}s")
    print(f"  Avg:       {statistics.mean(times):.2f}s")
    print(f"  Median:    {p50:.2f}s")
    print(f"  p95:       {p95:.2f}s")
    print(f"  Max:       {max(times):.2f}s")
    print(f"  Over {TARGET_SECONDS:.0f}s:   {len(over)} / {len(times)}")
    all_under = len(over) == 0
    print(f"  TARGET:    {'PASS (all < 8s)' if all_under else 'FAIL'}")
    if over:
        print("  --- queries over target ---")
        for idx, lang, q, el in over:
            print(f"    #{idx} {el:.2f}s {lang} {q[:50]}")

    # Salva report JSON
    report = {
        'timestamp': datetime.now().isoformat(),
        'model': llm.codellama.model,
        'num_queries': len(times),
        'target_seconds': TARGET_SECONDS,
        'min': min(times), 'avg': statistics.mean(times),
        'median': p50, 'p95': p95, 'max': max(times),
        'over_target': len(over),
        'all_under_target': all_under,
        'times': [round(x, 3) for x in times],
    }
    with open('benchmark_results.json', 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\n  Report salvato in benchmark_results.json")
    print(f"{'='*64}\n")

    sys.exit(0 if all_under else 1)


if __name__ == '__main__':
    main()

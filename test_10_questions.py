"""
Phase 4 test suite: 10 domande prescritte contro il bot Mistral locale.
Misura latenza vs metrica < 8s, lunghezza/completezza risposta.
Esegue il path reale del bot (HybridLLMHandler -> LLMHandler -> Mistral /v1).
"""
import time
from hybrid_llm_handler import get_hybrid_handler

BUG_SNIPPET = (
    "def media(numeri):\n"
    "    tot = 0\n"
    "    for n in numeri:\n"
    "        tot += n\n"
    "    return tot / len(numeri) + 1   # bug logico\n"
)
STACK_TRACE = (
    "Traceback (most recent call last):\n"
    "  File 'app.py', line 12, in <module>\n"
    "    main()\n"
    "  File 'app.py', line 8, in main\n"
    "    print(data['key'])\n"
    "KeyError: 'key'\n"
)

QUESTIONS = [
    ("Spiega come funziona una closure in JavaScript", "JavaScript"),
    ("Quali sono i principali design pattern in Python?", "Python"),
    (f"Correggi questo bug:\n{BUG_SNIPPET}", "Python"),
    ("Come ottimizzare una query SQL lenta?", "SQL"),
    ("Genera uno stub per una funzione REST API in Node.js", "JavaScript"),
    ("Quali sono le best practice per il versionamento semantico?", "Python"),
    ("Confronta async/await vs Promise.then()", "JavaScript"),
    ("Come implementare dependency injection in Java?", "Java"),
    ("Spiega i trade-off tra SQL e NoSQL", "SQL"),
    (f"Aiutami a debuggare questo stack trace:\n{STACK_TRACE}", "Python"),
]


def main():
    llm = get_hybrid_handler(enable_reasoning=True, enable_cache=True, num_recursions=3)
    if not llm.mistral.available:
        print("ENDPOINT OFFLINE - abort")
        return

    print(f"\nMODEL: {llm.mistral.model}\n" + "=" * 78)
    results = []
    for i, (q, lang) in enumerate(QUESTIONS, 1):
        t = time.time()
        resp = llm.generate_response(q, lang, ui_language="it")
        dt = time.time() - t
        ok = bool(resp) and len(resp) > 80
        results.append((i, lang, dt, len(resp or ""), ok))
        print(f"\n[{i}] ({lang}) {dt:.2f}s  len={len(resp or '')}  "
              f"{'<8s OK' if dt < 8 else 'OVER 8s'}  {'quality OK' if ok else 'WEAK'}")
        print((resp or "")[:160].replace("\n", " ") + "...")

    print("\n" + "=" * 78 + "\nSUMMARY")
    under8 = sum(1 for r in results if r[2] < 8)
    quality = sum(1 for r in results if r[4])
    avg = sum(r[2] for r in results) / len(results)
    print(f"  Tests run:        {len(results)}/10")
    print(f"  Quality OK:       {quality}/10")
    print(f"  Latency < 8s:     {under8}/10")
    print(f"  Avg latency:      {avg:.2f}s")
    print(f"  Min/Max latency:  {min(r[2] for r in results):.2f}s / {max(r[2] for r in results):.2f}s")


if __name__ == "__main__":
    main()

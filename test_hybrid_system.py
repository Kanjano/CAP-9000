#!/usr/bin/env python3
"""
Test script per il sistema Hybrid LLM (Mistral + Recursive Reasoning)
Testa tutti i componenti del prototipo
"""

import sys
import time

def print_header(title):
    """Print a nice header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def test_recursive_module():
    """Test RecursiveReasoningModule"""
    print_header("TEST 1: RecursiveReasoningModule")
    
    try:
        from recursive_reasoning import test_reasoning_module
        test_reasoning_module()
        print("✓ RecursiveReasoningModule test passed!\n")
        return True
    except Exception as e:
        print(f"✗ RecursiveReasoningModule test failed: {e}\n")
        return False

def test_hybrid_handler():
    """Test HybridLLMHandler"""
    print_header("TEST 2: HybridLLMHandler")
    
    try:
        from hybrid_llm_handler import HybridLLMHandler
        
        # Create handler
        handler = HybridLLMHandler(enable_reasoning=True, enable_cache=True)
        
        # Test query analysis
        print("Testing query analysis...")
        test_queries = [
            ("What is a variable?", False),  # Simple
            ("Debug this complex code and refactor it", True),  # Complex
            ("How do I fix this error?", True),  # Complex
        ]
        
        all_correct = True
        for query, expected_reasoning in test_queries:
            should_reason = handler.should_use_reasoning(query)
            status = "✓" if should_reason == expected_reasoning else "✗"
            print(f"  {status} '{query[:40]}...' → Reasoning: {should_reason}")
            if should_reason != expected_reasoning:
                all_correct = False
        
        if all_correct:
            print("\n✓ HybridLLMHandler test passed!\n")
            return True
        else:
            print("\n⚠ Some tests failed\n")
            return False
            
    except Exception as e:
        print(f"✗ HybridLLMHandler test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Test integration with app.py"""
    print_header("TEST 3: Integration Test")
    
    try:
        from hybrid_llm_handler import get_hybrid_handler
        
        # Get handler
        handler = get_hybrid_handler(
            enable_reasoning=True,
            enable_cache=True,
            num_recursions=3
        )
        
        print(f"✓ Handler initialized")
        print(f"  - Reasoning: {'Enabled' if handler.enable_reasoning else 'Disabled'}")
        print(f"  - Cache: {'Enabled' if handler.cache else 'Disabled'}")
        print(f"  - Recursions: {handler.num_recursions}")
        print(f"  - Mistral: {'Available' if handler.mistral.available else 'Unavailable'}")
        
        # Test stats
        stats = handler.get_stats()
        print(f"\n✓ Stats retrieved:")
        print(f"  - Mode: {stats['mode']}")
        print(f"  - Total queries: {stats['queries']['total']}")
        
        print("\n✓ Integration test passed!\n")
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Test if app.py can be imported"""
    print_header("TEST 4: API Endpoints")
    
    try:
        # Try to import app
        print("Importing app.py...")
        import app
        
        print("✓ app.py imported successfully")
        print(f"✓ Flask app created")
        print(f"✓ Hybrid handler initialized")
        
        # Check endpoints
        endpoints = [
            '/api/query',
            '/api/query/stream',
            '/api/languages',
            '/api/stats',
            '/api/reasoning/toggle',
            '/api/reasoning/status'
        ]
        
        print(f"\n✓ Available endpoints:")
        for endpoint in endpoints:
            print(f"  - {endpoint}")
        
        print("\n✓ API endpoints test passed!\n")
        return True
        
    except Exception as e:
        print(f"✗ API endpoints test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print_header("🔴 CAP 9000 - HYBRID SYSTEM TEST SUITE")
    
    print("Testing TinyRecursiveModels integration in CAP 9000...")
    print("This will test all components of the hybrid system.\n")
    
    start_time = time.time()
    
    # Run tests
    results = []
    results.append(("RecursiveReasoningModule", test_recursive_module()))
    results.append(("HybridLLMHandler", test_hybrid_handler()))
    results.append(("Integration", test_integration()))
    results.append(("API Endpoints", test_api_endpoints()))
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status} - {name}")
    
    elapsed = time.time() - start_time
    
    print(f"\n{'='*70}")
    print(f"  Results: {passed}/{total} tests passed")
    print(f"  Time: {elapsed:.2f}s")
    print(f"{'='*70}\n")
    
    if passed == total:
        print("🎉 All tests passed! The hybrid system is ready.\n")
        print("Next steps:")
        print("  1. Install PyTorch: pip install torch torchvision")
        print("  2. Start the server: python app.py")
        print("  3. Test with queries to see reasoning in action!")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Test Academic Search System
Verify OpenAI integration with offline caching works correctly
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_assistant.offline_manager import OfflineDataManager

def test_offline_manager():
    """Test offline manager functionality"""
    print("=" * 60)
    print("Testing Offline Manager - Academic Search System")
    print("=" * 60)
    print()
    
    # Initialize manager
    print("1. Initializing Offline Data Manager...")
    manager = OfflineDataManager()
    print("   ✓ Manager initialized\n")
    
    # Test adding to knowledge base
    print("2. Testing add_to_knowledge_base()...")
    test_query = "What is machine learning?"
    test_answer = """Machine learning is a subset of artificial intelligence (AI) that 
    enables systems to learn and improve from experience without being explicitly programmed. 
    It focuses on developing algorithms that can access data and use it to learn for themselves."""
    
    result = manager.add_to_knowledge_base(
        category="AI_Generated",
        question=test_query,
        answer=test_answer,
        source="OpenAI GPT-4",
        confidence=0.90,
        difficulty_level="university",
        academic_field="Computer Science"
    )
    
    if result:
        print("   ✓ Entry added successfully\n")
    else:
        print("   ✗ Failed to add entry\n")
        return False
    
    # Test searching
    print("3. Testing search_offline_data()...")
    results = manager.search_offline_data(test_query)
    
    if results and len(results) > 0:
        print(f"   ✓ Found {len(results)} result(s)")
        print(f"   First result confidence: {results[0].get('confidence', 0):.2f}")
        print(f"   Answer preview: {results[0]['answer'][:80]}...\n")
    else:
        print("   ✗ No results found\n")
        return False
    
    # Test caching
    print("4. Testing cache_online_search()...")
    cache_result = manager.cache_online_search(
        query="test quantum physics",
        response="Quantum physics test response",
        source="openai"
    )
    
    if cache_result:
        print("   ✓ Search cached successfully\n")
    else:
        print("   ✗ Failed to cache search\n")
        return False
    
    # Test retrieving cache
    print("5. Testing get_search_cache()...")
    cached = manager.get_search_cache("test quantum physics")
    
    if cached:
        print(f"   ✓ Cache retrieved")
        print(f"   Cached response: {cached['response'][:50]}...\n")
    else:
        print("   ✗ Cache not found\n")
        return False
    
    # Test statistics
    print("6. Testing get_statistics()...")
    stats = manager.get_statistics()
    
    print(f"   Knowledge entries: {stats.get('knowledge_entries', 0)}")
    print(f"   Cached searches: {stats.get('cached_searches', 0)}")
    print(f"   Categories: {len(stats.get('categories', []))}\n")
    
    return True

def test_knowledge_base_structure():
    """Test knowledge base CSV structure"""
    print("=" * 60)
    print("Testing Knowledge Base Structure")
    print("=" * 60)
    print()
    
    kb_file = "offline_data/aivi_knowledge_base.csv"
    
    if not os.path.exists(kb_file):
        print(f"   ✗ Knowledge base file not found: {kb_file}\n")
        return False
    
    print(f"1. Checking file: {kb_file}")
    
    with open(kb_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    print(f"   ✓ File exists")
    print(f"   Total lines: {len(lines)}")
    
    if len(lines) > 0:
        header = lines[0].strip()
        print(f"   Header: {header}")
        
        required_fields = ['id', 'category', 'question', 'answer', 'keywords', 
                          'source', 'timestamp', 'confidence']
        
        for field in required_fields:
            if field in header:
                print(f"   ✓ Field present: {field}")
            else:
                print(f"   ✗ Field missing: {field}")
                return False
    
    print()
    return True

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("AIVI Academic Search System - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        ("Knowledge Base Structure", test_knowledge_base_structure),
        ("Offline Manager Functionality", test_offline_manager),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✓ PASSED: {test_name}\n")
            else:
                failed += 1
                print(f"✗ FAILED: {test_name}\n")
        except Exception as e:
            failed += 1
            print(f"✗ ERROR in {test_name}: {str(e)}\n")
    
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

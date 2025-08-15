#!/usr/bin/env python3
"""
System test script for TrueCast News RAG Fact-Checker
Tests all major components to ensure they're working correctly.
"""

import sys
import traceback
from core.config import SETTINGS
from core.ingestion import run_ingestion_once
from core.retriever import retrieve_with_context
from core.misinfo import check_misinformation
from core.generator import generate_fact_checked_answer
from core.credibility import assess_sources

def test_config():
    """Test configuration loading."""
    print("🔧 Testing configuration...")
    try:
        assert SETTINGS.VECTOR_DIR == "data/chroma"
        assert SETTINGS.MODEL_EMBED == "sentence-transformers/all-MiniLM-L6-v2"
        print("✅ Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_ingestion():
    """Test news ingestion."""
    print("📰 Testing news ingestion...")
    try:
        articles = run_ingestion_once()
        print(f"✅ Ingestion successful: {articles} articles processed")
        return True
    except Exception as e:
        print(f"❌ Ingestion test failed: {e}")
        return False

def test_retrieval():
    """Test document retrieval."""
    print("🔍 Testing document retrieval...")
    try:
        context, hits = retrieve_with_context("stock market today")
        assert len(hits) > 0
        print(f"✅ Retrieval successful: {len(hits)} documents found")
        return True
    except Exception as e:
        print(f"❌ Retrieval test failed: {e}")
        return False

def test_misinformation_detection():
    """Test misinformation detection."""
    print("🛡️ Testing misinformation detection...")
    try:
        result = check_misinformation("Bitcoin will reach $1 million by next week")
        assert "misinformation_flag" in result
        assert "evidence" in result
        print(f"✅ Misinformation detection successful: {result['misinformation_flag']}")
        return True
    except Exception as e:
        print(f"❌ Misinformation detection test failed: {e}")
        return False

def test_fact_checking():
    """Test fact-checked answer generation."""
    print("🤖 Testing fact-checked answer generation...")
    try:
        answer, hits = generate_fact_checked_answer("What's happening with the stock market?")
        assert len(answer) > 0
        assert len(hits) > 0
        print(f"✅ Fact-checking successful: {len(answer)} characters generated")
        return True
    except Exception as e:
        print(f"❌ Fact-checking test failed: {e}")
        return False

def test_credibility():
    """Test source credibility assessment."""
    print("📊 Testing source credibility assessment...")
    try:
        # Create mock hits for testing
        mock_hits = [{"site": "reuters.com"}, {"site": "cnbc.com"}]
        score = assess_sources(mock_hits)
        assert 0 <= score <= 100
        print(f"✅ Credibility assessment successful: {score}/100")
        return True
    except Exception as e:
        print(f"❌ Credibility assessment test failed: {e}")
        return False

def main():
    """Run all system tests."""
    print("🚀 Starting TrueCast System Tests\n")
    
    tests = [
        test_config,
        test_ingestion,
        test_retrieval,
        test_misinformation_detection,
        test_fact_checking,
        test_credibility
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            traceback.print_exc()
        print()
    
    print("📋 Test Summary")
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

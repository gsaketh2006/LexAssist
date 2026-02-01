#!/usr/bin/env python
"""
Quick test script to verify StartupLex Backend is working with test mode
Run this to test the backend without needing the RAG API running
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health check endpoint"""
    print("=" * 80)
    print("Testing Health Check")
    print("=" * 80)
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Server Status: {data['status']}")
            print(f"✓ Mode: {data['mode']}")
            print(f"✓ Service: {data['service']}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    print()

def test_query(question):
    """Test a query"""
    print("-" * 80)
    print(f"Question: {question}")
    print("-" * 80)
    try:
        payload = {
            "question": question,
            "context": ""
        }
        response = requests.post(
            f"{BASE_URL}/api/query",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data['status']}")
            print(f"Mode: {data['mode']}")
            print(f"\nResponse:")
            print(f"{data['answer']}")
            print()
        else:
            print(f"✗ Query failed: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"✗ Error: {e}")
    print()

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " STARTUPLEX BACKEND - TEST MODE VERIFICATION ".center(78) + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Test health check
    test_health()
    
    # Wait a moment for server to be ready
    time.sleep(0.5)
    
    # Test various queries
    test_queries = [
        "What documents do I need to incorporate my startup?",
        "How should I structure equity for my first employees?",
        "What is a SAFE and when should we use it?",
        "What GDPR compliance do we need for our SaaS?",
        "How do we protect our intellectual property?",
        "What's the standard vesting schedule for founders?",
        "What should be in our operating agreement?",
        "Do we need employment agreements?",
        "What licenses do we need for our startup?",
        "What's the difference between a C-corp and S-corp?",
    ]
    
    print("=" * 80)
    print("Testing Sample Queries")
    print("=" * 80)
    print()
    
    for i, question in enumerate(test_queries, 1):
        print(f"[Query {i}/{len(test_queries)}]")
        test_query(question)
        time.sleep(0.3)  # Small delay between requests
    
    print("=" * 80)
    print("✓ All tests completed!")
    print("=" * 80)
    print("\nNotes:")
    print("- Backend is running in TEST MODE")
    print("- Using mock responses from test_queries.py")
    print("- When RAG API is ready, set TEST_MODE=False in .env")
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Fatal Error: {e}")
        print("\nMake sure the Flask backend is running:")
        print("  .\.venv\Scripts\python.exe app.py")

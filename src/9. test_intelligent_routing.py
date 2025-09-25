#!/usr/bin/env python3
"""
Test Script for Intelligent Medical Routing Agent
================================================

This script demonstrates the intelligent routing functionality by testing
different types of medical queries and showing how the AI agent routes them
to appropriate tools.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import intelligent_medical_agent

def test_routing_queries():
    """
    Test various types of medical queries to demonstrate routing
    """
    
    test_queries = [
        # Database/Statistics queries
        {
            "query": "Show me the top 5 ages with highest heart disease cases",
            "expected_intent": "database",
            "description": "Statistics query - should route to database tools"
        },
        {
            "query": "How many cancer patients are there by gender?",
            "expected_intent": "database", 
            "description": "Data aggregation query - should route to database tools"
        },
        {
            "query": "What is the average age of diabetes patients?",
            "expected_intent": "database",
            "description": "Statistical analysis query - should route to database tools"
        },
        
        # Web search queries
        {
            "query": "What are the common symptoms of diabetes?",
            "expected_intent": "web",
            "description": "Symptom definition query - should route to web search"
        },
        {
            "query": "What is heart disease and how is it treated?",
            "expected_intent": "web",
            "description": "Definition and treatment query - should route to web search"
        },
        {
            "query": "Tell me about cancer prevention methods",
            "expected_intent": "web",
            "description": "General knowledge query - should route to web search"
        },
        
        # Mixed queries
        {
            "query": "What is diabetes and show me the statistics of diabetic patients",
            "expected_intent": "mixed",
            "description": "Mixed query - should route to both web and database tools"
        },
        {
            "query": "Explain heart disease symptoms and show me the age distribution",
            "expected_intent": "mixed", 
            "description": "Mixed query - should route to both web and database tools"
        }
    ]
    
    print("🧠 Testing Intelligent Medical Routing Agent")
    print("=" * 60)
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n📋 Test {i}: {test_case['description']}")
        print(f"Query: \"{test_case['query']}\"")
        print(f"Expected Intent: {test_case['expected_intent']}")
        print("-" * 40)
        
        try:
            # Test the routing analysis
            analysis = intelligent_medical_agent.analyze_query_intent(test_case['query'])
            
            print(f"✅ Detected Intent: {analysis['intent']}")
            print(f"📊 Confidence: {analysis['confidence']:.2f}")
            print(f"💭 Reasoning: {analysis['reasoning']}")
            print(f"🔧 Recommended Tools: {', '.join(analysis['recommended_tools'])}")
            
            # Check if routing matches expectation
            if analysis['intent'] == test_case['expected_intent']:
                print("✅ PASS: Routing matches expected intent")
            else:
                print(f"⚠️  PARTIAL: Expected {test_case['expected_intent']}, got {analysis['intent']}")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
        
        print("-" * 40)

def test_full_execution():
    """
    Test full query execution with a few examples
    """
    print("\n🚀 Testing Full Query Execution")
    print("=" * 60)
    
    test_queries = [
        "What are the symptoms of diabetes?",
        "Show me heart disease statistics by age",
        "What is cancer and how many patients do we have?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: \"{query}\"")
        print("-" * 40)
        
        try:
            result = intelligent_medical_agent.route_and_execute(query)
            
            print(f"📊 Status: {result['status']}")
            print(f"🧠 Routing Decision: {result['routing_decision']['intent']}")
            print(f"📈 Confidence: {result['routing_decision']['confidence']:.2f}")
            print(f"🔧 Tools Used: {', '.join(result['tools_used']) if result['tools_used'] else 'None'}")
            print(f"💬 Response: {result['response'][:200]}...")
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
        
        print("-" * 40)

if __name__ == "__main__":
    print("🏥 Medical Intelligent Routing Agent Test Suite")
    print("=" * 60)
    
    # Test routing analysis
    test_routing_queries()
    
    # Test full execution (commented out to avoid API calls during testing)
    # Uncomment the line below to test full execution
    # test_full_execution()
    
    print("\n✅ Test Suite Completed!")
    print("\n💡 To test full execution, uncomment the test_full_execution() call in the script")

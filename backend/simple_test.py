#!/usr/bin/env python3
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_api():
    print("🚀 Testing GitHub Resume Points Generator API")
    
    # Check environment
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key or gemini_key == "your-gemini-api-key-here":
        print("❌ GEMINI_API_KEY not set correctly")
        return
    print("✅ GEMINI_API_KEY is set")
    
    # Test data
    test_data = {
        "github_url": "https://github.com/octocat/Hello-World",
        "num_points": 3,
        "technical_level": "medium",
        "output_tone": "action-oriented",
        "generate_technical": True
    }
    
    try:
        # Health check
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ API is running")
        else:
            print("❌ API health check failed")
            return
    except:
        print("❌ Could not connect to API. Start with: python3 main.py")
        return
    
    # Test main endpoint
    try:
        print("🔄 Generating resume points...")
        response = requests.post("http://localhost:8000/generate-resume-points", 
                               json=test_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"Repository: {result['repository_info']['name']}")
            print("Generated points:")
            for i, point in enumerate(result['points'], 1):
                print(f"  {i}. {point}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_api()
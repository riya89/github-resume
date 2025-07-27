#!/usr/bin/env python3
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_flask_api():
    print("🚀 Testing Flask-based GitHub Resume Points Generator")
    print("=" * 55)
    
    # Check environment
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key or gemini_key == "your-gemini-api-key-here":
        print("❌ GEMINI_API_KEY not set correctly")
        print("   Set it in your .env file: GEMINI_API_KEY=your_actual_key")
        return
    print("✅ GEMINI_API_KEY is set")
    
    # Test data
    test_data = {
        "github_url": "https://github.com/octocat/Hello-World",
        "num_points": 3,
        "technical_level": "medium", 
        "output_tone": "action-oriented"
    }
    
    try:
        # Health check first
        print("\n🔍 Checking API health...")
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ API is running and healthy")
        else:
            print("❌ API health check failed")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API")
        print("   Make sure to run: python3 flask_main.py")
        return
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test main endpoint
    try:
        print(f"\n🔄 Testing with repository: {test_data['github_url']}")
        print("   Generating resume points...")
        
        response = requests.post(
            "http://localhost:8000/generate-resume-points", 
            json=test_data, 
            timeout=30
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API request successful!")
            print(f"⏱️  Processing time: {result.get('processing_time', 'N/A')}")
            
            repo_info = result['repository_info']
            print(f"\n📁 Repository Info:")
            print(f"   Name: {repo_info['name']}")
            print(f"   Language: {repo_info['language']}")
            print(f"   Stars: {repo_info['stars']}")
            print(f"   Forks: {repo_info['forks']}")
            
            print(f"\n📝 Generated Resume Points:")
            for i, point in enumerate(result['points'], 1):
                print(f"   {i}. {point}")
                
        else:
            print(f"❌ API request failed")
            try:
                error_detail = response.json()
                print(f"   Error: {error_detail}")
            except:
                print(f"   Response: {response.text}")
                
    except requests.exceptions.Timeout:
        print("❌ Request timed out (>30s)")
        print("   This might be due to:")
        print("   - Slow Gemini API response")
        print("   - Large repository analysis")
        print("   - Network issues")
        
    except Exception as e:
        print(f"❌ Request error: {e}")

def test_gemini_direct():
    print("\n🤖 Testing Gemini API directly...")
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        
        # Test simple generation
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Generate 1 resume bullet point for a Python developer.")
        
        if response.text:
            print("✅ Gemini API working correctly")
            print(f"   Sample: {response.text[:100]}...")
        else:
            print("❌ Gemini API returned empty response")
            
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")

if __name__ == "__main__":
    test_gemini_direct()
    test_flask_api()
    
    print("\n" + "=" * 55)
    print("✅ Test completed!")
    print("\nIf there are issues:")
    print("1. Make sure Flask app is running: python3 flask_main.py")
    print("2. Check your .env file has the correct GEMINI_API_KEY")
    print("3. Try with a different GitHub repository")
    print("4. Check the Flask app logs for detailed errors")
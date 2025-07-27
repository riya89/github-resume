#!/usr/bin/env python3
"""
Test script for GitHub Resume Points Generator API
Run this to test your API locally and debug issues
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api():
    """Test the API with a sample GitHub repository"""
    
    # API endpoint
    url = "http://localhost:8000/generate-resume-points"
    
    # Test data
    test_data = {
        "github_url": "https://github.com/octocat/Hello-World",
        "num_points": 3,
        "technical_level": "medium",
        "output_tone": "action-oriented",
        "generate_technical": True
    }
    
    print("🚀 Testing GitHub Resume Points Generator API")
    print(f"📍 Endpoint: {url}")
    print(f"📦 Test Repository: {test_data['github_url']}")
    print("-" * 50)
    
    try:
        # Check if API is running
        health_response = requests.get("http://localhost:8000/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ API is running and healthy")
        else:
            print("❌ API health check failed")
            return
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the backend is running on port 8000")
        print("   Run: python main.py")
        return
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    try:
        # Test the main endpoint
        print("\n🔄 Sending request to generate resume points...")
        response = requests.post(url, json=test_data, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API request successful!")
            print(f"⏱️  Processing time: {result.get('processing_time', 'N/A')}")
            print(f"📁 Repository: {result['repository_info']['name']}")
            print(f"⭐ Stars: {result['repository_info']['stars']}")
            print(f"🍴 Forks: {result['repository_info']['forks']}")
            print(f"💻 Language: {result['repository_info']['language']}")
            
            print("\n📝 Generated Resume Points:")
            for i, point in enumerate(result['points'], 1):
                print(f"   {i}. {point}")
                
        else:
            print(f"❌ API request failed with status {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Error details: {error_detail}")
            except:
                print(f"Error text: {response.text}")
                
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The API might be taking too long to respond.")
        print("   This could be due to:")
        print("   - Slow Gemini API response")
        print("   - Large repository analysis")
        print("   - Network issues")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the backend is running.")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def check_environment():
    """Check if environment is properly configured"""
    print("\n🔧 Environment Check:")
    print("-" * 30)
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key and gemini_key != "your-gemini-api-key-here":
        print("✅ GEMINI_API_KEY is set")
    else:
        print("❌ GEMINI_API_KEY is not set or using placeholder")
        print("   Please set your Gemini API key in the .env file")
        print("   Get your key from: https://makersuite.google.com/app/apikey")
        return False
    
    return True

def test_gemini_directly():
    """Test Gemini API directly"""
    print("\n🤖 Testing Gemini API directly:")
    print("-" * 35)
    
    try:
        import google.generativeai as genai
        
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        
        # Try to initialize the model
        try:
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            print("✅ Gemini 2.0 Flash model initialized")
        except Exception as e:
            print(f"⚠️  Gemini 2.0 Flash not available: {e}")
            try:
                model = genai.GenerativeModel('gemini-pro')
                print("✅ Gemini Pro model initialized as fallback")
            except Exception as e2:
                print(f"❌ No Gemini model available: {e2}")
                return False
        
        # Test generation
        response = model.generate_content("Generate 2 resume bullet points for a Python developer.")
        if response.text:
            print("✅ Gemini API is working correctly")
            print("Sample response:")
            print(response.text[:200] + "..." if len(response.text) > 200 else response.text)
        else:
            print("❌ Gemini API returned empty response")
            return False
            
    except ImportError:
        print("❌ google-generativeai library not installed")
        print("   Run: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔍 GitHub Resume Points Generator - API Test")
    print("=" * 50)
    
    # Check environment first
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above.")
        exit(1)
    
    # Test Gemini API directly
    if not test_gemini_directly():
        print("\n❌ Gemini API test failed. Please check your API key.")
        exit(1)
    
    # Test the main API
    test_api()
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")
    print("\nIf there are issues:")
    print("1. Check that backend is running: python main.py")
    print("2. Verify .env file has correct GEMINI_API_KEY")
    print("3. Check backend logs for detailed error messages")
    print("4. Try with a different GitHub repository URL")
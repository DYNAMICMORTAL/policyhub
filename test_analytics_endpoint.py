#!/usr/bin/env python3
"""
Quick script to test the analytics endpoint directly
"""
import requests
import json

def test_analytics_endpoint():
    print("🧪 Testing Analytics Endpoint")
    print("=" * 40)
    
    try:
        response = requests.get('http://localhost:5000/analytics')
        
        if response.status_code == 200:
            print("✅ Analytics endpoint is working!")
            print(f"   - Status Code: {response.status_code}")
            print(f"   - Content Length: {len(response.text)} characters")
            print("   - Page loaded successfully")
        else:
            print(f"❌ Analytics endpoint returned status: {response.status_code}")
            print(f"   - Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Error accessing analytics endpoint: {e}")

if __name__ == '__main__':
    test_analytics_endpoint()

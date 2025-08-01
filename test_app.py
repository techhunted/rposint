#!/usr/bin/env python3
"""
Simple test script for OSINT application
"""

import requests
import json
import time

def test_endpoints(base_url="http://localhost:5000"):
    """Test all endpoints of the OSINT application"""
    
    print("🔍 Testing OSINT Application Endpoints")
    print("=" * 50)
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check: PASSED")
        else:
            print(f"❌ Health check: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Health check: ERROR ({str(e)})")
    
    # Test debug endpoint
    try:
        response = requests.get(f"{base_url}/debug")
        if response.status_code == 200:
            data = response.json()
            print("✅ Debug endpoint: PASSED")
            print(f"   - Templates exist: {data.get('filesystem', {}).get('templates_exist', False)}")
            print(f"   - Static exists: {data.get('filesystem', {}).get('static_exists', False)}")
        else:
            print(f"❌ Debug endpoint: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Debug endpoint: ERROR ({str(e)})")
    
    # Test API status
    try:
        response = requests.get(f"{base_url}/api/status")
        if response.status_code == 200:
            data = response.json()
            print("✅ API status: PASSED")
            print(f"   - API keys configured: {sum(data.get('api_keys', {}).values())}")
        else:
            print(f"❌ API status: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ API status: ERROR ({str(e)})")
    
    # Test phone OSINT endpoint
    try:
        response = requests.post(f"{base_url}/api/phone", 
                               json={"phone_number": "+1234567890"})
        if response.status_code == 200:
            print("✅ Phone OSINT: PASSED")
        else:
            print(f"❌ Phone OSINT: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Phone OSINT: ERROR ({str(e)})")
    
    # Test email OSINT endpoint
    try:
        response = requests.post(f"{base_url}/api/email", 
                               json={"email": "test@example.com"})
        if response.status_code == 200:
            print("✅ Email OSINT: PASSED")
        else:
            print(f"❌ Email OSINT: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Email OSINT: ERROR ({str(e)})")
    
    print("\n" + "=" * 50)
    print("🎯 Test completed!")

if __name__ == "__main__":
    # Test local development server
    test_endpoints()
    
    # Uncomment to test deployed version
    # test_endpoints("https://your-app-name.onrender.com") 
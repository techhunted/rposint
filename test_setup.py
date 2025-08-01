#!/usr/bin/env python3
"""
Test script to verify OSINT platform setup
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

def test_python_imports():
    """Test if all required Python packages can be imported"""
    print("🔍 Testing Python imports...")
    
    required_packages = [
        'flask',
        'flask_cors',
        'aiohttp',
        'requests',
        'PIL',
        'numpy',
        'cv2',
        'tensorflow',
        'torch'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    return len(failed_imports) == 0

def test_tool_availability():
    """Test if OSINT tools are available"""
    print("\n🔍 Testing tool availability...")
    
    tools_to_check = [
        ('tools/phoneinfoga/phoneinfoga', 'PhoneInfoga'),
        ('tools/sherlock/sherlock/sherlock.py', 'Sherlock'),
        ('tools/theHarvester/theHarvester.py', 'theHarvester'),
        ('tools/Sublist3r/sublist3r.py', 'Sublist3r'),
        ('tools/exiftool/exiftool.exe', 'ExifTool'),
        ('tools/amass/amass', 'Amass')
    ]
    
    available_tools = []
    missing_tools = []
    
    for tool_path, tool_name in tools_to_check:
        if os.path.exists(tool_path):
            print(f"✅ {tool_name}")
            available_tools.append(tool_name)
        else:
            print(f"❌ {tool_name} (not found)")
            missing_tools.append(tool_name)
    
    return available_tools, missing_tools

def test_api_keys():
    """Test if API keys are configured"""
    print("\n🔍 Testing API key configuration...")
    
    api_keys = {
        'OPENAI_API_KEY': 'OpenAI (ChatGPT)',
        'GEMINI_API_KEY': 'Google Gemini',
        'NUMVERIFY_API_KEY': 'Numverify',
        'TWILIO_API_KEY': 'Twilio',
        'HIBP_API_KEY': 'HaveIBeenPwned',
        'EMAILREP_API_KEY': 'EmailRep.io',
        'HUNTER_API_KEY': 'Hunter.io',
        'INTELX_API_KEY': 'IntelX',
        'EPIEOS_API_KEY': 'Epieos'
    }
    
    configured_keys = []
    missing_keys = []
    
    for key_name, service_name in api_keys.items():
        if os.getenv(key_name) and os.getenv(key_name) != f'your_{key_name.lower()}_here':
            print(f"✅ {service_name}")
            configured_keys.append(service_name)
        else:
            print(f"❌ {service_name} (not configured)")
            missing_keys.append(service_name)
    
    return configured_keys, missing_keys

def test_flask_app():
    """Test if Flask app can start"""
    print("\n🔍 Testing Flask application...")
    
    try:
        # Try to import the Flask app
        sys.path.append('.')
        from osint_app import app
        
        # Test if app can be created
        with app.test_client() as client:
            response = client.get('/api/status')
            if response.status_code == 200:
                print("✅ Flask app is working")
                return True
            else:
                print(f"❌ Flask app returned status {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def test_network_connectivity():
    """Test network connectivity to external services"""
    print("\n🔍 Testing network connectivity...")
    
    test_urls = [
        ('https://api.openai.com', 'OpenAI API'),
        ('https://generativelanguage.googleapis.com', 'Google Gemini API'),
        ('https://emailrep.io', 'EmailRep.io'),
        ('https://haveibeenpwned.com', 'HaveIBeenPwned'),
        ('https://api.hunter.io', 'Hunter.io')
    ]
    
    working_services = []
    failed_services = []
    
    for url, service_name in test_urls:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code in [200, 401, 403]:  # 401/403 means service is reachable
                print(f"✅ {service_name}")
                working_services.append(service_name)
            else:
                print(f"❌ {service_name} (status: {response.status_code})")
                failed_services.append(service_name)
        except Exception as e:
            print(f"❌ {service_name} (error: {e})")
            failed_services.append(service_name)
    
    return working_services, failed_services

def test_file_structure():
    """Test if required files and directories exist"""
    print("\n🔍 Testing file structure...")
    
    required_files = [
        'osint_app.py',
        'requirements.txt',
        'setup_tools.py',
        'README.md',
        'templates/osint_app.html'
    ]
    
    required_dirs = [
        'tools',
        'templates',
        'models',
        'data',
        'logs'
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")
            missing_files.append(file_path)
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ (missing)")
            missing_dirs.append(dir_path)
    
    return len(missing_files) == 0 and len(missing_dirs) == 0

def generate_report(imports_ok, available_tools, missing_tools, configured_keys, missing_keys, flask_ok, working_services, failed_services, structure_ok):
    """Generate a comprehensive setup report"""
    print("\n" + "="*60)
    print("📊 OSINT PLATFORM SETUP REPORT")
    print("="*60)
    
    # Overall status
    total_tests = 5
    passed_tests = 0
    
    if imports_ok:
        passed_tests += 1
    if len(available_tools) > 0:
        passed_tests += 1
    if len(configured_keys) > 0:
        passed_tests += 1
    if flask_ok:
        passed_tests += 1
    if structure_ok:
        passed_tests += 1
    
    print(f"\n🎯 Overall Status: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 Setup is complete and ready to use!")
    else:
        print("⚠️  Setup needs attention - see details below")
    
    # Detailed breakdown
    print(f"\n📦 Python Dependencies: {'✅ OK' if imports_ok else '❌ Issues'}")
    print(f"🛠️  OSINT Tools: {len(available_tools)} available, {len(missing_tools)} missing")
    print(f"🔑 API Keys: {len(configured_keys)} configured, {len(missing_keys)} missing")
    print(f"🌐 Network: {len(working_services)} services reachable, {len(failed_services)} failed")
    print(f"📁 File Structure: {'✅ OK' if structure_ok else '❌ Issues'}")
    print(f"🚀 Flask App: {'✅ OK' if flask_ok else '❌ Issues'}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    
    if len(missing_tools) > 0:
        print(f"   - Run 'python setup_tools.py' to install missing tools")
    
    if len(missing_keys) > 0:
        print(f"   - Configure API keys in .env file for better functionality")
    
    if len(failed_services) > 0:
        print(f"   - Check internet connection and firewall settings")
    
    if not structure_ok:
        print(f"   - Ensure all required files and directories exist")
    
    print(f"\n🚀 To start the application:")
    print(f"   python osint_app.py")
    print(f"   Then open http://localhost:5000 in your browser")

def main():
    """Main test function"""
    print("🧪 OSINT Platform Setup Test")
    print("="*40)
    
    # Run all tests
    imports_ok = test_python_imports()
    available_tools, missing_tools = test_tool_availability()
    configured_keys, missing_keys = test_api_keys()
    flask_ok = test_flask_app()
    working_services, failed_services = test_network_connectivity()
    structure_ok = test_file_structure()
    
    # Generate report
    generate_report(
        imports_ok,
        available_tools,
        missing_tools,
        configured_keys,
        missing_keys,
        flask_ok,
        working_services,
        failed_services,
        structure_ok
    )

if __name__ == "__main__":
    main() 
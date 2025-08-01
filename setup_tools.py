#!/usr/bin/env python3
"""
Comprehensive OSINT Tools Setup Script
Installs all required tools and dependencies for the OSINT platform
"""

import os
import sys
import subprocess
import requests
import zipfile
import tarfile
import shutil
from pathlib import Path

def run_command(command, description=""):
    """Run a command and handle errors"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed: {e.stderr}")
        return False

def download_file(url, filename):
    """Download a file from URL"""
    print(f"📥 Downloading {filename}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False

def extract_archive(archive_path, extract_to):
    """Extract archive file"""
    print(f"📦 Extracting {archive_path}...")
    try:
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        elif archive_path.endswith('.tar.gz'):
            with tarfile.open(archive_path, 'r:gz') as tar_ref:
                tar_ref.extractall(extract_to)
        print(f"✅ Extracted {archive_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to extract {archive_path}: {e}")
        return False

def install_python_package(package_name, install_name=None):
    """Install Python package"""
    if install_name is None:
        install_name = package_name
    return run_command(f"pip install {install_name}", f"Installing {package_name}")

def clone_repository(repo_url, target_dir):
    """Clone a git repository"""
    if os.path.exists(target_dir):
        print(f"📁 {target_dir} already exists, skipping...")
        return True
    return run_command(f"git clone {repo_url} {target_dir}", f"Cloning {repo_url}")

def setup_environment():
    """Setup environment variables and directories"""
    print("🔧 Setting up environment...")
    
    # Create necessary directories
    directories = ['tools', 'models', 'data', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("""# OSINT Platform Environment Variables
# Add your API keys here

# OpenAI (ChatGPT)
OPENAI_API_KEY=your_openai_api_key_here

# Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here

# Grok (placeholder - not publicly available yet)
GROK_API_KEY=your_grok_api_key_here

# Phone Number APIs
NUMVERIFY_API_KEY=your_numverify_api_key_here
TWILIO_API_KEY=your_twilio_api_key_here

# Email APIs
HIBP_API_KEY=your_hibp_api_key_here
EMAILREP_API_KEY=your_emailrep_api_key_here
HUNTER_API_KEY=your_hunter_api_key_here

# IntelX API
INTELX_API_KEY=your_intelx_api_key_here

# Epieos API
EPIEOS_API_KEY=your_epieos_api_key_here
""")
        print("✅ Created .env file with API key placeholders")

def install_phone_tools():
    """Install phone number OSINT tools"""
    print("\n📞 Installing Phone Number OSINT Tools...")
    
    # PhoneInfoga
    clone_repository("https://github.com/sundowndev/phoneinfoga", "tools/phoneinfoga")
    run_command("cd tools/phoneinfoga && go build -o phoneinfoga", "Building PhoneInfoga")
    
    # NumSpy
    clone_repository("https://github.com/numspy/numspy", "tools/numsby")
    
    # phoner
    clone_repository("https://github.com/sundowndev/phoner", "tools/phoner")
    
    # Phone-Recon
    clone_repository("https://github.com/evilsocket/phone-recon", "tools/phone-recon")
    
    # Pynfone
    clone_repository("https://github.com/evilsocket/pynfone", "tools/pynfone")

def install_email_tools():
    """Install email OSINT tools"""
    print("\n📧 Installing Email OSINT Tools...")
    
    # Holehe
    install_python_package("holehe")
    
    # Maigret
    clone_repository("https://github.com/soxoj/maigret", "tools/maigret")
    run_command("cd tools/maigret && pip install -r requirements.txt", "Installing Maigret dependencies")
    
    # Infoga
    clone_repository("https://github.com/m4ll0k/Infoga", "tools/infoga")
    run_command("cd tools/infoga && pip install -r requirements.txt", "Installing Infoga dependencies")
    
    # theHarvester
    clone_repository("https://github.com/theHarvester/theHarvester", "tools/theHarvester")
    run_command("cd tools/theHarvester && pip install -r requirements.txt", "Installing theHarvester dependencies")
    
    # GHunt
    clone_repository("https://github.com/mxrch/GHunt", "tools/ghunt")
    run_command("cd tools/ghunt && pip install -r requirements.txt", "Installing GHunt dependencies")

def install_image_tools():
    """Install image OSINT tools"""
    print("\n🖼️ Installing Image OSINT Tools...")
    
    # ExifTool
    if not os.path.exists("tools/exiftool"):
        download_file("https://exiftool.org/exiftool-13.33_64.zip", "tools/exiftool.zip")
        extract_archive("tools/exiftool.zip", "tools/")
        os.rename("tools/exiftool-13.33_64", "tools/exiftool")
        os.remove("tools/exiftool.zip")
    
    # DeepFace (already in requirements.txt)
    install_python_package("deepface")
    
    # StegSeek
    clone_repository("https://github.com/RickdeJager/stegseek", "tools/stegseek")
    run_command("cd tools/stegseek && cmake . && make", "Building StegSeek")
    
    # ExifHunter
    clone_repository("https://github.com/evilsocket/exifhunter", "tools/exifhunter")

def install_video_tools():
    """Install video OSINT tools"""
    print("\n🎞️ Installing Video OSINT Tools...")
    
    # FFmpeg
    if sys.platform == "win32":
        download_file("https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip", "tools/ffmpeg.zip")
        extract_archive("tools/ffmpeg.zip", "tools/")
        # Add to PATH
        ffmpeg_path = os.path.abspath("tools/ffmpeg-*/bin")
        print(f"Add {ffmpeg_path} to your PATH")
    else:
        run_command("sudo apt-get install ffmpeg", "Installing FFmpeg")
    
    # YT-DLP
    install_python_package("yt-dlp")
    
    # Video-OSINT
    clone_repository("https://github.com/AI-Video-Intelligence-Platform/Video-OSINT", "tools/video-osint")
    
    # InVID Toolkit
    clone_repository("https://github.com/InVID-Framework/InVID", "tools/invid")
    
    # FakeVideoDetector
    clone_repository("https://github.com/ondyari/FaceForensics", "tools/faceforensics")

def install_deepfake_tools():
    """Install deepfake detection tools"""
    print("\n🎭 Installing Deepfake Detection Tools...")
    
    # Deepware Scanner
    clone_repository("https://github.com/deepware/deepware-scanner", "tools/deepware-scanner")
    
    # FaceForensics++
    clone_repository("https://github.com/ondyari/FaceForensics", "tools/faceforensics")
    
    # DFDC
    clone_repository("https://github.com/ondyari/FaceForensics", "tools/dfdc")
    
    # MesoNet
    clone_repository("https://github.com/DariusAf/MesoNet", "tools/mesonet")
    
    # FakeFinder
    clone_repository("https://github.com/evilsocket/fakefinder", "tools/fakefinder")

def install_face_tools():
    """Install face detection tools"""
    print("\n🙂 Installing Face Detection Tools...")
    
    # DeepFace (already in requirements.txt)
    install_python_package("deepface")
    
    # InsightFace
    install_python_package("insightface")
    
    # face_recognition
    install_python_package("face-recognition")
    
    # MTCNN
    install_python_package("mtcnn")
    
    # RetinaFace
    install_python_package("retinaface")

def install_website_tools():
    """Install website OSINT tools"""
    print("\n🌐 Installing Website OSINT Tools...")
    
    # Sublist3r
    clone_repository("https://github.com/aboul3la/Sublist3r", "tools/Sublist3r")
    run_command("cd tools/Sublist3r && pip install -r requirements.txt", "Installing Sublist3r dependencies")
    
    # theHarvester (already installed)
    print("theHarvester already installed")
    
    # Amass
    if sys.platform == "win32":
        download_file("https://github.com/owasp-amass/amass/releases/latest/download/amass_windows_amd64.zip", "tools/amass.zip")
        extract_archive("tools/amass.zip", "tools/")
    else:
        run_command("sudo snap install amass", "Installing Amass")
    
    # Photon
    clone_repository("https://github.com/s0md3v/Photon", "tools/Photon")
    run_command("cd tools/Photon && pip install -r requirements.txt", "Installing Photon dependencies")
    
    # WhatWeb
    clone_repository("https://github.com/urbanadventurer/WhatWeb", "tools/WhatWeb")

def install_social_tools():
    """Install social media OSINT tools"""
    print("\n📱 Installing Social Media OSINT Tools...")
    
    # Maigret (already installed)
    print("Maigret already installed")
    
    # Sherlock
    clone_repository("https://github.com/sherlock-project/sherlock", "tools/sherlock")
    run_command("cd tools/sherlock && pip install -r requirements.txt", "Installing Sherlock dependencies")
    
    # Social Analyzer
    install_python_package("social-analyzer")
    
    # Osintgram
    clone_repository("https://github.com/Datalux/Osintgram", "tools/osintgram")
    run_command("cd tools/osintgram && pip install -r requirements.txt", "Installing Osintgram dependencies")
    
    # Twint
    clone_repository("https://github.com/twintproject/twint", "tools/twint")
    run_command("cd tools/twint && pip install -r requirements.txt", "Installing Twint dependencies")

def install_ai_models():
    """Install AI models and dependencies"""
    print("\n🤖 Installing AI Models...")
    
    # Download pre-trained models for face detection
    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)
    
    # DeepFace models will be downloaded automatically on first use
    print("✅ AI models will be downloaded automatically on first use")

def create_startup_script():
    """Create startup script"""
    print("\n🚀 Creating startup script...")
    
    if sys.platform == "win32":
        with open("start_osint.bat", "w") as f:
            f.write("""@echo off
echo Starting OSINT Platform...
python osint_app.py
pause
""")
        print("✅ Created start_osint.bat")
    else:
        with open("start_osint.sh", "w") as f:
            f.write("""#!/bin/bash
echo "Starting OSINT Platform..."
python3 osint_app.py
""")
        os.chmod("start_osint.sh", 0o755)
        print("✅ Created start_osint.sh")

def main():
    """Main setup function"""
    print("🔧 OSINT Platform Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Install Python dependencies
    print("\n📦 Installing Python Dependencies...")
    run_command("pip install -r requirements.txt", "Installing Python dependencies")
    
    # Install tools by category
    install_phone_tools()
    install_email_tools()
    install_image_tools()
    install_video_tools()
    install_deepfake_tools()
    install_face_tools()
    install_website_tools()
    install_social_tools()
    install_ai_models()
    
    # Create startup script
    create_startup_script()
    
    print("\n🎉 Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Edit .env file and add your API keys")
    print("2. Run the application:")
    if sys.platform == "win32":
        print("   - Double-click start_osint.bat")
        print("   - Or run: python osint_app.py")
    else:
        print("   - Run: ./start_osint.sh")
        print("   - Or run: python3 osint_app.py")
    print("3. Open http://localhost:5000 in your browser")
    print("\n⚠️  Note: Some tools may require additional setup or API keys")
    print("📚 Check the documentation for each tool for specific requirements")

if __name__ == "__main__":
    main() 
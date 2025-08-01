# 🕵️ Powerful OSINT Web Application

A comprehensive, AI-powered OSINT (Open Source Intelligence) platform that integrates the top 5 tools for each category with ChatGPT, Gemini, and Grok analysis.

## 🌟 Features

### 📞 Phone Number OSINT
- **PhoneInfoga** - Advanced phone number reconnaissance
- **NumSpy** - Phone number intelligence gathering
- **phoner** - Phone number OSINT tool
- **Phone-Recon** - Phone reconnaissance framework
- **Pynfone** - Python-based phone OSINT

### 📧 Email OSINT
- **Holehe** - Email breach checker
- **Maigret** - Username/email search across platforms
- **Infoga** - Email OSINT and reconnaissance
- **theHarvester** - Email, subdomain, and DNS reconnaissance
- **GHunt** - Google Workspace reconnaissance

### 🖼️ Image OSINT
- **ExifTool** - Image metadata extraction
- **DeepFace** - Face analysis and recognition
- **Search by Image** - Reverse image search
- **StegSeek** - Steganography detection
- **ExifHunter** - Advanced image forensics

### 🎞️ Video OSINT
- **Video-OSINT** - Video intelligence platform
- **InVID Toolkit** - Video verification tools
- **FFmpeg** - Video metadata and analysis
- **YT-DLP** - YouTube video intelligence
- **FakeVideoDetector** - Video manipulation detection

### 🎭 Deepfake Detection
- **Deepware Scanner** - AI-powered deepfake detection
- **FaceForensics++** - Face manipulation detection
- **DFDC** - Deepfake Detection Challenge models
- **MesoNet** - Mesoscopic analysis
- **FakeFinder** - Fake media detection

### 🙂 Face Detection
- **DeepFace** - Face recognition and analysis
- **InsightFace** - High-performance face recognition
- **face_recognition** - Simple face recognition
- **MTCNN** - Multi-task cascaded networks
- **RetinaFace** - Robust face detection

### 🌐 Website OSINT
- **Sublist3r** - Subdomain enumeration
- **theHarvester** - Domain reconnaissance
- **Amass** - Network mapping and attack surface
- **Photon** - Web crawler and intelligence
- **WhatWeb** - Web application fingerprinting

### 📱 Social Media OSINT
- **Maigret** - Username search across platforms
- **Sherlock** - Username enumeration
- **Social Analyzer** - Social media intelligence
- **Osintgram** - Instagram OSINT
- **Twint** - Twitter intelligence

### 🤖 AI Integration
- **ChatGPT** - OpenAI GPT-4 analysis
- **Gemini** - Google AI analysis
- **Grok** - xAI analysis (when available)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- FFmpeg (for video analysis)
- Go (for some phone tools)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd osint-platform
```

2. **Run the setup script:**
```bash
python setup_tools.py
```

3. **Configure API keys:**
Edit the `.env` file and add your API keys:
```env
# OpenAI (ChatGPT)
OPENAI_API_KEY=your_openai_api_key_here

# Google Gemini
GEMINI_API_KEY=your_gemini_api_key_here

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
```

4. **Start the application:**
```bash
# Windows
start_osint.bat

# Linux/Mac
./start_osint.sh

# Or directly
python osint_app.py
```

5. **Open your browser:**
Navigate to `http://localhost:5000`

## 📖 Usage

### Phone Number Analysis
1. Click on "📞 Phone Number OSINT"
2. Enter a phone number (e.g., +1234567890)
3. Click "Analyze"
4. View results from all 5 tools plus AI analysis

### Email Analysis
1. Click on "📧 Email OSINT"
2. Enter an email address
3. Click "Analyze"
4. View breach data, social media presence, and AI insights

### Image Analysis
1. Click on "🖼️ Image OSINT"
2. Upload an image file
3. Click "Analyze"
4. View metadata, face analysis, and hidden data

### Video Analysis
1. Click on "🎞️ Video OSINT"
2. Upload a video file
3. Click "Analyze"
4. View metadata, manipulation detection, and AI insights

### Deepfake Detection
1. Click on "🎭 Deepfake Detection"
2. Select media type (image/video)
3. Upload media file
4. Click "Analyze"
5. View detection results from multiple AI models

### Face Detection
1. Click on "🙂 Face Detection"
2. Upload an image
3. Click "Analyze"
4. View face detection results from multiple algorithms

### Website Analysis
1. Click on "🌐 Website OSINT"
2. Enter a domain name
3. Click "Analyze"
4. View subdomains, technologies, and vulnerabilities

### Social Media Analysis
1. Click on "📱 Social Media OSINT"
2. Enter a username
3. Click "Analyze"
4. View social media presence across platforms

## 🔧 API Endpoints

The application provides REST API endpoints for programmatic access:

### Phone Number OSINT
```bash
POST /api/phone
Content-Type: application/json
{
  "phone_number": "+1234567890"
}
```

### Email OSINT
```bash
POST /api/email
Content-Type: application/json
{
  "email": "example@domain.com"
}
```

### Image OSINT
```bash
POST /api/image
Content-Type: multipart/form-data
image: [file]
```

### Video OSINT
```bash
POST /api/video
Content-Type: multipart/form-data
video: [file]
```

### Deepfake Detection
```bash
POST /api/deepfake
Content-Type: multipart/form-data
media: [file]
media_type: "image" or "video"
```

### Face Detection
```bash
POST /api/face
Content-Type: multipart/form-data
image: [file]
```

### Website OSINT
```bash
POST /api/website
Content-Type: application/json
{
  "domain": "example.com"
}
```

### Social Media OSINT
```bash
POST /api/social
Content-Type: application/json
{
  "username": "username"
}
```

### AI Analysis
```bash
POST /api/ai/analyze
Content-Type: application/json
{
  "provider": "openai",
  "prompt": "Analyze this data",
  "results": {...}
}
```

### Status Check
```bash
GET /api/status
```

## 🛠️ Tool Configuration

### Required API Keys

#### Free APIs (No key required):
- EmailRep.io
- HaveIBeenPwned (limited without key)

#### Paid APIs (Recommended):
- **OpenAI** - ChatGPT analysis
- **Google Gemini** - AI analysis
- **Numverify** - Phone number validation
- **Twilio** - Phone number lookup
- **Hunter.io** - Email verification
- **IntelX** - Intelligence platform
- **Epieos** - OSINT platform

### Tool-Specific Setup

Some tools require additional setup:

#### PhoneInfoga
- Requires Go installation
- May need API keys for some services

#### Maigret
- Requires Python dependencies
- May need browser automation setup

#### DeepFace
- Downloads models automatically on first use
- Requires significant disk space

#### FFmpeg
- Windows: Downloaded automatically
- Linux: `sudo apt-get install ffmpeg`
- Mac: `brew install ffmpeg`

## 🔒 Security & Legal

### Important Disclaimers

1. **Legal Use Only**: This tool is for legitimate OSINT research only
2. **Respect Privacy**: Always respect privacy laws and terms of service
3. **Rate Limiting**: Be mindful of API rate limits
4. **Data Protection**: Handle sensitive data responsibly

### Best Practices

- Use VPN when appropriate
- Respect robots.txt and terms of service
- Implement proper rate limiting
- Log and audit all activities
- Secure API keys and credentials

## 🐛 Troubleshooting

### Common Issues

1. **"Tool not found" errors**
   - Run `python setup_tools.py` again
   - Check if Git is installed
   - Verify internet connection

2. **API key errors**
   - Check `.env` file configuration
   - Verify API key validity
   - Check API service status

3. **Memory issues**
   - Some AI models require significant RAM
   - Close other applications
   - Consider using smaller models

4. **Permission errors**
   - Run as administrator (Windows)
   - Use `sudo` (Linux/Mac)
   - Check file permissions

### Debug Mode

Enable debug mode for detailed logging:
```bash
export FLASK_ENV=development
python osint_app.py
```

## 📊 Performance

### System Requirements

- **Minimum:**
  - 4GB RAM
  - 10GB disk space
  - Python 3.8+

- **Recommended:**
  - 8GB+ RAM
  - 50GB+ disk space
  - GPU for AI models
  - Fast internet connection

### Optimization Tips

1. **Use SSD storage** for faster model loading
2. **Increase RAM** for AI model processing
3. **Use GPU** for deep learning models
4. **Implement caching** for repeated queries
5. **Use async processing** for multiple tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

### Adding New Tools

1. Add tool to appropriate category in `osint_app.py`
2. Update tool paths in `OSINTToolManager`
3. Add installation steps to `setup_tools.py`
4. Update documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- All the open-source OSINT tool developers
- OpenAI, Google, and xAI for AI APIs
- The OSINT community for inspiration

## 📞 Support

- **Issues**: Create GitHub issues
- **Discussions**: Use GitHub discussions
- **Documentation**: Check the wiki

---

**⚠️ Disclaimer**: This tool is for educational and legitimate OSINT research purposes only. Users are responsible for complying with all applicable laws and regulations. 
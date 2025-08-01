#!/usr/bin/env python3
"""
Powerful OSINT Web Application
Integrates top 5 tools for each category + AI analysis
"""

import os
import json
import asyncio
import aiohttp
import subprocess
import requests
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import threading
import time
import base64
from PIL import Image
import io
import hashlib
import tempfile
import shutil

app = Flask(__name__)
CORS(app)

class OSINTToolManager:
    def __init__(self):
        self.api_keys = {
            'openai': os.getenv('OPENAI_API_KEY'),
            'gemini': os.getenv('GEMINI_API_KEY'),
            'grok': os.getenv('GROK_API_KEY'),
            'numverify': os.getenv('NUMVERIFY_API_KEY'),
            'twilio': os.getenv('TWILIO_API_KEY'),
            'hibp': os.getenv('HIBP_API_KEY'),
            'emailrep': os.getenv('EMAILREP_API_KEY'),
            'hunter': os.getenv('HUNTER_API_KEY'),
            'intelx': os.getenv('INTELX_API_KEY'),
            'epieos': os.getenv('EPIEOS_API_KEY')
        }
        
        # Tool paths (will be set during installation)
        self.tool_paths = {
            'phoneinfoga': 'phoneinfoga/phoneinfoga',
            'numsby': 'numsby/numsby',
            'phoner': 'phoner/phoner',
            'phone_recon': 'phone-recon/phone_recon',
            'pynfone': 'pynfone/pynfone',
            'holehe': 'holehe/holehe',
            'maigret': 'maigret/maigret',
            'infoga': 'infoga/infoga',
            'theharvester': 'theHarvester/theHarvester.py',
            'ghunt': 'ghunt/ghunt',
            'exiftool': 'exiftool-13.33_64/exiftool.exe',
            'sherlock': 'sherlock/sherlock/sherlock.py',
            'sublist3r': 'Sublist3r/sublist3r.py',
            'amass': 'amass/amass',
            'photon': 'Photon/photon.py',
            'whatweb': 'WhatWeb/whatweb'
        }

    async def call_ai_api(self, provider, prompt, results=None):
        """Call AI APIs (ChatGPT, Gemini, Grok) for analysis"""
        if not self.api_keys.get(provider):
            return {"error": f"{provider.upper()} API key not configured"}
        
        try:
            if provider == 'openai':
                return await self._call_openai(prompt, results)
            elif provider == 'gemini':
                return await self._call_gemini(prompt, results)
            elif provider == 'grok':
                return await self._call_grok(prompt, results)
        except Exception as e:
            return {"error": f"AI API error: {str(e)}"}

    async def _call_openai(self, prompt, results=None):
        """Call OpenAI ChatGPT API"""
        headers = {
            'Authorization': f'Bearer {self.api_keys["openai"]}',
            'Content-Type': 'application/json'
        }
        
        content = f"{prompt}\n\nOSINT Results:\n{json.dumps(results, indent=2) if results else 'No results available'}"
        
        data = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": content}],
            "max_tokens": 1000
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post('https://api.openai.com/v1/chat/completions', 
                                  headers=headers, json=data) as response:
                result = await response.json()
                return {"analysis": result.get('choices', [{}])[0].get('message', {}).get('content', 'No response')}

    async def _call_gemini(self, prompt, results=None):
        """Call Google Gemini API"""
        headers = {
            'Content-Type': 'application/json'
        }
        
        content = f"{prompt}\n\nOSINT Results:\n{json.dumps(results, indent=2) if results else 'No results available'}"
        
        data = {
            "contents": [{"parts": [{"text": content}]}]
        }
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_keys['gemini']}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                result = await response.json()
                return {"analysis": result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No response')}

    async def _call_grok(self, prompt, results=None):
        """Call Grok API (placeholder - replace with actual Grok API)"""
        # Note: Grok API is not publicly available yet, this is a placeholder
        return {"analysis": "Grok analysis placeholder - API not publicly available"}

    def run_command(self, command, timeout=30):
        """Run a command with timeout and error handling"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Phone Number OSINT Methods
    async def phone_osint(self, phone_number):
        """Run all phone number OSINT tools"""
        results = {}
        
        # PhoneInfoga
        try:
            cmd = f"python {self.tool_paths['phoneinfoga']} -n {phone_number}"
            result = self.run_command(cmd)
            results['PhoneInfoga'] = result
        except Exception as e:
            results['PhoneInfoga'] = {"success": False, "error": str(e)}

        # NumSpy
        try:
            cmd = f"python {self.tool_paths['numsby']} {phone_number}"
            result = self.run_command(cmd)
            results['NumSpy'] = result
        except Exception as e:
            results['NumSpy'] = {"success": False, "error": str(e)}

        # phoner
        try:
            cmd = f"python {self.tool_paths['phoner']} {phone_number}"
            result = self.run_command(cmd)
            results['phoner'] = result
        except Exception as e:
            results['phoner'] = {"success": False, "error": str(e)}

        # Phone-Recon
        try:
            cmd = f"python {self.tool_paths['phone_recon']} {phone_number}"
            result = self.run_command(cmd)
            results['Phone-Recon'] = result
        except Exception as e:
            results['Phone-Recon'] = {"success": False, "error": str(e)}

        # Pynfone
        try:
            cmd = f"python {self.tool_paths['pynfone']} {phone_number}"
            result = self.run_command(cmd)
            results['Pynfone'] = result
        except Exception as e:
            results['Pynfone'] = {"success": False, "error": str(e)}

        # API-based phone lookups
        api_results = await self.phone_api_lookups(phone_number)
        results.update(api_results)

        return results

    async def phone_api_lookups(self, phone_number):
        """Run API-based phone number lookups"""
        results = {}
        
        # Numverify API
        if self.api_keys.get('numverify'):
            try:
                url = f"http://apilayer.net/api/validate?access_key={self.api_keys['numverify']}&number={phone_number}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        data = await response.json()
                        results['Numverify'] = {"success": True, "data": data}
            except Exception as e:
                results['Numverify'] = {"success": False, "error": str(e)}

        # Twilio Lookup
        if self.api_keys.get('twilio'):
            try:
                url = f"https://lookups.twilio.com/v1/PhoneNumbers/{phone_number}"
                auth = (self.api_keys['twilio'], 'your_twilio_auth_token')
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, auth=aiohttp.BasicAuth(auth[0], auth[1])) as response:
                        data = await response.json()
                        results['Twilio'] = {"success": True, "data": data}
            except Exception as e:
                results['Twilio'] = {"success": False, "error": str(e)}

        return results

    # Email OSINT Methods
    async def email_osint(self, email):
        """Run all email OSINT tools"""
        results = {}
        
        # Holehe
        try:
            cmd = f"holehe {email}"
            result = self.run_command(cmd)
            results['Holehe'] = result
        except Exception as e:
            results['Holehe'] = {"success": False, "error": str(e)}

        # Maigret
        try:
            cmd = f"maigret {email}"
            result = self.run_command(cmd)
            results['Maigret'] = result
        except Exception as e:
            results['Maigret'] = {"success": False, "error": str(e)}

        # Infoga
        try:
            cmd = f"python {self.tool_paths['infoga']} -d {email}"
            result = self.run_command(cmd)
            results['Infoga'] = result
        except Exception as e:
            results['Infoga'] = {"success": False, "error": str(e)}

        # theHarvester
        try:
            cmd = f"python {self.tool_paths['theharvester']} -d {email}"
            result = self.run_command(cmd)
            results['theHarvester'] = result
        except Exception as e:
            results['theHarvester'] = {"success": False, "error": str(e)}

        # GHunt
        try:
            cmd = f"ghunt email {email}"
            result = self.run_command(cmd)
            results['GHunt'] = result
        except Exception as e:
            results['GHunt'] = {"success": False, "error": str(e)}

        # API-based email lookups
        api_results = await self.email_api_lookups(email)
        results.update(api_results)

        return results

    async def email_api_lookups(self, email):
        """Run API-based email lookups"""
        results = {}
        
        # HaveIBeenPwned
        if self.api_keys.get('hibp'):
            try:
                url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
                headers = {'hibp-api-key': self.api_keys['hibp']}
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers) as response:
                        data = await response.json()
                        results['HaveIBeenPwned'] = {"success": True, "data": data}
            except Exception as e:
                results['HaveIBeenPwned'] = {"success": False, "error": str(e)}

        # EmailRep.io
        if self.api_keys.get('emailrep'):
            try:
                url = f"https://emailrep.io/{email}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        data = await response.json()
                        results['EmailRep'] = {"success": True, "data": data}
            except Exception as e:
                results['EmailRep'] = {"success": False, "error": str(e)}

        # Hunter.io
        if self.api_keys.get('hunter'):
            try:
                url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={self.api_keys['hunter']}"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        data = await response.json()
                        results['Hunter'] = {"success": True, "data": data}
            except Exception as e:
                results['Hunter'] = {"success": False, "error": str(e)}

        return results

    # Image OSINT Methods
    async def image_osint(self, image_data):
        """Run all image OSINT tools"""
        results = {}
        
        # Save image to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(image_data)
            image_path = tmp_file.name

        try:
            # ExifTool
            try:
                cmd = f"{self.tool_paths['exiftool']} {image_path}"
                result = self.run_command(cmd)
                results['ExifTool'] = result
            except Exception as e:
                results['ExifTool'] = {"success": False, "error": str(e)}

            # DeepFace
            try:
                from deepface import DeepFace
                analysis = DeepFace.analyze(image_path, actions=['age', 'gender', 'race', 'emotion'])
                results['DeepFace'] = {"success": True, "data": analysis}
            except Exception as e:
                results['DeepFace'] = {"success": False, "error": str(e)}

            # Search by Image (Google Lens API placeholder)
            try:
                # This would require Google Cloud Vision API
                results['Search_by_Image'] = {"success": False, "error": "Google Cloud Vision API required"}
            except Exception as e:
                results['Search_by_Image'] = {"success": False, "error": str(e)}

            # StegSeek
            try:
                cmd = f"stegseek {image_path}"
                result = self.run_command(cmd)
                results['StegSeek'] = result
            except Exception as e:
                results['StegSeek'] = {"success": False, "error": str(e)}

            # ExifHunter
            try:
                cmd = f"python {self.tool_paths['exifhunter']} {image_path}"
                result = self.run_command(cmd)
                results['ExifHunter'] = result
            except Exception as e:
                results['ExifHunter'] = {"success": False, "error": str(e)}

        finally:
            # Clean up temporary file
            if os.path.exists(image_path):
                os.unlink(image_path)

        return results

    # Video OSINT Methods
    async def video_osint(self, video_data):
        """Run all video OSINT tools"""
        results = {}
        
        # Save video to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(video_data)
            video_path = tmp_file.name

        try:
            # Video-OSINT
            try:
                cmd = f"python video_osint.py {video_path}"
                result = self.run_command(cmd)
                results['Video-OSINT'] = result
            except Exception as e:
                results['Video-OSINT'] = {"success": False, "error": str(e)}

            # InVID Toolkit
            try:
                cmd = f"python invid_toolkit.py {video_path}"
                result = self.run_command(cmd)
                results['InVID_Toolkit'] = result
            except Exception as e:
                results['InVID_Toolkit'] = {"success": False, "error": str(e)}

            # FFmpeg
            try:
                cmd = f"ffmpeg -i {video_path} -f ffmetadata -"
                result = self.run_command(cmd)
                results['FFmpeg'] = result
            except Exception as e:
                results['FFmpeg'] = {"success": False, "error": str(e)}

            # YT-DLP
            try:
                cmd = f"yt-dlp --dump-json {video_path}"
                result = self.run_command(cmd)
                results['YT-DLP'] = result
            except Exception as e:
                results['YT-DLP'] = {"success": False, "error": str(e)}

            # FakeVideoDetector
            try:
                cmd = f"python fake_video_detector.py {video_path}"
                result = self.run_command(cmd)
                results['FakeVideoDetector'] = result
            except Exception as e:
                results['FakeVideoDetector'] = {"success": False, "error": str(e)}

        finally:
            # Clean up temporary file
            if os.path.exists(video_path):
                os.unlink(video_path)

        return results

    # Deepfake Detection Methods
    async def deepfake_detection(self, media_data, media_type='image'):
        """Run all deepfake detection tools"""
        results = {}
        
        # Save media to temporary file
        extension = '.jpg' if media_type == 'image' else '.mp4'
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
            tmp_file.write(media_data)
            media_path = tmp_file.name

        try:
            # Deepware Scanner
            try:
                cmd = f"python deepware_scanner.py {media_path}"
                result = self.run_command(cmd)
                results['Deepware_Scanner'] = result
            except Exception as e:
                results['Deepware_Scanner'] = {"success": False, "error": str(e)}

            # FaceForensics++
            try:
                cmd = f"python faceforensics.py {media_path}"
                result = self.run_command(cmd)
                results['FaceForensics++'] = result
            except Exception as e:
                results['FaceForensics++'] = {"success": False, "error": str(e)}

            # DFDC
            try:
                cmd = f"python dfdc_detector.py {media_path}"
                result = self.run_command(cmd)
                results['DFDC'] = result
            except Exception as e:
                results['DFDC'] = {"success": False, "error": str(e)}

            # MesoNet
            try:
                cmd = f"python mesonet.py {media_path}"
                result = self.run_command(cmd)
                results['MesoNet'] = result
            except Exception as e:
                results['MesoNet'] = {"success": False, "error": str(e)}

            # FakeFinder
            try:
                cmd = f"python fakefinder.py {media_path}"
                result = self.run_command(cmd)
                results['FakeFinder'] = result
            except Exception as e:
                results['FakeFinder'] = {"success": False, "error": str(e)}

        finally:
            # Clean up temporary file
            if os.path.exists(media_path):
                os.unlink(media_path)

        return results

    # Face Detection Methods
    async def face_detection(self, image_data):
        """Run all face detection tools"""
        results = {}
        
        # Save image to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(image_data)
            image_path = tmp_file.name

        try:
            # DeepFace
            try:
                from deepface import DeepFace
                faces = DeepFace.extract_faces(image_path)
                results['DeepFace'] = {"success": True, "data": faces}
            except Exception as e:
                results['DeepFace'] = {"success": False, "error": str(e)}

            # InsightFace
            try:
                import insightface
                app = insightface.app.FaceAnalysis()
                app.prepare(ctx_id=0, det_size=(640, 640))
                faces = app.get(image_path)
                results['InsightFace'] = {"success": True, "data": faces}
            except Exception as e:
                results['InsightFace'] = {"success": False, "error": str(e)}

            # face_recognition
            try:
                import face_recognition
                image = face_recognition.load_image_file(image_path)
                face_locations = face_recognition.face_locations(image)
                face_encodings = face_recognition.face_encodings(image, face_locations)
                results['face_recognition'] = {"success": True, "data": {
                    "locations": face_locations,
                    "encodings": [enc.tolist() for enc in face_encodings]
                }}
            except Exception as e:
                results['face_recognition'] = {"success": False, "error": str(e)}

            # MTCNN
            try:
                from mtcnn import MTCNN
                detector = MTCNN()
                faces = detector.detect_faces(image_path)
                results['MTCNN'] = {"success": True, "data": faces}
            except Exception as e:
                results['MTCNN'] = {"success": False, "error": str(e)}

            # RetinaFace
            try:
                from retinaface import RetinaFace
                faces = RetinaFace.detect_faces(image_path)
                results['RetinaFace'] = {"success": True, "data": faces}
            except Exception as e:
                results['RetinaFace'] = {"success": False, "error": str(e)}

        finally:
            # Clean up temporary file
            if os.path.exists(image_path):
                os.unlink(image_path)

        return results

    # Website OSINT Methods
    async def website_osint(self, domain):
        """Run all website OSINT tools"""
        results = {}
        
        # Sublist3r
        try:
            cmd = f"python {self.tool_paths['sublist3r']} -d {domain}"
            result = self.run_command(cmd)
            results['Sublist3r'] = result
        except Exception as e:
            results['Sublist3r'] = {"success": False, "error": str(e)}

        # theHarvester
        try:
            cmd = f"python {self.tool_paths['theharvester']} -d {domain}"
            result = self.run_command(cmd)
            results['theHarvester'] = result
        except Exception as e:
            results['theHarvester'] = {"success": False, "error": str(e)}

        # Amass
        try:
            cmd = f"{self.tool_paths['amass']} enum -d {domain}"
            result = self.run_command(cmd)
            results['Amass'] = result
        except Exception as e:
            results['Amass'] = {"success": False, "error": str(e)}

        # Photon
        try:
            cmd = f"python {self.tool_paths['photon']} -u https://{domain}"
            result = self.run_command(cmd)
            results['Photon'] = result
        except Exception as e:
            results['Photon'] = {"success": False, "error": str(e)}

        # WhatWeb
        try:
            cmd = f"{self.tool_paths['whatweb']} {domain}"
            result = self.run_command(cmd)
            results['WhatWeb'] = result
        except Exception as e:
            results['WhatWeb'] = {"success": False, "error": str(e)}

        return results

    # Social Media OSINT Methods
    async def social_media_osint(self, username):
        """Run all social media OSINT tools"""
        results = {}
        
        # Maigret
        try:
            cmd = f"maigret {username}"
            result = self.run_command(cmd)
            results['Maigret'] = result
        except Exception as e:
            results['Maigret'] = {"success": False, "error": str(e)}

        # Sherlock
        try:
            cmd = f"python {self.tool_paths['sherlock']} {username}"
            result = self.run_command(cmd)
            results['Sherlock'] = result
        except Exception as e:
            results['Sherlock'] = {"success": False, "error": str(e)}

        # Social Analyzer
        try:
            cmd = f"social-analyzer --username {username}"
            result = self.run_command(cmd)
            results['Social_Analyzer'] = result
        except Exception as e:
            results['Social_Analyzer'] = {"success": False, "error": str(e)}

        # Osintgram
        try:
            cmd = f"osintgram {username}"
            result = self.run_command(cmd)
            results['Osintgram'] = result
        except Exception as e:
            results['Osintgram'] = {"success": False, "error": str(e)}

        # Twint
        try:
            cmd = f"twint -u {username}"
            result = self.run_command(cmd)
            results['Twint'] = result
        except Exception as e:
            results['Twint'] = {"success": False, "error": str(e)}

        return results

# Initialize the OSINT tool manager
osint_manager = OSINTToolManager()

@app.route('/')
def index():
    """Serve the main OSINT application"""
    return render_template('osint_app.html')

@app.route('/api/status')
def get_status():
    """Get the status of all tools and API keys"""
    status = {
        'tools': {},
        'api_keys': {},
        'timestamp': datetime.now().isoformat()
    }
    
    # Check tool availability
    for tool_name, tool_path in osint_manager.tool_paths.items():
        status['tools'][tool_name] = os.path.exists(tool_path)
    
    # Check API key availability
    for api_name, api_key in osint_manager.api_keys.items():
        status['api_keys'][api_name] = api_key is not None
    
    return jsonify(status)

@app.route('/api/phone', methods=['POST'])
async def phone_osint_endpoint():
    """Phone number OSINT endpoint"""
    data = request.get_json()
    phone_number = data.get('phone_number')
    
    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400
    
    # Run all phone OSINT tools
    results = await osint_manager.phone_osint(phone_number)
    
    # Get AI analysis
    ai_analysis = await osint_manager.call_ai_api('openai', 
        f"Analyze this phone number OSINT data for {phone_number}. Provide insights, patterns, and recommendations.", 
        results)
    
    return jsonify({
        "phone_number": phone_number,
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/email', methods=['POST'])
async def email_osint_endpoint():
    """Email OSINT endpoint"""
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    # Run all email OSINT tools
    results = await osint_manager.email_osint(email)
    
    # Get AI analysis
    ai_analysis = await osint_manager.call_ai_api('openai', 
        f"Analyze this email OSINT data for {email}. Provide insights, patterns, and recommendations.", 
        results)
    
    return jsonify({
        "email": email,
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/image', methods=['POST'])
async def image_osint_endpoint():
    """Image OSINT endpoint"""
    if 'image' not in request.files:
        return jsonify({"error": "Image file is required"}), 400
    
    image_file = request.files['image']
    image_data = image_file.read()
    
    # Run all image OSINT tools
    results = await osint_manager.image_osint(image_data)
    
    # Get AI analysis
    ai_analysis = await osint_manager.call_ai_api('openai', 
        "Analyze this image OSINT data. Provide insights about metadata, faces, and any hidden information.", 
        results)
    
    return jsonify({
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/video', methods=['POST'])
async def video_osint_endpoint():
    """Video OSINT endpoint"""
    if 'video' not in request.files:
        return jsonify({"error": "Video file is required"}), 400
    
    video_file = request.files['video']
    video_data = video_file.read()
    
    # Run all video OSINT tools
    results = await osint_manager.video_osint(video_data)
    
    # Get AI analysis
    ai_analysis = await osint_manager.call_ai_api('openai', 
        "Analyze this video OSINT data. Provide insights about metadata, content, and any suspicious patterns.", 
        results)
    
    return jsonify({
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/deepfake', methods=['POST'])
async def deepfake_detection_endpoint():
    """Deepfake detection endpoint"""
    if 'media' not in request.files:
        return jsonify({"error": "Media file is required"}), 400
    
    media_file = request.files['media']
    media_data = media_file.read()
    media_type = request.form.get('media_type', 'image')
    
    # Run all deepfake detection tools
    results = await osint_manager.deepfake_detection(media_data, media_type)
    
    # Get AI analysis
    ai_analysis = await osint_manager.call_ai_api('openai', 
        "Analyze this deepfake detection data. Provide insights about the likelihood of manipulation and key indicators.", 
        results)
    
    return jsonify({
        "media_type": media_type,
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/face', methods=['POST'])
async def face_detection_endpoint():
    """Face detection endpoint"""
    if 'image' not in request.files:
        return jsonify({"error": "Image file is required"}), 400
    
    image_file = request.files['image']
    image_data = image_file.read()
    
    # Run all face detection tools
    results = await osint_manager.face_detection(image_data)
    
    # Get AI analysis
    ai_analysis = await osint_manager.call_ai_api('openai', 
        "Analyze this face detection data. Provide insights about detected faces, features, and any notable characteristics.", 
        results)
    
    return jsonify({
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/website', methods=['POST'])
async def website_osint_endpoint():
    """Website OSINT endpoint"""
    data = request.get_json()
    domain = data.get('domain')
    
    if not domain:
        return jsonify({"error": "Domain is required"}), 400
    
    # Run all website OSINT tools
    results = await osint_manager.website_osint(domain)
    
    # Get AI analysis
    ai_analysis = await osint_manager.call_ai_api('openai', 
        f"Analyze this website OSINT data for {domain}. Provide insights about subdomains, technologies, and potential vulnerabilities.", 
        results)
    
    return jsonify({
        "domain": domain,
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/social', methods=['POST'])
async def social_media_osint_endpoint():
    """Social media OSINT endpoint"""
    data = request.get_json()
    username = data.get('username')
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    # Run all social media OSINT tools
    results = await osint_manager.social_media_osint(username)
    
    # Get AI analysis
    ai_analysis = await osint_manager.call_ai_api('openai', 
        f"Analyze this social media OSINT data for {username}. Provide insights about online presence, patterns, and potential risks.", 
        results)
    
    return jsonify({
        "username": username,
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/ai/analyze', methods=['POST'])
async def ai_analysis_endpoint():
    """AI analysis endpoint"""
    data = request.get_json()
    provider = data.get('provider', 'openai')
    prompt = data.get('prompt')
    results = data.get('results')
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    # Get AI analysis
    ai_analysis = await osint_manager.call_ai_api(provider, prompt, results)
    
    return jsonify({
        "provider": provider,
        "analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
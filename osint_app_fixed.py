#!/usr/bin/env python3
"""
Powerful OSINT Web Application
Integrates top 5 tools for each category + AI analysis
"""

import os
import json
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
import numpy as np

app = Flask(__name__)
CORS(app)

class OSINTToolManager:
    def __init__(self):
        self.api_keys = {
            'openai': os.getenv('OPENAI_API_KEY', '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'),
            'gemini': os.getenv('GEMINI_API_KEY', 'AIzaSyAVNUUu6pPVIoBn2GnxaO1Vddo4znZAXvA'),
            'grok': os.getenv('GROK_API_KEY'),
            'numverify': os.getenv('NUMVERIFY_API_KEY', 'b377e38280c77532e15bb7741f6e9bb8'),
            'twilio': os.getenv('TWILIO_API_KEY'),
            'hibp': os.getenv('HIBP_API_KEY'),
            'emailrep': os.getenv('EMAILREP_API_KEY'),
            'hunter': os.getenv('HUNTER_API_KEY'),
            'intelx': os.getenv('INTELX_API_KEY'),
            'epieos': os.getenv('EPIEOS_API_KEY'),
            'shodan': os.getenv('SHODAN_API_KEY', 'a72Q4g76UyurRjlrLp2O8eVkPvGfpheB')
        }

    def call_ai_api(self, provider, prompt, results=None):
        """Call AI APIs (ChatGPT, Gemini, Grok) for analysis"""
        if not self.api_keys.get(provider):
            return {"error": f"{provider.upper()} API key not configured"}
        
        try:
            if provider == 'openai':
                return self._call_openai(prompt, results)
            elif provider == 'gemini':
                return self._call_gemini(prompt, results)
            elif provider == 'grok':
                return self._call_grok(prompt, results)
        except Exception as e:
            return {"error": f"AI API error: {str(e)}"}

    def _call_openai(self, prompt, results=None):
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
        
        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', 
                                  headers=headers, json=data)
            result = response.json()
            return {"analysis": result.get('choices', [{}])[0].get('message', {}).get('content', 'No response')}
        except Exception as e:
            return {"error": f"OpenAI API error: {str(e)}"}

    def _call_gemini(self, prompt, results=None):
        """Call Google Gemini API"""
        headers = {
            'Content-Type': 'application/json'
        }
        
        content = f"{prompt}\n\nOSINT Results:\n{json.dumps(results, indent=2) if results else 'No results available'}"
        
        data = {
            "contents": [{"parts": [{"text": content}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000
            }
        }
        
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={self.api_keys['gemini']}"
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            
            # Debug: Print the response to see what we're getting
            print(f"Gemini API Response: {result}")
            
            if 'candidates' in result and result['candidates']:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    if parts and 'text' in parts[0]:
                        return {"analysis": parts[0]['text']}
            
            # If we can't parse the response properly, return the raw response
            return {"analysis": f"Gemini Response: {str(result)}"}
        except Exception as e:
            return {"error": f"Gemini API error: {str(e)}"}

    def _call_grok(self, prompt, results=None):
        """Call Grok API (placeholder - replace with actual Grok API)"""
        # Note: Grok API is not publicly available yet, this is a placeholder
        return {"analysis": "Grok analysis placeholder - API not publicly available"}

    def run_command(self, command, timeout=30):
        """Run a command with timeout and error handling"""
        try:
            import subprocess
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
    def phone_osint(self, phone_number):
        """Run all phone number OSINT tools"""
        results = {}
        
        # Phone number validation
        import re
        phone_regex = re.compile(r'^[\+]?[1-9][\d]{0,15}$')
        cleaned_number = phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        match_result = phone_regex.match(cleaned_number)
        results['Phone_Validation'] = {
            "success": True,
            "data": {
                "valid": match_result is not None,
                "format": phone_number,
                "country_code": phone_number[1:3] if phone_number.startswith('+') else 'Unknown'
            }
        }
        
        # Investigation links for phone number
        results['Investigation_Links'] = {
            "success": True,
            "data": {
                "links": [
                    {"name": "Truecaller", "url": f"https://www.truecaller.com/search/{phone_number}"},
                    {"name": "NumLookup", "url": f"https://numlookupapi.com/{phone_number}"},
                    {"name": "PhoneInfoga", "url": f"https://github.com/sundowndev/phoneinfoga"},
                    {"name": "OSINT Framework", "url": "https://osintframework.com/"},
                    {"name": "SpyDialer", "url": f"https://spydialer.com/{phone_number}"},
                    {"name": "Whitepages", "url": f"https://www.whitepages.com/phone/{phone_number}"}
                ]
            }
        }

        # NumVerify API lookup
        try:
            if self.api_keys.get('numverify'):
                response = requests.get(f"http://apilayer.net/api/validate?access_key={self.api_keys['numverify']}&number={phone_number}")
                if response.status_code == 200:
                    data = response.json()
                    if data.get('valid'):
                        results['NumLookup'] = {
                            "success": True, 
                            "data": {
                                "valid": data.get('valid'),
                                "number": data.get('number'),
                                "local_format": data.get('local_format'),
                                "international_format": data.get('international_format'),
                                "country_prefix": data.get('country_prefix'),
                                "country_code": data.get('country_code'),
                                "country_name": data.get('country_name'),
                                "location": data.get('location'),
                                "carrier": data.get('carrier'),
                                "line_type": data.get('line_type')
                            }
                        }
                    else:
                        results['NumLookup'] = {"success": False, "error": "Invalid phone number"}
                else:
                    results['NumLookup'] = {"success": False, "error": f"API error: {response.status_code}"}
            else:
                results['NumLookup'] = {"success": False, "error": "NumVerify API key not configured"}
        except Exception as e:
            results['NumLookup'] = {"success": False, "error": str(e)}

        return results

    # Email OSINT Methods
    def email_osint(self, email):
        """Run all email OSINT tools"""
        results = {}
        
        # Email validation
        import re
        email_regex = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')
        match_result = email_regex.match(email)
        results['Email_Validation'] = {
            "success": True,
            "data": {
                "valid": match_result is not None,
                "domain": email.split('@')[1] if '@' in email else None,
                "username": email.split('@')[0] if '@' in email else None
            }
        }
        
        # Investigation links for email
        results['Investigation_Links'] = {
            "success": True,
            "data": {
                "links": [
                    {"name": "HaveIBeenPwned", "url": f"https://haveibeenpwned.com/unifiedsearch/{email}"},
                    {"name": "EmailRep.io", "url": f"https://emailrep.io/{email}"},
                    {"name": "Holehe", "url": "https://github.com/megadose/holehe"},
                    {"name": "H8mail", "url": "https://github.com/khast3x/h8mail"},
                    {"name": "Hunt", "url": "https://hunt.io/"},
                    {"name": "BreachDirectory", "url": "https://breachdirectory.p.rapidapi.com/"}
                ]
            }
        }

        # Free email API
        try:
            response = requests.get(f"https://emailrep.io/{email}")
            if response.status_code == 200:
                results['EmailRep'] = {"success": True, "data": response.json()}
            else:
                results['EmailRep'] = {"success": False, "error": "API unavailable"}
        except Exception as e:
            results['EmailRep'] = {"success": False, "error": str(e)}

        return results

    # Image OSINT Methods
    def image_osint(self, image_data):
        """Run all image OSINT tools"""
        results = {}
        
        # Save image to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(image_data)
            image_path = tmp_file.name

        try:
            # Basic image analysis
            try:
                with Image.open(image_path) as img:
                    results['Image_Analysis'] = {
                        "success": True,
                        "data": {
                            "format": img.format,
                            "mode": img.mode,
                            "size": img.size,
                            "width": img.width,
                            "height": img.height
                        }
                    }
            except Exception as e:
                results['Image_Analysis'] = {"success": False, "error": str(e)}

            # EXIF data (basic)
            try:
                with Image.open(image_path) as img:
                    exif_data = img.getexif()
                    if exif_data:
                        # Convert EXIF data to JSON-serializable format
                        exif_dict = {}
                        for tag_id, value in exif_data.items():
                            try:
                                # Convert rational numbers and other non-serializable types
                                if hasattr(value, 'numerator') and hasattr(value, 'denominator'):
                                    exif_dict[str(tag_id)] = float(value.numerator) / float(value.denominator)
                                else:
                                    exif_dict[str(tag_id)] = str(value)
                            except:
                                exif_dict[str(tag_id)] = str(value)
                        results['EXIF_Data'] = {"success": True, "data": exif_dict}
                    else:
                        results['EXIF_Data'] = {"success": True, "data": {"message": "No EXIF data found"}}
            except Exception as e:
                results['EXIF_Data'] = {"success": False, "error": str(e)}

        finally:
            # Clean up temporary file
            if os.path.exists(image_path):
                os.unlink(image_path)

        return results

    # Website OSINT Methods
    def website_osint(self, domain):
        """Run all website OSINT tools"""
        results = {}
        
        # Domain validation
        import re
        domain_regex = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$')
        match_result = domain_regex.match(domain)
        results['Domain_Validation'] = {
            "success": True,
            "data": {
                "valid": match_result is not None,
                "domain": domain
            }
        }
        
        # Investigation links for domain
        results['Investigation_Links'] = {
            "success": True,
            "data": {
                "links": [
                    {"name": "Sublist3r", "url": "https://github.com/aboul3la/Sublist3r"},
                    {"name": "Amass", "url": "https://github.com/owasp-amass/amass"},
                    {"name": "BuiltWith", "url": f"https://builtwith.com/{domain}"},
                    {"name": "Wappalyzer", "url": f"https://www.wappalyzer.com/lookup/{domain}"},
                    {"name": "SecurityTrails", "url": f"https://securitytrails.com/app/domain/{domain}"},
                    {"name": "ViewDNS", "url": f"https://viewdns.info/reverseip/?host={domain}"},
                    {"name": "DNSDumpster", "url": "https://dnsdumpster.com/"},
                    {"name": "Censys", "url": "https://censys.io/"}
                ]
            }
        }

        # Basic DNS lookup simulation
        results['DNS_Lookup'] = {
            "success": True,
            "data": {
                "message": "DNS lookup would require additional libraries",
                "domain": domain
            }
        }
        
        # Shodan search for domain
        try:
            if self.api_keys.get('shodan'):
                # Search for the domain in Shodan
                shodan_url = f"https://api.shodan.io/shodan/host/search?key={self.api_keys['shodan']}&query=hostname:{domain}"
                response = requests.get(shodan_url)
                
                if response.status_code == 200:
                    shodan_data = response.json()
                    results['Shodan_Search'] = {
                        "success": True,
                        "data": {
                            "total_results": shodan_data.get('total', 0),
                            "matches": shodan_data.get('matches', []),
                            "message": f"Found {shodan_data.get('total', 0)} Shodan results for {domain}"
                        }
                    }
                elif response.status_code == 403:
                    # Free plan limitation
                    results['Shodan_Search'] = {
                        "success": False,
                        "error": "Shodan search requires paid membership. Free plan has limited access.",
                        "upgrade_info": {
                            "current_plan": "oss (Open Source Software)",
                            "recommendation": "Upgrade to Membership or Professional plan for full search access",
                            "alternative": "Use Shodan web interface for manual searches"
                        }
                    }
                else:
                    results['Shodan_Search'] = {
                        "success": False,
                        "error": f"Shodan API error: {response.status_code} - {response.text}"
                    }
            else:
                results['Shodan_Search'] = {
                    "success": False,
                    "error": "Shodan API key not configured"
                }
        except Exception as e:
            results['Shodan_Search'] = {
                "success": False,
                "error": f"Shodan search failed: {str(e)}"
            }

        return results

    # Social Media OSINT Methods
    def social_media_osint(self, username):
        """Run all social media OSINT tools"""
        results = {}
        
        # Username validation
        import re
        username_regex = re.compile(r'^[a-zA-Z0-9_]{3,20}$')
        match_result = username_regex.match(username)
        results['Username_Validation'] = {
            "success": True,
            "data": {
                "valid": match_result is not None,
                "username": username
            }
        }
        
        # Investigation links for username
        results['Investigation_Links'] = {
            "success": True,
            "data": {
                "links": [
                    {"name": "Maigret", "url": "https://github.com/soxoj/maigret"},
                    {"name": "Sherlock", "url": "https://github.com/sherlock-project/sherlock"},
                    {"name": "WhatsMyName", "url": "https://whatsmyname.app/"},
                    {"name": "NameChk", "url": "https://namechk.com/"},
                    {"name": "CheckUsernames", "url": "https://checkusernames.com/"},
                    {"name": "KnowEm", "url": "https://knowem.com/"},
                    {"name": "UserSearch", "url": "https://usersearch.org/"},
                    {"name": "Social Searcher", "url": "https://www.social-searcher.com/"}
                ]
            }
        }

        # Social media platforms to check
        platforms = ['twitter', 'instagram', 'facebook', 'linkedin', 'github']
        results['Platform_Check'] = {
            "success": True,
            "data": {
                "message": "Manual checking required for each platform",
                "platforms": platforms
            }
        }

        return results

    # Video OSINT Methods
    def video_osint(self, video_data):
        """Run all video OSINT tools"""
        results = {}
        
        # Save video to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            tmp_file.write(video_data)
            video_path = tmp_file.name

        try:
            # Advanced video analysis with OpenCV
            try:
                import cv2
                import moviepy
                from moviepy import VideoFileClip
                
                print(f"OpenCV version: {cv2.__version__}")
                print(f"MoviePy version: {moviepy.__version__}")
                
                # Basic video analysis
                results['Video_Analysis'] = {
                    "success": True,
                    "data": {
                        "size_bytes": len(video_data),
                        "size_mb": round(len(video_data) / (1024 * 1024), 2),
                        "message": "Advanced video analysis enabled with OpenCV"
                    }
                }

                # Video metadata extraction
                try:
                    clip = VideoFileClip(video_path)
                    results['Video_Metadata'] = {
                        "success": True,
                        "data": {
                            "duration_seconds": round(clip.duration, 2),
                            "fps": clip.fps,
                            "size": clip.size,
                            "width": clip.w,
                            "height": clip.h,
                            "audio": clip.audio is not None,
                            "message": "Video metadata extracted successfully"
                        }
                    }
                    clip.close()
                except Exception as e:
                    results['Video_Metadata'] = {
                        "success": False,
                        "error": f"Metadata extraction failed: {str(e)}"
                    }

                # Frame analysis
                try:
                    cap = cv2.VideoCapture(video_path)
                    if cap.isOpened():
                        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                        fps = cap.get(cv2.CAP_PROP_FPS)
                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        
                        # Sample frames for analysis
                        frame_count = 0
                        sample_frames = []
                        
                        while cap.isOpened() and frame_count < 10:  # Sample first 10 frames
                            ret, frame = cap.read()
                            if not ret:
                                break
                            
                            if frame_count % 3 == 0:  # Sample every 3rd frame
                                # Convert to grayscale for analysis
                                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                                
                                # Basic frame analysis
                                brightness = np.mean(gray)
                                contrast = np.std(gray)
                                
                                sample_frames.append({
                                    "frame_number": frame_count,
                                    "brightness": round(brightness, 2),
                                    "contrast": round(contrast, 2),
                                    "size": frame.shape
                                })
                            
                            frame_count += 1
                        
                        cap.release()
                        
                        results['Frame_Analysis'] = {
                            "success": True,
                            "data": {
                                "total_frames": total_frames,
                                "fps": fps,
                                "resolution": f"{width}x{height}",
                                "sample_frames": sample_frames,
                                "message": f"Analyzed {len(sample_frames)} sample frames"
                            }
                        }
                    else:
                        results['Frame_Analysis'] = {
                            "success": False,
                            "error": "Could not open video file"
                        }
                except Exception as e:
                    results['Frame_Analysis'] = {
                        "success": False,
                        "error": f"Frame analysis failed: {str(e)}"
                    }

                # Motion detection (basic)
                try:
                    cap = cv2.VideoCapture(video_path)
                    if cap.isOpened():
                        motion_detected = False
                        motion_frames = 0
                        
                        ret, prev_frame = cap.read()
                        if ret:
                            prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
                            
                            while cap.isOpened():
                                ret, frame = cap.read()
                                if not ret:
                                    break
                                
                                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                                
                                # Calculate frame difference
                                frame_diff = cv2.absdiff(prev_gray, gray)
                                motion_score = np.mean(frame_diff)
                                
                                if motion_score > 10:  # Threshold for motion detection
                                    motion_detected = True
                                    motion_frames += 1
                                
                                prev_gray = gray
                            
                            cap.release()
                            
                            results['Motion_Detection'] = {
                                "success": True,
                                "data": {
                                    "motion_detected": motion_detected,
                                    "motion_frames": motion_frames,
                                    "message": "Motion analysis completed"
                                }
                            }
                        else:
                            results['Motion_Detection'] = {
                                "success": False,
                                "error": "Could not read video frames"
                            }
                    else:
                        results['Motion_Detection'] = {
                            "success": False,
                            "error": "Could not open video file"
                        }
                except Exception as e:
                    results['Motion_Detection'] = {
                        "success": False,
                        "error": f"Motion detection failed: {str(e)}"
                    }

            except ImportError as e:
                # Fallback if OpenCV is not available
                print(f"ImportError: {e}")
                results['Video_Analysis'] = {
                    "success": True,
                    "data": {
                        "message": "OpenCV not available - basic analysis only",
                        "size_bytes": len(video_data),
                        "size_mb": round(len(video_data) / (1024 * 1024), 2)
                    }
                }
                
                results['Video_Metadata'] = {
                    "success": True,
                    "data": {
                        "message": "Advanced metadata extraction requires OpenCV",
                        "file_size": f"{len(video_data)} bytes"
                    }
                }
            except Exception as e:
                # Fallback for any other error
                print(f"Video analysis error: {e}")
                results['Video_Analysis'] = {
                    "success": True,
                    "data": {
                        "message": f"Video analysis error: {str(e)}",
                        "size_bytes": len(video_data),
                        "size_mb": round(len(video_data) / (1024 * 1024), 2)
                    }
                }
                
                results['Video_Metadata'] = {
                    "success": True,
                    "data": {
                        "message": f"Metadata extraction error: {str(e)}",
                        "file_size": f"{len(video_data)} bytes"
                    }
                }

        finally:
            # Clean up temporary file
            if os.path.exists(video_path):
                os.unlink(video_path)

        return results

    # Deepfake Detection Methods
    def deepfake_detection(self, media_data, media_type='image'):
        """Run deepfake detection on media"""
        results = {}
        
        # Save media to temporary file
        extension = '.jpg' if media_type == 'image' else '.mp4'
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp_file:
            tmp_file.write(media_data)
            media_path = tmp_file.name

        try:
            # Basic deepfake detection simulation
            results['Deepfake_Detection'] = {
                "success": True,
                "data": {
                    "message": f"Deepfake detection for {media_type} would require specialized AI models",
                    "media_type": media_type,
                    "file_size": f"{len(media_data)} bytes",
                    "analysis_available": False
                }
            }

            # Media analysis
            results['Media_Analysis'] = {
                "success": True,
                "data": {
                    "format": media_type,
                    "size_bytes": len(media_data),
                    "size_mb": round(len(media_data) / (1024 * 1024), 2)
                }
            }

        finally:
            # Clean up temporary file
            if os.path.exists(media_path):
                os.unlink(media_path)

        return results

    # Face Detection Methods
    def face_detection(self, image_data):
        """Run face detection on image"""
        results = {}
        
        # Save image to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            tmp_file.write(image_data)
            image_path = tmp_file.name

        try:
            # Basic image analysis
            try:
                with Image.open(image_path) as img:
                    results['Image_Analysis'] = {
                        "success": True,
                        "data": {
                            "format": img.format,
                            "mode": img.mode,
                            "size": img.size,
                            "width": img.width,
                            "height": img.height
                        }
                    }
            except Exception as e:
                results['Image_Analysis'] = {"success": False, "error": str(e)}

            # Face detection simulation
            results['Face_Detection'] = {
                "success": True,
                "data": {
                    "message": "Face detection would require OpenCV or similar libraries",
                    "faces_detected": "Unknown",
                    "confidence": "Unknown"
                }
            }

        finally:
            # Clean up temporary file
            if os.path.exists(image_path):
                os.unlink(image_path)

        return results

    # IP Address OSINT Methods
    def ip_osint(self, ip_address):
        """Run all IP address OSINT tools"""
        results = {}
        
        # IP validation
        import re
        ip_regex = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
        match_result = ip_regex.match(ip_address)
        results['IP_Validation'] = {
            "success": True,
            "data": {
                "valid": match_result is not None,
                "ip": ip_address
            }
        }
        
        # Investigation links for IP address
        results['Investigation_Links'] = {
            "success": True,
            "data": {
                "links": [
                    {"name": "AbuseIPDB", "url": f"https://www.abuseipdb.com/check/{ip_address}"},
                    {"name": "VirusTotal", "url": f"https://www.virustotal.com/gui/ip-address/{ip_address}"},
                    {"name": "IPVoid", "url": f"https://www.ipvoid.com/ip-blacklist-check/{ip_address}"},
                    {"name": "IPQualityScore", "url": f"https://www.ipqualityscore.com/free-ip-lookup-proxy-vpn-test/lookup/{ip_address}"},
                    {"name": "IP2Location", "url": f"https://www.ip2location.com/demo/{ip_address}"},
                    {"name": "MaxMind", "url": "https://www.maxmind.com/en/geoip2-demo"},
                    {"name": "Shodan", "url": f"https://www.shodan.io/host/{ip_address}"},
                    {"name": "Censys", "url": f"https://censys.io/ipv4/{ip_address}"}
                ]
            }
        }

        # Free IP geolocation API
        try:
            response = requests.get(f"https://ipapi.co/{ip_address}/json/")
            if response.status_code == 200:
                results['IP_Geolocation'] = {"success": True, "data": response.json()}
            else:
                results['IP_Geolocation'] = {"success": False, "error": "API unavailable"}
        except Exception as e:
            results['IP_Geolocation'] = {"success": False, "error": str(e)}
        
        # Shodan search for IP address
        try:
            if self.api_keys.get('shodan'):
                # Search for the IP in Shodan
                shodan_url = f"https://api.shodan.io/shodan/host/{ip_address}?key={self.api_keys['shodan']}"
                response = requests.get(shodan_url)
                
                if response.status_code == 200:
                    shodan_data = response.json()
                    results['Shodan_IP_Search'] = {
                        "success": True,
                        "data": {
                            "ip": shodan_data.get('ip_str'),
                            "ports": shodan_data.get('ports', []),
                            "hostnames": shodan_data.get('hostnames', []),
                            "country_name": shodan_data.get('country_name'),
                            "city": shodan_data.get('city'),
                            "org": shodan_data.get('org'),
                            "os": shodan_data.get('os'),
                            "data": shodan_data.get('data', []),
                            "message": f"Shodan data found for IP {ip_address}"
                        }
                    }
                elif response.status_code == 403:
                    # Free plan limitation
                    results['Shodan_IP_Search'] = {
                        "success": False,
                        "error": "Shodan search requires paid membership. Free plan has limited access.",
                        "upgrade_info": {
                            "current_plan": "oss (Open Source Software)",
                            "recommendation": "Upgrade to Membership or Professional plan for full search access",
                            "alternative": "Use Shodan web interface for manual searches"
                        }
                    }
                else:
                    results['Shodan_IP_Search'] = {
                        "success": False,
                        "error": f"Shodan API error: {response.status_code} - {response.text}"
                    }
            else:
                results['Shodan_IP_Search'] = {
                    "success": False,
                    "error": "Shodan API key not configured"
                }
        except Exception as e:
            results['Shodan_IP_Search'] = {
                "success": False,
                "error": f"Shodan IP search failed: {str(e)}"
            }

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
    
    # Check API key availability
    for api_name, api_key in osint_manager.api_keys.items():
        status['api_keys'][api_name] = api_key is not None
    
    return jsonify(status)

@app.route('/api/phone', methods=['POST'])
def phone_osint_endpoint():
    """Phone number OSINT endpoint"""
    data = request.get_json()
    phone_number = data.get('phone_number')
    
    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400
    
    # Run all phone OSINT tools
    results = osint_manager.phone_osint(phone_number)
    
    # Get AI analysis
    ai_analysis = osint_manager.call_ai_api('gemini', 
        f"Analyze this phone number OSINT data for {phone_number}. Provide insights, patterns, and recommendations.", 
        results)
    
    return jsonify({
        "phone_number": phone_number,
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/download/<analysis_type>', methods=['POST'])
def download_results(analysis_type):
    """Download OSINT results as JSON file"""
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"osint_{analysis_type}_{timestamp}.json"
    
    # Create response with JSON file
    response = jsonify(data)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "application/json"
    
    return response

@app.route('/api/email', methods=['POST'])
def email_osint_endpoint():
    """Email OSINT endpoint"""
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    # Run all email OSINT tools
    results = osint_manager.email_osint(email)
    
    # Get AI analysis
    ai_analysis = osint_manager.call_ai_api('openai', 
        f"Analyze this email OSINT data for {email}. Provide insights, patterns, and recommendations.", 
        results)
    
    return jsonify({
        "email": email,
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/image', methods=['POST'])
def image_osint_endpoint():
    """Image OSINT endpoint"""
    if 'image' not in request.files:
        return jsonify({"error": "Image file is required"}), 400
    
    image_file = request.files['image']
    image_data = image_file.read()
    
    # Run all image OSINT tools
    results = osint_manager.image_osint(image_data)
    
    # Get AI analysis
    ai_analysis = osint_manager.call_ai_api('openai', 
        "Analyze this image OSINT data. Provide insights about metadata, faces, and any hidden information.", 
        results)
    
    return jsonify({
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/website', methods=['POST'])
def website_osint_endpoint():
    """Website OSINT endpoint"""
    data = request.get_json()
    domain = data.get('domain')
    
    if not domain:
        return jsonify({"error": "Domain is required"}), 400
    
    # Run all website OSINT tools
    results = osint_manager.website_osint(domain)
    
    # Get AI analysis
    ai_analysis = osint_manager.call_ai_api('openai', 
        f"Analyze this website OSINT data for {domain}. Provide insights about subdomains, technologies, and potential vulnerabilities.", 
        results)
    
    return jsonify({
        "domain": domain,
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/social', methods=['POST'])
def social_media_osint_endpoint():
    """Social media OSINT endpoint"""
    data = request.get_json()
    username = data.get('username')
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    # Run all social media OSINT tools
    results = osint_manager.social_media_osint(username)
    
    # Get AI analysis
    ai_analysis = osint_manager.call_ai_api('openai', 
        f"Analyze this social media OSINT data for {username}. Provide insights about online presence, patterns, and potential risks.", 
        results)
    
    return jsonify({
        "username": username,
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/ip', methods=['POST'])
def ip_osint_endpoint():
    """IP address OSINT endpoint"""
    data = request.get_json()
    ip_address = data.get('ip_address')
    
    if not ip_address:
        return jsonify({"error": "IP address is required"}), 400
    
    # Run all IP OSINT tools
    results = osint_manager.ip_osint(ip_address)
    
    # Get AI analysis
    ai_analysis = osint_manager.call_ai_api('openai', 
        f"Analyze this IP address OSINT data for {ip_address}. Provide insights about geolocation, ISP, and potential risks.", 
        results)
    
    return jsonify({
        "ip_address": ip_address,
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/video', methods=['POST'])
def video_osint_endpoint():
    """Video OSINT endpoint"""
    if 'video' not in request.files:
        return jsonify({"error": "Video file is required"}), 400
    
    video_file = request.files['video']
    video_data = video_file.read()
    
    # Run all video OSINT tools
    results = osint_manager.video_osint(video_data)
    
    # Get AI analysis
    ai_analysis = osint_manager.call_ai_api('openai', 
        "Analyze this video OSINT data. Provide insights about metadata, content, and any hidden information.", 
        results)
    
    return jsonify({
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/deepfake', methods=['POST'])
def deepfake_detection_endpoint():
    """Deepfake detection endpoint"""
    if 'media' not in request.files:
        return jsonify({"error": "Media file is required"}), 400
    
    media_file = request.files['media']
    media_data = media_file.read()
    media_type = request.form.get('media_type', 'image')
    
    # Run deepfake detection
    results = osint_manager.deepfake_detection(media_data, media_type)
    
    # Get AI analysis
    ai_analysis = osint_manager.call_ai_api('openai', 
        f"Analyze this {media_type} for deepfake detection. Provide insights about authenticity and potential manipulation.", 
        results)
    
    return jsonify({
        "media_type": media_type,
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/face', methods=['POST'])
def face_detection_endpoint():
    """Face detection endpoint"""
    if 'image' not in request.files:
        return jsonify({"error": "Image file is required"}), 400
    
    image_file = request.files['image']
    image_data = image_file.read()
    
    # Run face detection
    results = osint_manager.face_detection(image_data)
    
    # Get AI analysis
    ai_analysis = osint_manager.call_ai_api('openai', 
        "Analyze this image for face detection. Provide insights about faces, expressions, and potential identification.", 
        results)
    
    return jsonify({
        "results": results,
        "ai_analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/shodan', methods=['POST'])
def shodan_search_endpoint():
    """Shodan search endpoint"""
    data = request.get_json()
    query = data.get('query')
    search_type = data.get('type', 'host')  # host, domain, or general
    
    if not query:
        return jsonify({"error": "Search query is required"}), 400
    
    if not osint_manager.api_keys.get('shodan'):
        return jsonify({"error": "Shodan API key not configured"}), 400
    
    try:
        if search_type == 'host':
            # Search for specific host/IP
            url = f"https://api.shodan.io/shodan/host/{query}?key={osint_manager.api_keys['shodan']}"
        else:
            # General search
            url = f"https://api.shodan.io/shodan/host/search?key={osint_manager.api_keys['shodan']}&query={query}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            shodan_data = response.json()
            
            if search_type == 'host':
                results = {
                    "Shodan_Host_Search": {
                        "success": True,
                        "data": {
                            "ip": shodan_data.get('ip_str'),
                            "ports": shodan_data.get('ports', []),
                            "hostnames": shodan_data.get('hostnames', []),
                            "country_name": shodan_data.get('country_name'),
                            "city": shodan_data.get('city'),
                            "org": shodan_data.get('org'),
                            "os": shodan_data.get('os'),
                            "data": shodan_data.get('data', []),
                            "message": f"Shodan data found for {query}"
                        }
                    }
                }
            else:
                results = {
                    "Shodan_General_Search": {
                        "success": True,
                        "data": {
                            "total_results": shodan_data.get('total', 0),
                            "matches": shodan_data.get('matches', []),
                            "message": f"Found {shodan_data.get('total', 0)} Shodan results for '{query}'"
                        }
                    }
                }
        elif response.status_code == 403:
            # Free plan limitation
            results = {
                "Shodan_Search": {
                    "success": False,
                    "error": "Shodan search requires paid membership. Free plan has limited access.",
                    "upgrade_info": {
                        "current_plan": "oss (Open Source Software)",
                        "recommendation": "Upgrade to Membership or Professional plan for full search access",
                        "alternative": "Use Shodan web interface for manual searches",
                        "web_interface": f"https://www.shodan.io/search?query={query}"
                    }
                }
            }
        else:
            results = {
                "Shodan_Search": {
                    "success": False,
                    "error": f"Shodan API error: {response.status_code} - {response.text}"
                }
            }
        
        # Get AI analysis
        ai_analysis = osint_manager.call_ai_api('openai', 
            f"Analyze this Shodan search data for '{query}'. Provide insights about exposed services, potential vulnerabilities, and security recommendations.", 
            results)
        
        return jsonify({
            "query": query,
            "search_type": search_type,
            "results": results,
            "ai_analysis": ai_analysis,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Shodan search failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/ai/analyze', methods=['POST'])
def ai_analysis_endpoint():
    """AI analysis endpoint"""
    data = request.get_json()
    provider = data.get('provider', 'openai')
    prompt = data.get('prompt')
    results = data.get('results')
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    # Get AI analysis
    ai_analysis = osint_manager.call_ai_api(provider, prompt, results)
    
    return jsonify({
        "provider": provider,
        "analysis": ai_analysis,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
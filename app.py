from flask import Flask, render_template, request, jsonify, session
import os
import json
import threading
import time
import sys
import ssl
from datetime import datetime
import requests
import tempfile
import re
from typing import Dict, List, Optional

try:
    import assemblyai as aai
    ASSEMBLYAI_AVAILABLE = True
except ImportError:
    ASSEMBLYAI_AVAILABLE = False

from utils.api_keys import get_api_keys
from utils.content_generator import ContentGenerator
from utils.voice_manager import VoiceManager
from utils.ai_analyzer import AIAnalyzer

app = Flask(__name__)
app.secret_key = 'ai_learning_platform_secret_2024'

print("🔄 Initializing AI Learning Platform...")
api_keys = get_api_keys()
content_generator = ContentGenerator(api_keys)
voice_manager = VoiceManager(api_keys)
ai_analyzer = AIAnalyzer(api_keys)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_content', methods=['POST'])
def generate_content():
    try:
        data = request.json
        academic_level = data.get('academic_level')
        subject = data.get('subject')
        topic = data.get('topic')
        
        if not all([academic_level, subject, topic]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        session['academic_level'] = academic_level
        session['subject'] = subject
        session['topic'] = topic
        session['session_id'] = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        content_data = content_generator.generate_comprehensive_content(
            academic_level=academic_level,
            subject=subject,
            topic=topic
        )
        
        session['generated_content'] = content_data
        
        return jsonify({
            'success': True,
            'content': content_data['content'],
            'references': content_data['references'],
            'key_points': content_data['key_points'],
            'session_id': session['session_id']
        })
        
    except Exception as e:
        print(f"❌ Content generation error: {e}")
        return jsonify({'error': f'Content generation failed: {str(e)}'}), 500

@app.route('/transcribe_audio', methods=['POST'])
def transcribe_audio():
    try:
        audio_file = request.files.get('audio')
        if not audio_file:
            return jsonify({'error': 'No audio file provided'}), 400
        
        temp_path = f"temp/audio_{session.get('session_id', 'unknown')}.wav"
        os.makedirs('temp', exist_ok=True)
        audio_file.save(temp_path)
        
        print(f"🔄 Starting transcription of {temp_path}")
        
        transcription = voice_manager.transcribe_audio(temp_path)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        print(f"✅ Transcription result: {transcription[:100]}...")
        
        return jsonify({
            'success': True,
            'transcription': transcription
        })
    
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500

@app.route('/analyze_response', methods=['POST'])
def analyze_response():
    try:
        data = request.json
        user_response = data.get('response', '').strip()
        
        if not user_response:
            return jsonify({'error': 'No response provided'}), 400
        
        if not session.get('generated_content'):
            return jsonify({'error': 'No content session found'}), 400
        
        analysis = ai_analyzer.analyze_user_response(
            user_response=user_response,
            original_content=session['generated_content'],
            academic_level=session.get('academic_level'),
            subject=session.get('subject'),
            topic=session.get('topic')
        )
        
        session['last_analysis'] = analysis
        session['last_response'] = user_response
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/get_session_data')
def get_session_data():
    return jsonify({
        'academic_level': session.get('academic_level'),
        'subject': session.get('subject'),
        'topic': session.get('topic'),
        'session_id': session.get('session_id'),
        'has_content': bool(session.get('generated_content')),
        'last_analysis': session.get('last_analysis')
    })

@app.route('/reset_session', methods=['POST'])
def reset_session():
    session.clear()
    return jsonify({'success': True})

@app.route('/voice_status')
def voice_status():
    return jsonify(voice_manager.get_voice_status())

def create_self_signed_cert():
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        import datetime
        import ipaddress
        
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Local"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Local"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "AI Learning Platform"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            datetime.datetime.utcnow() + datetime.timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName("127.0.0.1"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        with open("cert.pem", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open("key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        print("✅ Self-signed certificate created")
        return True
        
    except ImportError:
        print("❌ cryptography package not available for HTTPS")
        return False
    except Exception as e:
        print(f"❌ Failed to create certificate: {e}")
        return False

if __name__ == '__main__':
    os.makedirs('temp', exist_ok=True)
    os.makedirs('static/audio', exist_ok=True)
    
    print("\n🎓 AI LEARNING PLATFORM")
    print(f"🐍 Python {sys.version_info.major}.{sys.version_info.minor}")
    
    use_https = False
    if not os.path.exists("cert.pem") or not os.path.exists("key.pem"):
        print("🔒 Creating self-signed certificate for HTTPS...")
        use_https = create_self_signed_cert()
    else:
        use_https = True
    
    if use_https:
        print("🔒 Starting with HTTPS for microphone access")
        print("🌐 Open https://localhost:5000 in your browser")
        print("⚠️  You'll see a security warning - click 'Advanced' then 'Proceed to localhost'")
        print("=" * 70)
        
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('cert.pem', 'key.pem')
        
        app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=context)
    else:
        print("🌐 Starting with HTTP - microphone may not work on network IPs")
        print("🌐 For microphone access, use: http://localhost:5000")
        print("⚠️  Do NOT use IP addresses - use localhost only")
        print("=" * 70)
        
        app.run(debug=True, host='0.0.0.0', port=5000)

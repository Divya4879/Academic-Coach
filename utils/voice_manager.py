import os
import requests
import tempfile
import re
from typing import Optional, Dict

ASSEMBLYAI_AVAILABLE = False

try:
    import assemblyai as aai
    ASSEMBLYAI_AVAILABLE = True
    print("✅ AssemblyAI module loaded")
except ImportError as e:
    print(f"❌ AssemblyAI not available: {e}")

class VoiceManager:
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.assemblyai_available = False
        
        self._init_assemblyai()
        self._print_status()
        
    def _init_assemblyai(self):
        """Initialize AssemblyAI with API key"""
        if ASSEMBLYAI_AVAILABLE and self.api_keys.get('ASSEMBLYAI_API_KEY'):
            try:
                aai.settings.api_key = self.api_keys['ASSEMBLYAI_API_KEY']
                
                test_config = aai.TranscriptionConfig(
                    language_detection=True,
                    punctuate=True,
                    format_text=True
                )
                
                self.assemblyai_available = True
                print("✅ AssemblyAI initialized successfully")
                    
            except Exception as e:
                print(f"❌ AssemblyAI initialization failed: {e}")
                self.assemblyai_available = False
        else:
            if not ASSEMBLYAI_AVAILABLE:
                print("❌ AssemblyAI module not installed")
            else:
                print("❌ AssemblyAI API key not provided")
    
    def _print_status(self):
        """Print voice features status"""
        print("\n🎤 VOICE FEATURES STATUS:")
        print(f"   AssemblyAI Available: {'✅' if self.assemblyai_available else '❌'}")
        print(f"   Voice Recording: {'✅' if self.assemblyai_available else '❌'}")
        print(f"   Audio Transcription: {'✅' if self.assemblyai_available else '❌'}")
        print()
    
    def get_voice_status(self) -> Dict[str, bool]:
        """Get current voice feature status"""
        return {
            'assemblyai_available': self.assemblyai_available,
            'voice_recording_available': self.assemblyai_available,
            'transcription_available': self.assemblyai_available,
            'api_key_configured': bool(self.api_keys.get('ASSEMBLYAI_API_KEY'))
        }
    
    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file using AssemblyAI
        """
        if not os.path.exists(audio_file_path):
            return "❌ Audio file not found"
        
        if self.assemblyai_available:
            try:
                print("🔄 Trying AssemblyAI SDK...")
                
                config = aai.TranscriptionConfig(
                    language_detection=True,
                    punctuate=True,
                    format_text=True,
                    speaker_labels=False,
                    auto_highlights=False
                )
                
                transcriber = aai.Transcriber(config=config)
                transcript = transcriber.transcribe(audio_file_path)
                
                if transcript.status == "completed":
                    print("✅ AssemblyAI SDK transcription successful")
                    return self._clean_transcription(transcript.text)
                elif transcript.status == "error":
                    print(f"❌ AssemblyAI SDK error: {transcript.error}")
                    return f"❌ Transcription error: {transcript.error}"
                else:
                    print(f"⚠️ AssemblyAI SDK status: {transcript.status}")
                    return f"⚠️ Transcription status: {transcript.status}"
                    
            except Exception as e:
                print(f"❌ AssemblyAI SDK error: {e}")
        
        if self.api_keys.get('ASSEMBLYAI_API_KEY'):
            try:
                print("🔄 Trying AssemblyAI Direct API...")
                result = self._transcribe_with_api(audio_file_path)
                if result and not result.startswith("❌") and not result.startswith("Error"):
                    print("✅ AssemblyAI API transcription successful")
                    return self._clean_transcription(result)
                else:
                    print(f"❌ AssemblyAI API failed: {result}")
                    return result
            except Exception as e:
                print(f"❌ AssemblyAI API error: {e}")
                return f"❌ API transcription error: {str(e)}"
        
        return "❌ Transcription failed. AssemblyAI API key may be missing or invalid. Please type your response instead."
    
    def _transcribe_with_api(self, audio_file_path: str) -> str:
        """
        Transcribe using direct AssemblyAI API calls
        """
        try:
            headers = {'authorization': self.api_keys['ASSEMBLYAI_API_KEY']}
            
            print("📤 Uploading audio file...")
            with open(audio_file_path, 'rb') as f:
                response = requests.post(
                    'https://api.assemblyai.com/v2/upload',
                    headers=headers,
                    files={'file': f},
                    timeout=60
                )
            
            if response.status_code != 200:
                return f"❌ Upload failed: {response.status_code} - {response.text}"
            
            upload_url = response.json()['upload_url']
            print(f"✅ File uploaded: {upload_url}")
            
            print("🔄 Requesting transcription...")
            data = {
                'audio_url': upload_url,
                'language_detection': True,
                'punctuate': True,
                'format_text': True,
                'speaker_labels': False,
                'auto_highlights': False
            }
            
            response = requests.post(
                'https://api.assemblyai.com/v2/transcript',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code != 200:
                return f"❌ Transcription request failed: {response.status_code} - {response.text}"
            
            transcript_id = response.json()['id']
            print(f"🔄 Transcription ID: {transcript_id}")
            
            print("⏳ Waiting for transcription to complete...")
            max_attempts = 60
            attempt = 0
            
            while attempt < max_attempts:
                response = requests.get(
                    f'https://api.assemblyai.com/v2/transcript/{transcript_id}',
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code != 200:
                    return f"❌ Status check failed: {response.status_code}"
                
                result = response.json()
                status = result['status']
                
                if status == 'completed':
                    print("✅ Transcription completed")
                    return result['text'] or "❌ No text in transcription result"
                elif status == 'error':
                    error_msg = result.get('error', 'Unknown error')
                    return f"❌ Transcription error: {error_msg}"
                elif status in ['queued', 'processing']:
                    print(f"⏳ Status: {status} (attempt {attempt + 1}/{max_attempts})")
                    import time
                    time.sleep(2)
                    attempt += 1
                else:
                    return f"❌ Unknown status: {status}"
            
            return "❌ Transcription timeout - took too long to process"
            
        except requests.exceptions.Timeout:
            return "❌ Request timeout - please try again"
        except requests.exceptions.RequestException as e:
            return f"❌ Network error: {str(e)}"
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"
    
    def _clean_transcription(self, text: str) -> str:
        """
        Clean and format transcription text
        """
        if not text:
            return "❌ Empty transcription result"
        
        text = text.strip()
        
        text = re.sub(r'\s+', ' ', text)
        
        text = re.sub(r'([.!?])\s*([a-z])', lambda m: m.group(1) + ' ' + m.group(2).upper(), text)
        
        if text and not text[0].isupper():
            text = text[0].upper() + text[1:]
        
        if text and text[-1] not in '.!?':
            text += '.'
        
        return text
    
    def validate_audio_file(self, file_path: str) -> Dict[str, any]:
        """
        Validate audio file for transcription
        """
        if not os.path.exists(file_path):
            return {
                'valid': False,
                'error': 'File does not exist',
                'file_size': 0
            }
        
        file_size = os.path.getsize(file_path)
        max_size = 100 * 1024 * 1024
        
        if file_size > max_size:
            return {
                'valid': False,
                'error': f'File too large: {file_size / (1024*1024):.1f}MB (max 100MB)',
                'file_size': file_size
            }
        
        if file_size < 1000:
            return {
                'valid': False,
                'error': 'File too small - may be empty or corrupted',
                'file_size': file_size
            }
        
        return {
            'valid': True,
            'error': None,
            'file_size': file_size,
            'file_size_mb': file_size / (1024 * 1024)
        }

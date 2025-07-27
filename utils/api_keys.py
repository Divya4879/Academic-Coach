import os
from typing import Dict

def get_api_keys() -> Dict[str, str]:
    """
    For local development, create a file called 'api_keys_config.py' in this folder with:
    
    GROQ_API_KEY = "gsk_your_groq_api_key_here"
    ASSEMBLYAI_API_KEY = "your_assemblyai_api_key_here"
    """
    
    api_keys = {}
    
    api_keys['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
    api_keys['ASSEMBLYAI_API_KEY'] = os.getenv('ASSEMBLYAI_API_KEY')
    
    try:
        from utils.api_keys_config import GROQ_API_KEY, ASSEMBLYAI_API_KEY
        
        if not api_keys['GROQ_API_KEY']:
            api_keys['GROQ_API_KEY'] = GROQ_API_KEY
        if not api_keys['ASSEMBLYAI_API_KEY']:
            api_keys['ASSEMBLYAI_API_KEY'] = ASSEMBLYAI_API_KEY
            
    except ImportError:
        print("⚠️  Local API keys config file not found. Using environment variables only.")
        print("📝 For local development, create utils/api_keys_config.py")
    
    return {k: v for k, v in api_keys.items() if v}

def validate_api_keys(api_keys: Dict[str, str]) -> Dict[str, bool]:
    """
    Validate that required API keys are present
    """
    validation = {
        'assemblyai_available': bool(api_keys.get('ASSEMBLYAI_API_KEY')),
        'groq_available': bool(api_keys.get('GROQ_API_KEY')),
        'all_features_available': False
    }
    
    validation['all_features_available'] = (
        validation['assemblyai_available'] and 
        validation['groq_available']
    )
    
    return validation

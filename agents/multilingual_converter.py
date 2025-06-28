import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class MultilingualConverterAgent:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.supported_languages = {
            'hindi': 'Hindi (हिंदी)',
            'marathi': 'Marathi (मराठी)',
            'bengali': 'Bengali (বাংলা)',
            'tamil': 'Tamil (தமிழ்)',
            'kannada': 'Kannada (ಕನ್ನಡ)'
        }
    
    def convert_languages(self, clause_text):
        """Convert clause to multiple Indian languages"""
        try:
            translations = {}
            
            for lang_code, lang_name in self.supported_languages.items():
                translation = self._translate_to_language(clause_text, lang_code, lang_name)
                translations[lang_code] = {
                    'language_name': lang_name,
                    'translated_text': translation,
                    'ready_for_distribution': True
                }
            
            return {
                'source_language': 'English',
                'translations': translations,
                'total_languages': len(translations),
                'rural_customer_ready': True
            }
            
        except Exception as e:
            return {'error': f'Translation failed: {str(e)}'}
    
    def _translate_to_language(self, text, lang_code, lang_name):
        """Translate text to specific language"""
        prompt = f"""
        Translate this simple English insurance clause into {lang_name} for rural customers:
        
        English text: {text}
        
        Requirements:
        - Use simple, everyday words in {lang_name}
        - Avoid complex insurance jargon
        - Keep the meaning clear and accurate
        - Make it suitable for customers with basic education
        
        {lang_name} translation:
        """
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=300,
                temperature=0.3
            )
        )
        
        return response.text.strip()

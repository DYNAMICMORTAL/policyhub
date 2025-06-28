import google.generativeai as genai
import re
import os
from textstat import flesch_reading_ease, flesch_kincaid_grade
from dotenv import load_dotenv

load_dotenv()

class PolicyRewriterAgent:
    def __init__(self):
        # Initialize Gemini client with environment variable
        api_key = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def rewrite(self, clause_text):
        """Rewrite policy clause in plain English"""
        try:
            # Calculate original readability metrics
            original_flesch = flesch_reading_ease(clause_text)
            original_grade = flesch_kincaid_grade(clause_text)
            original_word_count = len(clause_text.split())
            
            # Generate plain English version
            plain_english = self._generate_plain_english(clause_text)
            
            # Calculate improved readability metrics
            new_flesch = flesch_reading_ease(plain_english)
            new_grade = flesch_kincaid_grade(plain_english)
            new_word_count = len(plain_english.split())
            
            return {
                'original_text': clause_text,
                'plain_english_text': plain_english,
                'original_metrics': {
                    'flesch_score': round(original_flesch, 2),
                    'grade_level': round(original_grade, 2),
                    'word_count': original_word_count
                },
                'improved_metrics': {
                    'flesch_score': round(new_flesch, 2),
                    'grade_level': round(new_grade, 2),
                    'word_count': new_word_count
                },
                'readability_improvement': round(new_flesch - original_flesch, 2),
                'meets_irdai_standards': new_grade <= 8.0
            }
            
        except Exception as e:
            return {'error': f'Rewriting failed: {str(e)}'}
    
    def _generate_plain_english(self, clause_text):
        """Use Gemini to generate plain English version"""
        prompt = f"""
        Rewrite this insurance policy clause in plain English that meets IRDAI readability standards:
        
        Original clause: {clause_text}
        
        Requirements:
        - Dont say okay this is the plain English version
        - Just rewrite the clause directly
        - Use simple words (8th grade reading level)
        - Short sentences (max 20 words)
        - Active voice when possible
        - Remove legal jargon
        - Keep the same legal meaning
        - Make it customer-friendly
        
        Plain English version:
        """
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=300,
                temperature=0.3
            )
        )
        
        return response.text.strip()

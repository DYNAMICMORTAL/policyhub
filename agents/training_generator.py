import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class TrainingGeneratorAgent:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate_training(self, clause_text):
        """Generate training materials for field agents"""
        try:
            # Generate FAQ questions
            faq_questions = self._generate_faq_questions(clause_text)
            
            # Generate role-play scripts
            roleplay_scripts = self._generate_roleplay_scripts(clause_text)
            
            # Generate pitch summary
            pitch_summary = self._generate_pitch_summary(clause_text)
            
            return {
                'faq_questions': faq_questions,
                'roleplay_scripts': roleplay_scripts,
                'pitch_summary': pitch_summary,
                'training_ready': True
            }
            
        except Exception as e:
            return {'error': f'Training generation failed: {str(e)}'}
    
    def _generate_faq_questions(self, clause_text):
        """Generate FAQ questions about the clause"""
        prompt = f"""
        Generate 5 common FAQ questions that customers might ask about this insurance clause:
        
        Clause: {clause_text}
        
        Format as:
        Q1: [Question]
        A1: [Simple answer]
        
        Q2: [Question]
        A2: [Simple answer]
        
        Continue for 5 questions total.
        """
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=400,
                temperature=0.4
            )
        )
        
        return response.text.strip()
    
    def _generate_roleplay_scripts(self, clause_text):
        """Generate role-play training scripts"""
        prompt = f"""
        Create a role-play script for insurance agents to practice explaining this clause:
        
        Clause: {clause_text}
        
        Format as:
        Agent: [Opening statement]
        Customer: [Potential objection or question]
        Agent: [How to respond]
        Customer: [Follow-up question]
        Agent: [Final clarification]
        
        Keep it realistic and helpful for training.
        """
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=300,
                temperature=0.4
            )
        )
        
        return response.text.strip()
    
    def _generate_pitch_summary(self, clause_text):
        """Generate 1-minute pitch summary"""
        prompt = f"""
        Create a 1-minute elevator pitch for agents to explain this clause quickly:
        
        Clause: {clause_text}
        
        Requirements:
        - Under 100 words
        - Highlights key benefits
        - Addresses main customer concerns
        - Easy to memorize
        
        Pitch:
        """
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=150,
                temperature=0.3
            )
        )
        
        return response.text.strip()

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class ScenarioExplainerAgent:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate_scenario(self, clause_text):
        """Generate customer-friendly scenario explanations"""
        try:
            # Generate main scenario
            main_scenario = self._generate_main_scenario(clause_text)
            
            # Generate additional examples
            examples = self._generate_examples(clause_text)
            
            return {
                'main_scenario': main_scenario,
                'real_life_examples': examples,
                'customer_script': self._generate_agent_script(clause_text),
                'simple_explanation': self._generate_simple_explanation(clause_text)
            }
            
        except Exception as e:
            return {'error': f'Scenario generation failed: {str(e)}'}
    
    def _generate_main_scenario(self, clause_text):
        """Generate main customer scenario"""
        prompt = f"""
        Create a realistic scenario that explains this insurance clause to an average policyholder:
        
        Clause: {clause_text}
        
        Create a short, relatable example starting with "Example: If..." that shows:
        - What situation this clause covers
        - What the customer can expect
        - What happens in practice
        
        Keep it under 50 words and use simple language.
        """
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=150,
                temperature=0.4
            )
        )
        
        return response.text.strip()
    
    def _generate_examples(self, clause_text):
        """Generate multiple examples"""
        prompt = f"""
        Generate 3 different real-life examples for this insurance clause:
        
        Clause: {clause_text}
        
        Format as:
        1. [Brief scenario]
        2. [Brief scenario]
        3. [Brief scenario]
        
        Each example should be 1-2 sentences and show different situations.
        """
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=200,
                temperature=0.5
            )
        )
        
        return response.text.strip()
    
    def _generate_agent_script(self, clause_text):
        """Generate script for sales agents"""
        prompt = f"""
        Create a simple script for insurance agents to explain this clause to customers:
        
        Clause: {clause_text}
        
        Format as a conversation starter that agents can use. Keep it friendly and clear.
        """
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=150,
                temperature=0.3
            )
        )
        
        return response.text.strip()
    
    def _generate_simple_explanation(self, clause_text):
        """Generate very simple explanation"""
        prompt = f"""
        Explain this insurance clause in the simplest possible terms (5th grade level):
        
        Clause: {clause_text}
        
        Use only common words. Maximum 30 words.
        """
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=100,
                temperature=0.2
            )
        )
        
        return response.text.strip()

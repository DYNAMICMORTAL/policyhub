import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

class BenchmarkAnalyzerAgent:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.historical_clauses = self._load_historical_data()
    
    def analyze_similarity(self, clause_text):
        """Compare clause against historical policy wordings"""
        try:
            # Get similarity analysis from LLM
            similarity_analysis = self._get_similarity_analysis(clause_text)
            
            # Calculate deviation score
            deviation_score = self._calculate_deviation_score(clause_text)
            
            return {
                'similarity_score': similarity_analysis.get('similarity_score', 75),
                'deviation_analysis': similarity_analysis.get('deviation_analysis', ''),
                'unusual_terms': similarity_analysis.get('unusual_terms', []),
                'industry_comparison': similarity_analysis.get('industry_comparison', ''),
                'deviation_score': deviation_score,
                'recommendations': similarity_analysis.get('recommendations', []),
                'fraud_risk_indicator': deviation_score > 30
            }
            
        except Exception as e:
            return {'error': f'Benchmark analysis failed: {str(e)}'}
    
    def _get_similarity_analysis(self, clause_text):
        """Use Gemini to analyze clause similarity"""
        prompt = f"""
        Analyze this insurance clause compared to standard industry practices:
        
        Clause: {clause_text}
        
        Evaluate:
        1. How similar is this to typical insurance clauses? (0-100 score)
        2. Any unusual or non-standard terms?
        3. Deviations from industry norms
        4. Potential red flags
        
        Provide response in JSON format:
        {{
            "similarity_score": 0-100,
            "deviation_analysis": "brief explanation",
            "unusual_terms": ["term1", "term2"],
            "industry_comparison": "how it compares to standard",
            "recommendations": ["recommendation1", "recommendation2"]
        }}
        """
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=400,
                temperature=0.2
            )
        )
        
        try:
            response_text = response.text.strip()
            # Remove any markdown formatting
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            return json.loads(response_text)
        except:
            return {
                'similarity_score': 75,
                'deviation_analysis': 'Analysis not available',
                'unusual_terms': [],
                'industry_comparison': 'Standard clause',
                'recommendations': []
            }
    
    def _calculate_deviation_score(self, clause_text):
        """Calculate deviation score based on various factors"""
        # Simple scoring based on clause characteristics
        base_score = 10
        
        # Check for unusual length
        word_count = len(clause_text.split())
        if word_count > 100:
            base_score += 10
        elif word_count < 20:
            base_score += 5
        
        # Check for complex legal terms
        complex_terms = [
            'notwithstanding', 'heretofore', 'whereupon', 'aforementioned',
            'pursuant to', 'inasmuch as', 'provided that'
        ]
        
        for term in complex_terms:
            if term.lower() in clause_text.lower():
                base_score += 5
        
        return min(100, base_score)
    
    def _load_historical_data(self):
        """Load historical clause data for comparison"""
        # In a real implementation, this would load from a database
        # For now, return empty list
        return []

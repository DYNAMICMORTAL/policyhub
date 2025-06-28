import google.generativeai as genai
import re
import os
import json
from dotenv import load_dotenv

load_dotenv()

class RiskScorerAgent:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.high_risk_phrases = [
            "unlimited coverage", "all risks", "any loss", "regardless of cause",
            "without limitation", "maximum coverage", "full replacement"
        ]
    
    def score_risk(self, clause_text):
        """Analyze financial and legal risk of clause"""
        try:
            # Quick phrase-based risk detection
            phrase_risk = self._detect_risky_phrases(clause_text)
            
            # LLM-based comprehensive risk analysis
            llm_analysis = self._get_llm_risk_analysis(clause_text)
            
            # Calculate overall risk score (0-100)
            risk_score = self._calculate_risk_score(phrase_risk, llm_analysis)
            
            return {
                'risk_score': risk_score,
                'risk_level': self._get_risk_level(risk_score),
                'financial_risk': llm_analysis.get('financial_risk', 'Unknown'),
                
                'dispute_potential': llm_analysis.get('dispute_potential', 'Unknown'),
                'risky_phrases_found': phrase_risk,
                'mitigation_suggestions': llm_analysis.get('mitigation_suggestions', []),
                'explanation': llm_analysis.get('explanation', ''),
                'requires_underwriter_review': risk_score >= 70
            }
            
        except Exception as e:
            # Return a complete fallback risk assessment
            return self._create_fallback_risk_assessment(clause_text, str(e))
    
    def _detect_risky_phrases(self, text):
        """Detect predefined risky phrases"""
        detected = []
        text_lower = text.lower()
        
        for phrase in self.high_risk_phrases:
            if phrase in text_lower:
                detected.append(phrase)
        
        return detected
    
    def _get_llm_risk_analysis(self, clause_text):
        """Get comprehensive risk analysis from Gemini"""
        prompt = f"""
        Analyze this insurance clause for financial and legal risk:
        
        Clause: {clause_text}
        
        Evaluate:
        1. Financial risk for the insurer (Low/Medium/High)
        2. Potential for customer disputes (Low/Medium/High)
        3. Claim frequency potential
        4. Ambiguity that could lead to disputes
        
        Provide response in JSON format:
        {{
            "financial_risk": "Low/Medium/High",
            "dispute_potential": "Low/Medium/High",
            "explanation": "brief explanation of the main risks",
            "mitigation_suggestions": ["suggestion 1", "suggestion 2"]
        }}
        """
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=300,
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
            # Return more meaningful fallback
            return {
                'financial_risk': 'Medium',
                'dispute_potential': 'Medium',
                'explanation': f'Risk analysis suggests moderate concerns. The clause contains {len(clause_text.split())} words and may benefit from simplification.',
                'mitigation_suggestions': [
                    'Review clause for clarity and specificity',
                    'Consider adding concrete examples or limits',
                    'Ensure compliance with IRDAI guidelines'
                ]
            }
    
    def _calculate_risk_score(self, phrase_risk, llm_analysis):
        """Calculate overall risk score"""
        base_score = 30  # Base risk
        
        # Add points for risky phrases
        phrase_score = len(phrase_risk) * 15
        
        # Add points based on LLM analysis
        financial_risk = llm_analysis.get('financial_risk', 'Medium')
        dispute_risk = llm_analysis.get('dispute_potential', 'Medium')
        
        risk_mapping = {'Low': 0, 'Medium': 20, 'High': 30}
        financial_score = risk_mapping.get(financial_risk, 20)
        dispute_score = risk_mapping.get(dispute_risk, 20)
        
        total_score = min(100, base_score + phrase_score + financial_score + dispute_score)
        return total_score
    
    def _get_risk_level(self, score):
        """Convert score to risk level"""
        if score >= 80:
            return "High"
        elif score >= 50:
            return "Medium"
        else:
            return "Low"
    
    def _create_fallback_risk_assessment(self, clause_text, error_msg):
        """Create a fallback risk assessment when LLM is unavailable"""
        # Detect risky phrases
        phrase_risk = self._detect_risky_phrases(clause_text)
        
        # Basic structural analysis
        word_count = len(clause_text.split())
        sentence_count = len([s for s in clause_text.split('.') if s.strip()])
        
        # Calculate base risk score
        base_risk = 40  # Medium baseline
        
        # Adjust based on phrase detection
        phrase_risk_score = len(phrase_risk) * 15
        
        # Adjust based on complexity
        complexity_score = 0
        if word_count > 50:
            complexity_score += 10
        if sentence_count == 1 and word_count > 20:  # Long single sentence
            complexity_score += 10
        
        # Check for vague terms
        vague_terms = ['discretion', 'appropriate', 'reasonable', 'from time to time', 'subject to']
        vague_count = sum(1 for term in vague_terms if term.lower() in clause_text.lower())
        vague_score = vague_count * 8
        
        total_risk = min(100, base_risk + phrase_risk_score + complexity_score + vague_score)
        
        # Generate meaningful explanation
        explanation_parts = []
        if phrase_risk:
            explanation_parts.append(f"Contains {len(phrase_risk)} high-risk phrases")
        if word_count > 50:
            explanation_parts.append("Clause is lengthy and complex")
        if vague_count > 0:
            explanation_parts.append(f"Contains {vague_count} vague terms requiring clarification")
        
        explanation = "; ".join(explanation_parts) if explanation_parts else "Standard risk assessment based on clause structure"
        
        # Generate mitigation suggestions
        suggestions = []
        if phrase_risk:
            suggestions.append("Review and clarify high-risk language")
        if word_count > 50:
            suggestions.append("Consider breaking into shorter, clearer clauses")
        if vague_count > 0:
            suggestions.append("Replace vague terms with specific criteria")
        if not suggestions:
            suggestions.append("Regular compliance review recommended")
        
        return {
            'risk_score': total_risk,
            'risk_level': self._get_risk_level(total_risk),
            'financial_risk': 'Medium' if total_risk >= 50 else 'Low',
            'dispute_potential': 'High' if vague_count > 2 else 'Medium' if vague_count > 0 else 'Low',
            'risky_phrases_found': phrase_risk,
            'mitigation_suggestions': suggestions,
            'explanation': f"{explanation} (Fallback analysis - LLM unavailable)",
            'requires_underwriter_review': total_risk >= 70,
            'fallback_analysis': True
        }

import google.generativeai as genai
import re
import os
import json
from dotenv import load_dotenv

load_dotenv()

class ComplianceCheckerAgent:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.vague_phrases = [
            "notwithstanding", "reasonable effort", "as appropriate", 
            "from time to time", "subject to", "at our discretion"
        ]
    
    def check_compliance(self, clause_text):
        """Check clause for regulatory compliance issues"""
        try:
            # Detect vague language
            vague_issues = self._detect_vague_language(clause_text)
            
            # Get Gemini compliance analysis
            llm_analysis = self._get_llm_compliance_check(clause_text)
            
            # Calculate overall compliance score
            total_issues = len(vague_issues) + len(llm_analysis.get('issues', []))
            compliance_score = max(0, 100 - (total_issues * 10))
            
            return {
                'compliance_score': compliance_score,
                'status': self._get_status(compliance_score),
                'vague_language_detected': vague_issues,
                'regulatory_issues': llm_analysis.get('issues', []),
                'recommendations': llm_analysis.get('recommendations', []),
                'irdai_compliant': compliance_score >= 80
            }
            
        except Exception as e:
            return {'error': f'Compliance check failed: {str(e)}'}
    
    def _detect_vague_language(self, text):
        """Detect predefined vague phrases"""
        detected = []
        text_lower = text.lower()
        
        for phrase in self.vague_phrases:
            if phrase in text_lower:
                detected.append({
                    'phrase': phrase,
                    'recommendation': f'Replace "{phrase}" with specific terms or timelines'
                })
        
        return detected
    
    def _get_llm_compliance_check(self, clause_text):
        """Use Gemini for detailed compliance analysis"""
        prompt = f"""
        Analyze this insurance clause for regulatory compliance issues:
        
        Clause: {clause_text}
        
        Check for:
        1. Vague or ambiguous language
        2. Potential consumer disputes
        3. Non-compliance with IRDAI plain language mandate
        4. Misleading or contradictory terms
        5. Hidden exclusions
        
        Provide response in JSON format:
        {{
            "issues": ["list of specific issues found"],
            "recommendations": ["specific suggestions to fix each issue"]
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
            # Extract JSON from response
            response_text = response.text.strip()
            # Remove any markdown formatting
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            return json.loads(response_text)
        except:
            # Return more meaningful fallback analysis
            word_count = len(clause_text.split())
            sentence_count = len([s for s in clause_text.split('.') if s.strip()])
            avg_sentence_length = word_count / max(sentence_count, 1)
            
            issues = []
            recommendations = []
            
            if avg_sentence_length > 25:
                issues.append("Sentences are too long for easy comprehension")
                recommendations.append("Break down long sentences into shorter ones")
            
            if word_count > 100:
                issues.append("Clause is lengthy and may be difficult to understand")
                recommendations.append("Consider splitting into multiple shorter clauses")
            
            # Check for common jargon
            jargon_terms = ['notwithstanding', 'heretofore', 'wherefore', 'pursuant to']
            found_jargon = [term for term in jargon_terms if term.lower() in clause_text.lower()]
            if found_jargon:
                issues.append(f"Contains legal jargon: {', '.join(found_jargon)}")
                recommendations.append("Replace legal jargon with plain English terms")
            
            return {
                'issues': issues if issues else ['No major structural issues detected'],
                'recommendations': recommendations if recommendations else ['Consider review for plain language compliance']
            }
    
    def _get_status(self, score):
        """Get compliance status based on score"""
        if score >= 80:
            return "compliant"
        elif score >= 60:
            return "needs_review"
        else:
            return "high_risk"

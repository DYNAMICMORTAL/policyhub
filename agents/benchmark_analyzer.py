import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv
from difflib import SequenceMatcher

load_dotenv()

class BenchmarkAnalyzerAgent:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Industry standard clause library for comparison
        self.industry_standards = {
            'exclusions': [
                "This policy does not cover losses caused by war, invasion, acts of foreign enemies, hostilities, or warlike operations.",
                "Losses arising from nuclear reaction, nuclear radiation, or radioactive contamination are excluded.",
                "Damage caused by wear and tear, gradual deterioration, or inherent defects is not covered."
            ],
            'claims': [
                "All claims must be reported to the insurer within 30 days of the loss occurrence.",
                "The insured must provide all necessary documentation to support the claim.",
                "Claims will be settled within 30 days of receiving all required documents."
            ],
            'liability': [
                "The insurer's liability shall not exceed the sum insured specified in the policy schedule.",
                "Coverage is subject to the terms, conditions, and exclusions contained herein.",
                "The insurer reserves the right to investigate all claims before settlement."
            ],
            'termination': [
                "This policy may be cancelled by either party with 30 days written notice.",
                "Upon cancellation, unearned premium will be refunded on a pro-rata basis.",
                "Policy automatically terminates upon sale or transfer of insured property."
            ]
        }
        
        # Similarity threshold for matches
        self.similarity_threshold = 0.6
    
    def analyze_similarity(self, clause_text):
        """Analyze similarity with industry standards and provide benchmarking"""
        try:
            # Find similar clauses in our database
            similar_clauses = self._find_similar_clauses(clause_text)
            
            # Calculate overall similarity score
            similarity_score = self._calculate_similarity_score(clause_text, similar_clauses)
            
            # Get industry comparison using LLM
            industry_comparison = self._get_industry_comparison(clause_text)
            
            # Generate analysis summary
            analysis_summary = self._generate_analysis_summary(
                clause_text, similarity_score, similar_clauses, industry_comparison
            )
            
            return {
                'similarity_score': similarity_score,
                'similar_clauses': similar_clauses[:5],  # Top 5 matches
                'industry_comparison': industry_comparison,
                'analysis_summary': analysis_summary,
                'benchmark_grade': self._get_benchmark_grade(similarity_score),
                'recommendations': self._generate_recommendations(similarity_score, industry_comparison)
            }
            
        except Exception as e:
            return {
                'error': f'Benchmark analysis failed: {str(e)}',
                'similarity_score': 75,
                'analysis_summary': 'No analysis summary available.',
                'similar_clauses': [],
                'industry_comparison': {
                    'standard': 'Not available',
                    'rating': 'Not rated',
                    'recommendation': 'No specific recommendation'
                }
            }
    
    def _find_similar_clauses(self, clause_text):
        """Find clauses similar to the input from industry standards"""
        similar_clauses = []
        clause_lower = clause_text.lower()
        
        # Search through all industry standard categories
        for category, standards in self.industry_standards.items():
            for standard_clause in standards:
                similarity = self._calculate_text_similarity(clause_text, standard_clause)
                
                if similarity >= self.similarity_threshold:
                    similar_clauses.append({
                        'text': standard_clause,
                        'similarity': round(similarity * 100, 1),
                        'category': category,
                        'match_type': 'exact' if similarity > 0.9 else 'similar'
                    })
        
        # Sort by similarity score
        similar_clauses.sort(key=lambda x: x['similarity'], reverse=True)
        
        # If no good matches, add some related clauses based on keywords
        if not similar_clauses:
            similar_clauses = self._find_keyword_matches(clause_text)
        
        return similar_clauses
    
    def _calculate_text_similarity(self, text1, text2):
        """Calculate similarity between two text strings"""
        # Use SequenceMatcher for basic similarity
        basic_similarity = SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        
        # Calculate keyword similarity
        keywords1 = set(re.findall(r'\b\w+\b', text1.lower()))
        keywords2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        if not keywords1 or not keywords2:
            return basic_similarity
        
        keyword_similarity = len(keywords1.intersection(keywords2)) / len(keywords1.union(keywords2))
        
        # Weighted average
        return (basic_similarity * 0.6) + (keyword_similarity * 0.4)
    
    def _find_keyword_matches(self, clause_text):
        """Find matches based on keywords when no direct similarity found"""
        keyword_matches = []
        clause_keywords = set(re.findall(r'\b\w+\b', clause_text.lower()))
        
        insurance_keywords = {
            'coverage', 'claim', 'premium', 'deductible', 'liability',
            'exclusion', 'loss', 'damage', 'insured', 'policy'
        }
        
        relevant_keywords = clause_keywords.intersection(insurance_keywords)
        
        if 'claim' in relevant_keywords:
            keyword_matches.extend([
                {
                    'text': 'Standard claims must be reported within reasonable time',
                    'similarity': 45.0,
                    'category': 'claims',
                    'match_type': 'keyword'
                }
            ])
        
        if 'exclusion' in relevant_keywords or 'exclude' in clause_text.lower():
            keyword_matches.extend([
                {
                    'text': 'Common exclusions apply to extraordinary circumstances',
                    'similarity': 40.0,
                    'category': 'exclusions',
                    'match_type': 'keyword'
                }
            ])
        
        return keyword_matches
    
    def _calculate_similarity_score(self, clause_text, similar_clauses):
        """Calculate overall similarity score based on matches found"""
        if not similar_clauses:
            return 25  # Low score if no matches
        
        # Get the best match score
        best_match = max(similar_clauses, key=lambda x: x['similarity'])
        best_score = best_match['similarity']
        
        # Adjust based on number of matches
        match_bonus = min(10, len(similar_clauses) * 2)
        
        final_score = min(100, best_score + match_bonus)
        return round(final_score)
    
    def _get_industry_comparison(self, clause_text):
        """Get industry comparison analysis using LLM"""
        prompt = f"""
        Compare this insurance clause with industry standards:
        
        Clause: {clause_text}
        
        Analyze:
        1. How it compares to typical industry language
        2. Whether it's customer-friendly or industry-standard
        3. Any recommendations for improvement
        
        Provide response in JSON format:
        {{
            "standard": "Industry standard assessment",
            "rating": "Above Average/Average/Below Average",
            "recommendation": "Specific recommendation"
        }}
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=200,
                    temperature=0.3
                )
            )
            
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            return json.loads(response_text)
            
        except:
            # Fallback analysis
            word_count = len(clause_text.split())
            complexity = 'Complex' if word_count > 30 else 'Standard'
            
            return {
                'standard': f'{complexity} language structure typical for insurance',
                'rating': 'Average',
                'recommendation': 'Consider simplifying for better customer understanding'
            }
    
    def _generate_analysis_summary(self, clause_text, similarity_score, similar_clauses, industry_comparison):
        """Generate comprehensive analysis summary"""
        summary_parts = []
        
        # Similarity assessment
        if similarity_score >= 80:
            summary_parts.append("High similarity to industry standards")
        elif similarity_score >= 60:
            summary_parts.append("Moderate alignment with industry practices")
        else:
            summary_parts.append("Limited similarity to standard industry clauses")
        
        # Match quality
        if similar_clauses:
            best_match = max(similar_clauses, key=lambda x: x['similarity'])
            summary_parts.append(f"Best match: {best_match['similarity']}% similarity")
        
        # Industry rating
        rating = industry_comparison.get('rating', 'Average')
        summary_parts.append(f"Industry rating: {rating}")
        
        return '. '.join(summary_parts) + '.'
    
    def _get_benchmark_grade(self, similarity_score):
        """Convert similarity score to letter grade"""
        if similarity_score >= 90:
            return 'A+'
        elif similarity_score >= 80:
            return 'A'
        elif similarity_score >= 70:
            return 'B'
        elif similarity_score >= 60:
            return 'C'
        else:
            return 'D'
    
    def _generate_recommendations(self, similarity_score, industry_comparison):
        """Generate actionable recommendations"""
        recommendations = []
        
        if similarity_score < 60:
            recommendations.append("Consider aligning language with industry standards")
        
        if similarity_score > 90:
            recommendations.append("Clause follows industry best practices")
        
        # Add recommendation from industry comparison
        if industry_comparison.get('recommendation'):
            recommendations.append(industry_comparison['recommendation'])
        
        if not recommendations:
            recommendations.append("Clause appears to meet standard industry requirements")
        
        return recommendations

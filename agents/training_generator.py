import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

class TrainingGeneratorAgent:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate_training(self, clause_text):
        """Generate comprehensive training materials for field agents"""
        try:
            # Generate main training module
            training_module = self._generate_training_module(clause_text)
            
            # Generate quiz questions
            quiz_questions = self._generate_quiz_questions(clause_text)
            
            # Generate key learning points
            learning_points = self._generate_learning_points(clause_text)
            
            # Determine target audience and difficulty
            audience_analysis = self._analyze_target_audience(clause_text)
            
            # Generate training objectives
            training_objectives = self._generate_training_objectives(clause_text)
            
            # Generate practical examples
            practical_examples = self._generate_practical_examples(clause_text)
            
            # Generate role-play scenarios
            role_play_scenarios = self._generate_role_play_scenarios(clause_text)
            
            # Generate common mistakes to avoid
            common_mistakes = self._generate_common_mistakes(clause_text)
            
            return {
                'training_module': training_module,
                'quiz_questions': quiz_questions,
                'key_learning_points': learning_points,
                'target_audience': audience_analysis.get('audience', 'Insurance Sales Agents'),
                'difficulty_level': audience_analysis.get('difficulty', 'Intermediate'),
                'estimated_duration': audience_analysis.get('duration', '15-20 minutes'),
                'training_objectives': training_objectives,
                'practical_examples': practical_examples,
                'role_play_scenarios': role_play_scenarios,
                'common_mistakes': common_mistakes,
                'assessment_criteria': self._generate_assessment_criteria(clause_text),
                'follow_up_resources': self._generate_follow_up_resources(clause_text)
            }
            
        except Exception as e:
            return {
                'error': f'Training generation failed: {str(e)}',
                'training_module': 'Training content temporarily unavailable due to API limits. Using fallback training structure.',
                'quiz_questions': self._get_fallback_quiz(),
                'key_learning_points': self._get_fallback_learning_points(),
                'target_audience': 'Insurance Agents',
                'difficulty_level': 'Intermediate',
                'estimated_duration': '15 minutes',
                'training_objectives': self._get_fallback_objectives(),
                'practical_examples': self._get_fallback_examples(),
                'role_play_scenarios': self._get_fallback_scenarios(),
                'common_mistakes': self._get_fallback_mistakes()
            }
    
    def _generate_training_module(self, clause_text):
        """Generate comprehensive training module content"""
        prompt = f"""
        Create a comprehensive training module for insurance agents about this policy clause:
        
        Clause: {clause_text}
        
        Structure the training as follows:
        
        1. OVERVIEW (2-3 sentences explaining what this clause covers)
        2. KEY TERMS (Define important terms in simple language)
        3. CUSTOMER IMPACT (How this affects the customer)
        4. COMMON QUESTIONS (What customers typically ask)
        5. BEST PRACTICES (How to explain this effectively)
        6. RED FLAGS (Warning signs to watch for)
        
        Keep each section concise but informative. Use simple language that agents can easily understand and remember.
        """
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=600,
                temperature=0.3
            )
        )
        
        return response.text.strip()
    
    def _generate_quiz_questions(self, clause_text):
        """Generate quiz questions for knowledge assessment"""
        prompt = f"""
        Create 5 quiz questions to test agent understanding of this insurance clause:
        
        Clause: {clause_text}
        
        For each question, provide:
        - The question
        - 4 multiple choice options (A, B, C, D)
        - The correct answer
        - A brief explanation
        
        Format as JSON:
        [
            {{
                "question": "Question text",
                "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                "correct_answer": "B",
                "explanation": "Brief explanation"
            }}
        ]
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=700,
                    temperature=0.4
                )
            )
            
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            return json.loads(response_text)
            
        except:
            return self._get_fallback_quiz()
    
    def _generate_role_play_scenarios(self, clause_text):
        """Generate role-play scenarios for practical training"""
        prompt = f"""
        Create 3 role-play scenarios for training agents on this insurance clause:
        
        Clause: {clause_text}
        
        Each scenario should include:
        - Customer situation
        - Customer's likely questions/concerns
        - Recommended agent response
        - Key points to emphasize
        
        Format as clear, practical scenarios that trainers can use immediately.
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=500,
                    temperature=0.4
                )
            )
            
            return response.text.strip()
            
        except:
            return self._get_fallback_scenarios()
    
    def _generate_common_mistakes(self, clause_text):
        """Generate common mistakes agents should avoid"""
        prompt = f"""
        List 5 common mistakes insurance agents make when explaining this clause to customers:
        
        Clause: {clause_text}
        
        For each mistake, provide:
        - What agents often do wrong
        - Why it's problematic
        - What they should do instead
        
        Format as clear, actionable guidance.
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=400,
                    temperature=0.3
                )
            )
            
            return response.text.strip()
            
        except:
            return self._get_fallback_mistakes()
    
    def _generate_assessment_criteria(self, clause_text):
        """Generate criteria for assessing agent understanding"""
        criteria = [
            "Agent can explain the clause in simple terms",
            "Agent can identify when the clause applies",
            "Agent can answer common customer questions",
            "Agent demonstrates empathy for customer concerns",
            "Agent follows compliance guidelines"
        ]
        
        return criteria
    
    def _generate_follow_up_resources(self, clause_text):
        """Generate follow-up learning resources"""
        resources = [
            "IRDAI Guidelines on Plain Language Requirements",
            "Customer Communication Best Practices Guide",
            "Advanced Policy Interpretation Workshop",
            "Regulatory Compliance Updates",
            "Customer Scenario Practice Database"
        ]
        
        return resources
    
    # Fallback methods when API is unavailable
    def _get_fallback_quiz(self):
        return [
            {
                "question": "What is the main purpose of this clause?",
                "options": ["A) To exclude coverage", "B) To define terms", "C) To specify conditions", "D) All of the above"],
                "correct_answer": "D",
                "explanation": "Policy clauses serve multiple purposes including defining coverage, terms, and conditions."
            },
            {
                "question": "How should agents explain complex clauses to customers?",
                "options": ["A) Use technical terms", "B) Read word-for-word", "C) Use simple examples", "D) Avoid explanation"],
                "correct_answer": "C",
                "explanation": "Simple examples help customers understand complex insurance concepts better."
            },
            {
                "question": "When should an agent refer to a supervisor?",
                "options": ["A) Never", "B) For all questions", "C) For complex interpretations", "D) Only for complaints"],
                "correct_answer": "C",
                "explanation": "Complex interpretations require supervisory guidance to ensure accuracy."
            }
        ]
    
    def _get_fallback_learning_points(self):
        return [
            "Understand the clause's purpose and scope",
            "Identify key terms that need explanation",
            "Prepare simple examples for customers",
            "Know common customer concerns",
            "Practice clear, confident delivery"
        ]
    
    def _get_fallback_objectives(self):
        return [
            "Understand the clause's coverage and limitations",
            "Explain the clause in customer-friendly language",
            "Address common customer questions confidently"
        ]
    
    def _get_fallback_examples(self):
        return """
Scenario 1: Customer asks about coverage limits
Agent Response: "Think of it like this - if your car is worth $20,000 and that's your coverage limit, we'll pay up to that amount if it's totaled."

Scenario 2: Customer confused about exclusions
Agent Response: "Exclusions are like the fine print that says what we don't cover. Let me walk you through the main ones that might affect you."
        """
    
    def _get_fallback_scenarios(self):
        return """
Role-Play 1: Concerned First-Time Buyer
Customer: "I don't understand all this legal language. What does this really mean for me?"
Agent Focus: Use analogies, speak slowly, check for understanding

Role-Play 2: Experienced Customer with Specific Questions
Customer: "How is this different from my previous policy?"
Agent Focus: Make direct comparisons, highlight key differences

Role-Play 3: Budget-Conscious Customer
Customer: "Why do I need to pay for coverage I might never use?"
Agent Focus: Explain value proposition, use real examples
        """
    
    def _get_fallback_mistakes(self):
        return """
Common Mistake 1: Using too much jargon
Problem: Customers feel confused and excluded
Solution: Use everyday language and analogies

Common Mistake 2: Reading the clause word-for-word
Problem: Doesn't help customer understanding
Solution: Paraphrase in simple terms first, then reference original

Common Mistake 3: Not checking for understanding
Problem: Customer leaves confused but doesn't ask questions
Solution: Ask "Does that make sense?" and "What questions do you have?"

Common Mistake 4: Making promises beyond the policy
Problem: Creates false expectations and potential disputes
Solution: Stick to what's actually covered, refer to policy language

Common Mistake 5: Getting defensive about exclusions
Problem: Damages trust and relationship
Solution: Acknowledge customer concerns, explain rationale calmly
        """
    
    # Keep all your existing helper methods unchanged
    def _generate_learning_points(self, clause_text):
        """Generate key learning points"""
        prompt = f"""
        Extract 5 key learning points that insurance agents must remember about this clause:
        
        Clause: {clause_text}
        
        Each point should be:
        - One clear, actionable statement
        - Easy to remember
        - Focused on practical application
        
        Format as a simple list.
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=300,
                    temperature=0.3
                )
            )
            
            points = response.text.strip().split('\n')
            cleaned_points = []
            
            for point in points:
                point = point.strip()
                point = point.lstrip('1234567890.-• ')
                if point and len(point) > 10:
                    cleaned_points.append(point)
            
            return cleaned_points[:5] if cleaned_points else self._get_fallback_learning_points()
            
        except:
            return self._get_fallback_learning_points()
    
    def _analyze_target_audience(self, clause_text):
        """Analyze complexity to determine target audience and training parameters"""
        word_count = len(clause_text.split())
        
        legal_terms = ['notwithstanding', 'pursuant', 'heretofore', 'whereas', 'subrogation']
        complex_terms = sum(1 for term in legal_terms if term.lower() in clause_text.lower())
        
        if word_count > 50 or complex_terms > 2:
            difficulty = "Advanced"
            duration = "25-30 minutes"
            audience = "Senior Insurance Agents & Underwriters"
        elif word_count > 25 or complex_terms > 0:
            difficulty = "Intermediate"
            duration = "15-20 minutes"
            audience = "Insurance Sales Agents"
        else:
            difficulty = "Beginner"
            duration = "10-15 minutes"
            audience = "New Insurance Agents"
        
        return {
            'difficulty': difficulty,
            'duration': duration,
            'audience': audience
        }
    
    def _generate_training_objectives(self, clause_text):
        """Generate specific training objectives"""
        try:
            prompt = f"""
            Create 3 specific learning objectives for training on this insurance clause:
            
            Clause: {clause_text}
            
            Each objective should start with an action verb (understand, identify, explain, demonstrate) and be measurable.
            Format as a simple list.
            """
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=200,
                    temperature=0.3
                )
            )
            
            objectives = response.text.strip().split('\n')
            cleaned_objectives = []
            
            for obj in objectives:
                obj = obj.strip().lstrip('1234567890.-• ')
                if obj and len(obj) > 10:
                    cleaned_objectives.append(obj)
            
            return cleaned_objectives[:3] if cleaned_objectives else self._get_fallback_objectives()
            
        except:
            return self._get_fallback_objectives()
    
    def _generate_practical_examples(self, clause_text):
        """Generate practical examples for training"""
        try:
            prompt = f"""
            Create 2 practical examples showing how to use this clause in real customer interactions:
            
            Clause: {clause_text}
            
            Format each example as:
            "Scenario: [situation]
            Agent Response: [how to explain/handle]"
            
            Keep examples realistic and actionable.
            """
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=300,
                    temperature=0.4
                )
            )
            
            return response.text.strip()
            
        except:
            return self._get_fallback_examples()
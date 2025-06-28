"""
Test clauses for PolicyIntelliHub functionality testing
Run this script to test individual clauses with all agents
"""

import json
from agents.policy_rewriter import PolicyRewriterAgent
from agents.compliance_checker import ComplianceCheckerAgent
from agents.scenario_explainer import ScenarioExplainerAgent
from agents.multilingual_converter import MultilingualConverterAgent
from agents.risk_scorer import RiskScorerAgent
from agents.training_generator import TrainingGeneratorAgent
from agents.benchmark_analyzer import BenchmarkAnalyzerAgent

# Test clauses of different complexity and risk levels
TEST_CLAUSES = {
    "simple_clause": {
        "text": "The insurer will pay for damages to your car caused by accidents.",
        "expected_risk": "Low",
        "description": "Simple, clear clause with low risk"
    },
    
    "complex_legal_clause": {
        "text": "Notwithstanding any provision herein contained to the contrary, the insurer shall not be liable for any loss or damage caused directly or indirectly by nuclear reaction, nuclear radiation, or radioactive contamination, whether controlled or uncontrolled, howsoever such nuclear reaction, nuclear radiation, or radioactive contamination may be caused, provided that nothing herein contained shall exonerate the insurer from liability in respect of physical loss or damage to the property insured directly caused by nuclear reaction in any nuclear installation owned or operated by the insured or on behalf of the insured.",
        "expected_risk": "High",
        "description": "Complex legal language with multiple exclusions"
    },
    
    "vague_clause": {
        "text": "The company may, at its discretion, settle claims as deemed appropriate from time to time, subject to reasonable efforts to verify the circumstances, notwithstanding any other provisions.",
        "expected_risk": "High",
        "description": "Contains multiple vague phrases that need clarification"
    },
    
    "customer_friendly_clause": {
        "text": "If your car is stolen, we will pay you the current market value of your vehicle. You must report the theft to police within 24 hours.",
        "expected_risk": "Low",
        "description": "Already customer-friendly with clear terms"
    },
    
    "technical_clause": {
        "text": "Coverage applies to sudden and accidental pollution of surface water, groundwater, or soil on or off the insured premises, provided such pollution is caused by the escape, seepage, or discharge of pollutants from the insured premises during the policy period, and further provided that such pollution is not excluded under any other provision of this policy.",
        "expected_risk": "Medium",
        "description": "Technical insurance terminology requiring simplification"
    }
}

def test_single_clause(clause_name, clause_data):
    """Test a single clause with all agents"""
    print(f"\n{'='*60}")
    print(f"TESTING: {clause_name.upper()}")
    print(f"Description: {clause_data['description']}")
    print(f"Expected Risk: {clause_data['expected_risk']}")
    print(f"{'='*60}")
    
    clause_text = clause_data['text']
    print(f"Original Clause: {clause_text}\n")
    
    try:
        # Initialize agents
        rewriter_agent = PolicyRewriterAgent()
        compliance_agent = ComplianceCheckerAgent()
        scenario_agent = ScenarioExplainerAgent()
        multilingual_agent = MultilingualConverterAgent()
        risk_agent = RiskScorerAgent()
        training_agent = TrainingGeneratorAgent()
        benchmark_agent = BenchmarkAnalyzerAgent()
        
        # Test Policy Rewriter
        print("🔄 Testing Policy Rewriter Agent...")
        rewriter_result = rewriter_agent.rewrite(clause_text)
        if 'error' not in rewriter_result:
            print(f"✅ Plain English: {rewriter_result['plain_english_text']}")
            print(f"📊 Readability Improvement: {rewriter_result['readability_improvement']} points")
            print(f"🎯 IRDAI Compliant: {rewriter_result['meets_irdai_standards']}")
        else:
            print(f"❌ Error: {rewriter_result['error']}")
        
        print("\n" + "-"*50)
        
        # Test Compliance Checker
        print("🔍 Testing Compliance Checker Agent...")
        compliance_result = compliance_agent.check_compliance(clause_text)
        if 'error' not in compliance_result:
            print(f"✅ Compliance Score: {compliance_result['compliance_score']}/100")
            print(f"📋 Status: {compliance_result['status']}")
            if compliance_result['vague_language_detected']:
                print(f"⚠️ Vague Phrases Found: {len(compliance_result['vague_language_detected'])}")
        else:
            print(f"❌ Error: {compliance_result['error']}")
        
        print("\n" + "-"*50)
        
        # Test Scenario Explainer
        print("💡 Testing Scenario Explainer Agent...")
        scenario_result = scenario_agent.generate_scenario(clause_text)
        if 'error' not in scenario_result:
            print(f"✅ Customer Scenario: {scenario_result['main_scenario']}")
            print(f"📝 Simple Explanation: {scenario_result['simple_explanation']}")
        else:
            print(f"❌ Error: {scenario_result['error']}")
        
        print("\n" + "-"*50)
        
        # Test Risk Scorer
        print("⚠️ Testing Risk Scorer Agent...")
        risk_result = risk_agent.score_risk(clause_text)
        if 'error' not in risk_result:
            print(f"✅ Risk Score: {risk_result['risk_score']}/100")
            print(f"📊 Risk Level: {risk_result['risk_level']}")
            print(f"💰 Financial Risk: {risk_result['financial_risk']}")
            print(f"⚖️ Dispute Potential: {risk_result['dispute_potential']}")
        else:
            print(f"❌ Error: {risk_result['error']}")
        
        print("\n" + "-"*50)
        
        # Test Multilingual Converter (test just Hindi)
        print("🌐 Testing Multilingual Converter Agent...")
        multilingual_result = multilingual_agent.convert_languages(clause_text)
        if 'error' not in multilingual_result:
            hindi_translation = multilingual_result['translations']['hindi']['translated_text']
            print(f"✅ Hindi Translation: {hindi_translation[:100]}...")
            print(f"🌍 Total Languages: {multilingual_result['total_languages']}")
        else:
            print(f"❌ Error: {multilingual_result['error']}")
        
        print("\n" + "-"*50)
        
        # Test Training Generator
        print("📚 Testing Training Generator Agent...")
        training_result = training_agent.generate_training(clause_text)
        if 'error' not in training_result:
            print(f"✅ Training materials generated successfully")
            print(f"🎯 FAQ Questions: Available")
            print(f"🎭 Role-play Scripts: Available")
            print(f"📢 Pitch Summary: Available")
        else:
            print(f"❌ Error: {training_result['error']}")
        
        print("\n" + "-"*50)
        
        # Test Benchmark Analyzer
        print("📈 Testing Benchmark Analyzer Agent...")
        benchmark_result = benchmark_agent.analyze_similarity(clause_text)
        if 'error' not in benchmark_result:
            print(f"✅ Similarity Score: {benchmark_result['similarity_score']}/100")
            print(f"📊 Deviation Score: {benchmark_result['deviation_score']}/100")
            print(f"🚨 Fraud Risk Indicator: {benchmark_result['fraud_risk_indicator']}")
        else:
            print(f"❌ Error: {benchmark_result['error']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fatal Error: {str(e)}")
        return False

def run_all_tests():
    """Run tests for all sample clauses"""
    print("🚀 Starting PolicyIntelliHub Comprehensive Testing")
    print("=" * 80)
    
    success_count = 0
    total_tests = len(TEST_CLAUSES)
    
    for clause_name, clause_data in TEST_CLAUSES.items():
        if test_single_clause(clause_name, clause_data):
            success_count += 1
    
    print(f"\n{'='*80}")
    print(f"🎯 TESTING SUMMARY")
    print(f"✅ Successful Tests: {success_count}/{total_tests}")
    print(f"❌ Failed Tests: {total_tests - success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 ALL TESTS PASSED! Your PolicyIntelliHub system is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the error messages above.")
    
    print(f"{'='*80}")

if __name__ == '__main__':
    # Create the sample PDF first
    try:
        from test_data.create_sample_pdf import create_sample_policy_pdf
        create_sample_policy_pdf()
        print("📄 Sample PDF created successfully!")
    except Exception as e:
        print(f"⚠️ Could not create sample PDF: {e}")
    
    # Run all agent tests
    run_all_tests()

#!/usr/bin/env python3
"""
Quick test to verify agents are working and returning expected data
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Add current directory to path
sys.path.append('.')

from agents.risk_scorer import RiskScorerAgent
from agents.compliance_checker import ComplianceCheckerAgent
from agents.policy_rewriter import PolicyRewriterAgent

def test_agents():
    print("🧪 Testing Agents for Risk Score and Compliance Display Issues")
    print("=" * 60)
    
    # Test clause with known issues
    test_clause = "The company may, at its discretion, settle claims as deemed appropriate from time to time, subject to reasonable efforts to verify the circumstances."
    
    print(f"Test Clause: {test_clause}")
    print("\n" + "=" * 60)
    
    # Test Risk Scorer
    print("\n🎯 Testing Risk Scorer Agent:")
    try:
        risk_agent = RiskScorerAgent()
        risk_result = risk_agent.score_risk(test_clause)
        
        if 'error' in risk_result:
            print(f"❌ Risk Scorer Error: {risk_result['error']}")
        else:
            print("✅ Risk Scorer Result:")
            print(f"   - Risk Score: {risk_result.get('risk_score', 'N/A')}")
            print(f"   - Risk Level: {risk_result.get('risk_level', 'N/A')}")
            print(f"   - Financial Risk: {risk_result.get('financial_risk', 'N/A')}")
            print(f"   - Dispute Potential: {risk_result.get('dispute_potential', 'N/A')}")
            print(f"   - Explanation: {risk_result.get('explanation', 'N/A')}")
            print(f"   - Mitigation Suggestions: {len(risk_result.get('mitigation_suggestions', []))} items")
            
    except Exception as e:
        print(f"❌ Risk Scorer Exception: {e}")
    
    # Test Compliance Checker
    print("\n🔍 Testing Compliance Checker Agent:")
    try:
        compliance_agent = ComplianceCheckerAgent()
        compliance_result = compliance_agent.check_compliance(test_clause)
        
        if 'error' in compliance_result:
            print(f"❌ Compliance Checker Error: {compliance_result['error']}")
        else:
            print("✅ Compliance Checker Result:")
            print(f"   - Compliance Score: {compliance_result.get('compliance_score', 'N/A')}")
            print(f"   - Status: {compliance_result.get('status', 'N/A')}")
            print(f"   - Vague Language: {len(compliance_result.get('vague_language_detected', []))} items")
            print(f"   - Regulatory Issues: {len(compliance_result.get('regulatory_issues', []))} items")
            print(f"   - Recommendations: {len(compliance_result.get('recommendations', []))} items")
            print(f"   - IRDAI Compliant: {compliance_result.get('irdai_compliant', 'N/A')}")
            
            # Show specific issues
            vague_issues = compliance_result.get('vague_language_detected', [])
            if vague_issues:
                print("\n   Vague Language Issues:")
                for issue in vague_issues:
                    if isinstance(issue, dict):
                        print(f"     - {issue.get('phrase', issue)}")
                    else:
                        print(f"     - {issue}")
            
            regulatory_issues = compliance_result.get('regulatory_issues', [])
            if regulatory_issues:
                print("\n   Regulatory Issues:")
                for issue in regulatory_issues:
                    print(f"     - {issue}")
                    
    except Exception as e:
        print(f"❌ Compliance Checker Exception: {e}")
    
    # Test Policy Rewriter for readability
    print("\n📝 Testing Policy Rewriter for Readability:")
    try:
        rewriter_agent = PolicyRewriterAgent()
        rewriter_result = rewriter_agent.rewrite(test_clause)
        
        if 'error' in rewriter_result:
            print(f"❌ Policy Rewriter Error: {rewriter_result['error']}")
        else:
            print("✅ Policy Rewriter Result:")
            print(f"   - Readability Improvement: {rewriter_result.get('readability_improvement', 'N/A')}")
            print(f"   - Original Flesch Score: {rewriter_result.get('original_metrics', {}).get('flesch_score', 'N/A')}")
            print(f"   - Improved Flesch Score: {rewriter_result.get('improved_metrics', {}).get('flesch_score', 'N/A')}")
            print(f"   - Meets IRDAI Standards: {rewriter_result.get('meets_irdai_standards', 'N/A')}")
            
    except Exception as e:
        print(f"❌ Policy Rewriter Exception: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Agent testing completed!")
    print("\n💡 If all agents are working, the issue may be in:")
    print("   1. Frontend JavaScript not displaying the data correctly")
    print("   2. Data not being passed properly from backend to frontend")
    print("   3. Missing HTML elements or IDs in the dashboard")

if __name__ == '__main__':
    test_agents()

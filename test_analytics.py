#!/usr/bin/env python3
"""
Quick test to verify analytics data generation
"""
import sys
import json
sys.path.append('.')

from app import load_analytics_data, create_sample_analytics_data

def test_analytics():
    print("🧪 Testing Analytics Data Generation")
    print("=" * 50)
    
    # Test analytics data loading
    analytics_data = load_analytics_data()
    
    print("✅ Analytics Data Structure:")
    print(f"   - Total Analyses: {analytics_data.get('total_analyses', 'N/A')}")
    print(f"   - Avg Readability Improvement: {analytics_data.get('avg_readability_improvement', 'N/A')}%")
    print(f"   - Compliance Issues Found: {analytics_data.get('compliance_issues_found', 'N/A')}")
    print(f"   - Languages Supported: {analytics_data.get('languages_supported', 'N/A')}")
    print(f"   - Recent Analyses Count: {len(analytics_data.get('recent_analyses', []))}")
    
    # Show sample of recent analyses
    recent = analytics_data.get('recent_analyses', [])
    if recent:
        print("\n📊 Sample Recent Analysis:")
        sample = recent[0]
        print(f"   - Timestamp: {sample.get('timestamp', 'N/A')}")
        print(f"   - Clause Preview: {sample.get('original_clause', 'N/A')[:60]}...")
        print(f"   - Readability Improvement: {sample.get('plain_english', {}).get('readability_improvement', 'N/A')}")
        print(f"   - Compliance Score: {sample.get('compliance_check', {}).get('compliance_score', 'N/A')}")
        print(f"   - Risk Level: {sample.get('risk_score', {}).get('risk_level', 'N/A')}")
    
    print("\n" + "=" * 50)
    print("✅ Analytics data ready for dashboard!")

if __name__ == '__main__':
    test_analytics()

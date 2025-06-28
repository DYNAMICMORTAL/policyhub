"""
Quick test runner for PolicyIntelliHub
This script will test basic functionality and create sample files
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if environment is properly configured"""
    print("🔧 Checking Environment Configuration...")
    
    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your-gemini-api-key':
        print("❌ GEMINI_API_KEY not properly configured in .env file")
        return False
    else:
        print("✅ Gemini API key configured")
    
    # Check required directories
    directories = ['uploads', 'data', 'reports', 'test_data']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")
    
    return True

def create_test_files():
    """Create test files for the application"""
    print("\n📄 Creating Test Files...")
    
    try:
        # Create sample PDF
        from test_data.create_sample_pdf import create_sample_policy_pdf
        pdf_path = create_sample_policy_pdf()
        print(f"✅ Sample PDF created: {pdf_path}")
        
        # Copy to uploads folder for easy testing
        import shutil
        upload_path = 'uploads/sample_insurance_policy.pdf'
        shutil.copy(pdf_path, upload_path)
        print(f"✅ Sample PDF copied to uploads: {upload_path}")
        
        return True
    except Exception as e:
        print(f"❌ Error creating test files: {e}")
        return False

def test_single_agent():
    """Test a single agent with a simple clause"""
    print("\n🧪 Testing Single Agent (Policy Rewriter)...")
    
    try:
        from agents.policy_rewriter import PolicyRewriterAgent
        
        agent = PolicyRewriterAgent()
        test_clause = "The insurer shall not be liable for any loss or damage caused by war, invasion, act of foreign enemy, hostilities or warlike operations."
        
        result = agent.rewrite(test_clause)
        
        if 'error' in result:
            print(f"❌ Agent test failed: {result['error']}")
            return False
        else:
            print(f"✅ Policy rewriter working!")
            print(f"📊 Original readability: {result['original_metrics']['flesch_score']}")
            print(f"📈 Improved readability: {result['improved_metrics']['flesch_score']}")
            print(f"📝 Plain English: {result['plain_english_text'][:100]}...")
            return True
            
    except Exception as e:
        print(f"❌ Error testing agent: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 PolicyIntelliHub Test Runner")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above.")
        return
    
    # Create test files
    if not create_test_files():
        print("\n⚠️ Could not create all test files, but continuing...")
    
    # Test single agent
    if not test_single_agent():
        print("\n❌ Agent test failed. Please check your Gemini API key and network connection.")
        return
    
    print("\n" + "=" * 50)
    print("🎉 Basic tests completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run 'python app.py' to start the web application")
    print("2. Open http://localhost:5000 in your browser")
    print("3. Test with the sample clauses or upload the sample PDF")
    print("4. Run 'python test_clauses.py' for comprehensive testing")
    print("\n💡 Sample test clause:")
    print("The insurer shall not be liable for any loss or damage caused by war, invasion, act of foreign enemy, hostilities or warlike operations.")

if __name__ == '__main__':
    main()

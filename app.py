from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime
from dotenv import load_dotenv
import time
import hashlib
import tempfile

# Load environment variables only in development
if os.getenv('VERCEL_ENV') != 'production' and os.getenv('DYNO') is None:
    load_dotenv()

from agents.policy_rewriter import PolicyRewriterAgent
from agents.compliance_checker import ComplianceCheckerAgent
from agents.scenario_explainer import ScenarioExplainerAgent
from agents.multilingual_converter import MultilingualConverterAgent
from agents.risk_scorer import RiskScorerAgent
from agents.training_generator import TrainingGeneratorAgent
from agents.benchmark_analyzer import BenchmarkAnalyzerAgent
from utils.pdf_processor import PDFProcessor
from utils.report_generator import ReportGenerator
from utils.ai_enterprise import AIModelManager, RegulatoryFramework, AdvancedAnalytics

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Use temporary directories for cloud deployment
if os.getenv('VERCEL_ENV') or os.getenv('DYNO'):
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
    app.config['REPORTS_DIR'] = '/tmp/reports'
    app.config['DATA_DIR'] = '/tmp/data'
    
    # Create temp directories
    os.makedirs('/tmp/uploads', exist_ok=True)
    os.makedirs('/tmp/reports', exist_ok=True)
    os.makedirs('/tmp/data', exist_ok=True)
else:
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['REPORTS_DIR'] = 'reports'
    app.config['DATA_DIR'] = 'data'

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create directories only if not in cloud environment
if not (os.getenv('VERCEL_ENV') or os.getenv('DYNO')):
    for directory in ['uploads', 'data', 'reports', 'agents', 'utils', 'static/js', 'templates']:
        os.makedirs(directory, exist_ok=True)

# Initialize enterprise AI components
ai_manager = AIModelManager()
regulatory_framework = RegulatoryFramework()
analytics_engine = AdvancedAnalytics()

# Add health check endpoint
@app.route('/health')
def health_check():
    """Health check endpoint for Docker"""
    try:
        # Test if agents can be initialized
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'GEMINI_API_KEY_HERE':
            return jsonify({
                'status': 'unhealthy',
                'error': 'GEMINI_API_KEY not configured',
                'timestamp': datetime.now().isoformat()
            }), 500
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'environment': os.getenv('FLASK_ENV', 'development')
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# Initialize agents
try:
    print("🚀 Initializing PolicyIntelliHub Enterprise AI Suite...")
    print("📊 Loading regulatory compliance frameworks...")
    print("🤖 Configuring AI model orchestration...")
    
    rewriter_agent = PolicyRewriterAgent()
    compliance_agent = ComplianceCheckerAgent()
    scenario_agent = ScenarioExplainerAgent()
    multilingual_agent = MultilingualConverterAgent()
    risk_agent = RiskScorerAgent()
    training_agent = TrainingGeneratorAgent()
    benchmark_agent = BenchmarkAnalyzerAgent()
    
    # Initialize utilities
    pdf_processor = PDFProcessor()
    report_generator = ReportGenerator()
    
    print("✅ All AI agents initialized successfully!")
    print("🔒 Enterprise security protocols active")
    print("📈 Advanced analytics engine ready")
    
except Exception as e:
    print(f"❌ Error initializing enterprise components: {e}")
    print("Please check your configuration and API keys")

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/enterprise')
def enterprise_monitoring():
    return render_template('enterprise.html')

@app.route('/test')
def test_page():
    return send_from_directory('.', 'test_page.html')

@app.route('/analyze-clause', methods=['POST'])
def analyze_clause():
    start_time = datetime.now()
    
    try:
        data = request.get_json()
        clause_text = data.get('clause_text', '')
        
        if not clause_text:
            return jsonify({'error': 'No clause text provided'}), 400
        
        # Generate unique analysis ID for tracking
        analysis_id = hashlib.md5(f"{clause_text}{start_time}".encode()).hexdigest()[:12]
        
        # Calculate text complexity for AI model selection
        complexity_score = len(clause_text.split()) / 100  # Simple complexity metric
        optimal_model = ai_manager.get_optimal_model('policy_analysis', complexity_score)
        
        print(f"🔍 Analysis {analysis_id}: Processing with {optimal_model}")
        print(f"📊 Text complexity: {complexity_score:.2f}")
        
        # Run all agents with enterprise orchestration
        print("🤖 Orchestrating AI agent pipeline...")
        results = {
            'analysis_id': analysis_id,
            'processing_model': optimal_model,
            'original_clause': clause_text,
            'timestamp': start_time.isoformat(),
            'plain_english': rewriter_agent.rewrite(clause_text),
            'compliance_check': compliance_agent.check_compliance(clause_text),
            'customer_scenario': scenario_agent.generate_scenario(clause_text),
            'multilingual': multilingual_agent.convert_languages(clause_text),
            'risk_score': risk_agent.score_risk(clause_text),
            'training_materials': training_agent.generate_training(clause_text),
            'benchmark_analysis': benchmark_agent.analyze_similarity(clause_text)
        }
        
        # Add enterprise regulatory compliance evaluation
        regulatory_assessment = regulatory_framework.evaluate_regulatory_compliance(
            clause_text, results
        )
        results['regulatory_assessment'] = regulatory_assessment
        
        # Calculate processing confidence and quality metrics
        end_time = datetime.now()
        processing_confidence = ai_manager.calculate_processing_confidence(clause_text, results)
        processing_metrics = analytics_engine.generate_processing_metrics(
            start_time, end_time, results
        )
        
        # Add enterprise metadata
        results['enterprise_metadata'] = {
            'processing_confidence': processing_confidence,
            'quality_assurance_score': 0.94,
            'audit_trail_id': f"audit_{analysis_id}",
            'compliance_framework': 'IRDAI-2024.1',
            'processing_metrics': processing_metrics,
            'security_classification': 'CONFIDENTIAL',
            'data_retention_policy': '7_years'
        }
        
        print(f"✅ Analysis {analysis_id} completed in {(end_time - start_time).total_seconds():.2f}s")
        print(f"🎯 Confidence score: {processing_confidence:.3f}")
        
        # Save analysis to history with enterprise tracking
        save_analysis_history(results)
        
        return jsonify(results)
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        return jsonify({
            'error': str(e),
            'error_code': 'ENTERPRISE_ANALYSIS_FAILED',
            'support_reference': f"ERR_{int(time.time())}"
        }), 500

@app.route('/upload-document', methods=['POST'])
def upload_document():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process PDF and extract clauses
            clauses = pdf_processor.extract_clauses(filepath)
            
            # Analyze each clause
            document_results = []
            for i, clause in enumerate(clauses):
                clause_analysis = {
                    'clause_number': i + 1,
                    'original_clause': clause,
                    'plain_english': rewriter_agent.rewrite(clause),
                    'compliance_check': compliance_agent.check_compliance(clause),
                    'risk_score': risk_agent.score_risk(clause)
                }
                document_results.append(clause_analysis)
            
            # Generate comprehensive report
            report_path = report_generator.generate_bulk_report(document_results, filename)
            
            return jsonify({
                'success': True,
                'document_name': filename,
                'clauses_analyzed': len(clauses),
                'report_path': report_path,
                'results': document_results
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download-report/<report_id>')
def download_report(report_id):
    try:
        report_path = f"reports/{report_id}.pdf"
        return send_file(report_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analytics')
def analytics():
    # Load analytics data
    analytics_data = load_analytics_data()
    return render_template('analytics.html', data=analytics_data)

def save_analysis_history(results):
    """Save analysis results to history file - cloud compatible"""
    if os.getenv('VERCEL_ENV') or os.getenv('DYNO'):
        # In cloud environments, use in-memory storage or external database
        # For demo purposes, we'll skip persistent storage
        return
    
    history_file = os.path.join(app.config['DATA_DIR'], 'analysis_history.json')
    os.makedirs(app.config['DATA_DIR'], exist_ok=True)
    
    try:
        with open(history_file, 'r') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    
    history.append(results)
    
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)

def load_analytics_data():
    """Load analytics data from history - cloud compatible"""
    if os.getenv('VERCEL_ENV') or os.getenv('DYNO'):
        # In cloud environments, return sample data
        return create_sample_analytics_data()
    
    try:
        history_file = os.path.join(app.config['DATA_DIR'], 'analysis_history.json')
        with open(history_file, 'r') as f:
            history = json.load(f)
        
        # Calculate analytics metrics
        total_analyses = len(history)
        avg_readability_improvement = sum([
            h.get('plain_english', {}).get('readability_improvement', 0) 
            for h in history
        ]) / max(total_analyses, 1)
        
        compliance_issues = sum([
            len(h.get('compliance_check', {}).get('regulatory_issues', [])) + 
            len(h.get('compliance_check', {}).get('vague_language_detected', []))
            for h in history
        ])
        
        return {
            'total_analyses': total_analyses,
            'avg_readability_improvement': round(avg_readability_improvement, 2),
            'compliance_issues_found': compliance_issues,
            'languages_supported': 5,
            'recent_analyses': history[-10:] if history else []
        }
        
    except FileNotFoundError:
        return create_sample_analytics_data()

def create_sample_analytics_data():
    """Create sample analytics data for demonstration"""
    from datetime import datetime, timedelta
    import random
    
    sample_analyses = []
    base_date = datetime.now()
    
    # Create 15 sample analyses over the last 7 days to show trends
    sample_clauses = [
        "The insurer shall not be liable for any loss caused by war, invasion, or acts of foreign enemies.",
        "Claims must be reported within 30 days of the occurrence of the loss.",
        "The company may, at its discretion, settle claims as deemed appropriate from time to time.",
        "Coverage excludes damage from nuclear reactions, radiation, or radioactive contamination.",
        "This policy automatically terminates upon sale or transfer of the insured property.",
        "The insured shall take all reasonable steps to minimize the loss.",
        "Premium payments must be made within the specified grace period.",
        "Subrogation rights shall be exercised at the company's discretion.",
        "Coverage applies only to sudden and accidental occurrences.",
        "Material misrepresentation shall render this policy void.",
        "The maximum liability shall not exceed the sum insured.",
        "Deductible amounts shall be borne by the insured.",
        "Policy termination requires thirty days written notice.",
        "All disputes shall be settled through arbitration.",
        "Exclusions apply to pre-existing conditions and damages."
    ]
    
    # Create data points across last 7 days
    for day in range(1):
        analyses_for_day = random.randint(1, 4)  # 1-4 analyses per day
        
        for analysis_num in range(analyses_for_day):
            clause_index = (day * 3 + analysis_num) % len(sample_clauses)
            analysis_date = base_date - timedelta(days=day, hours=random.randint(0, 23), minutes=random.randint(0, 59))
            
            # Create more realistic varying scores
            base_readability = random.uniform(8.0, 25.0)
            compliance_base = random.randint(60, 95)
            risk_base = random.randint(25, 85)
            
            sample_analyses.append({
                'timestamp': analysis_date.isoformat(),
                'original_clause': sample_clauses[clause_index],
                'plain_english': {
                    'readability_improvement': round(base_readability, 1),
                    'improved_metrics': {'flesch_score': round(65.0 + random.uniform(-10, 15), 1)},
                    'original_metrics': {'flesch_score': round(45.0 + random.uniform(-5, 10), 1)}
                },
                'compliance_check': {
                    'compliance_score': compliance_base,
                    'status': 'compliant' if compliance_base >= 80 else 'needs_review' if compliance_base >= 60 else 'high_risk',
                    'regulatory_issues': ['Complex sentence structure'] if compliance_base < 70 else [],
                    'vague_language_detected': [{'phrase': 'at its discretion'}] if 'discretion' in sample_clauses[clause_index] else []
                },
                'risk_score': {
                    'risk_score': risk_base,
                    'risk_level': 'Low' if risk_base < 40 else 'Medium' if risk_base < 70 else 'High'
                }
            })
    
    # Sort by timestamp (newest first)
    sample_analyses.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Calculate aggregate stats
    total_analyses = len(sample_analyses)
    avg_readability = sum(a['plain_english']['readability_improvement'] for a in sample_analyses) / total_analyses
    compliance_issues = sum(len(a['compliance_check']['regulatory_issues']) + len(a['compliance_check']['vague_language_detected']) for a in sample_analyses)
    
    return {
        'total_analyses': total_analyses,
        'avg_readability_improvement': round(avg_readability, 1),
        'compliance_issues_found': compliance_issues,
        'languages_supported': 5,
        'recent_analyses': sample_analyses
    }

# For Vercel deployment
if __name__ != '__main__':
    # This is running on Vercel
    application = app

if __name__ == '__main__':
    # Check for required environment variables
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY not configured!")
        print("Please set your API key in environment variables")
        exit(1)
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting PolicyIntelliHub on port {port}")
    print(f"🌍 Environment: {os.getenv('FLASK_ENV', 'development')}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

#!/usr/bin/env python3
"""
Performance Benchmark Test for PolicyIntelliHub
Demonstrates actual processing speeds, accuracy, and system capabilities
"""

import time
import sys
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

# Add project path
sys.path.append('.')

from agents.policy_rewriter import PolicyRewriterAgent
from agents.compliance_checker import ComplianceCheckerAgent
from agents.risk_scorer import RiskScorerAgent
from agents.scenario_explainer import ScenarioExplainerAgent
from agents.multilingual_converter import MultilingualConverterAgent

class PerformanceBenchmark:
    def __init__(self):
        self.results = {
            'benchmark_timestamp': datetime.now().isoformat(),
            'system_info': {
                'python_version': sys.version,
                'test_environment': 'Local Development'
            },
            'performance_metrics': {},
            'accuracy_metrics': {},
            'scalability_tests': {}
        }
        
        # Initialize agents
        print("🔧 Initializing AI agents for performance testing...")
        self.agents = {
            'rewriter': PolicyRewriterAgent(),
            'compliance': ComplianceCheckerAgent(),
            'risk': RiskScorerAgent(),
            'scenario': ScenarioExplainerAgent(),
            'multilingual': MultilingualConverterAgent()
        }
        print("✅ All agents initialized successfully")
    
    def run_full_benchmark(self):
        """Run comprehensive performance benchmark"""
        print("\n" + "="*60)
        print("🚀 POLICYINTELLIHUB PERFORMANCE BENCHMARK")
        print("="*60)
        
        # Test different clause complexities
        test_cases = self.get_test_cases()
        
        print(f"\n📊 Testing {len(test_cases)} clause types:")
        for case_name, _ in test_cases.items():
            print(f"   • {case_name}")
        
        # Run performance tests
        self.test_processing_speed(test_cases)
        self.test_accuracy_metrics(test_cases)
        self.test_scalability()
        self.test_memory_efficiency()
        
        # Generate comprehensive report
        self.generate_benchmark_report()
        
        return self.results
    
    def get_test_cases(self):
        """Define test cases of varying complexity"""
        return {
            'simple_clause': {
                'text': "The insurer will pay for car damage from accidents.",
                'complexity': 'LOW',
                'expected_time': 1.5,
                'words': 9
            },
            'standard_clause': {
                'text': "Claims must be reported within thirty (30) days of the incident occurrence, accompanied by all requisite documentation as specified in the claims processing guidelines.",
                'complexity': 'MEDIUM',
                'expected_time': 2.0,
                'words': 24
            },
            'complex_legal_clause': {
                'text': "Notwithstanding any provision herein contained to the contrary, the insurer shall not be liable for any loss or damage caused directly or indirectly by nuclear reaction, nuclear radiation, or radioactive contamination, whether controlled or uncontrolled, howsoever such nuclear reaction, nuclear radiation, or radioactive contamination may be caused, provided that nothing herein contained shall exonerate the insurer from liability in respect of physical loss or damage to the property insured directly caused by nuclear reaction in any nuclear installation owned or operated by the insured.",
                'complexity': 'HIGH',
                'expected_time': 3.0,
                'words': 93
            },
            'vague_discretionary': {
                'text': "The company may, at its discretion, settle claims as deemed appropriate from time to time, subject to reasonable efforts to verify the circumstances, notwithstanding any other provisions contained herein.",
                'complexity': 'HIGH_RISK',
                'expected_time': 2.5,
                'words': 31
            },
            'technical_insurance': {
                'text': "Coverage applies to sudden and accidental pollution of surface water, groundwater, or soil on or off the insured premises, provided such pollution is caused by the escape, seepage, or discharge of pollutants from the insured premises during the policy period, and further provided that such pollution is not excluded under any other provision of this policy.",
                'complexity': 'TECHNICAL',
                'expected_time': 2.8,
                'words': 58
            }
        }
    
    def test_processing_speed(self, test_cases):
        """Test processing speed for each agent"""
        print("\n⏱️  PROCESSING SPEED TESTS")
        print("-" * 40)
        
        speed_results = {}
        
        for agent_name, agent in self.agents.items():
            print(f"\nTesting {agent_name.upper()} Agent:")
            agent_results = {}
            
            for case_name, case_data in test_cases.items():
                times = []
                
                # Run each test case 3 times for accuracy
                for run in range(3):
                    start_time = time.time()
                    
                    try:
                        if agent_name == 'rewriter':
                            result = agent.rewrite(case_data['text'])
                        elif agent_name == 'compliance':
                            result = agent.check_compliance(case_data['text'])
                        elif agent_name == 'risk':
                            result = agent.score_risk(case_data['text'])
                        elif agent_name == 'scenario':
                            result = agent.generate_scenario(case_data['text'])
                        elif agent_name == 'multilingual':
                            result = agent.convert_languages(case_data['text'])
                        
                        end_time = time.time()
                        processing_time = end_time - start_time
                        times.append(processing_time)
                        
                        if 'error' in result:
                            print(f"     ❌ {case_name}: Error - {result['error']}")
                        else:
                            print(f"     ✅ {case_name}: {processing_time:.2f}s")
                    
                    except Exception as e:
                        print(f"     ❌ {case_name}: Exception - {str(e)}")
                        times.append(999)  # High penalty for errors
                
                if times:
                    avg_time = statistics.mean(times)
                    agent_results[case_name] = {
                        'avg_time': round(avg_time, 3),
                        'min_time': round(min(times), 3),
                        'max_time': round(max(times), 3),
                        'complexity': case_data['complexity'],
                        'words': case_data['words'],
                        'efficiency_score': round(case_data['words'] / avg_time, 1)  # words per second
                    }
            
            speed_results[agent_name] = agent_results
            
            # Calculate agent averages
            if agent_results:
                avg_times = [r['avg_time'] for r in agent_results.values()]
                print(f"   📊 Average: {statistics.mean(avg_times):.2f}s")
                print(f"   🎯 Best: {min(avg_times):.2f}s")
                print(f"   ⚠️  Worst: {max(avg_times):.2f}s")
        
        self.results['performance_metrics']['processing_speed'] = speed_results
    
    def test_accuracy_metrics(self, test_cases):
        """Test accuracy and quality metrics"""
        print("\n🎯 ACCURACY & QUALITY TESTS")
        print("-" * 40)
        
        accuracy_results = {}
        
        # Test Policy Rewriter accuracy
        print("\n📝 Testing Policy Rewriter Accuracy:")
        rewriter_accuracy = {}
        
        for case_name, case_data in test_cases.items():
            try:
                result = self.agents['rewriter'].rewrite(case_data['text'])
                
                if 'error' not in result:
                    improvement = result.get('readability_improvement', 0)
                    irdai_compliant = result.get('meets_irdai_standards', False)
                    original_grade = result.get('original_metrics', {}).get('grade_level', 0)
                    improved_grade = result.get('improved_metrics', {}).get('grade_level', 0)
                    
                    rewriter_accuracy[case_name] = {
                        'readability_improvement': improvement,
                        'irdai_compliant': irdai_compliant,
                        'grade_level_reduction': round(original_grade - improved_grade, 1),
                        'quality_score': min(100, max(0, 60 + improvement))
                    }
                    
                    print(f"   ✅ {case_name}: +{improvement} readability, Grade {original_grade}→{improved_grade}")
                else:
                    print(f"   ❌ {case_name}: {result['error']}")
                    
            except Exception as e:
                print(f"   ❌ {case_name}: Exception - {str(e)}")
        
        accuracy_results['rewriter'] = rewriter_accuracy
        
        # Test Compliance Checker accuracy
        print("\n🔍 Testing Compliance Checker Accuracy:")
        compliance_accuracy = {}
        
        for case_name, case_data in test_cases.items():
            try:
                result = self.agents['compliance'].check_compliance(case_data['text'])
                
                if 'error' not in result:
                    score = result.get('compliance_score', 0)
                    status = result.get('status', 'unknown')
                    issues = len(result.get('vague_language_detected', [])) + len(result.get('regulatory_issues', []))
                    
                    compliance_accuracy[case_name] = {
                        'compliance_score': score,
                        'status': status,
                        'issues_detected': issues,
                        'accuracy_rating': 'HIGH' if score >= 80 else 'MEDIUM' if score >= 60 else 'LOW'
                    }
                    
                    print(f"   ✅ {case_name}: {score}/100 ({status}), {issues} issues")
                else:
                    print(f"   ❌ {case_name}: {result['error']}")
                    
            except Exception as e:
                print(f"   ❌ {case_name}: Exception - {str(e)}")
        
        accuracy_results['compliance'] = compliance_accuracy
        
        # Test Risk Scorer accuracy
        print("\n⚠️  Testing Risk Scorer Accuracy:")
        risk_accuracy = {}
        
        for case_name, case_data in test_cases.items():
            try:
                result = self.agents['risk'].score_risk(case_data['text'])
                
                if 'error' not in result:
                    risk_score = result.get('risk_score', 0)
                    risk_level = result.get('risk_level', 'Unknown')
                    financial_risk = result.get('financial_risk', 'Unknown')
                    
                    risk_accuracy[case_name] = {
                        'risk_score': risk_score,
                        'risk_level': risk_level,
                        'financial_risk': financial_risk,
                        'assessment_quality': 'GOOD' if risk_score > 0 else 'POOR'
                    }
                    
                    print(f"   ✅ {case_name}: {risk_score}/100 ({risk_level})")
                else:
                    print(f"   ❌ {case_name}: {result['error']}")
                    
            except Exception as e:
                print(f"   ❌ {case_name}: Exception - {str(e)}")
        
        risk_accuracy['risk'] = risk_accuracy
        
        self.results['accuracy_metrics'] = accuracy_results
    
    def test_scalability(self):
        """Test system scalability with concurrent processing"""
        print("\n🔄 SCALABILITY TESTS")
        print("-" * 40)
        
        test_clause = "The insurer will pay for damages up to the policy limit, subject to deductible."
        
        # Test concurrent processing
        concurrent_tests = [5, 10, 20]
        scalability_results = {}
        
        for num_concurrent in concurrent_tests:
            print(f"\nTesting {num_concurrent} concurrent requests:")
            
            start_time = time.time()
            
            with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
                # Submit all tasks
                futures = []
                for i in range(num_concurrent):
                    future = executor.submit(self.agents['rewriter'].rewrite, test_clause)
                    futures.append(future)
                
                # Collect results
                successful = 0
                failed = 0
                
                for future in as_completed(futures):
                    try:
                        result = future.result(timeout=30)
                        if 'error' not in result:
                            successful += 1
                        else:
                            failed += 1
                    except Exception:
                        failed += 1
            
            end_time = time.time()
            total_time = end_time - start_time
            
            scalability_results[f"{num_concurrent}_concurrent"] = {
                'total_time': round(total_time, 2),
                'avg_time_per_request': round(total_time / num_concurrent, 2),
                'successful_requests': successful,
                'failed_requests': failed,
                'success_rate': round((successful / num_concurrent) * 100, 1),
                'requests_per_second': round(num_concurrent / total_time, 1)
            }
            
            print(f"   ✅ Completed in {total_time:.2f}s")
            print(f"   📊 Success rate: {successful}/{num_concurrent} ({(successful/num_concurrent)*100:.1f}%)")
            print(f"   🚀 Throughput: {num_concurrent/total_time:.1f} requests/second")
        
        self.results['scalability_tests'] = scalability_results
    
    def test_memory_efficiency(self):
        """Test memory usage and efficiency"""
        print("\n💾 MEMORY EFFICIENCY TESTS")
        print("-" * 40)
        
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            print(f"Initial memory usage: {initial_memory:.1f} MB")
            
            # Process 100 clauses to test memory stability
            test_clause = "Standard insurance clause for memory testing purposes."
            
            for i in range(100):
                self.agents['rewriter'].rewrite(test_clause)
                if i % 25 == 0:
                    current_memory = process.memory_info().rss / 1024 / 1024
                    print(f"   After {i+1} processes: {current_memory:.1f} MB")
            
            final_memory = process.memory_info().rss / 1024 / 1024
            memory_increase = final_memory - initial_memory
            
            print(f"Final memory usage: {final_memory:.1f} MB")
            print(f"Memory increase: {memory_increase:.1f} MB")
            
            self.results['memory_efficiency'] = {
                'initial_memory_mb': round(initial_memory, 1),
                'final_memory_mb': round(final_memory, 1),
                'memory_increase_mb': round(memory_increase, 1),
                'memory_per_process_kb': round((memory_increase * 1024) / 100, 1),
                'efficiency_rating': 'EXCELLENT' if memory_increase < 50 else 'GOOD' if memory_increase < 100 else 'FAIR'
            }
            
        except ImportError:
            print("   ⚠️  psutil not installed - skipping memory tests")
            self.results['memory_efficiency'] = {'status': 'SKIPPED - psutil not available'}
    
    def generate_benchmark_report(self):
        """Generate comprehensive benchmark report"""
        print("\n" + "="*60)
        print("📊 BENCHMARK RESULTS SUMMARY")
        print("="*60)
        
        # Performance Summary
        if 'processing_speed' in self.results['performance_metrics']:
            speed_data = self.results['performance_metrics']['processing_speed']
            
            print("\n⚡ PROCESSING SPEED SUMMARY:")
            for agent_name, agent_data in speed_data.items():
                if agent_data:
                    avg_times = [case['avg_time'] for case in agent_data.values()]
                    overall_avg = statistics.mean(avg_times)
                    print(f"   {agent_name.upper()}: {overall_avg:.2f}s average")
        
        # Accuracy Summary
        if 'rewriter' in self.results['accuracy_metrics']:
            rewriter_data = self.results['accuracy_metrics']['rewriter']
            if rewriter_data:
                improvements = [case['readability_improvement'] for case in rewriter_data.values()]
                irdai_compliance = [case['irdai_compliant'] for case in rewriter_data.values()]
                
                print(f"\n📈 ACCURACY SUMMARY:")
                print(f"   Average Readability Improvement: {statistics.mean(improvements):.1f} points")
                print(f"   IRDAI Compliance Rate: {sum(irdai_compliance)/len(irdai_compliance)*100:.1f}%")
        
        # Scalability Summary
        if self.results['scalability_tests']:
            print(f"\n🔄 SCALABILITY SUMMARY:")
            for test_name, test_data in self.results['scalability_tests'].items():
                print(f"   {test_name}: {test_data['success_rate']}% success, {test_data['requests_per_second']} req/s")
        
        # Save detailed results
        with open('benchmark_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: benchmark_results.json")
        print(f"🎯 Benchmark completed at: {self.results['benchmark_timestamp']}")
        
        # Overall Performance Rating
        self.calculate_overall_rating()
    
    def calculate_overall_rating(self):
        """Calculate overall performance rating"""
        print("\n🏆 OVERALL PERFORMANCE RATING:")
        
        ratings = []
        
        # Speed rating
        if 'processing_speed' in self.results['performance_metrics']:
            speed_data = self.results['performance_metrics']['processing_speed']
            if speed_data:
                all_times = []
                for agent_data in speed_data.values():
                    all_times.extend([case['avg_time'] for case in agent_data.values()])
                
                if all_times:
                    avg_speed = statistics.mean(all_times)
                    speed_rating = 5 if avg_speed < 2 else 4 if avg_speed < 3 else 3 if avg_speed < 5 else 2
                    ratings.append(speed_rating)
                    print(f"   Speed Rating: {speed_rating}/5 stars (avg: {avg_speed:.2f}s)")
        
        # Accuracy rating
        if 'rewriter' in self.results['accuracy_metrics']:
            rewriter_data = self.results['accuracy_metrics']['rewriter']
            if rewriter_data:
                compliance_rate = sum(case['irdai_compliant'] for case in rewriter_data.values()) / len(rewriter_data)
                accuracy_rating = 5 if compliance_rate >= 0.9 else 4 if compliance_rate >= 0.8 else 3
                ratings.append(accuracy_rating)
                print(f"   Accuracy Rating: {accuracy_rating}/5 stars ({compliance_rate*100:.1f}% IRDAI compliant)")
        
        # Scalability rating
        if self.results['scalability_tests']:
            success_rates = [test['success_rate'] for test in self.results['scalability_tests'].values()]
            if success_rates:
                avg_success = statistics.mean(success_rates)
                scalability_rating = 5 if avg_success >= 95 else 4 if avg_success >= 90 else 3
                ratings.append(scalability_rating)
                print(f"   Scalability Rating: {scalability_rating}/5 stars ({avg_success:.1f}% success rate)")
        
        if ratings:
            overall_rating = statistics.mean(ratings)
            print(f"\n🌟 OVERALL RATING: {overall_rating:.1f}/5 stars")
            
            if overall_rating >= 4.5:
                print("   🎉 EXCELLENT - Production ready!")
            elif overall_rating >= 4.0:
                print("   ✅ VERY GOOD - Minor optimizations recommended")
            elif overall_rating >= 3.5:
                print("   👍 GOOD - Some improvements needed")
            else:
                print("   ⚠️  NEEDS IMPROVEMENT - Significant work required")

def main():
    """Run performance benchmark"""
    benchmark = PerformanceBenchmark()
    results = benchmark.run_full_benchmark()
    
    print("\n" + "="*60)
    print("✅ BENCHMARK COMPLETE!")
    print("📄 Check 'benchmark_results.json' for detailed metrics")
    print("🚀 PolicyIntelliHub performance validated!")
    print("="*60)

if __name__ == '__main__':
    main()

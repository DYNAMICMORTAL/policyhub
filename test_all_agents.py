import requests
import json

# Test data
test_clause = "The insured shall be liable for all damages arising from accidents during the policy period."

# Make the request
url = "http://127.0.0.1:5000/analyze-clause"
payload = {"clause_text": test_clause}

try:
    response = requests.post(url, json=payload)
    result = response.json()
    
    if response.status_code == 200:
        print("Analysis completed successfully!")
        print(f"\nAgents that returned results:")
        agents = ['plain_english', 'compliance_check', 'customer_scenario', 'multilingual', 'risk_score', 'training_materials', 'benchmark_analysis']
        
        for agent in agents:
            if agent in result and result[agent]:
                print(f"✓ {agent}")
                # Print a sample of the content
                agent_data = result[agent]
                if isinstance(agent_data, dict):
                    if 'plain_english_text' in agent_data:
                        print(f"  Sample: {agent_data['plain_english_text'][:100]}...")
                    elif 'compliance_score' in agent_data:
                        print(f"  Score: {agent_data['compliance_score']}")
                    elif 'risk_score' in agent_data:
                        print(f"  Risk: {agent_data['risk_score']}")
                    elif 'training_module' in agent_data:
                        print(f"  Training available")
                    elif 'similarity_score' in agent_data:
                        print(f"  Similarity: {agent_data['similarity_score']}")
                    elif 'main_scenario' in agent_data:
                        print(f"  Scenario available")
                    elif 'translations' in agent_data:
                        print(f"  {len(agent_data['translations'])} translations")
            else:
                print(f"✗ {agent} - No data returned")
        
        print(f"\nTotal agents with results: {sum(1 for agent in agents if agent in result and result[agent])}/7")
    else:
        print(f"Error: {result}")
        
except Exception as e:
    print(f"Error making request: {e}")

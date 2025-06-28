document.addEventListener('DOMContentLoaded', function() {
    const clauseForm = document.getElementById('clauseForm');
    const uploadForm = document.getElementById('uploadForm');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsSection = document.getElementById('resultsSection');

    // Handle clause analysis form
    clauseForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const clauseText = document.getElementById('clauseText').value.trim();
        if (!clauseText) {
            alert('Please enter a policy clause to analyze');
            return;
        }

        showLoading();
        
        try {
            const response = await fetch('/analyze-clause', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ clause_text: clauseText })
            });

            const data = await response.json();
            
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }

            displayResults(data);
            
        } catch (error) {
            alert('Network error: ' + error.message);
        } finally {
            hideLoading();
        }
    });

    // Handle file upload form
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const fileInput = document.getElementById('pdfFile');
        if (!fileInput.files.length) {
            alert('Please select a PDF file to upload');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        showLoading();
        
        try {
            const response = await fetch('/upload-document', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }

            alert(`Document processed successfully! ${data.clauses_analyzed} clauses analyzed.`);
            // You could redirect to a bulk results page here
            
        } catch (error) {
            alert('Upload error: ' + error.message);
        } finally {
            hideLoading();
        }
    });

    function showLoading() {
        loadingSpinner.style.display = 'block';
        resultsSection.style.display = 'none';
    }

    function hideLoading() {
        loadingSpinner.style.display = 'none';
        resultsSection.style.display = 'block';
    }

    function displayResults(data) {
        // Show enterprise metadata if available
        if (data.enterprise_metadata) {
            const metadata = data.enterprise_metadata;
            
            // Add enterprise header
            const enterpriseInfo = document.createElement('div');
            enterpriseInfo.className = 'alert alert-success mb-3';
            enterpriseInfo.innerHTML = `
                <div class="row">
                    <div class="col-md-3">
                        <strong>Analysis ID:</strong><br>
                        <code>${data.analysis_id || 'N/A'}</code>
                    </div>
                    <div class="col-md-3">
                        <strong>Processing Model:</strong><br>
                        <span class="badge bg-primary">${data.processing_model || 'Enterprise AI'}</span>
                    </div>
                    <div class="col-md-3">
                        <strong>Confidence Score:</strong><br>
                        <span class="badge bg-success">${(metadata.processing_confidence * 100).toFixed(1)}%</span>
                    </div>
                    <div class="col-md-3">
                        <strong>Processing Time:</strong><br>
                        <span class="badge bg-info">${metadata.processing_metrics?.performance_metrics?.processing_time_ms || 'N/A'}ms</span>
                    </div>
                </div>
            `;
            
            const resultsCard = document.querySelector('#resultsSection .card-body');
            resultsCard.insertBefore(enterpriseInfo, resultsCard.firstChild);
        }

        // Display Plain English results
        if (data.plain_english) {
            document.getElementById('originalText').textContent = data.original_clause;
            document.getElementById('plainEnglishText').textContent = data.plain_english.plain_english_text;
            
            const original = data.plain_english.original_metrics;
            const improved = data.plain_english.improved_metrics;
            
            document.getElementById('originalReadability').textContent = original.flesch_score;
            document.getElementById('originalGrade').textContent = original.grade_level;
            document.getElementById('originalWords').textContent = original.word_count;
            
            document.getElementById('newReadability').textContent = improved.flesch_score;
            document.getElementById('newGrade').textContent = improved.grade_level;
            document.getElementById('newWords').textContent = improved.word_count;
            
            document.getElementById('readabilityImprovement').textContent = data.plain_english.readability_improvement;
            document.getElementById('irdaiCompliant').textContent = data.plain_english.meets_irdai_standards ? 'Yes' : 'No';
        }

        // Display Compliance results
        if (data.compliance_check) {
            const compliance = data.compliance_check;
            document.getElementById('complianceScore').textContent = compliance.compliance_score;
            
            const statusElement = document.getElementById('complianceStatus');
            statusElement.textContent = compliance.status.replace('_', ' ').toUpperCase();
            statusElement.className = `badge compliance-${compliance.status}`;
            
            // Display issues
            const issuesContainer = document.getElementById('complianceIssues');
            issuesContainer.innerHTML = '';
            if (compliance.regulatory_issues && compliance.regulatory_issues.length > 0) {
                compliance.regulatory_issues.forEach(issue => {
                    const issueDiv = document.createElement('div');
                    issueDiv.className = 'alert alert-warning';
                    issueDiv.textContent = issue;
                    issuesContainer.appendChild(issueDiv);
                });
            } else {
                issuesContainer.innerHTML = '<div class="alert alert-success">No major issues found</div>';
            }
            
            // Display recommendations
            const recsContainer = document.getElementById('complianceRecommendations');
            recsContainer.innerHTML = '';
            if (compliance.recommendations && compliance.recommendations.length > 0) {
                compliance.recommendations.forEach(rec => {
                    const recDiv = document.createElement('div');
                    recDiv.className = 'alert alert-info';
                    recDiv.textContent = rec;
                    recsContainer.appendChild(recDiv);
                });
            }
        }

        // Display Scenario results
        if (data.customer_scenario) {
            const scenario = data.customer_scenario;
            document.getElementById('mainScenario').textContent = scenario.main_scenario;
            document.getElementById('simpleExplanation').textContent = scenario.simple_explanation;
            document.getElementById('realLifeExamples').textContent = scenario.real_life_examples;
            document.getElementById('agentScript').textContent = scenario.customer_script;
        }

        // Display Multilingual results
        if (data.multilingual && data.multilingual.translations) {
            const translationsContainer = document.getElementById('translations');
            translationsContainer.innerHTML = '';
            
            Object.entries(data.multilingual.translations).forEach(([langCode, translation]) => {
                const colDiv = document.createElement('div');
                colDiv.className = 'col-md-6 mb-3';
                
                colDiv.innerHTML = `
                    <div class="card">
                        <div class="card-header">
                            <h6>${translation.language_name}</h6>
                        </div>
                        <div class="card-body">
                            <p>${translation.translated_text}</p>
                        </div>
                    </div>
                `;
                
                translationsContainer.appendChild(colDiv);
            });
        }

        // Display Risk results
        if (data.risk_score) {
            const risk = data.risk_score;
            document.getElementById('riskScore').textContent = risk.risk_score;
            
            const levelElement = document.getElementById('riskLevel');
            levelElement.textContent = risk.risk_level;
            levelElement.className = `badge bg-${risk.risk_level === 'High' ? 'danger' : risk.risk_level === 'Medium' ? 'warning' : 'success'}`;
            
            document.getElementById('financialRisk').textContent = risk.financial_risk;
            document.getElementById('disputePotential').textContent = risk.dispute_potential;
            document.getElementById('riskExplanation').textContent = risk.explanation;
            
            // Display mitigation suggestions
            const mitigationContainer = document.getElementById('mitigationSuggestions');
            mitigationContainer.innerHTML = '';
            if (risk.mitigation_suggestions && risk.mitigation_suggestions.length > 0) {
                risk.mitigation_suggestions.forEach(suggestion => {
                    const suggestionDiv = document.createElement('div');
                    suggestionDiv.className = 'alert alert-light';
                    suggestionDiv.textContent = suggestion;
                    mitigationContainer.appendChild(suggestionDiv);
                });
            }
        }

        // Display Training Materials results
        if (data.training_materials) {
            const training = data.training_materials;
            
            // Training module content
            document.getElementById('trainingModule').textContent = training.training_module || 'Training module content will be displayed here.';
            
            // Target audience info
            document.getElementById('targetAudience').textContent = training.target_audience || 'Not specified';
            document.getElementById('difficultyLevel').textContent = training.difficulty_level || 'Not specified';
            document.getElementById('estimatedDuration').textContent = training.estimated_duration || 'Not specified';
            
            // Quiz questions
            const quizContainer = document.getElementById('quizQuestions');
            quizContainer.innerHTML = '';
            if (training.quiz_questions && training.quiz_questions.length > 0) {
                training.quiz_questions.forEach((question, index) => {
                    const questionDiv = document.createElement('div');
                    questionDiv.className = 'mb-3 p-3 border rounded';
                    questionDiv.innerHTML = `
                        <strong>Q${index + 1}:</strong> ${question.question || question}<br>
                        ${question.options ? question.options.map((opt, i) => `<small class="text-muted">${String.fromCharCode(65 + i)}) ${opt}</small>`).join('<br>') : ''}
                        ${question.answer ? `<br><small class="text-success"><strong>Answer:</strong> ${question.answer}</small>` : ''}
                    `;
                    quizContainer.appendChild(questionDiv);
                });
            } else {
                quizContainer.innerHTML = '<p class="text-muted">No quiz questions available</p>';
            }
            
            // Learning points
            const learningContainer = document.getElementById('learningPoints');
            learningContainer.innerHTML = '';
            if (training.key_learning_points && training.key_learning_points.length > 0) {
                training.key_learning_points.forEach(point => {
                    const pointDiv = document.createElement('div');
                    pointDiv.className = 'alert alert-info mb-2';
                    pointDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${point}`;
                    learningContainer.appendChild(pointDiv);
                });
            } else {
                learningContainer.innerHTML = '<p class="text-muted">No specific learning points available</p>';
            }
        }

        // Display Benchmark Analysis results
        if (data.benchmark_analysis) {
            const benchmark = data.benchmark_analysis;
            
            // Similarity score
            document.getElementById('similarityScore').textContent = benchmark.similarity_score || '--';
            
            const qualityElement = document.getElementById('matchQuality');
            const score = parseFloat(benchmark.similarity_score) || 0;
            if (score >= 80) {
                qualityElement.textContent = 'High Match';
                qualityElement.className = 'badge bg-success';
            } else if (score >= 60) {
                qualityElement.textContent = 'Medium Match';
                qualityElement.className = 'badge bg-warning';
            } else {
                qualityElement.textContent = 'Low Match';
                qualityElement.className = 'badge bg-danger';
            }
            
            // Analysis summary
            document.getElementById('benchmarkSummary').textContent = benchmark.analysis_summary || 'No analysis summary available.';
            
            // Similar clauses
            const similarContainer = document.getElementById('similarClauses');
            similarContainer.innerHTML = '';
            if (benchmark.similar_clauses && benchmark.similar_clauses.length > 0) {
                benchmark.similar_clauses.forEach((clause, index) => {
                    const clauseDiv = document.createElement('div');
                    clauseDiv.className = 'mb-2 p-2 border rounded bg-light';
                    clauseDiv.innerHTML = `
                        <small class="text-muted">Match ${index + 1} (${clause.similarity || 'N/A'}% similar):</small><br>
                        <small>${clause.text || clause}</small>
                    `;
                    similarContainer.appendChild(clauseDiv);
                });
            } else {
                similarContainer.innerHTML = '<p class="text-muted">No similar clauses found</p>';
            }
            
            // Industry comparison
            const industryContainer = document.getElementById('industryComparison');
            industryContainer.innerHTML = '';
            if (benchmark.industry_comparison) {
                const comparisonDiv = document.createElement('div');
                comparisonDiv.className = 'p-3 border rounded bg-light';
                comparisonDiv.innerHTML = `
                    <p><strong>Industry Standard:</strong> ${benchmark.industry_comparison.standard || 'Not available'}</p>
                    <p><strong>Your Clause:</strong> ${benchmark.industry_comparison.rating || 'Not rated'}</p>
                    <p><strong>Recommendation:</strong> ${benchmark.industry_comparison.recommendation || 'No specific recommendation'}</p>
                `;
                industryContainer.appendChild(comparisonDiv);
            } else {
                industryContainer.innerHTML = '<p class="text-muted">No industry comparison available</p>';
            }
        }
    }
});

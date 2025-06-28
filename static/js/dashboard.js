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


        // Display Training Materials results (comprehensive version)
if (data.training_materials) {
    const training = data.training_materials;
    
    // Training module content with better formatting
    const moduleContent = training.training_module || 'Training module content will be displayed here.';
    document.getElementById('trainingModule').innerHTML = formatTrainingModule(moduleContent);
    
    // Target audience info
    document.getElementById('targetAudience').textContent = training.target_audience || 'Not specified';
    document.getElementById('difficultyLevel').textContent = training.difficulty_level || 'Not specified';
    document.getElementById('estimatedDuration').textContent = training.estimated_duration || 'Not specified';
    
    // Quiz questions with better formatting
    const quizContainer = document.getElementById('quizQuestions');
    quizContainer.innerHTML = '';
    if (training.quiz_questions && training.quiz_questions.length > 0) {
        training.quiz_questions.forEach((question, index) => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'mb-4 p-3 border rounded bg-light';
            
            let optionsHtml = '';
            if (question.options && Array.isArray(question.options)) {
                optionsHtml = question.options.map(opt => `<div class="form-check"><small class="text-muted">${opt}</small></div>`).join('');
            }
            
            questionDiv.innerHTML = `
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <strong class="text-primary">Q${index + 1}:</strong>
                    <span class="badge bg-secondary">${training.difficulty_level || 'Standard'}</span>
                </div>
                <p class="mb-3">${question.question || question}</p>
                ${optionsHtml}
                ${question.correct_answer ? `<div class="mt-2"><small class="text-success"><strong>Answer:</strong> ${question.correct_answer}</small></div>` : ''}
                ${question.explanation ? `<div class="mt-1"><small class="text-info"><strong>Explanation:</strong> ${question.explanation}</small></div>` : ''}
            `;
            quizContainer.appendChild(questionDiv);
        });
    } else {
        quizContainer.innerHTML = '<div class="alert alert-info"><i class="fas fa-info-circle"></i> Quiz questions will be generated based on clause complexity</div>';
    }
    
    // Learning points with icons
    const learningContainer = document.getElementById('learningPoints');
    learningContainer.innerHTML = '';
    if (training.key_learning_points && training.key_learning_points.length > 0) {
        training.key_learning_points.forEach((point, index) => {
            const pointDiv = document.createElement('div');
            pointDiv.className = 'alert alert-light border-start border-primary border-4 mb-2';
            pointDiv.innerHTML = `
                <div class="d-flex align-items-start">
                    <i class="fas fa-lightbulb text-warning me-2 mt-1"></i>
                    <div>
                        <strong>Key Point ${index + 1}:</strong> ${point}
                    </div>
                </div>
            `;
            learningContainer.appendChild(pointDiv);
        });
    } else {
        learningContainer.innerHTML = '<div class="alert alert-info"><i class="fas fa-info-circle"></i> Learning points will be customized for your training needs</div>';
    }
    
    // Add new training sections
    addTrainingObjectives(training, learningContainer);
    addPracticalExamples(training, learningContainer);
    addRolePlayScenarios(training, learningContainer);
    addCommonMistakes(training, learningContainer);
    addAssessmentCriteria(training, learningContainer);
}

// Helper functions for new training sections
function addTrainingObjectives(training, container) {
    if (training.training_objectives) {
        const objectivesContainer = document.createElement('div');
        objectivesContainer.className = 'mt-4';
        objectivesContainer.innerHTML = `
            <h6><i class="fas fa-target text-success"></i> Training Objectives</h6>
            <div class="alert alert-success">
                ${training.training_objectives.map((obj, i) => `
                    <div class="d-flex align-items-start mb-2">
                        <span class="badge bg-success me-2">${i + 1}</span>
                        <span>${obj}</span>
                    </div>
                `).join('')}
            </div>
        `;
        container.appendChild(objectivesContainer);
    }
}

function addPracticalExamples(training, container) {
    if (training.practical_examples) {
        const examplesContainer = document.createElement('div');
        examplesContainer.className = 'mt-4';
        examplesContainer.innerHTML = `
            <h6><i class="fas fa-users text-primary"></i> Practical Examples</h6>
            <div class="alert alert-info">
                <pre style="white-space: pre-wrap; font-family: inherit; margin-bottom: 0;">${training.practical_examples}</pre>
            </div>
        `;
        container.appendChild(examplesContainer);
    }
}

function addRolePlayScenarios(training, container) {
    if (training.role_play_scenarios) {
        const scenariosContainer = document.createElement('div');
        scenariosContainer.className = 'mt-4';
        scenariosContainer.innerHTML = `
            <h6><i class="fas fa-theater-masks text-purple"></i> Role-Play Scenarios</h6>
            <div class="alert alert-secondary">
                <pre style="white-space: pre-wrap; font-family: inherit; margin-bottom: 0;">${training.role_play_scenarios}</pre>
            </div>
        `;
        container.appendChild(scenariosContainer);
    }
}

function addCommonMistakes(training, container) {
    if (training.common_mistakes) {
        const mistakesContainer = document.createElement('div');
        mistakesContainer.className = 'mt-4';
        mistakesContainer.innerHTML = `
            <h6><i class="fas fa-exclamation-circle text-warning"></i> Common Mistakes to Avoid</h6>
            <div class="alert alert-warning">
                <pre style="white-space: pre-wrap; font-family: inherit; margin-bottom: 0;">${training.common_mistakes}</pre>
            </div>
        `;
        container.appendChild(mistakesContainer);
    }
}

function addAssessmentCriteria(training, container) {
    if (training.assessment_criteria) {
        const assessmentContainer = document.createElement('div');
        assessmentContainer.className = 'mt-4';
        assessmentContainer.innerHTML = `
            <h6><i class="fas fa-clipboard-check text-info"></i> Assessment Criteria</h6>
            <div class="alert alert-light border-info">
                ${training.assessment_criteria.map(criteria => `
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-check-circle text-success me-2"></i>
                        <span>${criteria}</span>
                    </div>
                `).join('')}
            </div>
        `;
        container.appendChild(assessmentContainer);
    }
}

// Enhanced helper function to format training module content
function formatTrainingModule(content) {
    return content
        .replace(/(\d+\.\s*[A-Z][A-Z\s]+):/g, '<h6 class="text-primary mt-3 mb-2"><i class="fas fa-bookmark me-1"></i>$1:</h6>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/^/, '<p>')
        .replace(/$/, '</p>');
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

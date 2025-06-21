// Chat functionality
class ChatApp {
    constructor() {
        this.chatContainer = document.getElementById('chat-container');
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-button');
        this.isLoading = false;
        
        // Mode switching elements
        this.manualMode = document.getElementById('manual-mode');
        this.simulationMode = document.getElementById('simulation-mode');
        this.batchMode = document.getElementById('batch-mode');
        this.analyzeMode = document.getElementById('analyze-mode');
        this.manualChat = document.getElementById('manual-chat');
        this.simulationChat = document.getElementById('simulation-chat');
        this.batchChat = document.getElementById('batch-chat');
        this.analyzeChat = document.getElementById('analyze-chat');
        
        // Simulation elements
        this.simulationContainer = document.getElementById('simulation-container');
        this.startSimulationButton = document.getElementById('start-simulation');
        this.simulationStatus = document.getElementById('simulation-status');
        
        // Batch elements
        this.batchContainer = document.getElementById('batch-container');
        this.startBatchButton = document.getElementById('start-batch');
        this.batchStatus = document.getElementById('batch-status');
        
        // Analyze elements
        this.analyzeContainer = document.getElementById('analyze-container');
        this.startAnalyzeButton = document.getElementById('start-analyze');
        this.analyzeStatus = document.getElementById('analyze-status');
        this.folderInput = document.getElementById('folder-input');
        
        this.init();
    }
    
    init() {
        // Add event listeners for manual chat
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Add event listeners for mode switching
        this.manualMode.addEventListener('click', () => this.switchMode('manual'));
        this.simulationMode.addEventListener('click', () => this.switchMode('simulation'));
        this.batchMode.addEventListener('click', () => this.switchMode('batch'));
        this.analyzeMode.addEventListener('click', () => this.switchMode('analyze'));
        
        // Add folder input listener
        this.folderInput.addEventListener('change', () => this.onFolderSelected());
        
        // Focus on input
        this.messageInput.focus();
        
        // Add welcome message
        this.addMessage('Hello! I\'m Llama. How can I help you today?', false);
    }
    
    switchMode(mode) {
        // Remove active class from all modes
        this.manualMode.classList.remove('active');
        this.simulationMode.classList.remove('active');
        this.batchMode.classList.remove('active');
        this.analyzeMode.classList.remove('active');
        this.manualChat.classList.remove('active');
        this.simulationChat.classList.remove('active');
        this.batchChat.classList.remove('active');
        this.analyzeChat.classList.remove('active');
        
        // Add active class to selected mode
        if (mode === 'manual') {
            this.manualMode.classList.add('active');
            this.manualChat.classList.add('active');
        } else if (mode === 'simulation') {
            this.simulationMode.classList.add('active');
            this.simulationChat.classList.add('active');
        } else if (mode === 'batch') {
            this.batchMode.classList.add('active');
            this.batchChat.classList.add('active');
        } else if (mode === 'analyze') {
            this.analyzeMode.classList.add('active');
            this.analyzeChat.classList.add('active');
        }
    }
    
    addMessage(message, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.textContent = message;
        
        this.chatContainer.appendChild(messageDiv);
        this.scrollToBottom(this.chatContainer);
    }
    
    addSimulationMessage(message, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `simulation-message ${type}-message`;
        messageDiv.textContent = message;
        
        this.simulationContainer.appendChild(messageDiv);
        this.scrollToBottom(this.simulationContainer);
    }
    
    scrollToBottom(container) {
        container.scrollTop = container.scrollHeight;
    }
    
    setLoading(loading) {
        this.isLoading = loading;
        this.sendButton.disabled = loading;
        this.messageInput.disabled = loading;
        
        if (loading) {
            this.sendButton.textContent = 'Sending...';
        } else {
            this.sendButton.textContent = 'Send';
        }
    }
    
    setSimulationStatus(status, type = 'running') {
        this.simulationStatus.textContent = status;
        this.simulationStatus.className = type;
        this.startSimulationButton.disabled = type === 'running';
    }
    
    setBatchStatus(status, type = 'running') {
        this.batchStatus.textContent = status;
        this.batchStatus.className = type;
        this.startBatchButton.disabled = type === 'running';
    }
    
    addBatchResult(agentType, result) {
        const resultDiv = document.createElement('div');
        resultDiv.className = `batch-result ${result.success ? 'success' : 'error'}`;
        
        const header = document.createElement('div');
        header.className = 'batch-result-header';
        header.textContent = `${agentType}: ${result.success ? 'Success' : 'Failed'}`;
        
        const details = document.createElement('div');
        details.className = 'batch-result-details';
        details.textContent = `${result.message} | Turns: ${result.turn_count}`;
        if (result.saved_filepath) {
            details.textContent += ` | Saved: ${result.saved_filepath}`;
        }
        
        resultDiv.appendChild(header);
        resultDiv.appendChild(details);
        this.batchContainer.appendChild(resultDiv);
        this.scrollToBottom(this.batchContainer);
    }
    
    setAnalyzeStatus(status, type = 'running') {
        this.analyzeStatus.textContent = status;
        this.analyzeStatus.className = type;
        this.startAnalyzeButton.disabled = type === 'running';
    }
    
    onFolderSelected() {
        const files = this.folderInput.files;
        const jsonFiles = Array.from(files).filter(file => file.name.endsWith('.json'));
        
        if (jsonFiles.length > 0) {
            this.startAnalyzeButton.disabled = false;
            this.setAnalyzeStatus(`${jsonFiles.length} JSON files selected`, 'completed');
        } else {
            this.startAnalyzeButton.disabled = true;
            this.setAnalyzeStatus('No JSON files found in selected folder', 'error');
        }
    }
    
    addAnalyzeResult(filename, result) {
        const resultDiv = document.createElement('div');
        resultDiv.className = `analyze-result ${result.success ? 'success' : 'error'}`;
        
        const header = document.createElement('div');
        header.className = 'analyze-result-header';
        
        const title = document.createElement('span');
        title.textContent = `${filename}: ${result.success ? 'Analyzed' : 'Failed'}`;
        
        const score = document.createElement('span');
        score.className = 'analyze-result-score';
        
        // Handle mixture of agents format
        if (result.success && result.mixture_of_agents && result.synthesis) {
            if (result.synthesis.overall_assessment && result.synthesis.overall_assessment.composite_score) {
                score.textContent = `Score: ${result.synthesis.overall_assessment.composite_score}/10`;
            } else if (result.synthesis.dimensional_scores && result.synthesis.dimensional_scores.weighted_average) {
                score.textContent = `Score: ${result.synthesis.dimensional_scores.weighted_average}/10`;
            } else {
                score.textContent = 'Multi-Agent Analysis';
            }
        } else if (result.success && result.analysis && result.analysis.overall_score) {
            // Handle legacy single agent format
            score.textContent = `Score: ${result.analysis.overall_score}/10`;
        } else {
            score.textContent = 'Error';
            score.style.backgroundColor = '#dc3545';
        }
        
        header.appendChild(title);
        header.appendChild(score);
        
        const details = document.createElement('div');
        details.className = 'analyze-result-details';
        
        if (result.success && result.mixture_of_agents) {
            // Handle mixture of agents format
            const summary = result.summary;
            details.textContent = `Agents: ${summary.successful_agents}/${summary.total_agents} successful`;
            
            if (result.synthesis && result.synthesis.overall_assessment) {
                details.textContent += ` | Grade: ${result.synthesis.overall_assessment.grade || 'N/A'}`;
                details.textContent += ` | Outcome: ${result.synthesis.overall_assessment.conversation_outcome || 'N/A'}`;
            }
        } else if (result.success && result.analysis) {
            // Handle legacy single agent format
            if (result.analysis.outcome) {
                details.textContent = `Outcome: ${result.analysis.outcome}`;
            }
            if (result.analysis.conversation_quality && result.analysis.conversation_quality.total_turns) {
                details.textContent += ` | Turns: ${result.analysis.conversation_quality.total_turns}`;
            }
        } else {
            details.textContent = result.error || 'Analysis failed';
        }
        
        resultDiv.appendChild(header);
        resultDiv.appendChild(details);
        
        // Add summary section
        if (result.success) {
            const summary = document.createElement('div');
            summary.className = 'analyze-result-summary';
            
            if (result.mixture_of_agents && result.synthesis && result.synthesis.executive_summary) {
                summary.textContent = result.synthesis.executive_summary;
            } else if (result.analysis && result.analysis.summary) {
                summary.textContent = result.analysis.summary;
            }
            
            if (summary.textContent) {
                resultDiv.appendChild(summary);
            }
        }
        
        // Add expandable details for mixture of agents
        if (result.success && result.mixture_of_agents) {
            const expandButton = document.createElement('button');
            expandButton.textContent = 'Show Agent Details';
            expandButton.className = 'analyze-expand-btn';
            expandButton.style.cssText = 'margin-top: 8px; padding: 4px 8px; font-size: 12px; background: #17a2b8; color: white; border: none; border-radius: 4px; cursor: pointer;';
            
            const detailsContainer = document.createElement('div');
            detailsContainer.className = 'analyze-agent-details';
            detailsContainer.style.display = 'none';
            detailsContainer.style.marginTop = '10px';
            detailsContainer.style.fontSize = '12px';
            detailsContainer.style.color = '#666';
            
            // Add individual agent results
            if (result.agent_analyses) {
                Object.entries(result.agent_analyses).forEach(([agentName, agentResult]) => {
                    const agentDiv = document.createElement('div');
                    agentDiv.style.marginBottom = '5px';
                    agentDiv.innerHTML = `<strong>${agentName}:</strong> ${agentResult.success ? 'Success' : 'Failed'}`;
                    detailsContainer.appendChild(agentDiv);
                });
            }
            
            expandButton.addEventListener('click', () => {
                if (detailsContainer.style.display === 'none') {
                    detailsContainer.style.display = 'block';
                    expandButton.textContent = 'Hide Agent Details';
                } else {
                    detailsContainer.style.display = 'none';
                    expandButton.textContent = 'Show Agent Details';
                }
            });
            
            resultDiv.appendChild(expandButton);
            resultDiv.appendChild(detailsContainer);
        }
        
        this.analyzeContainer.appendChild(resultDiv);
        this.scrollToBottom(this.analyzeContainer);
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isLoading) return;
        
        // Add user message to chat
        this.addMessage(message, true);
        this.messageInput.value = '';
        
        // Set loading state
        this.setLoading(true);
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.addMessage(`Error: ${data.error}`, false);
            } else {
                this.addMessage(data.response, false);
            }
        } catch (error) {
            this.addMessage(`Error: ${error.message}`, false);
        } finally {
            this.setLoading(false);
            this.messageInput.focus();
        }
    }
    
    async startSimulation() {
        const userAgentType = document.getElementById('user-agent-type').value;
        const chatAgentType = document.getElementById('chat-agent-type').value;
        const maxTurns = document.getElementById('max-turns').value;
        
        // Clear previous simulation
        this.simulationContainer.innerHTML = '';
        this.setSimulationStatus('Starting simulation...', 'running');
        
        try {
            const response = await fetch('/simulate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_agent_type: userAgentType,
                    chat_agent_type: chatAgentType,
                    max_turns: parseInt(maxTurns)
                }),
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.setSimulationStatus(`Error: ${data.error}`, 'error');
                return;
            }
            
            // Add system message with agent types
            this.addSimulationMessage(
                `Starting conversation between ${userAgentType} and ${chatAgentType}`,
                'system'
            );
            
            // Add each message from the conversation
            data.conversation.forEach(turn => {
                const type = turn.speaker === 'user_agent' ? 'user-agent' : 'chat-agent';
                this.addSimulationMessage(turn.message, type);
            });
            
            // Add completion message
            this.addSimulationMessage(
                `Conversation completed after ${data.turn_count} turns. Transcript saved to: ${data.saved_filepath}`,
                'system'
            );
            
            this.setSimulationStatus('Simulation completed successfully!', 'completed');
            
        } catch (error) {
            this.setSimulationStatus(`Error: ${error.message}`, 'error');
        }
    }
    
    async startBatchRun() {
        const chatAgentType = document.getElementById('batch-chat-agent-type').value;
        const maxTurns = document.getElementById('batch-max-turns').value;
        
        // Clear previous batch results
        this.batchContainer.innerHTML = '';
        this.setBatchStatus('Starting batch run with all user agent types...', 'running');
        
        try {
            const response = await fetch('/batch-run', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    chat_agent_type: chatAgentType,
                    max_turns: parseInt(maxTurns)
                }),
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.setBatchStatus(`Error: ${data.error}`, 'error');
                return;
            }
            
            // Add header with batch info
            const headerDiv = document.createElement('div');
            headerDiv.className = 'batch-result';
            headerDiv.innerHTML = `
                <div class="batch-result-header">Batch Run Results - ${data.batch_timestamp}</div>
                <div class="batch-result-details">
                    Total: ${data.total_runs} | Successful: ${data.successful_runs} | 
                    Total Turns: ${data.total_turns} | Folder: ${data.batch_folder}
                </div>
            `;
            this.batchContainer.appendChild(headerDiv);
            
            // Add results for each agent type
            const agentTypeNames = {
                'frustrated_customer': 'Frustrated Customer (Delayed Materials)',
                'confused_elderly': 'Confused Elderly (Tool Setup)',
                'anxious_student': 'Anxious DIYer (Overwhelmed Project)',
                'demanding_executive': 'Demanding Contractor (Urgent Job)',
                'frustrated_homeowner': 'Frustrated Homeowner (DIY Project)',
                'anxious_tech_user': 'Anxious Customer (Tool Problems)',
                'demanding_customer': 'Demanding Customer (Delayed Order)',
                'elderly_homeowner': 'Elderly Homeowner (Home Project)'
            };
            
            Object.entries(data.results).forEach(([agentKey, result]) => {
                const displayName = agentTypeNames[agentKey] || agentKey;
                this.addBatchResult(displayName, result);
            });
            
            this.setBatchStatus(
                `Batch run completed! ${data.successful_runs}/${data.total_runs} successful conversations`,
                'completed'
            );
            
        } catch (error) {
            this.setBatchStatus(`Error: ${error.message}`, 'error');
        }
    }
    
    async startAnalyze() {
        const files = this.folderInput.files;
        const jsonFiles = Array.from(files).filter(file => file.name.endsWith('.json'));
        
        if (jsonFiles.length === 0) {
            this.setAnalyzeStatus('No JSON files selected', 'error');
            return;
        }
        
        // Clear previous results
        this.analyzeContainer.innerHTML = '';
        this.setAnalyzeStatus(`Analyzing ${jsonFiles.length} transcripts...`, 'running');
        
        let completed = 0;
        let successful = 0;
        
        for (const file of jsonFiles) {
            try {
                // Read file content
                const fileContent = await this.readFileAsText(file);
                const conversationData = JSON.parse(fileContent);
                
                // Send to judge endpoint
                const response = await fetch('/judge', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        conversation_data: conversationData
                    }),
                });
                
                const result = await response.json();
                
                // Display result
                this.addAnalyzeResult(file.name, result);
                
                if (result.success) {
                    successful++;
                    
                    // Save analysis to file
                    const analysisFilename = file.name.replace('.json', '_judge.json');
                    const analysisData = {
                        original_file: file.name,
                        analysis_timestamp: new Date().toISOString(),
                        mixture_of_agents: result.mixture_of_agents || false,
                        analysis: result.analysis || null,
                        agent_analyses: result.agent_analyses || null,
                        synthesis: result.synthesis || null,
                        summary: result.summary || null,
                        raw_response: result.raw_response || null
                    };
                    
                    // Create download link for the analysis
                    this.downloadJSON(analysisData, analysisFilename);
                }
                
                completed++;
                this.setAnalyzeStatus(
                    `Progress: ${completed}/${jsonFiles.length} files processed (${successful} successful)`,
                    'running'
                );
                
                // Small delay to prevent overwhelming the API
                await new Promise(resolve => setTimeout(resolve, 500));
                
            } catch (error) {
                console.error(`Error processing ${file.name}:`, error);
                this.addAnalyzeResult(file.name, {
                    success: false,
                    error: error.message
                });
                completed++;
            }
        }
        
        this.setAnalyzeStatus(
            `Analysis completed! ${successful}/${jsonFiles.length} files successfully analyzed`,
            'completed'
        );
    }
    
    readFileAsText(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = e => resolve(e.target.result);
            reader.onerror = e => reject(e);
            reader.readAsText(file);
        });
    }
    
    downloadJSON(data, filename) {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Initialize the chat app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chatApp = new ChatApp();
});

// Legacy function for backward compatibility with onclick handlers
function sendMessage() {
    if (window.chatApp) {
        window.chatApp.sendMessage();
    }
}

function startSimulation() {
    if (window.chatApp) {
        window.chatApp.startSimulation();
    }
}

function startBatchRun() {
    if (window.chatApp) {
        window.chatApp.startBatchRun();
    }
}

function startAnalyze() {
    if (window.chatApp) {
        window.chatApp.startAnalyze();
    }
} 
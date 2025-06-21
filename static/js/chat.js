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
        this.manualChat = document.getElementById('manual-chat');
        this.simulationChat = document.getElementById('simulation-chat');
        
        // Simulation elements
        this.simulationContainer = document.getElementById('simulation-container');
        this.startSimulationButton = document.getElementById('start-simulation');
        this.simulationStatus = document.getElementById('simulation-status');
        
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
        
        // Focus on input
        this.messageInput.focus();
        
        // Add welcome message
        this.addMessage('Hello! I\'m Llama. How can I help you today?', false);
    }
    
    switchMode(mode) {
        if (mode === 'manual') {
            this.manualMode.classList.add('active');
            this.simulationMode.classList.remove('active');
            this.manualChat.classList.add('active');
            this.simulationChat.classList.remove('active');
        } else {
            this.manualMode.classList.remove('active');
            this.simulationMode.classList.add('active');
            this.manualChat.classList.remove('active');
            this.simulationChat.classList.add('active');
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
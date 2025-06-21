// Chat functionality
class ChatApp {
    constructor() {
        this.chatContainer = document.getElementById('chat-container');
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-button');
        this.isLoading = false;
        
        this.init();
    }
    
    init() {
        // Add event listeners
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Focus on input
        this.messageInput.focus();
        
        // Add welcome message
        this.addMessage('Hello! I\'m Llama. How can I help you today?', false);
    }
    
    addMessage(message, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        messageDiv.textContent = message;
        
        this.chatContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addLoadingMessage() {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.id = 'loading-message';
        
        const loadingSpinner = document.createElement('div');
        loadingSpinner.className = 'loading';
        
        messageDiv.appendChild(loadingSpinner);
        this.chatContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    removeLoadingMessage() {
        const loadingMessage = document.getElementById('loading-message');
        if (loadingMessage) {
            loadingMessage.remove();
        }
    }
    
    scrollToBottom() {
        this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    }
    
    setLoading(loading) {
        this.isLoading = loading;
        this.sendButton.disabled = loading;
        this.messageInput.disabled = loading;
        
        if (loading) {
            this.sendButton.textContent = 'Sending...';
            this.addLoadingMessage();
        } else {
            this.sendButton.textContent = 'Send';
            this.removeLoadingMessage();
        }
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
}

// Initialize the chat app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});

// Legacy function for backward compatibility
function sendMessage() {
    if (window.chatApp) {
        window.chatApp.sendMessage();
    }
} 
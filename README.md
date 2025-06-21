# Chat with Llama

A simple Flask web application that integrates with the Llama API to create a chat interface. The application features a clean, modern UI with separated HTML, CSS, and JavaScript files.

## Project Structure

```
chatbot_gym/
├── app.py                          # Flask web application
├── user_agent.py                   # UserAgent class for creating different user personas
├── chat_agent.py                   # ChatAgent class for creating different chat assistants
├── conversation_orchestrator.py    # Manages conversations between agents
├── example_conversation.py         # Example usage of the agent system
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                 # HTML template for web interface
├── static/
│   ├── css/
│   │   └── style.css              # Styling for web interface
│   └── js/
│       └── chat.js                # JavaScript functionality for web interface
├── conversations/                  # Directory for saved conversation transcripts
└── README.md
```

## Setup

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file in the root directory with your Llama API key:
   ```
   LLAMA_API_KEY=your_api_key_here
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

### Web Interface
- Type your message in the input field and click "Send" or press Enter
- The chat interface will display your messages and Llama's responses
- Messages are sent to the Llama API using the Llama-4-Maverick-17B-128E-Instruct-FP8 model

### Agent-to-Agent Conversations
The system includes a powerful agent conversation framework for creating automated dialogues:

#### UserAgent Class
Create different user personas with:
- **Personality prompt**: Defines character traits and behavior
- **Problem roleplay prompt**: Specific scenario or problem the agent faces
- **Base prompt**: Core instructions for agent behavior

```python
from user_agent import UserAgent

# Create a custom user agent
user_agent = UserAgent(
    agent_id="frustrated_customer",
    personality_prompt="You are impatient and easily frustrated...",
    problem_roleplay_prompt="You ordered a product that hasn't arrived...",
    base_prompt="You are roleplaying as a customer seeking help..."
)
```

#### Predefined Templates
Use ready-made agent templates:
```python
from user_agent import UserAgentTemplates

# Create agents using templates
frustrated_customer = UserAgentTemplates.create_frustrated_customer()
elderly_user = UserAgentTemplates.create_confused_elderly_user()
anxious_student = UserAgentTemplates.create_anxious_student()
demanding_executive = UserAgentTemplates.create_demanding_executive()
```

#### Running Conversations
```python
from conversation_orchestrator import ConversationOrchestrator
from chat_agent import ChatAgentTemplates

# Create agents
user_agent = UserAgentTemplates.create_frustrated_customer()
chat_agent = ChatAgentTemplates.create_customer_service_agent()

# Start conversation
orchestrator = ConversationOrchestrator(user_agent, chat_agent)
result = orchestrator.start_conversation(max_turns=10)

# Conversation transcript is automatically saved to conversations/ directory
```

#### Example Usage
Run the example script to see the system in action:
```bash
python example_conversation.py
```

This will demonstrate various agent interactions and save conversation transcripts.

## API Endpoint

The application exposes a single endpoint for chat:

- **POST /chat**
  - Request body: `{"message": "Your message here"}`
  - Response: `{"response": "Llama's response"}`

Example using curl:
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the moon made of?"}'
```

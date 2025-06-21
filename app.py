from flask import Flask, request, jsonify, render_template
import os
from llama_api_client import LlamaAPIClient
from dotenv import load_dotenv
from user_agent import UserAgent, UserAgentTemplates
from chat_agent import ChatAgent, ChatAgentTemplates
from conversation_orchestrator import ConversationOrchestrator

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Llama API client
try:
    llama_client = LlamaAPIClient(
        api_key=os.environ.get("LLAMA_API_KEY")
    )
except Exception as e:
    print(f"Error initializing Llama API client: {e}")
    llama_client = None

@app.route('/chat', methods=['POST'])
def chat():
    if not llama_client:
        return jsonify({
            'error': 'Llama API client not initialized. Please check your API key.'
        }), 500

    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Please provide a message in the request body'
            }), 400

        user_message = data['message']

        # Call Llama API
        completion = llama_client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct-FP8",
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
        )

        # Extract the response text
        response_text = completion.completion_message.content.text

        return jsonify({
            'response': response_text
        })

    except Exception as e:
        return jsonify({
            'error': f'Error processing request: {str(e)}'
        }), 500

@app.route('/simulate', methods=['POST'])
def simulate():
    """Endpoint to run a simulated conversation between agents."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Get simulation parameters
        user_agent_type = data.get('user_agent_type', 'frustrated_customer')
        chat_agent_type = data.get('chat_agent_type', 'homedepo_agent')
        max_turns = data.get('max_turns', 10)
        
        # Map frontend values to actual method names
        user_agent_methods = {
            'frustrated_customer': 'create_frustrated_customer',
            'confused_elderly': 'create_confused_elderly_user',
            'anxious_student': 'create_anxious_student',
            'demanding_executive': 'create_demanding_executive',
            'frustrated_homeowner': 'create_frustrated_homeowner',
            'anxious_tech_user': 'create_anxious_tech_user',
            'demanding_customer': 'create_demanding_customer',
            'elderly_homeowner': 'create_elderly_homeowner'
        }
        
        chat_agent_methods = {
            'homedepo_agent': 'create_homedepo_agent'
        }
        
        # Create agents based on selected types
        user_method = user_agent_methods.get(user_agent_type)
        chat_method = chat_agent_methods.get(chat_agent_type)
        
        if not user_method or not chat_method:
            return jsonify({'error': 'Invalid agent type selected'}), 400
        
        user_agent = getattr(UserAgentTemplates, user_method)()
        chat_agent = getattr(ChatAgentTemplates, chat_method)()
        
        # Create orchestrator
        orchestrator = ConversationOrchestrator(user_agent, chat_agent)
        
        # Run simulation - the orchestrator will use the chat_agent's initial_message if available
        result = orchestrator.start_conversation(
            max_turns=max_turns,
            delay_between_turns=0.1  # Faster for web interface
        )
        
        # Return conversation data
        return jsonify({
            'success': result['success'],
            'message': result['message'],
            'turn_count': result['turn_count'],
            'conversation': user_agent.conversation_history,
            'saved_filepath': result['saved_filepath']
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error running simulation: {str(e)}'
        }), 500

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

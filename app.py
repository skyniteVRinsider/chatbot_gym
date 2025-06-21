from flask import Flask, request, jsonify, render_template
import os
import json
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

@app.route('/judge', methods=['POST'])
def judge():
    """Endpoint to analyze a conversation transcript using the judge prompt."""
    try:
        data = request.get_json()
        if not data or 'conversation_data' not in data:
            return jsonify({'error': 'No conversation data provided'}), 400
        
        conversation_data = data['conversation_data']
        
        # Load judge prompt
        try:
            with open('judge_prompt.txt', 'r', encoding='utf-8') as f:
                judge_prompt = f.read().strip()
        except FileNotFoundError:
            return jsonify({'error': 'Judge prompt file not found'}), 500
        except Exception as e:
            return jsonify({'error': f'Error loading judge prompt: {str(e)}'}), 500
        
        if not llama_client:
            return jsonify({'error': 'Llama API client not initialized'}), 500
        
        # Prepare the full prompt
        full_prompt = f"{judge_prompt}\n\n{json.dumps(conversation_data, indent=2)}"
        
        # Call Llama API
        completion = llama_client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[
                {
                    "role": "user",
                    "content": full_prompt,
                }
            ],
        )
        
        # Extract the response
        analysis_text = completion.completion_message.content.text
        
        # Try to parse the JSON response
        try:
            # Look for JSON content in the response
            import re
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', analysis_text, re.DOTALL)
            if json_match:
                analysis_json = json.loads(json_match.group(1))
            else:
                # If no JSON block found, try to parse the entire response
                analysis_json = json.loads(analysis_text)
        except json.JSONDecodeError:
            # If JSON parsing fails, return the raw text
            analysis_json = {
                "error": "Could not parse JSON response",
                "raw_response": analysis_text
            }
        
        return jsonify({
            'success': True,
            'analysis': analysis_json,
            'raw_response': analysis_text
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error analyzing conversation: {str(e)}'
        }), 500

@app.route('/batch-run', methods=['POST'])
def batch_run():
    """Endpoint to run batch simulations with all user agents."""
    import threading
    from datetime import datetime
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Get simulation parameters
        chat_agent_type = data.get('chat_agent_type', 'homedepo_agent')
        max_turns = data.get('max_turns', 10)
        
        # Create batch folder with timestamp
        batch_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_folder = f"conversations/batch_{batch_timestamp}"
        os.makedirs(batch_folder, exist_ok=True)
        
        # All available user agent types
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
        
        # Validate chat agent type
        chat_method = chat_agent_methods.get(chat_agent_type)
        if not chat_method:
            return jsonify({'error': 'Invalid chat agent type selected'}), 400
        
        # Results storage
        results = {}
        results_lock = threading.Lock()
        
        def run_single_simulation(user_agent_key, user_method_name):
            """Run a single simulation in a thread."""
            try:
                # Create agents
                user_agent = getattr(UserAgentTemplates, user_method_name)()
                chat_agent = getattr(ChatAgentTemplates, chat_method)()
                
                # Create orchestrator
                orchestrator = ConversationOrchestrator(user_agent, chat_agent)
                
                # Run simulation
                result = orchestrator.start_conversation(
                    max_turns=max_turns,
                    delay_between_turns=0.1
                )
                
                # Move the saved file to the batch folder
                if result['saved_filepath']:
                    import shutil
                    filename = os.path.basename(result['saved_filepath'])
                    new_filepath = os.path.join(batch_folder, filename)
                    shutil.move(result['saved_filepath'], new_filepath)
                    result['saved_filepath'] = new_filepath
                
                # Store result
                with results_lock:
                    results[user_agent_key] = {
                        'success': result['success'],
                        'message': result['message'],
                        'turn_count': result['turn_count'],
                        'saved_filepath': result['saved_filepath'],
                        'conversation_summary': result['conversation_summary']
                    }
                    
            except Exception as e:
                with results_lock:
                    results[user_agent_key] = {
                        'success': False,
                        'message': f'Error: {str(e)}',
                        'turn_count': 0,
                        'saved_filepath': None,
                        'conversation_summary': None
                    }
        
        # Start all simulations in parallel threads
        threads = []
        for user_agent_key, user_method_name in user_agent_methods.items():
            thread = threading.Thread(
                target=run_single_simulation,
                args=(user_agent_key, user_method_name)
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Calculate summary statistics
        successful_runs = sum(1 for r in results.values() if r['success'])
        total_runs = len(results)
        total_turns = sum(r['turn_count'] for r in results.values())
        
        return jsonify({
            'success': True,
            'message': f'Batch run completed: {successful_runs}/{total_runs} successful',
            'batch_folder': batch_folder,
            'batch_timestamp': batch_timestamp,
            'total_runs': total_runs,
            'successful_runs': successful_runs,
            'total_turns': total_turns,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error running batch simulation: {str(e)}'
        }), 500

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template
import os
from llama_api_client import LlamaAPIClient
from dotenv import load_dotenv

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

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

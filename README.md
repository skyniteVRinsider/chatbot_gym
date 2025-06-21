# Chat with Llama

A simple Flask web application that integrates with the Llama API to create a chat interface. The application features a clean, modern UI with separated HTML, CSS, and JavaScript files.

## Project Structure

```
chatbot_gym/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── chat.js       # JavaScript functionality
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

- Type your message in the input field and click "Send" or press Enter
- The chat interface will display your messages and Llama's responses
- Messages are sent to the Llama API using the Llama-4-Maverick-17B-128E-Instruct-FP8 model

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

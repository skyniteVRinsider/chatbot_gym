import os
from typing import Optional
from llama_api_client import LlamaAPIClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ChatAgent:
    """
    A ChatAgent that can converse with UserAgents. This represents the other side
    of the conversation - typically a customer service agent, teacher, or assistant.
    """
    
    def __init__(self, 
                 agent_id: str = "chat_agent",
                 system_prompt: Optional[str] = None,
                 prompt_file: Optional[str] = None,
                 initial_message: Optional[str] = None,
                 model: str = "Llama-4-Maverick-17B-128E-Instruct-FP8"):
        """
        Initialize a ChatAgent.
        
        Args:
            agent_id: Unique identifier for this chat agent
            system_prompt: System prompt defining the chat agent's role and behavior
            prompt_file: Path to file containing system prompt (relative to chat_agents/ folder)
            initial_message: Optional initial message to start conversations
            model: Llama model to use for generating responses
        """
        self.agent_id = agent_id
        self.model = model
        self.initial_message = initial_message
        
        # Load system prompt from file if specified
        if prompt_file:
            self.system_prompt = self._load_prompt_from_file(prompt_file)
        elif system_prompt:
            self.system_prompt = system_prompt
        else:
            # Default system prompt if none provided
            self.system_prompt = """You are a helpful, professional customer service representative. 
Your goal is to assist users with their problems in a friendly, patient, and effective manner. 
You should:
- Listen carefully to their concerns
- Ask clarifying questions when needed
- Provide clear, actionable solutions
- Remain calm and professional even if the user is frustrated
- Follow up to ensure their issue is resolved"""
        
        # Initialize Llama API client
        try:
            self.llama_client = LlamaAPIClient(
                api_key=os.environ.get("LLAMA_API_KEY")
            )
        except Exception as e:
            print(f"Error initializing Llama API client: {e}")
            self.llama_client = None
    
    def _load_prompt_from_file(self, filename: str) -> str:
        """
        Load system prompt from a file in the chat_agents directory.
        
        Args:
            filename: Name of the file to load (e.g., "homedepo_chat_agent.txt")
            
        Returns:
            Content of the file as a string
        """
        try:
            filepath = os.path.join("chat_agents", filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Warning: Prompt file '{filepath}' not found. Using default prompt.")
            return """You are a helpful, professional customer service representative. 
Your goal is to assist users with their problems in a friendly, patient, and effective manner."""
        except Exception as e:
            print(f"Error loading prompt file '{filepath}': {e}")
            return """You are a helpful, professional customer service representative. 
Your goal is to assist users with their problems in a friendly, patient, and effective manner."""
    
    def generate_response(self, user_message: str, conversation_context: Optional[list] = None) -> Optional[str]:
        """
        Generate a response to the user's message.
        
        Args:
            user_message: Message from the user
            conversation_context: Previous conversation history as list of dicts
            
        Returns:
            Generated response or None if error occurred
        """
        if not self.llama_client:
            print("Llama API client not available")
            return None
        
        try:
            # Build messages for the API call
            messages = [
                {
                    "role": "system",
                    "content": self.system_prompt
                }
            ]
            
            # Add conversation context if provided
            if conversation_context:
                for turn in conversation_context:
                    # Map speaker roles for the API
                    role = "user" if turn["speaker"] == "user_agent" else "assistant"
                    messages.append({
                        "role": role,
                        "content": turn["message"]
                    })
            
            # Add the new user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Generate response
            completion = self.llama_client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            return completion.completion_message.content.text
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
    
    def __str__(self) -> str:
        """String representation of the ChatAgent."""
        return f"ChatAgent(id={self.agent_id})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the ChatAgent."""
        return f"ChatAgent(agent_id='{self.agent_id}', model='{self.model}')"


# Predefined ChatAgent templates for common scenarios
class ChatAgentTemplates:
    """Predefined templates for creating ChatAgents with specific roles."""
    
    @staticmethod
    def create_homedepo_agent(agent_id: str = "homedepo_agent") -> ChatAgent:
        """Create a Home Depot customer service ChatAgent using prompt file."""
        initial_message = "Hello! Welcome to The Home Depot. I'm here to help you with your home improvement project. What can I assist you with today?"
        return ChatAgent(
            agent_id=agent_id, 
            prompt_file="homedepo_chat_agent.txt",
            initial_message=initial_message
        ) 
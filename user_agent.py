import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from llama_api_client import LlamaAPIClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class UserAgent:
    """
    A UserAgent that can converse with a ChatAgent, with customizable personality,
    problem roleplay, and base prompts.
    """
    
    def __init__(self, 
                 agent_id: str,
                 personality_prompt: Optional[str] = None,
                 problem_roleplay_prompt: Optional[str] = None,
                 base_prompt: Optional[str] = None,
                 personality_file: Optional[str] = None,
                 problem_roleplay_file: Optional[str] = None,
                 base_prompt_file: Optional[str] = None,
                 model: str = "Llama-4-Maverick-17B-128E-Instruct-FP8"):
        """
        Initialize a UserAgent with specific prompts.
        
        Args:
            agent_id: Unique identifier for this agent
            personality_prompt: Defines the agent's personality traits (or use personality_file)
            problem_roleplay_prompt: Specific problem or scenario (or use problem_roleplay_file)
            base_prompt: Base instructions (or use base_prompt_file)
            personality_file: File in user_agents/personalities/ folder
            problem_roleplay_file: File in user_agents/problem_roleplay/ folder  
            base_prompt_file: File in user_agents/ folder (defaults to base_prompt.txt)
            model: Llama model to use for generating responses
        """
        self.agent_id = agent_id
        self.model = model
        
        # Load prompts from files or use provided strings
        self.base_prompt = self._load_prompt(
            base_prompt, base_prompt_file or "base_prompt.txt", "user_agents"
        )
        self.personality_prompt = self._load_prompt(
            personality_prompt, personality_file, "user_agents/personalities"
        )
        self.problem_roleplay_prompt = self._load_prompt(
            problem_roleplay_prompt, problem_roleplay_file, "user_agents/problem_roleplay"
        )
        
        # Initialize conversation history
        self.conversation_history: List[Dict[str, str]] = []
        
        # Initialize Llama API client
        try:
            self.llama_client = LlamaAPIClient(
                api_key=os.environ.get("LLAMA_API_KEY")
            )
        except Exception as e:
            print(f"Error initializing Llama API client: {e}")
            self.llama_client = None
    
    def _load_prompt(self, prompt_text: Optional[str], filename: Optional[str], folder: str) -> str:
        """
        Load prompt from text or file.
        
        Args:
            prompt_text: Direct prompt text (takes priority)
            filename: Name of file to load from
            folder: Folder containing the file
            
        Returns:
            Prompt text
        """
        if prompt_text:
            return prompt_text
        
        if not filename:
            raise ValueError(f"Either prompt_text or filename must be provided for {folder}")
        
        try:
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file '{filepath}' not found")
        except Exception as e:
            raise Exception(f"Error loading prompt file '{filepath}': {e}")
    
    def get_system_prompt(self) -> str:
        """
        Combine all prompts into a comprehensive system prompt.
        
        Returns:
            Combined system prompt string
        """
        return f"""
{self.base_prompt}

PERSONALITY:
{self.personality_prompt}

ROLEPLAY SCENARIO:
{self.problem_roleplay_prompt}

""".strip()
    
    def generate_response(self, chat_agent_message: str) -> Optional[str]:
        """
        Generate a response to the ChatAgent's message.
        
        Args:
            chat_agent_message: Message from the ChatAgent
            
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
                    "content": self.get_system_prompt()
                }
            ]
            
            # Add conversation history
            for turn in self.conversation_history:
                messages.append({
                    "role": "assistant" if turn["speaker"] == "user_agent" else "user",
                    "content": turn["message"]
                })
            
            # Add the new message from ChatAgent
            messages.append({
                "role": "user",
                "content": chat_agent_message
            })
            
            # Generate response
            completion = self.llama_client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            response = completion.completion_message.content.text
            
            # Only add the user_agent's response to conversation history
            # The conversation orchestrator will manage chat_agent messages
            self.conversation_history.append({
                "speaker": "user_agent",
                "message": response,
                "timestamp": datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
    
    def save_conversation(self, filename: Optional[str] = None) -> str:
        """
        Save the conversation transcript to a file.
        
        Args:
            filename: Optional custom filename. If None, generates based on agent_id and timestamp
            
        Returns:
            Path to the saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{self.agent_id}_{timestamp}.json"
        
        # Create conversations directory if it doesn't exist
        os.makedirs("conversations", exist_ok=True)
        filepath = os.path.join("conversations", filename)
        
        # Prepare conversation data
        conversation_data = {
            "agent_id": self.agent_id,
            "personality_prompt": self.personality_prompt,
            "problem_roleplay_prompt": self.problem_roleplay_prompt,
            "base_prompt": self.base_prompt,
            "model": self.model,
            "conversation_start": self.conversation_history[0]["timestamp"] if self.conversation_history else None,
            "conversation_end": self.conversation_history[-1]["timestamp"] if self.conversation_history else None,
            "total_turns": len(self.conversation_history),
            "conversation": self.conversation_history
        }
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_conversation(self, filepath: str) -> bool:
        """
        Load a conversation from a file.
        
        Args:
            filepath: Path to the conversation file
            
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.conversation_history = data.get("conversation", [])
            return True
            
        except Exception as e:
            print(f"Error loading conversation: {e}")
            return False
    
    def clear_conversation(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_conversation_summary(self) -> Dict:
        """
        Get a summary of the current conversation.
        
        Returns:
            Dictionary with conversation statistics
        """
        if not self.conversation_history:
            return {
                "total_turns": 0,
                "user_agent_turns": 0,
                "chat_agent_turns": 0,
                "conversation_started": None,
                "last_message": None
            }
        
        user_agent_turns = len([turn for turn in self.conversation_history if turn["speaker"] == "user_agent"])
        chat_agent_turns = len([turn for turn in self.conversation_history if turn["speaker"] == "chat_agent"])
        
        return {
            "total_turns": len(self.conversation_history),
            "user_agent_turns": user_agent_turns,
            "chat_agent_turns": chat_agent_turns,
            "conversation_started": self.conversation_history[0]["timestamp"],
            "last_message": self.conversation_history[-1]["timestamp"]
        }
    
    def __str__(self) -> str:
        """String representation of the UserAgent."""
        return f"UserAgent(id={self.agent_id}, turns={len(self.conversation_history)})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the UserAgent."""
        return f"UserAgent(agent_id='{self.agent_id}', model='{self.model}', conversation_turns={len(self.conversation_history)})"


# Predefined UserAgent templates for common scenarios
class UserAgentTemplates:
    """Predefined templates for creating UserAgents with common personalities and scenarios."""
    
    @staticmethod
    def create_frustrated_customer(agent_id: str = "frustrated_customer") -> UserAgent:
        """Create a frustrated customer with delayed materials."""
        return UserAgent(
            agent_id=agent_id,
            personality_file="frustrated.txt",
            problem_roleplay_file="delayed_materials.txt"
        )
    
    @staticmethod
    def create_confused_elderly_user(agent_id: str = "confused_elderly") -> UserAgent:
        """Create a confused elderly user with tool setup problems."""
        return UserAgent(
            agent_id=agent_id,
            personality_file="confused_elderly.txt",
            problem_roleplay_file="tool_setup.txt"
        )
    
    @staticmethod
    def create_anxious_student(agent_id: str = "anxious_student") -> UserAgent:
        """Create an anxious DIYer needing project help."""
        return UserAgent(
            agent_id=agent_id,
            personality_file="anxious.txt",
            problem_roleplay_file="diy_project_help.txt"
        )
    
    @staticmethod
    def create_demanding_executive(agent_id: str = "demanding_executive") -> UserAgent:
        """Create a demanding contractor with urgent commercial needs."""
        return UserAgent(
            agent_id=agent_id,
            personality_file="demanding.txt",
            problem_roleplay_file="commercial_urgent.txt"
        )
    
    @staticmethod
    def create_frustrated_homeowner(agent_id: str = "frustrated_homeowner") -> UserAgent:
        """Create a frustrated person with home improvement needs."""
        return UserAgent(
            agent_id=agent_id,
            personality_file="frustrated.txt",
            problem_roleplay_file="home_improvement.txt"
        )
    
    @staticmethod
    def create_anxious_tech_user(agent_id: str = "anxious_tech_user") -> UserAgent:
        """Create an anxious person with tool setup problems."""
        return UserAgent(
            agent_id=agent_id,
            personality_file="anxious.txt",
            problem_roleplay_file="tool_setup.txt"
        )
    
    @staticmethod
    def create_demanding_customer(agent_id: str = "demanding_customer") -> UserAgent:
        """Create a demanding customer with delayed materials."""
        return UserAgent(
            agent_id=agent_id,
            personality_file="demanding.txt",
            problem_roleplay_file="delayed_materials.txt"
        )
    
    @staticmethod
    def create_elderly_homeowner(agent_id: str = "elderly_homeowner") -> UserAgent:
        """Create an elderly person needing home improvement help."""
        return UserAgent(
            agent_id=agent_id,
            personality_file="confused_elderly.txt",
            problem_roleplay_file="home_improvement.txt"
        ) 
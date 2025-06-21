import time
from datetime import datetime
from typing import Optional, Dict, Any
from user_agent import UserAgent
from chat_agent import ChatAgent

class ConversationOrchestrator:
    """
    Orchestrates conversations between UserAgents and ChatAgents, managing
    the flow of conversation and saving transcripts.
    """
    
    def __init__(self, user_agent: UserAgent, chat_agent: ChatAgent):
        """
        Initialize the conversation orchestrator.
        
        Args:
            user_agent: The UserAgent instance
            chat_agent: The ChatAgent instance
        """
        self.user_agent = user_agent
        self.chat_agent = chat_agent
        self.conversation_active = False
    
    def start_conversation(self, initial_message: Optional[str] = None, max_turns: int = 10, 
                          delay_between_turns: float = 1.0) -> Dict[str, Any]:
        """
        Start a conversation between the agents.
        
        Args:
            initial_message: Optional initial message from ChatAgent. If None, uses chat_agent's initial_message or UserAgent starts.
            max_turns: Maximum number of conversation turns
            delay_between_turns: Delay in seconds between turns (for rate limiting)
            
        Returns:
            Dictionary with conversation results and metadata
        """
        print(f"Starting conversation between {self.user_agent.agent_id} and {self.chat_agent.agent_id}")
        print("=" * 60)
        
        self.conversation_active = True
        turn_count = 0
        
        # Determine initial message: parameter > chat_agent.initial_message > user agent starts
        if initial_message is not None:
            last_message = initial_message
        elif hasattr(self.chat_agent, 'initial_message') and self.chat_agent.initial_message:
            last_message = self.chat_agent.initial_message
        else:
            last_message = None
        
        # If we have an initial message from ChatAgent, use it
        if last_message is not None:
            print(f"[{self.chat_agent.agent_id}]: {last_message}")
        else:
            # Otherwise, let the user agent start
            print(f"\n[{self.user_agent.agent_id}] Starting conversation...")
            last_message = self.user_agent.generate_response("Hello, I need some help.")
            if last_message is None:
                return self._create_result_dict(False, "Failed to generate initial user message", turn_count)
            
            print(f"[{self.user_agent.agent_id}]: {last_message}")
            turn_count += 1
        
        # Main conversation loop
        while self.conversation_active and turn_count < max_turns:
            time.sleep(delay_between_turns)  # Rate limiting
            
            if turn_count % 2 == (0 if initial_message else 1):
                # ChatAgent's turn
                print(f"\n[{self.chat_agent.agent_id}] Thinking...")
                response = self.chat_agent.generate_response(
                    last_message, 
                    self.user_agent.conversation_history
                )
                
                if response is None:
                    print("ChatAgent failed to generate response")
                    break
                
                print(f"[{self.chat_agent.agent_id}]: {response}")
                last_message = response
                
                # Update UserAgent's conversation history with ChatAgent's response
                # (This will be done in the next UserAgent call)
                
            else:
                # UserAgent's turn
                print(f"\n[{self.user_agent.agent_id}] Thinking...")
                response = self.user_agent.generate_response(last_message)
                
                if response is None:
                    print("UserAgent failed to generate response")
                    break
                
                print(f"[{self.user_agent.agent_id}]: {response}")
                last_message = response
                
                # Check if UserAgent said goodbye - if so, let ChatAgent respond once more
                if self._should_end_conversation(last_message):
                    print(f"\n[{self.chat_agent.agent_id}] Providing final response...")
                    time.sleep(delay_between_turns)
                    
                    final_response = self.chat_agent.generate_response(
                        last_message, 
                        self.user_agent.conversation_history
                    )
                    
                    if final_response:
                        print(f"[{self.chat_agent.agent_id}]: {final_response}")
                        # Add the final ChatAgent response to conversation history
                        self.user_agent.conversation_history.append({
                            "speaker": "chat_agent",
                            "message": final_response,
                            "timestamp": datetime.now().isoformat()
                        })
                        turn_count += 1
                    
                    print("\nConversation ended naturally.")
                    break
            
            turn_count += 1
        
        print(f"Conversation completed after {turn_count} turns")
        
        # Save the conversation
        filepath = self.user_agent.save_conversation()
        print(f"Conversation saved to: {filepath}")
        
        return self._create_result_dict(True, "Conversation completed successfully", turn_count, filepath)
    
    def _should_end_conversation(self, message: str) -> bool:
        ending_phrase = "thank you, goodbye." #set in base_prompt.txt
        message_lower = message.lower()
        if ending_phrase in message_lower:
            return True
        else:
            return False
    
    def _create_result_dict(self, success: bool, message: str, turn_count: int, 
                           filepath: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a standardized result dictionary.
        
        Args:
            success: Whether the conversation was successful
            message: Result message
            turn_count: Number of turns in the conversation
            filepath: Path to saved conversation file
            
        Returns:
            Dictionary with conversation results
        """
        return {
            "success": success,
            "message": message,
            "turn_count": turn_count,
            "user_agent_id": self.user_agent.agent_id,
            "chat_agent_id": self.chat_agent.agent_id,
            "conversation_summary": self.user_agent.get_conversation_summary(),
            "saved_filepath": filepath
        }
    
    def stop_conversation(self):
        """Stop the current conversation."""
        self.conversation_active = False
        print("Conversation stopped by orchestrator.")
    
    def get_conversation_status(self) -> Dict[str, Any]:
        """
        Get current conversation status.
        
        Returns:
            Dictionary with status information
        """
        return {
            "active": self.conversation_active,
            "user_agent": str(self.user_agent),
            "chat_agent": str(self.chat_agent),
            "conversation_summary": self.user_agent.get_conversation_summary()
        } 
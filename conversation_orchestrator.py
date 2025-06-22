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
        
        # If we have an initial message from ChatAgent, use it and add to history
        if last_message is not None:
            print(f"[{self.chat_agent.agent_id}]: {last_message}")
            # Add initial chat_agent message to conversation history (no API call timing)
            self.user_agent.conversation_history.append({
                "speaker": "chat_agent",
                "message": last_message,
                "timestamp": datetime.now().isoformat(),
                "response_time_seconds": "0.0"  # No API call for initial message
            })
        else:
            # Otherwise, let the user agent start
            print(f"\n[{self.user_agent.agent_id}] Starting conversation...")
            
            # Track timing for initial user agent response
            start_time = time.time()
            last_message = self.user_agent.generate_response("Hello, I need some help.")
            end_time = time.time()
            response_time = end_time - start_time
            
            if last_message is None:
                return self._create_result_dict(False, "Failed to generate initial user message", turn_count)
            
            # Update the last conversation entry with timing data
            if self.user_agent.conversation_history:
                self.user_agent.conversation_history[-1]['response_time_seconds'] = str(round(response_time, 3))
            
            print(f"[{self.user_agent.agent_id}]: {last_message} (Response time: {response_time:.3f}s)")
            turn_count += 1
        
        # Main conversation loop
        while self.conversation_active and turn_count < max_turns:
            time.sleep(delay_between_turns)  # Rate limiting
            
            if turn_count % 2 == (0 if initial_message else 1):
                # ChatAgent's turn
                print(f"\n[{self.chat_agent.agent_id}] Thinking...")
                
                # Track timing for chat agent response
                start_time = time.time()
                response = self.chat_agent.generate_response(
                    last_message, 
                    self.user_agent.conversation_history
                )
                end_time = time.time()
                response_time = end_time - start_time
                
                if response is None:
                    print("ChatAgent failed to generate response")
                    break
                
                # Add chat agent response to user agent's conversation history with timing
                self.user_agent.conversation_history.append({
                    "speaker": "chat_agent",
                    "message": response,
                    "timestamp": datetime.now().isoformat(),
                    "response_time_seconds": str(round(response_time, 3))
                })
                
                print(f"[{self.chat_agent.agent_id}]: {response} (Response time: {response_time:.3f}s)")
                last_message = response
                
            else:
                # UserAgent's turn
                print(f"\n[{self.user_agent.agent_id}] Thinking...")
                
                # Track timing for user agent response
                start_time = time.time()
                response = self.user_agent.generate_response(last_message)
                end_time = time.time()
                response_time = end_time - start_time
                
                if response is None:
                    print("UserAgent failed to generate response")
                    break
                
                # Update the last conversation entry (user_agent response) with timing data
                if self.user_agent.conversation_history and self.user_agent.conversation_history[-1]['speaker'] == 'user_agent':
                    self.user_agent.conversation_history[-1]['response_time_seconds'] = str(round(response_time, 3))
                
                print(f"[{self.user_agent.agent_id}]: {response} (Response time: {response_time:.3f}s)")
                last_message = response
                
                # Check if UserAgent said goodbye - if so, let ChatAgent respond once more
                if self._should_end_conversation(last_message):
                    print(f"\n[{self.chat_agent.agent_id}] Providing final response...")
                    time.sleep(delay_between_turns)
                    
                    # Track timing for final chat agent response
                    start_time = time.time()
                    final_response = self.chat_agent.generate_response(
                        last_message, 
                        self.user_agent.conversation_history
                    )
                    end_time = time.time()
                    response_time = end_time - start_time
                    
                    if final_response:
                        print(f"[{self.chat_agent.agent_id}]: {final_response} (Response time: {response_time:.3f}s)")
                        # Add the final ChatAgent response to conversation history with timing
                        self.user_agent.conversation_history.append({
                            "speaker": "chat_agent",
                            "message": final_response,
                            "timestamp": datetime.now().isoformat(),
                            "response_time_seconds": str(round(response_time, 3))
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
        # Calculate timing statistics
        timing_stats = self._calculate_timing_stats()
        
        result = {
            "success": success,
            "message": message,
            "turn_count": turn_count,
            "user_agent_id": self.user_agent.agent_id,
            "chat_agent_id": self.chat_agent.agent_id,
            "conversation_summary": self.user_agent.get_conversation_summary(),
            "saved_filepath": filepath,
            "timing_statistics": timing_stats
        }
        
        return result
    
    def _calculate_timing_stats(self) -> Dict[str, Any]:
        """
        Calculate timing statistics from the conversation history.
        
        Returns:
            Dictionary with timing statistics
        """
        user_agent_times = []
        chat_agent_times = []
        
        for entry in self.user_agent.conversation_history:
            if 'response_time_seconds' in entry:
                try:
                    response_time = float(entry['response_time_seconds'])
                    if entry['speaker'] == 'user_agent':
                        user_agent_times.append(response_time)
                    elif entry['speaker'] == 'chat_agent':
                        chat_agent_times.append(response_time)
                except ValueError:
                    # Skip entries with invalid timing data
                    continue
        
        stats = {
            "total_requests": len(user_agent_times) + len(chat_agent_times),
            "user_agent": {
                "total_requests": len(user_agent_times),
                "total_time_seconds": round(sum(user_agent_times), 3) if user_agent_times else 0,
                "average_time_seconds": round(sum(user_agent_times) / len(user_agent_times), 3) if user_agent_times else 0,
                "min_time_seconds": min(user_agent_times) if user_agent_times else 0,
                "max_time_seconds": max(user_agent_times) if user_agent_times else 0
            },
            "chat_agent": {
                "total_requests": len(chat_agent_times),
                "total_time_seconds": round(sum(chat_agent_times), 3) if chat_agent_times else 0,
                "average_time_seconds": round(sum(chat_agent_times) / len(chat_agent_times), 3) if chat_agent_times else 0,
                "min_time_seconds": min(chat_agent_times) if chat_agent_times else 0,
                "max_time_seconds": max(chat_agent_times) if chat_agent_times else 0
            }
        }
        
        return stats
    
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
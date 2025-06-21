#!/usr/bin/env python3
"""
Example script demonstrating how to use the UserAgent system for 
agent-to-agent conversations with transcript saving.
"""

from user_agent import UserAgent, UserAgentTemplates
from chat_agent import ChatAgent, ChatAgentTemplates
from conversation_orchestrator import ConversationOrchestrator

def example_custom_agents():
    """Example using custom UserAgent and ChatAgent."""
    print("=== Custom Agents Example ===")
    
    # Create a custom UserAgent
    user_agent = UserAgent(
        agent_id="frustrated_shopper",
        personality_prompt="You are extremely frustrated and impatient. You've had a bad day and this problem is the last straw. You tend to be short-tempered and demand immediate solutions.",
        problem_roleplay_prompt="You ordered a birthday gift for your child 5 days ago with express shipping, but it hasn't arrived yet. The birthday party is tomorrow and you're panicking.",
        base_prompt="You are a customer calling customer service. Stay in character as an angry, frustrated parent who needs immediate help. Don't break character."
    )
    
    # Create a custom ChatAgent
    chat_agent = ChatAgent(
        agent_id="calm_service_rep",
        system_prompt="""You are an experienced, calm customer service representative. 
        You've dealt with many frustrated customers and know how to de-escalate situations.
        You should:
        - Remain calm and professional no matter how angry the customer gets
        - Acknowledge their frustration and apologize for the inconvenience
        - Ask for specific details (order number, address, etc.)
        - Provide concrete solutions and timelines
        - Follow up to ensure satisfaction"""
    )
    
    # Create orchestrator and start conversation
    orchestrator = ConversationOrchestrator(user_agent, chat_agent)
    result = orchestrator.start_conversation(
        initial_message="Hello! Thank you for calling customer service. How can I help you today?",
        max_turns=8,
        delay_between_turns=0.5
    )
    
    print(f"\nConversation Result: {result}")
    return result

def example_template_agents():
    """Example using predefined agent templates."""
    print("\n=== Template Agents Example ===")
    
    # Create agents using templates
    user_agent = UserAgentTemplates.create_confused_elderly_user("elderly_user_001")
    chat_agent = ChatAgentTemplates.create_tech_support_agent("tech_support_001")
    
    # Create orchestrator and start conversation
    orchestrator = ConversationOrchestrator(user_agent, chat_agent)
    result = orchestrator.start_conversation(
        max_turns=6,
        delay_between_turns=0.5
    )
    
    print(f"\nConversation Result: {result}")
    return result

def example_student_tutor():
    """Example of student-tutor interaction."""
    print("\n=== Student-Tutor Example ===")
    
    # Create agents
    user_agent = UserAgentTemplates.create_anxious_student("student_001")
    chat_agent = ChatAgentTemplates.create_academic_tutor("tutor_001")
    
    # Create orchestrator and start conversation
    orchestrator = ConversationOrchestrator(user_agent, chat_agent)
    result = orchestrator.start_conversation(
        initial_message="Hi! I understand you have an assignment you're worried about. Can you tell me what subject it's for and what specific help you need?",
        max_turns=10,
        delay_between_turns=0.5
    )
    
    print(f"\nConversation Result: {result}")
    return result

def demonstrate_conversation_analysis():
    """Demonstrate conversation analysis features."""
    print("\n=== Conversation Analysis Example ===")
    
    # Create a simple conversation
    user_agent = UserAgentTemplates.create_demanding_executive("exec_001")
    chat_agent = ChatAgentTemplates.create_executive_assistant("assistant_001")
    
    orchestrator = ConversationOrchestrator(user_agent, chat_agent)
    result = orchestrator.start_conversation(max_turns=4, delay_between_turns=0.3)
    
    # Analyze the conversation
    summary = user_agent.get_conversation_summary()
    print(f"\nConversation Analysis:")
    print(f"- Total turns: {summary['total_turns']}")
    print(f"- User agent turns: {summary['user_agent_turns']}")
    print(f"- Chat agent turns: {summary['chat_agent_turns']}")
    print(f"- Started: {summary['conversation_started']}")
    print(f"- Last message: {summary['last_message']}")
    
    return result

def main():
    """Run all examples."""
    print("UserAgent Conversation System Examples")
    print("=" * 50)
    
    try:
        # Run examples
        example_custom_agents()
        example_template_agents()
        example_student_tutor()
        demonstrate_conversation_analysis()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        print("Check the 'conversations' directory for saved transcripts.")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure you have:")
        print("1. Set up your LLAMA_API_KEY environment variable")
        print("2. Installed required dependencies (pip install -r requirements.txt)")

if __name__ == "__main__":
    main() 
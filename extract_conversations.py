#!/usr/bin/env python3
"""
Script to extract conversation data from batch folders and convert to Hugging Face compatible JSONL format.
Each line in the output will be a complete conversation in the format:
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
"""

import json
import os
import glob

def is_valid_conversation(data):
    """
    Check if a conversation is valid and should be included in the extraction.
    
    Args:
        data (dict): The conversation data loaded from JSON file
        
    Returns:
        bool: True if conversation is valid, False otherwise
    """
    # Check if conversation array exists and is not empty
    conversation = data.get('conversation', [])
    if not conversation or len(conversation) == 0:
        return False
    
    # Check if conversation_start and conversation_end are not null
    conversation_start = data.get('conversation_start')
    conversation_end = data.get('conversation_end')
    if conversation_start is None or conversation_end is None:
        return False
    
    # Check if total_turns is greater than 0
    total_turns = data.get('total_turns', 0)
    if total_turns <= 0:
        return False
    
    # Check if conversation has at least one user message and one assistant message
    user_messages = [msg for msg in conversation if msg.get('speaker') == 'user_agent']
    assistant_messages = [msg for msg in conversation if msg.get('speaker') == 'chat_agent']
    
    if len(user_messages) == 0 or len(assistant_messages) == 0:
        return False
    
    # Check if all messages have valid content
    for msg in conversation:
        if not msg.get('message') or not msg.get('speaker'):
            return False
    
    return True

def extract_conversations_to_jsonl(input_dir="conversations", output_file="conversations.jsonl"):
    """
    Extract all conversations from batch folders and save as Hugging Face compatible JSONL file.
    
    Args:
        input_dir (str): Directory containing batch folders
        output_file (str): Output JSONL file path
    """
    
    # Find all conversation JSON files
    conversation_files = []
    batch_dirs = glob.glob(os.path.join(input_dir, "batch_*"))
    
    for batch_dir in batch_dirs:
        if os.path.isdir(batch_dir):
            json_files = glob.glob(os.path.join(batch_dir, "conversation_*.json"))
            conversation_files.extend(json_files)
    
    print(f"Found {len(conversation_files)} conversation files")
    
    # Process each conversation file
    processed_count = 0
    skipped_count = 0
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file_path in conversation_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    data = json.load(infile)
                
                # Validate conversation before processing
                if not is_valid_conversation(data):
                    print(f"Skipping invalid conversation: {file_path}")
                    print(f"  - conversation_start: {data.get('conversation_start')}")
                    print(f"  - conversation_end: {data.get('conversation_end')}")
                    print(f"  - total_turns: {data.get('total_turns')}")
                    print(f"  - conversation_length: {len(data.get('conversation', []))}")
                    skipped_count += 1
                    continue
                
                # Extract conversation messages
                conversation = data.get('conversation', [])
                
                # Convert to required format
                messages = []
                
                # Add system message
                messages.append({
                    "role": "system",
                    "content": "You are a friendly homedepot chatbot."
                })
                
                # Convert conversation messages
                for msg in conversation:
                    speaker = msg.get('speaker', '')
                    content = msg.get('message', '')
                    
                    if speaker == 'chat_agent':
                        role = 'assistant'
                    elif speaker == 'user_agent':
                        role = 'user'
                    else:
                        # Skip unknown speaker types
                        continue
                    
                    messages.append({
                        "role": role,
                        "content": content
                    })
                
                # Write to JSONL file - each conversation as one line
                json_line = {"messages": messages}
                outfile.write(json.dumps(json_line, ensure_ascii=False) + '\n')
                processed_count += 1
                
                if processed_count % 10 == 0:
                    print(f"Processed {processed_count} conversations...")
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                skipped_count += 1
                continue
    
    print(f"Successfully processed {processed_count} conversations")
    print(f"Skipped {skipped_count} invalid conversations")
    print(f"Output saved to: {output_file}")
    
    return processed_count

def main():
    """Main function to run the extraction."""
    print("Starting conversation extraction for Hugging Face fine-tuning...")
    
    # Check if conversations directory exists
    if not os.path.exists("conversations"):
        print("Error: 'conversations' directory not found!")
        return
    
    # Extract conversations
    count = extract_conversations_to_jsonl()
    
    if count > 0:
        print(f"\n✅ Successfully extracted {count} conversations to conversations.jsonl")
        print("The file is now ready for Hugging Face fine-tuning!")
        print("Each line contains one complete conversation in the format:")
        print('{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}')
    else:
        print("❌ No conversations were extracted. Please check the conversations directory.")

if __name__ == "__main__":
    main() 
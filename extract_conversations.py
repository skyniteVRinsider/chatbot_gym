#!/usr/bin/env python3
"""
Script to extract conversation data from batch folders and convert to Hugging Face compatible JSONL format.
Each line in the output will be a complete conversation in the format:
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
"""

import json
import os
import glob

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
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file_path in conversation_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    data = json.load(infile)
                
                # Extract conversation messages
                conversation = data.get('conversation', [])
                if not conversation:
                    print(f"Warning: No conversation found in {file_path}")
                    continue
                
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
                continue
    
    print(f"Successfully processed {processed_count} conversations")
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
import json
import os
from sklearn.model_selection import train_test_split

def extract_prompt_response_pairs(messages):
    pairs = []
    history = []

    for i in range(len(messages) - 1):
        curr_msg = messages[i]
        next_msg = messages[i + 1]

        if curr_msg["role"] == "user" and next_msg["role"] == "assistant":
            # Format conversation history
            conversation = ""
            for m in history:
                role = m["role"].capitalize()
                conversation += f"{role}: {m['content']}\n"

            # Add current user turn
            conversation += f"User: {curr_msg['content']}"
            response = next_msg["content"]

            pairs.append({
                "prompt": conversation.strip(),
                "response": response.strip()
            })

        # Append to history regardless of role
        history.append(curr_msg)

    return pairs

def main():
    input_path = "conversations.jsonl"
    output_dir = "dataset"
    os.makedirs(output_dir, exist_ok=True)

    all_pairs = []
    with open(input_path, "r") as f:
        for line in f:
            try:
                sample = json.loads(line.strip())
                messages = sample.get("messages", [])
                pairs = extract_prompt_response_pairs(messages)
                all_pairs.extend(pairs)
            except Exception as e:
                print(f"Skipping a line due to error: {e}")

    # Split into train/test
    train, test = train_test_split(all_pairs, test_size=0.2, random_state=42)

    with open(f"{output_dir}/train_dataset.json", "w") as f:
        json.dump(train, f, indent=2, ensure_ascii=False)

    with open(f"{output_dir}/test_dataset.json", "w") as f:
        json.dump(test, f, indent=2, ensure_ascii=False)

    print(f"✅ Converted {len(all_pairs)} total examples")
    print(f"📁 Saved {len(train)} to {output_dir}/train_dataset.json")
    print(f"📁 Saved {len(test)} to {output_dir}/test_dataset.json")

if __name__ == "__main__":
    main()

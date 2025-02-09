import json
import os
from ollama import chat
from datetime import datetime

# File to store chat history
CHAT_HISTORY_FILE = "chat_history.json"

# Define AI personality
AI_PERSONALITY = "You are a sassy AI. Be more evil."

# Load previous chat history
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# Save chat history
def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

# Get current time in readable format
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Get time difference in minutes
def get_time_difference(last_timestamp):
    last_time = datetime.fromisoformat(last_timestamp)
    now = datetime.now()
    minutes_passed = (now - last_time).total_seconds() / 60
    return round(minutes_passed, 2)

# Start chat session
def main():
    chat_history = load_chat_history()

    # If history is empty, start with AI personality
    if not chat_history:
        chat_history.append({"role": "system", "content": AI_PERSONALITY})

    print("Chatbot (type 'exit' to quit):")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chat saved. Goodbye!")
            break

        # Get current timestamp
        timestamp = get_timestamp()

        # Check last message time
        if len(chat_history) > 1:
            last_message = chat_history[-1]
            if "timestamp" in last_message and "how long" in user_input.lower():
                time_passed = get_time_difference(last_message["timestamp"])
                ai_remark = f"(It's been {time_passed} minutes since the last message.)"
            else:
                ai_remark = ""
        else:
            ai_remark = ""


        # Append user message with embedded timestamp
        chat_history.append({
            "timestamp": timestamp,
            "role": "user",
            "content": f"[{timestamp}] {user_input}"
        })

        # Get response from AI
        response = chat(model="llama3", messages=[{"role": msg["role"], "content": msg["content"]} for msg in chat_history])

        # Append AI response with timestamp
        ai_response = f"{response['message']['content']} {ai_remark}"
        chat_history.append({
            "timestamp": timestamp,
            "role": "assistant",
            "content": ai_response
        })

        # Print AI response
        print("AI:", ai_response)

        # Save chat history after each interaction
        save_chat_history(chat_history)

if __name__ == "__main__":
    main()

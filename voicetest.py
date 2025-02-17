import os
import json
import random
from gtts import gTTS
from datetime import datetime
import playsound
import re
from ollama import chat

# File to store chat history
CHAT_HISTORY_FILE = "chat_history.json"
AI_PERSONALITY = "ai_personality.txt"

# Load AI personality from file
def load_ai_personality():
    if os.path.exists(AI_PERSONALITY):
        with open(AI_PERSONALITY, "r", encoding="utf-8") as file:
            return file.read().strip()
    return "You are a helpful and friendly AI assistant."

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

# Function to remove timestamps from responses
def remove_timestamp(text):
    return re.sub(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]", "", text).strip()

# Function to convert text to speech
def speak(text):
    tts = gTTS(text=text, lang="en", tld="com.au")  # "com.au" gives a girly Australian accent
    filename = "response.mp3"
    tts.save(filename)
    # playsound.playsound(filename)
    os.remove(filename)

# Get current time in readable format
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Get time difference in minutes
def get_time_difference(last_timestamp):
    last_time = datetime.fromisoformat(last_timestamp)
    now = datetime.now()
    return round((now - last_time).total_seconds() / 60, 2)

# Determine if AI should start the conversation
def should_ai_start(chat_history):
    if not chat_history:  
        return True  # Start the conversation if no history

    last_message = chat_history[-1]
    if "timestamp" in last_message:
        time_passed = get_time_difference(last_message["timestamp"])
        if time_passed > 10:  # If more than 10 minutes have passed, AI can re-engage
            return True

    return random.choice([True, False])  # Random chance of AI starting

# AI dynamically generates an opening message based on chat history
def ai_initiate_chat(chat_history):
    ai_personality = load_ai_personality()
    messages = [{"role": msg["role"], "content": msg["content"]} for msg in chat_history[-5:]]  # Use last 5 messages for context
    
    messages.insert(0, {"role": "system", "content": ai_personality})
    messages.append({"role": "user", "content": "Can you start the conversation?"})

    response = chat(model="llama3.2", messages=messages)
    return response['message']['content']

# Start chat session
def main():
    chat_history = load_chat_history()
    ai_personality = load_ai_personality()

    if not chat_history:
        chat_history.append({"role": "system", "content": ai_personality})

    print("Chatbot (type 'exit' to quit):")

    # AI initiates conversation if needed
    if should_ai_start(chat_history):
        ai_greeting = ai_initiate_chat(chat_history)
        print(f"LUNA: {ai_greeting}")
        speak(ai_greeting)

        chat_history.append({
            "timestamp": get_timestamp(),
            "role": "assistant",
            "content": ai_greeting
        })
        save_chat_history(chat_history)

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chat saved. Goodbye!")
            break

        timestamp = get_timestamp()

        chat_history.append({
            "timestamp": timestamp,
            "role": "user",
            "content": f"[{timestamp}] {user_input}"
        })

        # AI response
        response = chat(model="llama3.2", messages=[{"role": msg["role"], "content": msg["content"]} for msg in chat_history])
        ai_response = response['message']['content']

        chat_history.append({
            "timestamp": timestamp,
            "role": "assistant",
            "content": ai_response
        })

        print(f"LUNA: {ai_response}\n")
        speak(ai_response)

        save_chat_history(chat_history)

if __name__ == "__main__":
    main()

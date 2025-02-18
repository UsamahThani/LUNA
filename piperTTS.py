import os
import json
import random
import re
import requests
from datetime import datetime
from ollama import chat
import time
import shutil
from playsound import playsound  # Import the playsound module

# File to store chat history
CHAT_HISTORY_FILE = "chat_history.json"
AI_PERSONALITY = "ai_personality.txt"

# Piper server URL (Assuming it's running locally)
PIPER_SERVER_URL = "http://localhost:5000/"

# Init model name
modelname = "llama3.2"

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

# Check if the file is in use
def is_file_in_use(file_path):
    try:
        with open(file_path, 'r+'):
            return False
    except IOError:
        return True

# Delete the file after use if it's not in use
def delete_file(file_path):
    if not is_file_in_use(file_path):
        try:
            os.remove(file_path)
            print(f"File {file_path} deleted successfully.")
        except PermissionError:
            print("Error: The file is still in use by another process.")
    else:
        print(f"File {file_path} is in use, cannot delete it.")

# Function to convert text to speech using Piper TTS
def speak(text):
    response = requests.get(PIPER_SERVER_URL, params={"text": text})
    
    if response.status_code == 200:
        with open("response.wav", "wb") as f:
            f.write(response.content)

        # Wait until the file is created and accessible
        retries = 5
        while retries > 0:
            if os.path.exists("response.wav") and os.path.getsize("response.wav") > 0:
                break
            time.sleep(0.1)
            retries -= 1

        try:
            playsound("response.wav")
        except Exception as e:
            print(f"Error playing sound: {e}")
        finally:
            time.sleep(1)  # Ensure playback completes before deleting
            delete_file("response.wav")
    else:
        print("Error: Unable to generate speech.")
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

    response = chat(model=modelname, messages=messages)
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
        response = chat(model=modelname, messages=[{"role": msg["role"], "content": msg["content"]} for msg in chat_history])
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

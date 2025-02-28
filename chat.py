import json
import keyboard
import geocoder
from datetime import datetime
from tts import speak
from stt import record_audio, transcribe_audio
from weather import get_weather
from config import CHAT_HISTORY_FILE, AI_PERSONALITY, modelname
from ollama import chat

def load_ai_personality():
    with open(AI_PERSONALITY, "r", encoding="utf-8") as file:
        return file.read().strip()

def load_chat_history():
    if CHAT_HISTORY_FILE.exists():
        with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)

def chat_session():
    chat_history = load_chat_history()
    ai_personality = load_ai_personality()

    # Ensure the AI personality is set at the start of the session
    if not chat_history or chat_history[0]["role"] != "system":
        chat_history.insert(0, {"role": "system", "content": ai_personality})

    while True:
        print("Press ESC to type or Space to record your voice.")
        while True:
            event = keyboard.read_event(suppress=False)
            if event.event_type == "down":
                if event.name == "esc":
                    user_input = input("Type your message: ")
                    break
                elif event.name == "space":
                    audio_file = record_audio()
                    user_input = transcribe_audio(audio_file)
                    print(f"\nYou: {user_input}\n")
                    break

        if user_input.lower() == "exit":
            print("Chat saved. Goodbye!")
            save_chat_history(chat_history)  # Save history before exiting
            break

        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d")
        g = geocoder.ip('me')
        weather_info = get_weather()

        system_content = []

        if any(word in user_input.lower() for word in ["time", "clock"]):
            system_content.append(f"The current time is {current_time}. You should be aware of time.")

        if any(word in user_input.lower() for word in ["date"]):
            system_content.append(f"The current date is {current_date}. You should be aware of date.")

        if any(word in user_input.lower() for word in ["location", "where we at", "where am i"]):
            system_content.append(f"The location is {g.city}, {g.state}, {g.country}. Don't mention this unless the user asks for it.")

        if "weather" in user_input.lower():
            system_content.append(f"The weather now is {weather_info}. Don't mention this unless the user asks for it.")

        if system_content:
            chat_history.append({"role": "system", "content": " ".join(system_content)})

        # Add user input to chat history
        chat_history.append({"timestamp": current_time, "role": "user", "content": user_input})

        # Pass complete chat history (excluding timestamps) to AI
        messages = [{"role": msg["role"], "content": msg["content"]} for msg in chat_history]

        response = chat(model=modelname, messages=messages)
        ai_response = response['message']['content']

        # Append AI response to history
        chat_history.append({"timestamp": current_time, "role": "assistant", "content": ai_response})

        print(f"\nLUNA: {ai_response}\n")
        
        # Attempt to speak, but continue even if it fails
        if not speak(ai_response):
            print("Text-to-speech failed, continuing in text-only mode.")
        
        save_chat_history(chat_history)
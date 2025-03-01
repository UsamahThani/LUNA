import json
import keyboard
import geocoder
from datetime import datetime
from tts import speak
from stt import record_audio, transcribe_audio
from weather import get_weather
from config import CHAT_HISTORY_FILE, modelname
from ollama import chat

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

    while True:
        print("Press 'Ctrl + Shift + T' to type or 'Ctrl + Shift + R' to record your voice.")
        while True:
            if keyboard.is_pressed("ctrl+shift+t"):  # Ctrl + Shift + T for typing
                user_input = input("Type your message: ")
                break
            elif keyboard.is_pressed("ctrl+shift+r"):  # Ctrl + Shift + R for recording
                audio_file = record_audio()
                user_input = transcribe_audio(audio_file)
                print(f"\nYou: {user_input}\n")
                break
            elif keyboard.is_pressed("esc"):
                print("Chat saved. Goodbye!")
                save_chat_history(chat_history)
                return

        if user_input is None:
            continue

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

        # Add user input to chat history
        chat_history.append({"timestamp": current_time, "role": "user", "content": user_input})

        # Pass complete chat history (excluding timestamps) to AI
        messages = [{"role": msg["role"], "content": msg["content"]} for msg in chat_history]

        response = chat(model=modelname, messages=messages)
        ai_response = response['message']['content']

        # Append AI response to history
        chat_history.append({"timestamp": current_time, "role": "assistant", "content": ai_response})

        print(f"\nLUNA: {ai_response}\n")
        
        # Attempt to speak, and check if playback was interrupted
        success, playback_completed = speak(ai_response)
        if not success:
            print("Text-to-speech failed, continuing in text-only mode.")
        elif not playback_completed:
            system_content.append("User just mute/skip your voice. How rude. You should scold him.")

        if system_content:
            chat_history.append({"role": "system", "content": " ".join(system_content)})
        
        save_chat_history(chat_history)

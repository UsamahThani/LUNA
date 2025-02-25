import json
import keyboard
import geocoder
from datetime import datetime
from tts import speak
from stt import record_audio, transcribe_audio
from weather import get_weather
from config import CHAT_HISTORY_FILE, AI_PERSONALITY, modelname
from ollama import chat

# def load_ai_personality():
#     try:
#         with open(AI_PERSONALITY, "r", encoding="utf-8") as file:
#             return file.read().strip()
#     except Exception as e:
#         print(f"Error loading AI personality: {e}")
#         return "I am a helpful AI assistant."

def load_chat_history():
    try:
        if CHAT_HISTORY_FILE.exists():
            with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        return []
    except Exception as e:
        print(f"Error loading chat history: {e}")
        return []

def save_chat_history(history):
    try:
        with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=4)
        print("Chat history saved successfully.")
    except Exception as e:
        print(f"Error saving chat history: {e}")

def chat_session():
    # Load chat history and personality
    chat_history = load_chat_history()
    # ai_personality = load_ai_personality()

    # # Ensure the system message with personality is always present at the start
    # if not any(msg["role"] == "system" and ai_personality in msg["content"] for msg in chat_history):
    #     chat_history.insert(0, {"role": "system", "content": ai_personality})

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
            save_chat_history(chat_history)
            break

        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d")
        g = geocoder.ip('me')
        weather_info = get_weather()

        system_content = []

        if any(word in user_input.lower() for word in ["time", "clock"]):
            system_content.append(f"The current time is {current_time}.")

        if "date" in user_input.lower():
            system_content.append(f"The current date is {current_date}.")

        if any(word in user_input.lower() for word in ["location", "where we at", "where am i"]):
            system_content.append(f"You are in {g.city}, {g.state}, {g.country}.")

        if "weather" in user_input.lower():
            system_content.append(f"The weather now is {weather_info}.")

        # Append system content if there’s any
        if system_content:
            chat_history.append({"role": "system", "content": " ".join(system_content)})

        # Append user message
        chat_history.append({"role": "user", "content": user_input, "timestamp": current_time})

        # Prepare messages for Ollama (exclude timestamps from content)
        messages = [{"role": msg["role"], "content": msg["content"]} for msg in chat_history]

        # Call the chat model
        try:
            response = chat(model=modelname, messages=messages)
            ai_response = response['message']['content']
        except Exception as e:
            ai_response = f"Sorry, I encountered an error: {e}"
            print(f"Chat error: {e}")

        # Append AI response
        chat_history.append({"role": "assistant", "content": ai_response, "timestamp": current_time})

        print(f"\nLUNA: {ai_response}\n")
        speak(ai_response)
        save_chat_history(chat_history)
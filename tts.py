import os
import time
import requests
from pydub import AudioSegment
from pydub.playback import play
from config import OPENVOICE_SERVER_URL

def speak(text):
    # Try OpenVoice server first
    try:
        data = {"text": text, "voice": "march_voice", "accent": "en-newest", "speed": 1.0}
        response = requests.get(OPENVOICE_SERVER_URL, params=data, timeout=5)  # Added timeout
        
        if response.status_code == 200:
            audio_file = "response.wav"
            with open(audio_file, "wb") as f:
                f.write(response.content)

            try:
                sound = AudioSegment.from_wav(audio_file)
                play(sound)
            except Exception as e:
                print(f"Error playing sound: {e}")
            finally:
                time.sleep(1)
                if os.path.exists(audio_file):
                    os.remove(audio_file)
        else:
            print(f"OpenVoice server error: Status Code {response.status_code}")
            return False  # Indicate failure
    
    except requests.exceptions.RequestException as e:
        print(f"You forgot turn one your open voice server. You idiot.")
        return False  # Indicate failure
    
    return True  # Indicate success
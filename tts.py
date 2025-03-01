import os
import time
import requests
import keyboard
import threading
from pydub import AudioSegment
from config import OPENVOICE_SERVER_URL
import winsound

# Global flag to control playback
should_stop_playback = False

def monitor_keyboard():
    """Monitor for CTRL+M key press to stop audio playback"""
    global should_stop_playback
    while True:
        if keyboard.is_pressed("ctrl+m"):
            should_stop_playback = True
            break
        time.sleep(0.1)

def play_with_interrupt(sound, audio_file):
    """Play sound with an option to interrupt using CTRL+M"""
    global should_stop_playback
    should_stop_playback = False

    # Export the sound to a temporary WAV file (winsound only plays WAV files)
    temp_file = audio_file if os.path.exists(audio_file) else "temp_playback.wav"
    sound.export(temp_file, format="wav")

    # Start monitoring keyboard input in a separate thread
    monitor_thread = threading.Thread(target=monitor_keyboard, daemon=True)
    monitor_thread.start()

    # Play the audio asynchronously using winsound
    winsound.PlaySound(temp_file, winsound.SND_ASYNC | winsound.SND_FILENAME)

    # Poll to check if playback should stop
    duration = len(sound) / 1000  # Duration in seconds
    start_time = time.time()
    while time.time() - start_time < duration:
        if should_stop_playback:
            # Stop playback by playing a null sound (workaround for winsound)
            winsound.PlaySound(None, winsound.SND_PURGE)
            break
        time.sleep(0.1)

    # Clean up temporary file if it was created
    if temp_file != audio_file and os.path.exists(temp_file):
        os.remove(temp_file)

    return not should_stop_playback  # True if completed, False if interrupted

def speak(text):
    try:
        data = {"text": text, "voice": "march_voice", "accent": "en-newest", "speed": 1.0}
        response = requests.get(OPENVOICE_SERVER_URL, params=data, timeout=5)

        if response.status_code == 200:
            audio_file = "response.wav"
            with open(audio_file, "wb") as f:
                f.write(response.content)

            try:
                sound = AudioSegment.from_wav(audio_file)
                completed = play_with_interrupt(sound, audio_file)
                if not completed:
                    print("Playback interrupted with CTRL + M")
            except Exception as e:
                print(f"Error playing sound: {e}")
                return False, False  # Success=False, Completed=False
            finally:
                time.sleep(1)
                if os.path.exists(audio_file):
                    os.remove(audio_file)
            return True, completed  # Success=True, Completed=True/False based on interruption
        else:
            print(f"OpenVoice server error: Status Code {response.status_code}")
            return False, False  # Success=False, Completed=False

    except requests.exceptions.RequestException:
        return False, False  # Success=False, Completed=False
import os
import wave
import pyaudio
import keyboard
from faster_whisper import WhisperModel

def record_audio(output_filename="input.wav"):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    audio = pyaudio.PyAudio()
    
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    print("Recording... (Press SPACE to stop)")
    frames = []
    
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if keyboard.is_pressed("space"):
            print("Recording stopped.")
            break
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    
    return output_filename

def transcribe_audio(audio_path):
    model = WhisperModel("medium")
    segments, _ = model.transcribe(audio_path, language="en")
    transcribed_text = " ".join(segment.text for segment in segments).strip() or None
    
    # If the transcription is empty or None, return "*silence*"
    if not transcribed_text:
        transcribed_text = "*silence*"

    # Remove the file after transcription
    if os.path.exists(audio_path):
        os.remove(audio_path)
    
    return transcribed_text

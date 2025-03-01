import os
from pathlib import Path

# Configuration settings
CHAT_HISTORY_FILE = Path("memory/chat_history.json")
# AI_PERSONALITY = Path("memory/ai_personality.txt")
OPENVOICE_SERVER_URL = "http://192.168.0.9:8080/synthesize_speech/"
modelname = "luna"

# Add cuDNN to library path
os.add_dll_directory("C:\\Program Files\\NVIDIA\\CUDNN\\v9.7\\bin\\12.8")
# LUNA

Project initiated on February 6, 2025

## Prerequisites
Before cloning this repository, ensure you have the following dependencies installed:

### 1. OpenVoiceServer (TTS)
OpenVoiceServer is a high-quality Text-to-Speech (TTS) system using FastAPI. For optimal performance, run it on a separate device using WSL.
- **Repository:** [OpenVoiceServer](https://github.com/ValyrianTech/OpenVoice_server)
- **Guide:** [Setup in wsl](https://github.com/UsamahThani/LUNA/blob/main/guide/OpenVoiceServer_Guide.md)

### 2. CuDNN (for Faster Whisper)
CuDNN is necessary for running Faster Whisper efficiently.
- **Download:** [NVIDIA CuDNN](https://developer.nvidia.com/cudnn)


### 3. Faster Whisper (STT)
Faster Whisper is required for speech-to-text (STT) transcription.
- Install using: `pip install faster-whisper`
- **Repository:** [Faster Whisper](https://github.com/SYSTRAN/faster-whisper)
- **Youtube:** [Tutorial](https://www.youtube.com/watch?v=CfSGIj9QECc)
- If you encounter `Library cublas64_12.dll is not found or cannot be loaded` issue.
  -> Download this [single archive](https://github.com/Purfview/whisper-standalone-win/releases/tag/libs).
  -> Find the one for your Cuda version (11 or 12)
  -> Copy and paste the files into `C:\Program Files\NVIDIA\CUDNN\v9.7\bin\12.8`

### 4. Ollama (AI Model Runtime)
Ollama is used to run AI models. After installation, also install the **Llama3.2** model.
- **Website:** [Ollama](https://ollama.com/)

---
## Installation & Setup

1. **Clone this repository:**
   ```sh
   git clone https://github.com/UsamahThani/LUNA
   cd LUNA
   ```

2. **Create a virtual environment (Python 3.10 recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows, use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```sh
   python main.py
   
---
## Improvements

As for 24/2/2025, I have added fetures like:
1. Local memory: stored all of the chat logs in `chat_history,json` so the AI model could read the histry for more context.
2. Date and time: as the based model is not have this feature, I added the date and time feature whenever user ask for date or time.
3. Text to speech: cloning voice using OpenVoice and run it in server to make the AI speak.
4. Speech to text: transcribe the audio using whisper so the AI interaction more seemless.
5. Live 2D model: using Vtube Studio to run L2D model and using VBA drivers to make L2D model's mouth moving as the AI speaking
6. Weather: AI will be aware of current location weather by implementing simple weather API.

Demo Video: [Twitter Post](https://shorturl.at/n4v8n)

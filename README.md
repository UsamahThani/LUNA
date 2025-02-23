# Project Setup

## Prerequisites
Before cloning this repository, ensure you have the following dependencies installed:

### 1. OpenVoiceServer (TTS)
OpenVoiceServer is a high-quality Text-to-Speech (TTS) system using FastAPI. For optimal performance, run it on a separate device using WSL.
- **Repository:** [OpenVoiceServer](https://github.com/ValyrianTech/OpenVoice_server)

### 2. Faster Whisper (STT)
Faster Whisper is required for speech-to-text (STT) transcription.
- Install using: `pip install faster-whisper`
- **Repository:** [Faster Whisper](https://github.com/SYSTRAN/faster-whisper)

### 3. CuDNN (for Faster Whisper)
CuDNN is necessary for running Faster Whisper efficiently.
- **Download:** [NVIDIA CuDNN](https://developer.nvidia.com/cudnn)
- If you encounter issues, check online solutions.

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
   

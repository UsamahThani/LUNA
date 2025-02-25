# OpenVoice Server Installation Guide

## Overview

This guide provides step-by-step instructions for installing and running the OpenVoice server on Ubuntu.

## Prerequisites

- Ubuntu OS or WSL2 (Window)
- Conda installed ([Installation Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html))
- Git installed

## Installation Steps

### 1. Install Conda and Create a Virtual Environment

```sh
conda create -n openvoice python=3.9
conda activate openvoice
```

### 2. Clone the Repository

```sh
git https://github.com/UsamahThani/OpenVoice_server.git #sam use this
cd OpenVoice_server
```

or

```sh
git https://github.com/ValyrianTech/OpenVoice_server.git
cd OpenVoice_server
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
pip install -e .
```

### 4. Download Additional Resources

```sh
pip install git+https://github.com/myshell-ai/MeloTTS.git
python -m unidic download
```

### 5. Verify Installation

```sh
cd openvoice
```

Get checkpoints folder from [here](https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_1226.zip) and [here](https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip).
Extract and name `checkpoints` and `checkpoints_v2`

```sh
python -c "import openvoice_server; print(dir(openvoice_server))"
```

### 6. Obtain Resources using NLTK

```sh
python
>>> import nltk
>>> nltk.download('averaged_perceptron_tagger_eng')
>>> exit()
```

### 7. Run OpenVoice Server

```sh
uvicorn openvoice_server:app --host 0.0.0.0 --port 8080
```

## Usage

Once the server is running, you can access the OpenVoice API at `http://localhost:8080` or `http://your-server-ip:8080` if deployed on a remote machine.

## License

Refer to the original repository for licensing details.

## Troubleshooting

If you encounter any issues, ensure all dependencies are installed correctly and that you are using the correct Python environment (`openvoice`).

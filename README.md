# SimpleTranscriberWebApp

A simple web application to transcribe audio files to text using OpenAI's Whisper model.

## Motivation

Good audio-to-text converters are expensive. Open AI released [Whisper AI](https://github.com/openai/whisper) which is a state-of-the-art audio-to-text model. However, using Whisper requires some implementation. This repository aims to provide a coding-free state-of-the-art transcription tool free of charge.

<img src="static/UI-1.png" alt="UI-1" height="300"/> <img src="static/UI-2.png" alt="UI-2" height="300"/>

## Features

- Optimize for speed or precision by choosing the model size (`tiny`, `base`, `small`, `medium`, `large`)
- Support for multiple audio or video formats (`flac`, `m4a`, `mp3`, `mp4`, `mpeg`, `mpga`, `oga`, `ogg`, `wav`, `webm`)
- Option to download transcribed text in various formats: (`.txt`, `.docx`, `.pdf`, `.html`, `.json`)
- Automatic language detection for transcription. Other Languages can be prespecified for faster transcription
- Built-in translation. Just select your target language and the tool will translate the audio as well

### Installation

Clone the repository and install the requirements:

```bash
git clone https://github.com/henningheyen/SimpleTranscriberWebApp.git
cd SimpleTranscriberWebApp
pip install -r requirements.txt
```

## Getting Started

Once you have all require packages installed the app can be lauched with

```bash
python app.py
```

Then vist `http://127.0.0.1:5000` in your Browser.

Make sure your audio files are placed in the `uploads` folder. Your transcripted files will be located in the `transcripts` folder or can be downloaded from the WebApp directly. You can find some example audio files and its transcripts in this repository. 

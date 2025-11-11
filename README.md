# 🖐️ Sign Language Translator

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![VoiceRSS](https://img.shields.io/badge/TTS-VoiceRSS-lightblue.svg)](https://www.voicerss.org/)

> Real-time sign language to text translator with **camera-based gesture recognition** and **voice output** — powered by **MediaPipe**, **TensorFlow**, and **VoiceRSS TTS**.

---

## 🌍 Overview

This application translates **sign language gestures** into **text and speech** in real time.  
It uses a trained deep learning model to recognize ASL (American Sign Language) alphabets from webcam input, then converts the detected letters into text — and can **speak the text aloud** using online voices from the **VoiceRSS API**.

Built for accessibility, education, and fun exploration of AI-based computer vision.

---

## 🚀 Features

✅ Real-time **gesture recognition** using webcam  
✅ **Neural network classifier** (TensorFlow) for ASL alphabets  
✅ **Text-to-Speech** via [VoiceRSS](https://www.voicerss.org/)  
✅ **Voice selection** (male/female, multiple accents)  
✅ **Modern dark UI** built with `CustomTkinter`  
✅ **Alphabet guide window** with all sign images  
✅ Compatible with **Windows**, **Linux**, and **macOS**

---

## 📂 Project Structure

```
asl_translator/
│
├── src/
│   ├── app_view.py          # Main GUI
│   ├── app_controller.py    # Links the view and model
│   ├── sign_model.py        # Sign detection + VoiceRSS integration
│   ├── observer.py          # Observer base class
│   ├── subject.py           # Observable base class
│   ├── test_main.py         # App entry point
│   ├── images/              # Hand sign alphabet reference images
│   └── ffmpeg/              # (optional) Local FFmpeg binaries
│
├── nn_model/
│   ├── asl_nn_model.h5      # Pre-trained TensorFlow model
│   └── label_encoder.pkl    # Label encoder
│
├── .env                     # API key storage
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Ayyoub-Boulahri/asl_translator.git
cd asl_translator/src
```

### 2️⃣ Create and Activate a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # on Windows
# or
source venv/bin/activate   # on Linux / macOS
```

### 3️⃣ Install Dependencies
```bash
pip install -r ../requirements.txt
```

> If you don’t have `requirements.txt`, install manually:
> ```bash
> pip install tensorflow mediapipe customtkinter pillow opencv-python joblib requests playsound python-dotenv
> ```

---

## 🧠 Model Setup

Place your pre-trained model files inside the `nn_model/` folder:
```
asl_nn_model.h5
label_encoder.pkl
```

The model predicts ASL letters from MediaPipe’s hand landmark coordinates.

---

## 🔑 Setup VoiceRSS API

### Step 1 — Get Your API Key
- Go to [https://www.voicerss.org/](https://www.voicerss.org/)
- Create a free account and copy your **API key**

### Step 2 — Create a `.env` file in the project root
```
VOICERSS_API_KEY=your_api_key_here
```

Your key will be loaded automatically using `python-dotenv`.

---

## 🎙️ Optional: FFmpeg Setup

If you don’t have FFmpeg installed globally:

1. Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract the contents into:
   ```
   src/ffmpeg/bin/ffmpeg.exe
   src/ffmpeg/bin/ffprobe.exe
   ```

---

## 🖥️ How to Run

```bash
python test_main.py
```

---

## 🧭 Interface Overview

| Button | Description |
|---------|--------------|
| 🎥 **Start Camera** | Starts webcam and begins gesture recognition |
| ⏹ **Stop Camera** | Stops the video stream |
| 🧹 **Clear Text** | Clears translation output |
| 🔊 **Speak Text** | Speaks translated text using selected voice |
| ⚙️ **Alphabet Guide** | Opens a window showing all hand sign images |

---

## 🖼️ Alphabet Guide

When you click the ⚙️ button, a new window opens showing all the **sign language alphabet images** from the `/images/` directory — each labeled with its corresponding letter.

Example layout:

```
[ A 🖐️ ] [ B ✋ ] [ C 🤙 ] ...
```

---

## 💡 Notes

- Ensure your **camera is active** and has good lighting.  
- Hand gestures must be **clearly visible** to the webcam.  
- “space” and “del” gestures let you form words and correct text.  
- All speech playback uses **VoiceRSS**, requiring an internet connection.

---

## 🧱 Troubleshooting

| Issue | Cause | Solution |
|--------|--------|-----------|
| `WinError 2` | FFmpeg not found | Add FFmpeg to `src/ffmpeg/bin/` |
| No voice playback | Invalid or missing API key | Check `.env` |
| Black camera feed | Webcam in use elsewhere | Close Zoom/Discord/etc. |
| Wrong gesture prediction | Poor lighting or fast movement | Improve lighting and slow gestures |

---

## 🧩 Example TTS Usage

You can use VoiceRSS TTS directly in your own scripts:

```python
from utils import speak_voicerss

speak_voicerss("Hello World!", lang="en-us", voice="John")
```

---

## 🧠 Technologies Used

- 🧩 **TensorFlow** — neural network for gesture recognition  
- ✋ **MediaPipe** — hand tracking  
- 🪟 **CustomTkinter** — modern Python UI  
- 🗣️ **VoiceRSS API** — online text-to-speech  
- 🎥 **OpenCV** — real-time camera processing  
- 🧮 **Joblib** — label encoding  
- 🔐 **Dotenv** — API key management  

---

## 🪄 Future Improvements

- 🌐 Add **multi-language translation** (EN ↔ FR)  
- 🗣️ Enable **offline TTS** fallback  
- 🧠 Add **model training GUI**  
- 🧏 Expand to **full word recognition**

---

## 👤 Author

**Ayyoub Boulahri**  
🔗 [GitHub: Ayyoub-Boulahri](https://github.com/Ayyoub-Boulahri)

---

## 🪪 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 💬 Acknowledgments

Special thanks to:
- [MediaPipe](https://developers.google.com/mediapipe) for real-time hand tracking  
- [VoiceRSS](https://www.voicerss.org/) for high-quality TTS  
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the beautiful UI framework  

---

> 🧩 *“Bridging communication barriers through intelligent computer vision.”*

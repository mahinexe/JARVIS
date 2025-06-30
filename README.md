# 🤖 J.A.R.V.I.S - Python Voice Assistant

**J.A.R.V.I.S** (Just A Rather Very Intelligent System) is a desktop-based AI assistant built with **Python**. It interacts with users via voice or text, responds smartly using web data, opens websites, answers general questions, and provides a visually appealing GUI interface.

---

## 🎯 Features

✅ **Voice & Text Input**  
Ask questions by speaking or typing — Jarvis understands both.

✅ **Text-to-Speech (TTS)**  
All answers are spoken aloud using a natural voice.

✅ **DuckDuckGo API Integration**  
Pulls smart answers from the web using DuckDuckGo's Instant Answer API.

✅ **Dynamic Website Opener**  
Say “open facebook” or “open github” — Jarvis will launch `https://facebook.com`, etc.

✅ **Custom Responses**  
Try:  
- “Who made you?”  
- “Hey Jarvis who created you?”  
→ Jarvis will tell you proudly who its creator is.

✅ **Stop Speaking Button**  
Stops Jarvis from continuing to speak the current response.

✅ **Fullscreen GUI**  
Modern dark theme, large readable fonts, and scrollable log area.

✅ **Keyboard Shortcuts**  
- Press `Enter` to submit text  
- Press `Esc` to exit

---

## 🛠️ Technologies Used

- Python 3.x  
- `tkinter` – GUI  
- `speech_recognition` – Voice input  
- `pyttsx3` – Text-to-speech  
- `requests` – API integration  
- `threading` – Async responses  
- `webbrowser` – Opens websites  
- `DuckDuckGo Instant Answer API`

---

## 🚀 How to Run

1. **Install Required Packages:**
   ```bash
   pip install pyttsx3 SpeechRecognition requests
   pip install pipwin
   pipwin install pyaudio

   


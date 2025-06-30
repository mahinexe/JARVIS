import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import winsound
import datetime
import requests
import threading
import queue
import webbrowser

engine = pyttsx3.init()
speech_queue = queue.Queue()
speak_lock = threading.Lock()
def tts_worker():
    while True:
        text = speech_queue.get()
        if text is None:
            break
        with speak_lock:
            engine.say(text)
            engine.runAndWait()
        speech_queue.task_done()

tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()

def speak(text):
    append_text(f"Jarvis: {text}", color="lime")
    speech_queue.put(text)

def stop_speaking():
    with speak_lock:
        engine.stop()
    append_text("Jarvis: Speech stopped.", color="orange")

def append_text(text, color="white"):
    log_area.config(state=tk.NORMAL)
    log_area.insert(tk.END, text + "\n", color)
    log_area.see(tk.END)
    log_area.config(state=tk.DISABLED)

def update_live_transcription(text):
    transcription_var.set(f"You: {text}")

def play_listening_sound():
    winsound.Beep(1000, 300)

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        play_listening_sound()
        speak("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        update_live_transcription(command)
        append_text(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        update_live_transcription("Unrecognized speech")
        return "unrecognized"
    except sr.RequestError:
        update_live_transcription("Network error")
        return "error"

def answer_from_duckduckgo(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1"
        res = requests.get(url)
        data = res.json()
        if data.get("AbstractText"):
            return data["AbstractText"]
        elif data.get("Answer"):
            return data["Answer"]
        else:
            return "Sorry, I couldn't find an answer."
    except Exception as e:
        return f"Error: {str(e)}"

def is_creator_question(text):
    triggers = [
        "who made you", "who created you", "who developed you", "who is your creator",
        "who is your maker", "who built you", "who designed you", "who invented you",
        "who made jarvis", "who made you jarvis", "hey jarvis who made you", "who created", "create",
    ]
    return any(trigger in text for trigger in triggers)


def open_website(site_name):
    site = site_name.strip().replace(" ", "")
    url = f"https://{site}.com"
    webbrowser.open(url)
    speak(f"{site.capitalize()} has been opened.")


def handle_command(command):
    if is_creator_question(command):
        response = ("Mohammodullah Al Mahin made me. "
                    "He is currently pursuing Bachelor of Science in Computer Science and Engineering from Southeast University, "
                    "which means I have a good creator!")
        speak(response)
        append_text(f"Answer: {response}", color="lime")
    elif "open" in command:
        parts = command.split("open", 1)
        if len(parts) > 1:
            open_website(parts[1])
        else:
            speak("Sorry, I couldn't recognize the website name.")
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Current time is {now}.")
    elif command in ["unrecognized", "error"]:
        speak("Sorry, I didn't catch that.")
    else:
        response = answer_from_duckduckgo(command)
        speak(response)
        append_text(f"Answer: {response}", color="lime")

def on_speak_button():
    def task():
        command = listen_command()
        handle_command(command)
    threading.Thread(target=task).start()

def on_text_submit(event=None):
    command = text_entry.get().strip()
    if command:
        update_live_transcription(command)
        append_text(f"You said: {command}")
        text_entry.delete(0, tk.END)
        threading.Thread(target=lambda: handle_command(command)).start()

root = tk.Tk()
root.title("J.A.R.V.I.S Voice Assistant")
root.configure(bg="#121212")
root.attributes("-fullscreen", True)

FONT_TITLE = ("Segoe UI", 42, "bold")
FONT_TRANSCRIPTION = ("Segoe UI", 24)
FONT_LOG = ("Consolas", 18)
FONT_BUTTON = ("Segoe UI", 16, "bold")
FONT_ENTRY = ("Segoe UI", 16)
COLOR_BG = "#121212"
COLOR_TEXT = "#E0E0E0"
COLOR_HIGHLIGHT = "#00FFAA"
COLOR_BUTTON_BG = "#00b894"
COLOR_BUTTON_HOVER = "#019875"
COLOR_STOP_BUTTON_BG = "#d63031"
COLOR_STOP_BUTTON_HOVER = "#b71c1c"
COLOR_LOG_BG = "#1e1e1e"
COLOR_EXIT_BUTTON_BG = "#555555"
COLOR_EXIT_BUTTON_HOVER = "#777777"

title = tk.Label(root, text="J.A.R.V.I.S", font=FONT_TITLE, fg=COLOR_HIGHLIGHT, bg=COLOR_BG)
title.pack(pady=(25, 10))

transcription_var = tk.StringVar()
transcription_label = tk.Label(root, textvariable=transcription_var, font=FONT_TRANSCRIPTION, fg=COLOR_TEXT, bg=COLOR_BG)
transcription_label.pack(pady=(0, 15))

log_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=FONT_LOG, bg=COLOR_LOG_BG, fg=COLOR_TEXT, insertbackground=COLOR_TEXT)
log_area.tag_config("lime", foreground=COLOR_HIGHLIGHT)
log_area.tag_config("white", foreground=COLOR_TEXT)
log_area.tag_config("orange", foreground="#FFA500")
log_area.pack(padx=20, pady=(0,10), fill=tk.BOTH, expand=True)
log_area.config(state=tk.DISABLED)

bottom_frame = tk.Frame(root, bg=COLOR_BG, height=100)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
bottom_frame.pack_propagate(False)

btn_frame = tk.Frame(bottom_frame, bg=COLOR_BG)
btn_frame.pack(side=tk.LEFT, padx=30)

def on_enter(widget, color): widget['bg'] = color
def on_leave(widget, color): widget['bg'] = color

speak_btn = tk.Button(btn_frame, text="🎤 Speak", font=FONT_BUTTON, bg=COLOR_BUTTON_BG, fg="white",
                      activebackground=COLOR_BUTTON_HOVER, activeforeground="white", padx=25, pady=12,
                      command=on_speak_button, borderwidth=0, relief=tk.FLAT, cursor="hand2")
speak_btn.pack(side=tk.LEFT, padx=15)
speak_btn.bind("<Enter>", lambda e: on_enter(speak_btn, COLOR_BUTTON_HOVER))
speak_btn.bind("<Leave>", lambda e: on_leave(speak_btn, COLOR_BUTTON_BG))

text_entry = tk.Entry(btn_frame, font=FONT_ENTRY, width=40, bg="#222", fg=COLOR_TEXT, insertbackground=COLOR_TEXT, relief=tk.FLAT)
text_entry.pack(side=tk.LEFT, padx=15)
text_entry.bind("<Return>", on_text_submit)

submit_btn = tk.Button(btn_frame, text="📨 Submit", font=FONT_BUTTON, bg=COLOR_BUTTON_BG, fg="white",
                       activebackground=COLOR_BUTTON_HOVER, activeforeground="white", padx=20, pady=12,
                       command=on_text_submit, borderwidth=0, relief=tk.FLAT, cursor="hand2")
submit_btn.pack(side=tk.LEFT, padx=15)
submit_btn.bind("<Enter>", lambda e: on_enter(submit_btn, COLOR_BUTTON_HOVER))
submit_btn.bind("<Leave>", lambda e: on_leave(submit_btn, COLOR_BUTTON_BG))

stop_btn = tk.Button(btn_frame, text="🛑 Stop Speaking", font=FONT_BUTTON, bg=COLOR_STOP_BUTTON_BG, fg="white",
                     activebackground=COLOR_STOP_BUTTON_HOVER, activeforeground="white", padx=25, pady=12,
                     command=stop_speaking, borderwidth=0, relief=tk.FLAT, cursor="hand2")
stop_btn.pack(side=tk.LEFT, padx=15)
stop_btn.bind("<Enter>", lambda e: on_enter(stop_btn, COLOR_STOP_BUTTON_HOVER))
stop_btn.bind("<Leave>", lambda e: on_leave(stop_btn, COLOR_STOP_BUTTON_BG))

def on_exit_button():
    speech_queue.put(None)  # stops tts thread
    root.destroy()

exit_btn = tk.Button(btn_frame, text="⏻ Exit Jarvis", font=FONT_BUTTON, bg=COLOR_EXIT_BUTTON_BG, fg="white",
                     activebackground=COLOR_EXIT_BUTTON_HOVER, activeforeground="white", padx=20, pady=12,
                     command=on_exit_button, borderwidth=0, relief=tk.FLAT, cursor="hand2")
exit_btn.pack(side=tk.LEFT, padx=15)
exit_btn.bind("<Enter>", lambda e: on_enter(exit_btn, COLOR_EXIT_BUTTON_HOVER))
exit_btn.bind("<Leave>", lambda e: on_leave(exit_btn, COLOR_EXIT_BUTTON_BG))

watermark = tk.Label(
    bottom_frame,
    text="<Developed by Mohammodullah Al Mahin/>",
    font=("Fira Code", 14, "bold italic"),
    fg="#66FF66",
    bg=COLOR_BG
)
watermark.pack(side=tk.RIGHT, padx=30, pady=15)

def close(event):
    speech_queue.put(None)
    root.destroy()
root.bind("<Escape>", close)

def welcome_message():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        greeting = "Good morning Mahin, How can I help you sir?"
    elif 12 <= hour < 18:
        greeting = "Good afternoon Mahin, How can I help you sir?"
    else:
        greeting = "Good evening Mahin, How can I help you sir?"
    speak(greeting)

threading.Thread(target=welcome_message).start()

root.mainloop()

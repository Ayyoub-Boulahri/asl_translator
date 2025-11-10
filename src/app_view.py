import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
from observer import Observer
import requests
import tempfile
import os
import threading
from playsound import playsound
from voices import voices
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("VOICERSS_API_KEY")

# --- VoiceRSS function ---
def speak_voicerss(text, lang="en-us", voice="John"):
    """Fetch and play speech from VoiceRSS."""
    if not text.strip():
        return

    url = "https://api.voicerss.org/"
    params = {
        "key": api_key,
        "hl": lang,
        "src": text,
        "v": voice,                  
        "r": "0",
        "c": "MP3",
        "f": "44khz_16bit_stereo"
    }

    try:
        print(f"Requesting TTS from VoiceRSS ({voice})...")
        response = requests.get(url, params=params)

        if response.status_code != 200 or response.content.startswith(b'ERROR'):
            print("VoiceRSS error:", response.text)
            return

        # Save temporarily and play
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name

        playsound(tmp_path)
        os.remove(tmp_path)

    except Exception as e:
        print("TTS error:", e)


# --- GUI ---
class AppView(Observer):
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        root.title("Sign Language Translator")
        root.geometry("1200x700")

        # --- Top Bar ---
        top_bar = ctk.CTkFrame(root, height=70, fg_color="#1a1a1a", corner_radius=0)
        top_bar.pack(fill="x")

        ctk.CTkLabel(
            top_bar,
            text="🖐️  Sign Language Translator",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(side="left", padx=30, pady=15)

        ctk.CTkLabel(
            top_bar,
            text="Real-time sign language to text conversion",
            text_color="#999"
        ).pack(side="left", padx=10, pady=20)

        ctk.CTkButton(
            top_bar, text="⚙️", width=40, height=40,
            corner_radius=8, fg_color="#333333", hover_color="#444",
            command=self.show_alphabet_window
        ).pack(side="right", padx=30, pady=15)

        # --- Main Frame ---
        main_frame = ctk.CTkFrame(root, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Left (Camera)
        left_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="#1e1e1e")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)

        # Right (Controls + Output)
        right_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="#1e1e1e")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=10)

        # --- Camera Container ---
        camera_container = ctk.CTkFrame(left_frame, fg_color="#2b2b2b", corner_radius=15)
        camera_container.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        self.camera_label = ctk.CTkLabel(
            camera_container,
            text="📷 Camera is off",
            height=420, width=580,
            fg_color="#333333", corner_radius=12,
            text_color="#ccc", font=ctk.CTkFont(size=16)
        )
        self.camera_label.pack(expand=True, pady=10)

        # --- Camera Buttons ---
        btn_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        btn_frame.pack(pady=(10, 20))

        ctk.CTkButton(
            btn_frame, text="🎥 Start Camera", width=160, height=45,
            corner_radius=10, font=ctk.CTkFont(size=16, weight="bold"),
            command=self.controller.start_camera
        ).grid(row=0, column=0, padx=12)

        ctk.CTkButton(
            btn_frame, text="⏹ Stop Camera", width=160, height=45,
            corner_radius=10, fg_color="#a83232", hover_color="#d93c3c",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.controller.stop_camera
        ).grid(row=0, column=1, padx=12)

        # --- Translation Output ---
        ctk.CTkLabel(
            right_frame,
            text="Translation",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(25, 10))

        self.output_box = ctk.CTkTextbox(
            right_frame, width=450, height=350,
            corner_radius=12, font=ctk.CTkFont(size=16)
        )
        self.output_box.insert("1.0", "Translated text will appear here...")
        self.output_box.pack(pady=20, padx=20)

        # --- Voice + Buttons ---
        action_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        action_frame.pack(pady=(10, 10))

        ctk.CTkLabel(
            action_frame,
            text="Voice Selection",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 8))

        self.voice_dropdown = ctk.CTkOptionMenu(
            action_frame,
            values=list(voices.keys()),
            width=280,
            corner_radius=8
        )
        self.voice_dropdown.set("French - Canada (Louis)")
        self.voice_dropdown.grid(row=1, column=0, columnspan=2, pady=(0, 15))


        # --- Control Buttons (side by side) ---
        ctk.CTkButton(
            action_frame, text="🧹 Clear Text",
            width=150, height=40, corner_radius=10,
            fg_color="#444", hover_color="#666",
            command=self.controller.clear_text
        ).grid(row=2, column=0, padx=10, pady=5)

        ctk.CTkButton(
            action_frame, text="🔊 Speak Text",
            width=150, height=40, corner_radius=10,
            fg_color="#0066cc", hover_color="#3385ff",
            command=self.on_speak_button
        ).grid(row=2, column=1, padx=10, pady=5)

    # --- Speak Handler ---
    def on_speak_button(self):
        text = self.output_box.get("1.0", "end").strip()
        if not text:
            return

        lang, voice = voices[self.voice_dropdown.get()]
        threading.Thread(
            target=lambda: speak_voicerss(text, lang=lang, voice=voice),
            daemon=True
        ).start()

    def show_alphabet_window(self):
        """Open a window showing all sign alphabet images with labels."""
        images_dir = "alphabets_signs"

        if not os.path.exists(images_dir):
            print(f"Images folder not found at {images_dir}")
            return

        # --- Create the popup window ---
        win = ctk.CTkToplevel(self.root)
        win.title("ASL Alphabet Reference")
        win.geometry("1000x700")
        win.configure(fg_color="#1a1a1a")

        ctk.CTkLabel(
            win,
            text="🖐️ ASL Alphabet Reference",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(pady=20)

        frame = ctk.CTkScrollableFrame(win, fg_color="#222", corner_radius=15, width=950, height=550)
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        # --- Load all images ---
        image_files = sorted([
            f for f in os.listdir(images_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ])

        if not image_files:
            ctk.CTkLabel(frame, text="No images found.", text_color="#888").pack(pady=20)
            return

        # --- Grid layout for images ---
        max_columns = 5
        row, col = 0, 0
        for filename in image_files:
            letter = os.path.splitext(filename)[0].upper()
            path = os.path.join(images_dir, filename)

            try:
                img = Image.open(path).resize((150, 150))
                photo = ImageTk.PhotoImage(img)

                img_label = ctk.CTkLabel(frame, image=photo, text="")
                img_label.image = photo  # Keep a reference
                img_label.grid(row=row, column=col, padx=15, pady=15)

                ctk.CTkLabel(
                    frame,
                    text=letter,
                    font=ctk.CTkFont(size=18, weight="bold")
                ).grid(row=row + 1, column=col, pady=(0, 15))

                col += 1
                if col >= max_columns:
                    col = 0
                    row += 2  
            except Exception as e:
                print(f"Failed to load {filename}: {e}")

    # --- Observer Update ---
    def update(self, subject):
        frame = subject.frame
        text_output = subject.text_output
        current_prediction = subject.current_prediction

        if frame is not None:
            display = frame.copy()
            cv2.putText(display, f"Sign: {current_prediction}", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            img = Image.fromarray(cv2.cvtColor(display, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.configure(image=imgtk, text="")
            self.camera_label.image = imgtk
        else:
            self.camera_label.configure(text="📷 Camera is off", image="")

        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text_output)

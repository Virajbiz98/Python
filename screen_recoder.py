import pyautogui
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import sounddevice as sd
import wave
import os
import ffmpeg


class ScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder")

        # Variables
        self.recording = False
        self.is_paused = False
        self.output_file = "screen_recording.avi"
        self.audio_file = "audio.wav"
        self.final_output = ""
        self.fps = 20
        self.crf = 23  # Video quality (CRF value)
        self.audio_bitrate = "128k"  # Default audio bitrate
        self.resolution_options = {"Low (480p)": (640, 480), "Medium (720p)": (1280, 720), "High (1080p)": (1920, 1080)}
        self.selected_resolution = (1280, 720)  # Default resolution (720p)

        # GUI Elements
        tk.Label(root, text="Screen Recorder", font=("Arial", 16)).pack(pady=10)

        self.record_button = tk.Button(root, text="Start Recording", command=self.start_recording, bg="green", fg="white", width=20)
        self.record_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, bg="red", fg="white", width=20)
        self.stop_button.pack(pady=5)

        self.pause_button = tk.Button(root, text="Pause Recording", command=self.pause_recording, bg="yellow", fg="black", width=20)
        self.pause_button.pack(pady=5)

        self.resume_button = tk.Button(root, text="Resume Recording", command=self.resume_recording, bg="blue", fg="white", width=20)
        self.resume_button.pack(pady=5)

        # File Save Options
        tk.Button(root, text="Set Output File", command=self.set_output_file, width=20).pack(pady=5)

        # Resolution Options
        tk.Label(root, text="Video Quality (Resolution):", font=("Arial", 12)).pack(pady=5)
        self.resolution_var = tk.StringVar(value="Medium (720p)")
        self.resolution_menu = tk.OptionMenu(root, self.resolution_var, *self.resolution_options.keys())
        self.resolution_menu.pack(pady=5)

        # Audio Quality Options
        tk.Label(root, text="Audio Quality (Bitrate):", font=("Arial", 12)).pack(pady=5)
        self.audio_quality_var = tk.StringVar(value="128 kbps")  # Default audio quality
        self.audio_quality_menu = tk.OptionMenu(root, self.audio_quality_var, "64 kbps", "128 kbps", "192 kbps", "320 kbps")
        self.audio_quality_menu.pack(pady=5)

        tk.Button(root, text="Exit", command=root.quit, bg="gray", fg="white", width=20).pack(pady=5)

        self.recording_label = tk.Label(root, text="", font=("Arial", 12), fg="red")
        self.recording_label.pack(pady=10)

    def set_output_file(self):
        self.final_output = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        if self.final_output:
            messagebox.showinfo("File Saved", f"Output file set to: {self.final_output}")

    def start_recording(self):
        if self.recording:
            messagebox.showwarning("Warning", "Recording is already in progress!")
            return

        if not self.final_output:
            messagebox.showwarning("Warning", "Please set the output file first!")
            return

        # Set resolution and audio bitrate
        self.selected_resolution = self.resolution_options[self.resolution_var.get()]
        self.audio_bitrate = self.audio_quality_var.get().replace(" kbps", "k")  # Convert to FFmpeg format (e.g., "128k")

        self.recording = True
        self.is_paused = False
        self.recording_label.config(text="Recording...")

        # Start threads for screen and audio recording
        threading.Thread(target=self.record_screen).start()
        threading.Thread(target=self.record_audio).start()
        messagebox.showinfo("Recording", "Recording started. Click 'Stop Recording' to finish.")

    def stop_recording(self):
        if not self.recording:
            messagebox.showwarning("Warning", "No recording in progress!")
            return

        self.recording = False
        self.recording_label.config(text="")

        # Combine video and audio
        self.combine_audio_video()

    def pause_recording(self):
        if not self.recording or self.is_paused:
            messagebox.showwarning("Warning", "Cannot pause recording!")
            return

        self.is_paused = True
        self.recording_label.config(text="Recording Paused")

    def resume_recording(self):
        if not self.recording or not self.is_paused:
            messagebox.showwarning("Warning", "Cannot resume recording!")
            return

        self.is_paused = False
        self.recording_label.config(text="Recording...")

    def record_screen(self):
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(self.output_file, fourcc, self.fps, self.selected_resolution)

        while self.recording:
            if not self.is_paused:
                img = pyautogui.screenshot()
                img = img.resize(self.selected_resolution)  # Resize to selected resolution
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frame)
            time.sleep(1 / self.fps)

        out.release()

    def record_audio(self):
        fs = 44100  # Sample rate
        seconds = 1  # Record in chunks of 1 second
        channels = 2

        with wave.open(self.audio_file, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # Bytes per sample (16-bit audio)
            wf.setframerate(fs)

            while self.recording:
                if not self.is_paused:
                    audio_data = sd.rec(int(fs * seconds), samplerate=fs, channels=channels, dtype='int16')
                    sd.wait()
                    wf.writeframes(audio_data.tobytes())

    def combine_audio_video(self):
        if not os.path.exists(self.output_file):
            messagebox.showerror("Error", f"Video file not found: {self.output_file}")
            return
        if not os.path.exists(self.audio_file):
            messagebox.showerror("Error", f"Audio file not found: {self.audio_file}")
            return

        try:
            # Combine audio and video using FFmpeg with selected bitrate
            video_input = ffmpeg.input(self.output_file)
            audio_input = ffmpeg.input(self.audio_file)
            ffmpeg.output(
                video_input, audio_input, self.final_output,
                vcodec="libx264", acodec="aac", audio_bitrate=self.audio_bitrate, crf=self.crf
            ).run(overwrite_output=True)
            messagebox.showinfo("Success", f"Final video saved as: {self.final_output}")
        except ffmpeg.Error as e:
            messagebox.showerror("Error", f"FFmpeg failed: {e.stderr.decode('utf-8')}")


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorderApp(root)
    root.mainloop()

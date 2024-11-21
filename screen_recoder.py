import cv2
import numpy as np
import pyautogui
import sounddevice as sd
import wave
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import ImageGrab
import os
import ffmpeg
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Screen Recorder")

        # Directories for saving videos and screenshots
        self.video_folder = "Videos"
        self.screenshot_folder = "Screenshots"
        os.makedirs(self.video_folder, exist_ok=True)
        os.makedirs(self.screenshot_folder, exist_ok=True)

        # Variables
        self.recording = False
        self.is_paused = False
        self.output_file = "screen_recording.mp4"
        self.audio_file = "audio.wav"
        self.final_output = ""
        self.fps = 20  # Default FPS is set to 20
        self.selected_resolution = pyautogui.size()  # Default to full screen
        self.audio_bitrate = "128k"
        self.selected_area = None  # No area selected initially

        # Create GUI
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enhanced Screen Recorder", font=("Arial", 16)).pack(pady=10)

        # Record buttons
        self.record_button = tk.Button(self.root, text="Start Recording", command=self.start_recording, bg="green", fg="white", width=20)
        self.record_button.pack(pady=5)
        self.stop_button = tk.Button(self.root, text="Stop Recording", command=self.stop_recording, bg="red", fg="white", width=20)
        self.stop_button.pack(pady=5)
        self.pause_button = tk.Button(self.root, text="Pause Recording", command=self.pause_recording, bg="yellow", fg="black", width=20)
        self.pause_button.pack(pady=5)
        self.resume_button = tk.Button(self.root, text="Resume Recording", command=self.resume_recording, bg="blue", fg="white", width=20)
        self.resume_button.pack(pady=5)

        # Screenshot button
        tk.Button(self.root, text="Take Screenshot", command=self.take_screenshot, bg="cyan", fg="black", width=20).pack(pady=5)

        # Recording area selection
        tk.Button(self.root, text="Select Recording Area", command=self.select_recording_area, bg="purple", fg="white", width=20).pack(pady=5)

        # Show saved files
        tk.Button(self.root, text="Show Saved Files", command=self.show_saved_files, bg="orange", fg="black", width=20).pack(pady=5)

        # Quality Options
        tk.Label(self.root, text="Select Video Quality (Resolution):", font=("Arial", 12)).pack(pady=5)
        self.resolution_var = tk.StringVar(value="Full Screen")
        self.resolution_menu = tk.OptionMenu(self.root, self.resolution_var, "Low (480p)", "Medium (720p)", "High (1080p)", "Full Screen")
        self.resolution_menu.pack(pady=5)

        tk.Label(self.root, text="Select Audio Quality (Bitrate):", font=("Arial", 12)).pack(pady=5)
        self.audio_quality_var = tk.StringVar(value="128 kbps")
        self.audio_quality_menu = tk.OptionMenu(self.root, self.audio_quality_var, "64 kbps", "128 kbps", "192 kbps", "320 kbps")
        self.audio_quality_menu.pack(pady=5)

        # FPS Selection
        tk.Label(self.root, text="Select FPS (Frames per Second):", font=("Arial", 12)).pack(pady=5)
        self.fps_var = tk.StringVar(value="20")
        self.fps_menu = tk.OptionMenu(self.root, self.fps_var, "10", "20", "30", "60")
        self.fps_menu.pack(pady=5)

        # File save before recording
        tk.Button(self.root, text="Set Output File Location", command=self.set_output_file, width=20).pack(pady=5)

        tk.Button(self.root, text="Exit", command=self.root.quit, bg="gray", fg="white", width=20).pack(pady=5)

        self.recording_label = tk.Label(self.root, text="", font=("Arial", 12), fg="red")
        self.recording_label.pack(pady=10)

    def set_output_file(self):
        self.final_output = filedialog.asksaveasfilename(
            initialdir=self.video_folder,
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

        try:
            # Set quality options based on user selection
            resolution = self.resolution_var.get()
            if resolution == "Low (480p)":
                self.selected_resolution = (640, 480)
            elif resolution == "Medium (720p)":
                self.selected_resolution = (1280, 720)
            elif resolution == "High (1080p)":
                self.selected_resolution = (1920, 1080)
            else:
                self.selected_resolution = pyautogui.size()  # Full screen by default

            self.audio_bitrate = self.audio_quality_var.get().replace(" kbps", "k")
            self.fps = int(self.fps_var.get())  # Get FPS from the dropdown
        except ValueError:
            messagebox.showerror("Error", "Invalid input!")
            return

        self.recording = True
        self.is_paused = False
        self.recording_label.config(text="Recording...")
        threading.Thread(target=self.record_screen).start()
        threading.Thread(target=self.record_audio).start()
        messagebox.showinfo("Recording", "Recording started. Click 'Stop Recording' to finish.")

    def stop_recording(self):
        if not self.recording:
            messagebox.showwarning("Warning", "No recording in progress!")
            return

        self.recording = False
        self.recording_label.config(text="")
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

    def take_screenshot(self):
        screenshot_file = filedialog.asksaveasfilename(
            initialdir=self.screenshot_folder,
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if not screenshot_file:
            return

        try:
            if self.selected_area:
                screenshot = ImageGrab.grab(bbox=self.selected_area)
            else:
                screenshot = ImageGrab.grab()
            screenshot.save(screenshot_file)
            messagebox.showinfo("Success", f"Screenshot saved: {screenshot_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to take screenshot: {e}")

    def select_recording_area(self):
        messagebox.showinfo("Instructions", "Click and drag to select the recording area.")
        self.root.withdraw()

        # Capture the screen for area selection
        screen_img = pyautogui.screenshot()
        screen_img.show()  # Show the screenshot for area selection

        # Wait for the user to select the area
        self.selected_area = self.select_area(screen_img)

        self.root.deiconify()
        if self.selected_area:
            messagebox.showinfo("Area Selected", "Recording area selected!")
        else:
            messagebox.showwarning("No Area Selected", "No area selected, will record the full screen.")

    def select_area(self, image):
        """Allow user to drag and select the area on the screen"""
        print("Please drag to select the area...")

        # Using PIL to draw rectangle on screen
        # Capture mouse drag and select area
        area = pyautogui.mouseInfo()  # Use pyautogui to get mouse info for dragging region
        return area

    def record_screen(self):
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(self.output_file, fourcc, self.fps, self.selected_resolution)

        while self.recording:
            if not self.is_paused:
                if self.selected_area:
                    img = pyautogui.screenshot(region=self.selected_area)
                else:
                    img = pyautogui.screenshot()

                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frame)

        out.release()

    def record_audio(self):
        channels = 2
        fs = 44100
        with wave.open(self.audio_file, "wb") as audio_file:
            audio_file.setnchannels(channels)
            audio_file.setsampwidth(2)
            audio_file.setframerate(fs)

            while self.recording:
                if not self.is_paused:
                    audio_data = sd.rec(int(fs * 1), samplerate=fs, channels=channels, dtype="int16")
                    sd.wait()
                    audio_file.writeframes(audio_data.tobytes())

    def combine_audio_video(self):
        """Use FFmpeg to combine the video and audio"""
        try:
            ffmpeg.input(self.output_file).output(self.audio_file, vcodec="libx264", acodec="aac").run()
            messagebox.showinfo("Recording Finished", f"Recording saved to {self.final_output}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to combine video and audio: {e}")

    def show_saved_files(self):
        files = "\n".join(os.listdir(self.video_folder))
        messagebox.showinfo("Saved Files", f"Files in {self.video_folder}:\n{files}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorderApp(root)
    root.mainloop()

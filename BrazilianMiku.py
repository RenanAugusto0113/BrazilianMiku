'''
    Brazilian Miku is an simple tool designed to be used with OBS Studio to make a character
    (by default, the Brazilian Hatsune Miku represented by an image) say something
    (via audio) after a customizable and invisible timer reaches zero.

    Copyright (C) 2025  Renan Augusto Cristi Avelar

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Author's e-mail: renan.augusto0113@gmail.com
    Brazilian Miku Art by MagDraws

'''

import tkinter as tk
import random
import os
import sys
from PIL import Image, ImageTk
import pygame

# Without this, the program doesn't work after compile it
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Get path of media folder for audio files and the Miku's Image and set background color to magenta
IMAGE_PATH = resource_path(os.path.join("media", "BrazilianMiku.png"))
BACKGROUND_COLOR = "#FF00FF" # It doesn't need necessarily to be magenta, just a color that is not present in your image so it works with the OBS's Chroma Key filter
pygame.mixer.init()

remaining_time = 0

# Check for audio files in "media" folder
def get_random_audio():
    audio_files = []
    media_path = resource_path("media")
    for file in os.listdir(media_path):
        if file.lower().endswith(('.mp3', '.wav', '.ogg')): # Supported audio formats
            audio_files.append(resource_path(os.path.join("media", file)))
    return random.choice(audio_files) if audio_files else None

# Play a randomly selected audio
def play_audio():
    audio_file = get_random_audio()
    if audio_file:
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

def animate_exit():
    current_rely = float(image_label.place_info()['rely'])
    if current_rely < 2.0:
        image_label.place_configure(rely=current_rely + 0.05)
        root.after(10, animate_exit)
    else:
        image_label.destroy()

# Check if audio is playing, if not, animate the image to get away
def check_audio_finished():
    if pygame.mixer.music.get_busy():
        root.after(100, check_audio_finished)
    else:
        animate_exit()

def animate_entrance():
    current_rely = float(image_label.place_info()['rely'])
    if current_rely > 0.5:
        image_label.place_configure(rely=current_rely - 0.05)
        root.after(10, animate_entrance)

def show_image():
    try:
        image = Image.open(IMAGE_PATH).convert("RGBA") # It HAS to be RGBA, or the image won't have transparency
        photo = ImageTk.PhotoImage(image)
        global image_label
        image_label = tk.Label(root, image=photo, bg=BACKGROUND_COLOR)
        image_label.image = photo
        image_label.place(relx=0.5, rely=2, anchor="center")
        animate_entrance()
    except Exception as e:
        print(f"Error: Couldn't load image: {str(e)}")

def update_timer():
    global remaining_time
    if remaining_time > 0:
        remaining_time -= 1
        root.title(f"Hatsune Miku Brasileira | Tempo restante: {remaining_time}s")
        root.after(1000, update_timer)
    else:
        root.title("Hatsune Miku Brasileira ALERT!!!")
        show_image()
        play_audio()
        check_audio_finished()

def setup_input_screen():
    root.title("Timer")
    root.configure(bg="#646464")
    root.geometry("300x150")

    input_frame = tk.Frame(root, bg="#646464")
    input_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Label de instrução
    prompt_label = tk.Label(input_frame, text="Timer: (hh:mm:ss):", bg="#646464", font=("Arial", 12))
    prompt_label.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

    # Entradas para horas, minutos e segundos com labels ":" entre elas
    entry_hours = tk.Entry(input_frame, width=3, font=("Arial", 12))
    entry_hours.grid(row=1, column=0, padx=5)
    colon_label1 = tk.Label(input_frame, text=":", bg="#646464", font=("Arial", 12))
    colon_label1.grid(row=1, column=1)
    entry_minutes = tk.Entry(input_frame, width=3, font=("Arial", 12))
    entry_minutes.grid(row=1, column=2, padx=5)
    colon_label2 = tk.Label(input_frame, text=":", bg="#646464", font=("Arial", 12))
    colon_label2.grid(row=1, column=3)
    entry_seconds = tk.Entry(input_frame, width=3, font=("Arial", 12))
    entry_seconds.grid(row=1, column=4, padx=5)

    def validate_input():
        try:
            # Check if the input is valid and interpret blank input as "0"
            h = int(entry_hours.get().strip() or "0")
            m = int(entry_minutes.get().strip() or "0")
            s = int(entry_seconds.get().strip() or "0")
            if m < 0 or m > 59 or s < 0 or s > 59 or h < 0:
                raise ValueError
            total_seconds = h * 3600 + m * 60 + s
            if total_seconds <= 0:
                raise ValueError
            global remaining_time
            remaining_time = total_seconds
            input_frame.destroy()
            root.configure(bg=BACKGROUND_COLOR)
            root.geometry("512x512")
            update_timer()
        except ValueError:
            error_label.config(text="Valores inválidos!")

    start_button = tk.Button(input_frame, text="Iniciar", command=validate_input, font=("Arial", 12))
    start_button.grid(row=2, column=0, columnspan=5, pady=10)

    error_label = tk.Label(input_frame, text="", fg="red", bg="#646464", font=("Arial", 10))
    error_label.grid(row=3, column=0, columnspan=5)

root = tk.Tk()
setup_input_screen()
root.mainloop()
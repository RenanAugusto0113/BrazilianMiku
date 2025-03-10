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

'''

import tkinter as tk
import random
import os
import sys
from PIL import Image, ImageTk
import PIL._tkinter_finder
import pygame

# Things to make images and audios not break after compile
def resource_path(relative_path):
    """ Retorna o caminho absoluto para recursos, funcionando para desenvolvimento e para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

IMAGE_PATH = resource_path(os.path.join("media", "BrazilianMiku.png"))
BACKGROUND_COLOR = "#FF00FF"
TIMER_DURATION = 24 * 60  # Timer duration in seconds, add "* 60" to convert to minutes

pygame.mixer.init()

def get_random_audio():
    audio_extensions = ['.mp3', '.wav', '.ogg']  # Supported audio files
    audio_files = []
    
    try:
        media_path = resource_path("media")
        for file in os.listdir(media_path):
            if any(file.lower().endswith(ext) for ext in audio_extensions):
                audio_files.append(resource_path(os.path.join("media", file)))
                
        if not audio_files:
            raise FileNotFoundError("No audio file (.mp3, .wav, .ogg) found on media folder")
            
        return random.choice(audio_files)
        
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        return None

def play_audio():
    audio_file = get_random_audio()
    if audio_file:
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

def animate_exit():
    current_rely = float(image_label.place_info()['rely'])
    new_rely = current_rely + 0.05
    
    if new_rely < 2.0:
        image_label.place_configure(rely=new_rely)
        root.after(10, animate_exit)
    else:
        image_label.place_configure(rely=2.0)
        image_label.destroy()

def check_audio_finished():
    if pygame.mixer.music.get_busy():
        root.after(100, check_audio_finished)
    else:
        animate_exit()

def animate_entrance():
    current_rely = float(image_label.place_info()['rely'])
    new_rely = current_rely - 0.05
    
    if new_rely > 0.5:
        image_label.place_configure(rely=new_rely)
        root.after(10, animate_entrance)
    else:
        image_label.place_configure(rely=0.5)

def show_image():
    image = Image.open(IMAGE_PATH).convert("RGBA") # It was to be converted to RGBA so image can be transparent
    photo = ImageTk.PhotoImage(image)
    global image_label
    image_label = tk.Label(root, image=photo, bg=BACKGROUND_COLOR)
    image_label.image = photo
    image_label.place(relx=0.5, rely=2, anchor="center")
    animate_entrance()

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

root = tk.Tk()
root.title(f"Hatsune Miku Brasileira | Tempo restante: {TIMER_DURATION}s")
root.configure(bg=BACKGROUND_COLOR)
root.geometry("512x512")

remaining_time = TIMER_DURATION
update_timer()

root.mainloop()

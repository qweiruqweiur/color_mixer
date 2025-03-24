import tkinter as tk
import subprocess
import json
import os
from PIL import Image, ImageTk  # Requires Pillow library

# Image paths
MIXER_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/mixer.jpeg"
PALETTE_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/palette.jpeg"

SETTINGS_FILE = "appearance_settings.json"

# Appearance helpers
def load_appearance():
    default = {"theme": "light", "font_size": "medium", "font_family": "Arial"}
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return default
    return default

def get_font_settings():
    appearance = load_appearance()
    font_sizes = {
        "small": 10, "medium": 12, "large": 14, "extra large": 16
    }
    font_size = font_sizes.get(appearance.get("font_size", "medium"), 12)
    font_family = appearance.get("font_family", "Arial")
    theme = appearance.get("theme", "light")
    return font_family, font_size, theme

# Page Navigation
def open_general_color_mixer(tools_window):
    tools_window.destroy()
    subprocess.Popen(["python", "general_color_mixer.py"])

def open_color_palette_page(tools_window):
    tools_window.destroy()
    subprocess.Popen(["python", "color_palette_page.py"])

def go_back(tools_window):
    tools_window.destroy()
    subprocess.Popen(["python", "home.py"])

# Main Tools Page
def open_tools_page():
    font_family, font_size, theme = get_font_settings()
    font = (font_family, font_size)

    bg_color = "#333" if theme == "dark" else "white"
    fg_color = "white" if theme == "dark" else "black"

    tools_window = tk.Tk()
    tools_window.title("Tools")
    tools_window.configure(bg=bg_color)

    # Title Label
    title_label = tk.Label(
        tools_window, text="Tools", font=("Arial", 22, "bold"),
        fg=fg_color, bg=bg_color
    )
    title_label.pack(anchor="nw", padx=30, pady=20)

    # Main Content Frame
    main_frame = tk.Frame(tools_window, bg=bg_color)
    main_frame.pack(pady=20, padx=50)

    # Load images
    try:
        mixer_img = Image.open(MIXER_IMAGE_PATH).resize((200, 200))
        mixer_photo = ImageTk.PhotoImage(mixer_img)

        palette_img = Image.open(PALETTE_IMAGE_PATH).resize((200, 200))
        palette_photo = ImageTk.PhotoImage(palette_img)
    except Exception as e:
        print(f"Error loading images: {e}")
        mixer_photo = palette_photo = None

    # Color Mixer Section
    mixer_frame = tk.Frame(main_frame, bg=bg_color)
    mixer_frame.pack(anchor="w", pady=20)

    if mixer_photo:
        mixer_image_label = tk.Label(mixer_frame, image=mixer_photo, cursor="hand2", bg=bg_color)
        mixer_image_label.image = mixer_photo
        mixer_image_label.pack(side=tk.LEFT, padx=20)
        mixer_image_label.bind("<Button-1>", lambda event: open_general_color_mixer(tools_window))

    mixer_text_frame = tk.Frame(mixer_frame, bg=bg_color)
    mixer_text_frame.pack(side=tk.LEFT, padx=10)

    mixer_button = tk.Label(
        mixer_text_frame, text="Color Mixer", font=(font_family, font_size, "bold"),
        fg="blue", bg=bg_color, cursor="hand2"
    )
    mixer_button.pack(anchor="w")
    mixer_button.bind("<Button-1>", lambda event: open_general_color_mixer(tools_window))

    mixer_label = tk.Label(
        mixer_text_frame,
        text="Click here to access our color mixer page, where you can choose three different data formats to start mixing colors!",
        wraplength=400, justify="left", fg=fg_color, bg=bg_color, font=font
    )
    mixer_label.pack(anchor="w")

    # Color Palette Section
    palette_frame = tk.Frame(main_frame, bg=bg_color)
    palette_frame.pack(anchor="w", pady=20)

    if palette_photo:
        palette_image_label = tk.Label(palette_frame, image=palette_photo, cursor="hand2", bg=bg_color)
        palette_image_label.image = palette_photo
        palette_image_label.pack(side=tk.LEFT, padx=20)
        palette_image_label.bind("<Button-1>", lambda event: open_color_palette_page(tools_window))

    palette_text_frame = tk.Frame(palette_frame, bg=bg_color)
    palette_text_frame.pack(side=tk.LEFT, padx=10)

    palette_button = tk.Label(
        palette_text_frame, text="Color Palette", font=(font_family, font_size, "bold"),
        fg="blue", bg=bg_color, cursor="hand2"
    )
    palette_button.pack(anchor="w")
    palette_button.bind("<Button-1>", lambda event: open_color_palette_page(tools_window))

    palette_label = tk.Label(
        palette_text_frame,
        text="Click here to access our color palette page.",
        wraplength=400, justify="left", fg=fg_color, bg=bg_color, font=font
    )
    palette_label.pack(anchor="w")

    # Back Button
    back_button = tk.Button(
        tools_window,
        text="Back", font=(font_family, font_size),
        fg="black", bg="#e0e0e0", borderwidth=1, relief="raised",
        padx=20, pady=10,
        command=lambda: go_back(tools_window)
    )
    back_button.pack(pady=30)

    tools_window.mainloop()

# Run
if __name__ == "__main__":
    open_tools_page()

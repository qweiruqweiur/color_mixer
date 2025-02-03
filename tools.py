import tkinter as tk
import subprocess
from PIL import Image, ImageTk  # Requires Pillow library

# Image paths
MIXER_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/mixer.jpeg"
PALETTE_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/palette.jpeg"

# Functions to open other pages and close the tools page first
def open_general_color_mixer(tools_window):
    tools_window.destroy()  # Close the tools page
    subprocess.run(["python", "general_color_mixer.py"])  # Open General Color Mixer

def open_color_palette_page(tools_window):
    tools_window.destroy()  # Close the tools page
    subprocess.run(["python", "color_palette_page.py"])  # Open Color Palette Page

# Main function to open the Tools Page
def open_tools_page():
    # GUI Setup
    tools_window = tk.Tk()
    tools_window.title("Tools")

    # Title Label
    tk.Label(tools_window, text="Tools", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

    # Load images
    try:
        mixer_img = Image.open(MIXER_IMAGE_PATH).resize((100, 100))
        mixer_photo = ImageTk.PhotoImage(mixer_img)

        palette_img = Image.open(PALETTE_IMAGE_PATH).resize((100, 100))
        palette_photo = ImageTk.PhotoImage(palette_img)
    except Exception as e:
        print(f"Error loading images: {e}")
        mixer_photo = None
        palette_photo = None

    # Mixer Section
    mixer_frame = tk.Frame(tools_window)
    mixer_frame.grid(row=1, column=0, pady=10, padx=10, sticky="w")

    mixer_label = tk.Label(mixer_frame, text="Click here to access our color mixer page, where you can choose three different data formats to start mixing colors!", wraplength=300, justify="left")
    mixer_label.pack(side=tk.LEFT, padx=10)

    mixer_button = tk.Button(mixer_frame, text="Color Mixer", width=20, command=lambda: open_general_color_mixer(tools_window))
    mixer_button.pack(side=tk.LEFT, padx=10)

    if mixer_photo:
        mixer_image_label = tk.Label(mixer_frame, image=mixer_photo, cursor="hand2")
        mixer_image_label.image = mixer_photo
        mixer_image_label.pack(side=tk.LEFT)
        mixer_image_label.bind("<Button-1>", lambda event: open_general_color_mixer(tools_window))  # Make image clickable

    # Palette Section
    palette_frame = tk.Frame(tools_window)
    palette_frame.grid(row=2, column=0, pady=10, padx=10, sticky="w")

    palette_label = tk.Label(palette_frame, text="Click here to access our color palette page.", wraplength=300, justify="left")
    palette_label.pack(side=tk.LEFT, padx=10)

    palette_button = tk.Button(palette_frame, text="Color Palette", width=20, command=lambda: open_color_palette_page(tools_window))
    palette_button.pack(side=tk.LEFT, padx=10)

    if palette_photo:
        palette_image_label = tk.Label(palette_frame, image=palette_photo, cursor="hand2")
        palette_image_label.image = palette_photo
        palette_image_label.pack(side=tk.LEFT)
        palette_image_label.bind("<Button-1>", lambda event: open_color_palette_page(tools_window))  # Make image clickable

    # Back Button
    tk.Button(tools_window, text="Back", width=20, command=tools_window.destroy).grid(row=3, column=0, pady=20)

    tools_window.mainloop()

# Run Tools Page
if __name__ == "__main__":
    open_tools_page()

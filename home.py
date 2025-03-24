import tkinter as tk
import subprocess
import os
import json
from PIL import Image, ImageTk

# Image paths
MIXER_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/mixer.jpeg"
PALETTE_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/palette.jpeg"
FILES_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/files.png"

TEMP_FILE = "temp_saved_colors.txt"
SETTINGS_FILE = "appearance_settings.json"

# Load appearance settings
def load_appearance():
    default = {"theme": "light", "font_size": "medium", "font_family": "Arial"}
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return default
    return default

# Map font size
def get_font_settings():
    appearance = load_appearance()
    font_sizes = {
        "small": 10, "medium": 12, "large": 14, "extra large": 16
    }
    font_size = font_sizes.get(appearance.get("font_size", "medium"), 12)
    font_family = appearance.get("font_family", "Arial")
    theme = appearance.get("theme", "light")
    return font_family, font_size, theme

# Navigation Functions
def open_tools_page(current_window):
    current_window.destroy()
    subprocess.Popen(["python", "tools.py"])

def open_color_mixer(current_window):
    current_window.destroy()
    subprocess.Popen(["python", "general_color_mixer.py"])

def open_color_palette(current_window):
    current_window.destroy()
    subprocess.Popen(["python", "color_palette_page.py"])

def open_external_data(current_window):
    current_window.destroy()
    subprocess.Popen(["python", "external_data.py"])

def open_appearance_page(current_window):
    current_window.destroy()
    subprocess.Popen(["python", "appearance.py"])

def close_program(home_window):
    if os.path.exists(TEMP_FILE):
        open(TEMP_FILE, "w").close()
    home_window.destroy()
    os._exit(0)

# Main Home Page
def open_home_page():
    font_family, font_size, theme = get_font_settings()
    font = (font_family, font_size)

    bg_color = "#333" if theme == "dark" else "white"
    fg_color = "white" if theme == "dark" else "black"

    home_window = tk.Tk()
    home_window.title("Color Mixer")
    home_window.configure(bg=bg_color)

    # Top Navigation
    top_bar = tk.Frame(home_window, bg=bg_color)
    top_bar.pack(fill="x", pady=10, padx=30)

    title_label = tk.Label(top_bar, text="Color Mixer", font=("Arial", 18, "bold"), fg=fg_color, bg=bg_color)
    title_label.pack(side=tk.LEFT)

    nav_frame = tk.Frame(top_bar, bg=bg_color)
    nav_frame.pack(side=tk.RIGHT)

    def create_nav_button(parent, text, command):
        btn = tk.Button(
            parent, text=text, font=(font_family, font_size),
            fg=fg_color, bg=bg_color, borderwidth=0, highlightthickness=0,
            activebackground=bg_color, relief="flat",
            padx=20, pady=10, command=lambda: command(home_window)
        )
        btn.pack(side=tk.LEFT, padx=15)
        separator = tk.Frame(parent, width=1, height=20, bg="lightgrey")
        separator.pack(side=tk.LEFT, padx=5)

    create_nav_button(nav_frame, "Tools", open_tools_page)
    create_nav_button(nav_frame, "External Data", open_external_data)
    create_nav_button(nav_frame, "Settings", open_appearance_page)

    # Main Section
    main_frame = tk.Frame(home_window, bg=bg_color)
    main_frame.pack(pady=40, fill="both", expand=True)

    left_frame = tk.Frame(main_frame, bg=bg_color)
    left_frame.pack(side=tk.LEFT, padx=50, pady=20, expand=True)

    right_frame = tk.Frame(main_frame, bg=bg_color)
    right_frame.pack(side=tk.RIGHT, padx=50, pady=20, expand=True)

    question_label = tk.Label(
        left_frame,
        text="What color would you like to make today?",
        font=("Arial", 28, "bold"),
        fg=fg_color, bg=bg_color
    )
    question_label.pack(pady=10)

    get_started_button = tk.Button(
        left_frame, text="GET STARTED", font=("Arial", 14, "bold"),
        bg="black", fg="white",  # Always black button with white text
        activebackground="black", activeforeground="white",
        width=20, height=2,
        borderwidth=0, highlightthickness=0, relief="flat",
        command=lambda: open_tools_page(home_window)
    )
    get_started_button.pack(pady=20)

    try:
        color_wheel_img = Image.open(MIXER_IMAGE_PATH).resize((350, 350))
        color_wheel_photo = ImageTk.PhotoImage(color_wheel_img)
        color_wheel_label = tk.Label(right_frame, image=color_wheel_photo, bg=bg_color)
        color_wheel_label.image = color_wheel_photo
        color_wheel_label.pack()
    except Exception as e:
        print(f"Error loading color wheel image: {e}")

    tk.Frame(home_window, height=1, width=1500, bg="grey").pack(pady=10)

    bottom_frame = tk.Frame(home_window, bg=bg_color)
    bottom_frame.pack(pady=30)

    try:
        mixer_img = Image.open(MIXER_IMAGE_PATH).resize((100, 100))
        mixer_photo = ImageTk.PhotoImage(mixer_img)

        palette_img = Image.open(PALETTE_IMAGE_PATH).resize((100, 100))
        palette_photo = ImageTk.PhotoImage(palette_img)

        files_img = Image.open(FILES_IMAGE_PATH).resize((100, 100))
        files_photo = ImageTk.PhotoImage(files_img)
    except Exception as e:
        print(f"Error loading images: {e}")
        mixer_photo = palette_photo = files_photo = None

    def create_tool_section(frame, title, description, image, command):
        tool_frame = tk.Frame(frame, bg=bg_color)
        tool_frame.grid(row=0, column=len(frame.grid_slaves()), padx=30)

        tk.Label(tool_frame, text=title, font=("Arial", 16, "bold"), fg=fg_color, bg=bg_color).pack()
        tk.Label(tool_frame, text=description, wraplength=250, justify="center", fg=fg_color, bg=bg_color).pack()

        if image:
            image_label = tk.Label(tool_frame, image=image, cursor="hand2", bg=bg_color)
            image_label.image = image
            image_label.pack()
            image_label.bind("<Button-1>", lambda event: command(home_window))

    create_tool_section(
        bottom_frame,
        "Color Mixer",
        "Use our intuitive color mixer to create any color you desire and save it for later use.",
        mixer_photo,
        open_color_mixer
    )

    create_tool_section(
        bottom_frame,
        "Color Palette",
        "Generate your dream palette with our color palette tool.",
        palette_photo,
        open_color_palette
    )

    create_tool_section(
        bottom_frame,
        "File Features",
        "Import and export colors in various formats.",
        files_photo,
        open_external_data
    )

    home_window.protocol("WM_DELETE_WINDOW", lambda: close_program(home_window))
    home_window.mainloop()

# Run Home Page
if __name__ == "__main__":
    open_home_page()

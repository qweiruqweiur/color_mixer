import tkinter as tk
import subprocess
from PIL import Image, ImageTk  # Requires Pillow library

# Image paths
MIXER_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/mixer.jpeg"
PALETTE_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/palette.jpeg"
FILES_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/files.png"

# Functions to open other pages
def open_tools_page():
    subprocess.run(["python", "tools.py"])  # Corrected filename

def open_color_mixer():
    subprocess.run(["python", "general_color_mixer.py"])

def open_color_palette():
    subprocess.run(["python", "color_palette_page.py"])

def open_external_data():
    subprocess.run(["python", "external_data.py"])
    
# Main function to open the Home Page
def open_home_page():
    # GUI Setup
    home_window = tk.Tk()
    home_window.title("Color Mixer")

    # Title
    title_label = tk.Label(home_window, text="@ Color Mixer", font=("Arial", 18, "bold"))
    title_label.pack(pady=10)

    # Navigation Bar
    nav_frame = tk.Frame(home_window)
    nav_frame.pack()

    tk.Button(nav_frame, text="Tools", command=open_tools_page).pack(side=tk.LEFT, padx=10)
    tk.Button(nav_frame, text="External Data", command=open_external_data).pack(side=tk.LEFT, padx=10)
    tk.Button(nav_frame, text="Settings", state="disabled").pack(side=tk.LEFT, padx=10)

    # Main Section
    main_frame = tk.Frame(home_window)
    main_frame.pack(pady=20)

    question_label = tk.Label(main_frame, text="What color would you like to make today?", font=("Arial", 14, "bold"))
    question_label.pack()

    get_started_button = tk.Button(main_frame, text="GET STARTED", font=("Arial", 12), bg="black", fg="white", width=15, command=open_tools_page)
    get_started_button.pack(pady=10)

    # Load color wheel image
    try:
        color_wheel_img = Image.open(MIXER_IMAGE_PATH).resize((250, 250))  # Placeholder: Use correct path for color wheel
        color_wheel_photo = ImageTk.PhotoImage(color_wheel_img)
        color_wheel_label = tk.Label(main_frame, image=color_wheel_photo)
        color_wheel_label.image = color_wheel_photo
        color_wheel_label.pack()
    except Exception as e:
        print(f"Error loading color wheel image: {e}")

    # Bottom Section with Tool Descriptions and Images
    bottom_frame = tk.Frame(home_window)
    bottom_frame.pack(pady=20)

    # Load images
    try:
        mixer_img = Image.open(MIXER_IMAGE_PATH).resize((80, 80))
        mixer_photo = ImageTk.PhotoImage(mixer_img)

        palette_img = Image.open(PALETTE_IMAGE_PATH).resize((80, 80))
        palette_photo = ImageTk.PhotoImage(palette_img)

        files_img = Image.open(FILES_IMAGE_PATH).resize((80, 80))
        files_photo = ImageTk.PhotoImage(files_img)
    except Exception as e:
        print(f"Error loading images: {e}")
        mixer_photo = palette_photo = files_photo = None

    # Color Mixer Section
    mixer_frame = tk.Frame(bottom_frame)
    mixer_frame.grid(row=0, column=0, padx=20)

    mixer_label = tk.Label(mixer_frame, text="Color Mixer\nUse our intuitive color mixer to create any color you desire and save it for later use.", wraplength=200, justify="center")
    mixer_label.pack()

    if mixer_photo:
        mixer_image_label = tk.Label(mixer_frame, image=mixer_photo, cursor="hand2")
        mixer_image_label.image = mixer_photo
        mixer_image_label.pack()
        mixer_image_label.bind("<Button-1>", lambda event: open_color_mixer())

    # Color Palette Section
    palette_frame = tk.Frame(bottom_frame)
    palette_frame.grid(row=0, column=1, padx=20)

    palette_label = tk.Label(palette_frame, text="Color Palette\nNeed a palette for designing your website or decorating your home screen? Generate your dream palette with our color palette tool.", wraplength=200, justify="center")
    palette_label.pack()

    if palette_photo:
        palette_image_label = tk.Label(palette_frame, image=palette_photo, cursor="hand2")
        palette_image_label.image = palette_photo
        palette_image_label.pack()
        palette_image_label.bind("<Button-1>", lambda event: open_color_palette())

    # File Features Section
    files_frame = tk.Frame(bottom_frame)
    files_frame.grid(row=0, column=2, padx=20)

    files_label = tk.Label(files_frame, text="File Features\nImport colors and palettes in various compatible formats. Export colors and palettes made using the color tools.", wraplength=200, justify="center")
    files_label.pack()

    if files_photo:
        files_image_label = tk.Label(files_frame, image=files_photo, cursor="hand2")
        files_image_label.image = files_photo
        files_image_label.pack()
        files_image_label.bind("<Button-1>", lambda event: open_external_data())

    home_window.mainloop()

# Run Home Page
if __name__ == "__main__":
    open_home_page()

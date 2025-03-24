import tkinter as tk
import subprocess
import os
from PIL import Image, ImageTk  # Requires Pillow library

# Image paths for folder icons
IMPORT_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/files1.png"
EXPORT_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/files2.png"
EXPORT_PALETTE_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/files3.png"

# Functions to open other pages and close this one first
def open_import_colors(current_window):
    current_window.destroy()
    subprocess.Popen(["python", "import_colors.py"])

def open_export_colors(current_window):
    current_window.destroy()
    subprocess.Popen(["python", "export_colors.py"])

def open_export_palettes(current_window):
    current_window.destroy()
    subprocess.Popen(["python", "export_palettes.py"])

def go_back(current_window):
    current_window.destroy()
    subprocess.Popen(["python", "home.py"])

# Main function to open the External Data Page
def open_external_data_page():
    external_data_window = tk.Tk()
    external_data_window.title("External Data")
    external_data_window.configure(bg="white")

    BUTTON_STYLE = {
        "bg": "#e0e0e0",
        "fg": "black",
        "font": ("Arial", 11, "bold"),
        "bd": 1,
        "relief": "raised",
        "padx": 8,
        "pady": 4
    }

    # Title
    tk.Label(
        external_data_window,
        text="External Data",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="black"
    ).pack(pady=(20, 10))

    # Load images
    try:
        import_img = Image.open(IMPORT_IMAGE_PATH).resize((100, 100))
        import_photo = ImageTk.PhotoImage(import_img)

        export_img = Image.open(EXPORT_IMAGE_PATH).resize((100, 100))
        export_photo = ImageTk.PhotoImage(export_img)

        export_palette_img = Image.open(EXPORT_PALETTE_IMAGE_PATH).resize((100, 100))
        export_palette_photo = ImageTk.PhotoImage(export_palette_img)
    except Exception as e:
        print(f"Error loading images: {e}")
        import_photo = export_photo = export_palette_photo = None

    # --- Tool Options ---
    main_frame = tk.Frame(external_data_window, bg="white")
    main_frame.pack(pady=30, padx=40)

    def create_section(parent, title, description, image, command):
        section = tk.Frame(parent, bg="white")
        section.pack(side=tk.LEFT, padx=40)

        tk.Label(section, text=title, font=("Arial", 14, "bold"), bg="white", fg="black").pack(pady=(0, 8))

        if image:
            image_label = tk.Label(section, image=image, cursor="hand2", bg="white")
            image_label.image = image
            image_label.pack()
            image_label.bind("<Button-1>", lambda e: command(external_data_window))

        tk.Label(section, text=description, wraplength=200, justify="center", bg="white", fg="black").pack(pady=10)

    create_section(
        main_frame,
        "Import Colors",
        "Click the black folder to import colors from external files.",
        import_photo,
        open_import_colors
    )

    create_section(
        main_frame,
        "Export Colors",
        "Click the white folder to export your saved colors.",
        export_photo,
        open_export_colors
    )

    create_section(
        main_frame,
        "Export Palettes",
        "Click the yellow folder to export your custom color palettes.",
        export_palette_photo,
        open_export_palettes
    )

    # --- Back Button ---
    tk.Button(
        external_data_window,
        text="Back",
        width=20,
        command=lambda: go_back(external_data_window),
        **BUTTON_STYLE
    ).pack(pady=30)

    external_data_window.mainloop()

# Run External Data Page
if __name__ == "__main__":
    open_external_data_page()

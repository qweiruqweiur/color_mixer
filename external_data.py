import tkinter as tk
import subprocess
from PIL import Image, ImageTk  # Requires Pillow library

# Image paths for folder icons
IMPORT_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/files1.png"
EXPORT_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/files2.png"
EXPORT_PALETTE_IMAGE_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/files3.png"

# Functions to open other pages
def open_import_colors():
    subprocess.run(["python", "import_colors.py"])  # Open Import Colors Page

def open_export_colors():
    subprocess.run(["python", "export_colors.py"])  # Open Export Colors Page

def open_export_palettes():
    subprocess.run(["python", "export_palettes.py"])  # Open Export Palettes Page

def go_back():
    """Close External Data Page and return to Home Page."""
    external_data_window.destroy()
    subprocess.run(["python", "home.py"])

# Main function to open the External Data Page
def open_external_data_page():
    global external_data_window  # Needed to close the window in go_back()
    
    # GUI Setup
    external_data_window = tk.Tk()
    external_data_window.title("External Data")

    # Title
    title_label = tk.Label(external_data_window, text="External Data", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Load images
    try:
        import_img = Image.open(IMPORT_IMAGE_PATH).resize((80, 80))
        import_photo = ImageTk.PhotoImage(import_img)

        export_img = Image.open(EXPORT_IMAGE_PATH).resize((80, 80))
        export_photo = ImageTk.PhotoImage(export_img)

        export_palette_img = Image.open(EXPORT_PALETTE_IMAGE_PATH).resize((80, 80))
        export_palette_photo = ImageTk.PhotoImage(export_palette_img)
    except Exception as e:
        print(f"Error loading images: {e}")
        import_photo = export_photo = export_palette_photo = None

    # Layout Frame
    main_frame = tk.Frame(external_data_window)
    main_frame.pack(pady=20)

    # Import Colors Section
    import_frame = tk.Frame(main_frame)
    import_frame.grid(row=0, column=0, padx=20)

    import_label = tk.Label(import_frame, text="Import Colors", font=("Arial", 12, "bold"), fg="blue")
    import_label.pack()

    if import_photo:
        import_image_label = tk.Label(import_frame, image=import_photo, cursor="hand2")
        import_image_label.image = import_photo
        import_image_label.pack()
        import_image_label.bind("<Button-1>", lambda event: open_import_colors())

    import_desc = tk.Label(import_frame, text="Click the black folders to go to the import color page.", wraplength=200, justify="center")
    import_desc.pack()

    # Export Colors Section
    export_frame = tk.Frame(main_frame)
    export_frame.grid(row=0, column=1, padx=20)

    export_label = tk.Label(export_frame, text="Export Colors", font=("Arial", 12, "bold"), fg="blue")
    export_label.pack()

    if export_photo:
        export_image_label = tk.Label(export_frame, image=export_photo, cursor="hand2")
        export_image_label.image = export_photo
        export_image_label.pack()
        export_image_label.bind("<Button-1>", lambda event: open_export_colors())

    export_desc = tk.Label(export_frame, text="Click the white folders to go to the export color page.", wraplength=200, justify="center")
    export_desc.pack()

    # Export Palettes Section
    export_palette_frame = tk.Frame(main_frame)
    export_palette_frame.grid(row=0, column=2, padx=20)

    export_palette_label = tk.Label(export_palette_frame, text="Export Palettes", font=("Arial", 12, "bold"), fg="blue")
    export_palette_label.pack()

    if export_palette_photo:
        export_palette_image_label = tk.Label(export_palette_frame, image=export_palette_photo, cursor="hand2")
        export_palette_image_label.image = export_palette_photo
        export_palette_image_label.pack()
        export_palette_image_label.bind("<Button-1>", lambda event: open_export_palettes())

    export_palette_desc = tk.Label(export_palette_frame, text="Click the yellow folders to go to the export color palette page.", wraplength=200, justify="center")
    export_palette_desc.pack()

    # Back Button
    back_button = tk.Button(external_data_window, text="Back", command=go_back)
    back_button.pack(pady=20)

    external_data_window.mainloop()

# Run External Data Page
if __name__ == "__main__":
    open_external_data_page()


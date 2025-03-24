import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import subprocess

SETTINGS_FILE = "appearance_settings.json"

# Load settings
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {
        "theme": "light",
        "font_size": "medium",
        "font_family": "Arial"
    }

# Save settings
def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

# Theme updater (recursive, robust)
def update_theme():
    theme = "dark" if dark_mode.get() else "light"
    bg = "#333" if theme == "dark" else "white"
    fg = "white" if theme == "dark" else "black"

    root.configure(bg=bg)

    def apply_theme_recursive(widget):
        try:
            widget.configure(bg=bg)
        except:
            pass

        # ⛔ Don't change text color of apply/back buttons
        if widget not in [apply_button, back_button]:
            try:
                widget.configure(fg=fg)
            except:
                pass

        for child in widget.winfo_children():
            apply_theme_recursive(child)

    apply_theme_recursive(root)

    # 🎨 Theme toggle buttons (light/dark)
    if dark_mode.get():
        dark_button.configure(bg="#005f00", fg="black")
        light_button.configure(bg="#8B0000", fg="#8B0000")
    else:
        light_button.configure(bg="#005f00", fg="#005f00")
        dark_button.configure(bg="#8B0000", fg="#8B0000")


# Toggle theme
def toggle_theme(theme_choice):
    dark_mode.set(theme_choice == "dark")
    update_theme()

# Apply changes and refresh
def apply_changes():
    settings = {
        "theme": "dark" if dark_mode.get() else "light",
        "font_size": font_size_var.get(),
        "font_family": font_family_var.get()
    }
    save_settings(settings)
    messagebox.showinfo("Saved", "Appearance settings updated.\nPage will refresh.")
    root.destroy()
    subprocess.Popen(["python", "appearance.py"])

# Go back to home page
def go_back():
    root.destroy()
    subprocess.Popen(["python", "home.py"])

# ─────────────── UI SETUP ───────────────
root = tk.Tk()
root.title("Appearance Settings")
root.geometry("800x600")  # 🎯 Make window much larger
root.minsize(800, 600)

settings = load_settings()

# Font settings
font_sizes = {
    "small": 10,
    "medium": 12,
    "large": 14,
    "extra large": 16
}
font_size = font_sizes.get(settings.get("font_size", "medium"), 12)
font_family = settings.get("font_family", "Arial")
default_font = (font_family, font_size)

root.configure(bg="white")
dark_mode = tk.BooleanVar(value=settings.get("theme") == "dark")

BUTTON_STYLE = {
    "bg": "#e0e0e0", "font": default_font,
    "bd": 1, "relief": "raised", "padx": 12, "pady": 8
}

# ─────────────── Title ───────────────
title_label = tk.Label(root, text="Appearance Settings", font=("Arial", 20, "bold"), bg="white", fg="black")
title_label.pack(pady=20)

# ─────────────── Theme Toggle ───────────────
theme_frame = tk.Frame(root, bg="white")
theme_frame.pack(pady=15)

tk.Label(theme_frame, text="Theme:", font=("Arial", 14), bg="white", fg="black").pack(side=tk.LEFT, padx=10)

light_button = tk.Button(theme_frame, text="Light", font=default_font,
                         command=lambda: toggle_theme("light"))
dark_button = tk.Button(theme_frame, text="Dark", font=default_font,
                        command=lambda: toggle_theme("dark"))
light_button.pack(side=tk.LEFT, padx=10)
dark_button.pack(side=tk.LEFT, padx=10)

# ─────────────── Font Settings ───────────────
font_frame = tk.Frame(root, bg="white")
font_frame.pack(pady=20)

tk.Label(font_frame, text="Font Size:", bg="white", font=default_font).grid(row=0, column=0, sticky="e", padx=20, pady=10)
font_size_var = tk.StringVar(value=settings.get("font_size", "medium"))
font_size_dropdown = ttk.Combobox(font_frame, textvariable=font_size_var,
                                  values=["small", "medium", "large", "extra large"], state="readonly", font=default_font)
font_size_dropdown.grid(row=0, column=1, padx=10, ipadx=30)

tk.Label(font_frame, text="Font Family:", bg="white", font=default_font).grid(row=1, column=0, sticky="e", padx=20, pady=10)
font_family_var = tk.StringVar(value=settings.get("font_family", "Arial"))
font_family_dropdown = ttk.Combobox(font_frame, textvariable=font_family_var,
                                    values=["Arial", "Courier", "Times"], state="readonly", font=default_font)
font_family_dropdown.grid(row=1, column=1, padx=10, ipadx=30)

# ─────────────── Action Buttons ───────────────
bottom_frame = tk.Frame(root, bg="white")
bottom_frame.pack(pady=40)

# Action Buttons
apply_button = tk.Button(bottom_frame, text="Apply Changes", command=apply_changes, width=20, **BUTTON_STYLE)
apply_button.pack(pady=10)

back_button = tk.Button(bottom_frame, text="Back", command=go_back, width=20, **BUTTON_STYLE)
back_button.pack()


update_theme()
root.mainloop()

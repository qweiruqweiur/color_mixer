import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import json
import os
import subprocess

# Appearance settings file
SETTINGS_FILE = "appearance_settings.json"
USER_KEYS_FILE = "user_keys.json"

# Load settings
def load_settings():
    """Loads saved user settings or initializes default values."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {
        "theme": "light",
        "font_size": "medium",
        "font_family": "Arial",
        "user_key": ""
    }

# Save settings
def save_settings(settings):
    """Saves user settings to a JSON file."""
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

# Load user keys
def load_user_keys():
    """Loads saved user keys from a JSON file."""
    if os.path.exists(USER_KEYS_FILE):
        with open(USER_KEYS_FILE, "r") as file:
            return json.load(file)
    return []

# Save user keys
def save_user_keys(keys):
    """Saves user keys to a JSON file."""
    with open(USER_KEYS_FILE, "w") as file:
        json.dump(keys, file)

# Generate a new unique key
def generate_user_key():
    """Generates a unique user key and displays it."""
    new_key = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    user_key_entry.delete(0, tk.END)
    user_key_entry.insert(0, new_key)

# Change user key
def change_user_key():
    """Validates and updates the user key."""
    old_key = old_key_entry.get()
    new_key = new_key_entry.get()
    user_keys = load_user_keys()

    if old_key not in user_keys:
        messagebox.showerror("Invalid Key", "The old key is incorrect.")
        return

    if new_key in user_keys:
        key_error_label.config(text="Key already exists! Choose another.")
        return

    # Update key
    user_keys.remove(old_key)
    user_keys.append(new_key)
    save_user_keys(user_keys)

    # Update settings
    settings = load_settings()
    settings["user_key"] = new_key
    save_settings(settings)

    messagebox.showinfo("Success", "User key updated successfully!")

# Apply changes
def apply_changes():
    """Applies appearance settings and saves them."""
    settings = {
        "theme": "dark" if dark_mode.get() else "light",
        "font_size": font_size_var.get(),
        "font_family": font_family_var.get(),
        "user_key": user_key_entry.get()
    }
    save_settings(settings)
    messagebox.showinfo("Success", "Appearance settings updated!")

# Toggle theme
def toggle_theme(theme):
    """Switches between light and dark mode."""
    dark_mode.set(True if theme == "dark" else False)
    update_theme()

# Update theme
def update_theme():
    """Updates the background and text colors based on theme selection."""
    theme = "dark" if dark_mode.get() else "light"
    bg_color = "#333" if theme == "dark" else "#fff"
    fg_color = "#fff" if theme == "dark" else "#000"

    root.config(bg=bg_color)

    for widget in root.winfo_children():
        try:
            # Standard Tkinter widgets
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry)):
                widget.config(bg=bg_color, fg=fg_color)
            elif isinstance(widget, tk.Frame):
                widget.config(bg=bg_color)
            # Special handling for ttk widgets (they do not support bg/fg)
            elif isinstance(widget, ttk.Combobox):
                widget.option_add('*TCombobox*Listbox.foreground', fg_color)
                widget.option_add('*TCombobox*Listbox.background', bg_color)
                widget.option_add('*TCombobox.foreground', fg_color)
        except tk.TclError:
            pass  # Ignore errors for unsupported properties


# UI Setup
root = tk.Tk()
root.title("Appearance Settings")

settings = load_settings()

# Theme selection
dark_mode = tk.BooleanVar(value=settings["theme"] == "dark")
light_button = tk.Button(root, text="Light", command=lambda: toggle_theme("light"), bg="green" if not dark_mode.get() else "gray")
dark_button = tk.Button(root, text="Dark", command=lambda: toggle_theme("dark"), bg="green" if dark_mode.get() else "gray")

light_button.grid(row=0, column=0, padx=10, pady=5)
dark_button.grid(row=0, column=1, padx=10, pady=5)

# Font size selection
tk.Label(root, text="Font Size:").grid(row=1, column=0, sticky="w", padx=10)
font_size_var = tk.StringVar(value=settings["font_size"])
font_size_dropdown = ttk.Combobox(root, textvariable=font_size_var, values=["small", "medium", "large", "extra large"], state="readonly")
font_size_dropdown.grid(row=1, column=1, padx=10)

# Font family selection
tk.Label(root, text="Font Family:").grid(row=2, column=0, sticky="w", padx=10)
font_family_var = tk.StringVar(value=settings["font_family"])
font_family_dropdown = ttk.Combobox(root, textvariable=font_family_var, values=["Arial", "Courier", "Times"], state="readonly")
font_family_dropdown.grid(row=2, column=1, padx=10)

# User key generation
tk.Button(root, text="Generate Key", command=generate_user_key).grid(row=3, column=0, pady=5)
user_key_entry = tk.Entry(root, width=20)
user_key_entry.insert(0, settings["user_key"])
user_key_entry.grid(row=3, column=1, pady=5)

# Change user key
tk.Label(root, text="Old Key:").grid(row=4, column=0, padx=10)
old_key_entry = tk.Entry(root, width=20)
old_key_entry.grid(row=4, column=1, padx=10)

tk.Label(root, text="New Key:").grid(row=5, column=0, padx=10)
new_key_entry = tk.Entry(root, width=20)
new_key_entry.grid(row=5, column=1, padx=10)

tk.Button(root, text="Change Key", command=change_user_key).grid(row=6, column=1, pady=5)
key_error_label = tk.Label(root, text="", fg="red")
key_error_label.grid(row=7, column=1)

# Apply changes button
tk.Button(root, text="Apply Changes", command=apply_changes).grid(row=8, column=1, pady=10)

# Back button
def go_back():
    """Closes the settings page and returns to the main settings menu."""
    root.destroy()
    subprocess.run(["python", "home.py"])

tk.Button(root, text="Back", command=go_back).grid(row=9, column=1, pady=10)

update_theme()  # Apply initial theme
root.mainloop()


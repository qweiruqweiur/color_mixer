# This is the COMPLETE updated import_colors.py with conversion and send-to-mixer fix

import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import re
import os
import json
from PIL import Image, ImageTk

SAVE_ICON_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/save.png"
MIXER_INPUT_FILE = "mixer_input.txt"

def hex_to_rgb(hex_val):
    hex_val = hex_val.lstrip("#")
    return tuple(int(hex_val[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}".upper()

def cmyk_to_rgb(c, m, y, k):
    r = int(255 * (1 - c / 100) * (1 - k / 100))
    g = int(255 * (1 - m / 100) * (1 - k / 100))
    b = int(255 * (1 - y / 100) * (1 - k / 100))
    return r, g, b

def rgb_to_cmyk(r, g, b):
    r, g, b = r / 255, g / 255, b / 255
    k = 1 - max(r, g, b)
    if k == 1:
        return (0, 0, 0, 100)
    c = (1 - r - k) / (1 - k) * 100
    m = (1 - g - k) / (1 - k) * 100
    y = (1 - b - k) / (1 - k) * 100
    return (round(c), round(m), round(y), round(k * 100))

def convert_color_string_to_rgb(color_str):
    try:
        if color_str.startswith("RGB"):
            return eval(color_str[3:])
        elif color_str.startswith("#"):
            return hex_to_rgb(color_str)
        elif color_str.startswith("CMYK"):
            c, m, y, k = map(int, color_str[5:-1].split(","))
            return cmyk_to_rgb(c, m, y, k)
    except:
        return None

def calculate_mixed_rgb(components):
    total = sum(p for _, p in components)
    if total == 0:
        return (255, 255, 255)
    r = sum(convert_color_string_to_rgb(c)[0] * p for c, p in components) // total
    g = sum(convert_color_string_to_rgb(c)[1] * p for c, p in components) // total
    b = sum(convert_color_string_to_rgb(c)[2] * p for c, p in components) // total
    return (r, g, b)

def parse_color_data(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read().strip()
        try:
            data = json.loads(content.splitlines()[0])
            if "sectors" in data:
                return [(s["color"], s["potency"]) for s in data["sectors"]]
        except:
            pass
        return [(line.strip(), 1) for line in content.splitlines() if line.strip()]
    except Exception as e:
        messagebox.showerror("Error", f"Could not read file: {e}")
        return []

def open_import_colors_page():
    def choose_file():
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            file_path_var.set(path)

    def confirm_import():
        file_path = file_path_var.get()
        fmt = format_var.get()

        if not file_path or not fmt:
            messagebox.showerror("Missing Info", "Please select both format and file.")
            return

        raw = parse_color_data(file_path)
        if not raw:
            messagebox.showerror("No Colors", "No valid colors found.")
            return

        imported_colors.clear()
        imported_colors.extend(raw[:10])

        # Populate wheel & grid
        for i, (color_str, potency) in enumerate(imported_colors):
            rgb = convert_color_string_to_rgb(color_str)
            if not rgb:
                continue
            r, g, b = rgb
            hex_color = f"#{r:02x}{g:02x}{b:02x}"

            # Display raw color in selected format
            if fmt == "RGB":
                display = f"RGB({r}, {g}, {b})"
            elif fmt == "HEX":
                display = rgb_to_hex((r, g, b))
            elif fmt == "CMYK":
                display = f"CMYK{rgb_to_cmyk(r, g, b)}"
            else:
                display = color_str

            canvas.itemconfig(sectors[i], fill=hex_color)
            control_labels[i].config(text=f"{display}\n(p{potency})", bg=hex_color)

        # Update center
        mix = calculate_mixed_rgb([(c, p) for c, p in imported_colors])
        hex_mix = rgb_to_hex(mix)
        canvas.itemconfig(center_circle, fill=hex_mix)
        result_label.config(text=f"{fmt}: {mix if fmt == 'RGB' else (hex_mix if fmt == 'HEX' else 'CMYK' + str(rgb_to_cmyk(*mix)))}")

    def send_to_mixer():
        if not imported_colors:
            messagebox.showerror("No Color", "Confirm colors before sending.")
            return
        fmt = format_var.get()
        with open(MIXER_INPUT_FILE, "w") as f:
            for color_str, potency in imported_colors:
                rgb = convert_color_string_to_rgb(color_str)
                if not rgb:
                    continue
                if fmt == "RGB":
                    formatted = f"RGB({rgb[0]}, {rgb[1]}, {rgb[2]})"
                elif fmt == "HEX":
                    formatted = rgb_to_hex(rgb)
                elif fmt == "CMYK":
                    formatted = f"CMYK{rgb_to_cmyk(*rgb)}"
                else:
                    formatted = color_str
                f.write(f"{fmt}|{formatted}|{potency}\n")

        import_window.destroy()
        if fmt == "RGB":
            subprocess.Popen(["python", "rgb_page.py"])
        elif fmt == "HEX":
            subprocess.Popen(["python", "hex_page.py"])
        elif fmt == "CMYK":
            subprocess.Popen(["python", "cmyk_page.py"])

    def go_back():
        import_window.destroy()
        subprocess.Popen(["python", "external_data.py"])

    import_window = tk.Tk()
    import_window.title("Import Colors")
    import_window.configure(bg="white")

    BUTTON_STYLE = {
        "bg": "#e0e0e0", "fg": "black", "font": ("Arial", 11, "bold"),
        "bd": 1, "relief": "raised", "padx": 8, "pady": 4
    }

    imported_colors = []

    # Top
    top_frame = tk.Frame(import_window, bg="white")
    top_frame.pack(padx=20, pady=10, anchor="nw")

    try:
        save_img = Image.open(SAVE_ICON_PATH).resize((40, 40))
        save_icon = ImageTk.PhotoImage(save_img)
        icon_label = tk.Label(top_frame, image=save_icon, bg="white", cursor="hand2")
        icon_label.image = save_icon
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        icon_label.bind("<Button-1>", lambda e: choose_file())
    except:
        pass

    file_path_var = tk.StringVar()
    file_path_entry = tk.Entry(top_frame, textvariable=file_path_var, width=50, font=("Arial", 10), bd=1, relief="solid")
    file_path_entry.pack(side=tk.LEFT, padx=(0, 10))

    tk.Button(top_frame, text="Confirm", command=confirm_import, **BUTTON_STYLE).pack(side=tk.LEFT, padx=5)
    tk.Button(top_frame, text="Send to Mixer", command=send_to_mixer, **BUTTON_STYLE).pack(side=tk.LEFT, padx=5)

    # Format Select
    format_frame = tk.Frame(import_window, bg="white")
    format_frame.pack(anchor="w", padx=30)

    tk.Label(format_frame, text="Select Format:", font=("Arial", 11), bg="white", fg="black").pack(side=tk.LEFT)
    format_var = tk.StringVar()
    for fmt in ["RGB", "HEX", "CMYK"]:
        tk.Radiobutton(format_frame, text=fmt, variable=format_var, value=fmt, bg="white", fg="black", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)

    # Layout
    content_frame = tk.Frame(import_window, bg="white")
    content_frame.pack(padx=20, pady=20)

    # Wheel
    wheel_frame = tk.Frame(content_frame, bg="white")
    wheel_frame.grid(row=0, column=0, padx=(0, 30), sticky="n")

    canvas = tk.Canvas(wheel_frame, width=400, height=400, bg="white", highlightthickness=0)
    canvas.pack()

    sectors = []
    center_x, center_y = 200, 200
    radius = 150
    for i in range(10):
        arc = canvas.create_arc(center_x - radius, center_y - radius,
                                center_x + radius, center_y + radius,
                                start=i * 36, extent=36,
                                fill="white", outline="black")
        sectors.append(arc)

    center_circle = canvas.create_oval(center_x - 50, center_y - 50,
                                       center_x + 50, center_y + 50,
                                       fill="white", outline="black")
    canvas.tag_raise(center_circle)

    result_label = tk.Label(wheel_frame, text="", font=("Arial", 12), bg="white", fg="black")
    result_label.pack(pady=10)

    # Grid
    control_frame = tk.Frame(content_frame, bg="white")
    control_frame.grid(row=0, column=1, sticky="n")
    control_labels = []
    for row in range(5):
        for col in range(2):
            lbl = tk.Label(control_frame, text=" ", width=20, height=2, bg="white", relief="ridge", font=("Arial", 10))
            lbl.grid(row=row, column=col, padx=10, pady=5)
            control_labels.append(lbl)

    tk.Button(import_window, text="Back", width=20, command=go_back, **BUTTON_STYLE).pack(pady=20)

    import_window.mainloop()

if __name__ == "__main__":
    open_import_colors_page()

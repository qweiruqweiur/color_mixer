import tkinter as tk
from tkinter import messagebox, simpledialog
import math
import re
import subprocess
import os
import json

# Paths
TEMP_FILE = "temp_saved_colors.txt"
MIXER_INPUT_FILE = "mixer_input.txt"
SETTINGS_FILE = "appearance_settings.json"

COMPATIBLE_COLORS_RGB = {
    "red": (255, 0, 0), "orange": (255, 165, 0), "yellow": (255, 255, 0),
    "green": (0, 128, 0), "blue": (0, 0, 255), "purple": (128, 0, 128),
    "pink": (255, 192, 203), "black": (0, 0, 0), "brown": (165, 42, 42),
    "white": (255, 255, 255)
}

# === Appearance ===
def load_appearance():
    default = {"theme": "light", "font_size": "medium", "font_family": "Arial"}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except:
            return default
    return default

def get_font_settings():
    settings = load_appearance()
    sizes = {"small": 10, "medium": 12, "large": 14, "extra large": 16}
    return settings.get("font_family", "Arial"), sizes.get(settings.get("font_size", "medium"), 12), settings.get("theme", "light")

# === Utilities ===
def parse_rgb_input(input_text):
    if input_text.lower() in COMPATIBLE_COLORS_RGB:
        return COMPATIBLE_COLORS_RGB[input_text.lower()]
    match = re.match(r"\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", input_text)
    if match:
        r, g, b = map(int, match.groups())
        if all(0 <= v <= 255 for v in (r, g, b)):
            return r, g, b
    return None

def calculate_mixed_rgb(colors_and_potencies):
    red_sum = green_sum = blue_sum = total = 0
    for color, potency in colors_and_potencies:
        red_sum += color[0] * potency
        green_sum += color[1] * potency
        blue_sum += color[2] * potency
        total += potency
    return (255, 255, 255) if total == 0 else (
        red_sum // total, green_sum // total, blue_sum // total
    )

def extract_rgb_tuple(rgb_str):
    return tuple(map(int, rgb_str[4:-1].split(", ")))

def open_rgb_page():
    font_family, font_size, theme = get_font_settings()
    bg = "#000000" if theme == "dark" else "white"
    fg = "white" if theme == "dark" else "black"
    font = (font_family, font_size)

    def update_sector(index, increase=None):
        if index in locked_sectors:
            return
        value = inputs[index].get()
        rgb = parse_rgb_input(value)
        if rgb:
            cur = potencies[index].get()
            if increase is True and cur < 50:
                potencies[index].set(cur + 1)
            elif increase is False and cur > 1:
                potencies[index].set(cur - 1)
            hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
            canvas.itemconfig(sectors[index], fill=hex_color)
            potency_labels[index].config(text=str(potencies[index].get()))
            update_center_color()
        else:
            messagebox.showerror("Invalid Input", "Use a color name or (R, G, B) format.")

    def update_center_color():
        data = []
        for i in range(12):
            if i in locked_sectors:
                continue
            val = inputs[i].get()
            rgb = parse_rgb_input(val)
            if rgb:
                data.append((rgb, potencies[i].get()))
        mixed = calculate_mixed_rgb(data)
        hex_color = f"#{mixed[0]:02x}{mixed[1]:02x}{mixed[2]:02x}"
        canvas.itemconfig(center_circle, fill=hex_color)
        rgb_value_label.config(text=f"RGB({mixed[0]}, {mixed[1]}, {mixed[2]})")

    def save_color():
        name = simpledialog.askstring("Color Name", "Enter a name for this color:", initialvalue="Color 1")
        if not name:
            return
        sectors_data = []
        for i in range(12):
            if i in locked_sectors:
                continue
            raw = inputs[i].get()
            rgb = parse_rgb_input(raw)
            if rgb:
                rgb_str = f"RGB({rgb[0]}, {rgb[1]}, {rgb[2]})"
                sectors_data.append({"color": rgb_str, "potency": potencies[i].get()})
        if not sectors_data:
            messagebox.showerror("Error", "No valid colors to save.")
            return
        result_rgb = calculate_mixed_rgb([(extract_rgb_tuple(s["color"]), s["potency"]) for s in sectors_data])
        color_entry = {"name": name, "sectors": sectors_data, "result": f"RGB({result_rgb[0]}, {result_rgb[1]}, {result_rgb[2]})"}

        saved = []
        if os.path.exists(TEMP_FILE):
            with open(TEMP_FILE, "r") as file:
                for line in file:
                    try: saved.append(json.loads(line))
                    except: continue
        if any(entry.get("name") == name for entry in saved if isinstance(entry, dict)):
            messagebox.showerror("Error", f"A color named '{name}' already exists.")
            return
        with open(TEMP_FILE, "a") as file:
            file.write(json.dumps(color_entry) + "\n")
        messagebox.showinfo("Saved", f"Color '{name}' saved!")

    def reset_all():
        for i in range(12):
            if i in locked_sectors:
                continue
            inputs[i].delete(0, tk.END)
            potencies[i].set(1)
            potency_labels[i].config(text="1")
            canvas.itemconfig(sectors[i], fill="white")
        update_center_color()

    def delete_temp_file():
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)

    def open_general_color_mixer(window):
        window.destroy()
        import general_color_mixer
        general_color_mixer.open_general_color_mixer()

    rgb_window = tk.Tk()
    rgb_window.title("RGB Color Mixer")
    rgb_window.configure(bg=bg)

    BUTTON_STYLE = {"bg": "#e0e0e0", "fg": "black", "font": font, "bd": 1, "relief": "raised", "padx": 8, "pady": 4}
    ENTRY_STYLE = {"bg": "white", "fg": "black", "font": font, "bd": 1, "relief": "solid"}

    tk.Label(rgb_window, text="RGB Color Mixer", font=(font_family, font_size + 6, "bold"), bg=bg, fg=fg).pack(pady=10)

    content_frame = tk.Frame(rgb_window, bg=bg)
    content_frame.pack()

    # === Wheel ===
    wheel_frame = tk.Frame(content_frame, bg=bg)
    wheel_frame.grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="n")

    canvas_size = 500
    canvas = tk.Canvas(wheel_frame, width=canvas_size, height=canvas_size, bg="white", highlightthickness=0)
    canvas.pack()

    center_x = center_y = canvas_size // 2
    outer_radius = 200
    center_radius = 65

    inputs, potencies, potency_labels, sectors = [], [], [], []
    locked_sectors = [5, 11]

    for i in range(12):
        arc = canvas.create_arc(center_x - outer_radius, center_y - outer_radius,
                                center_x + outer_radius, center_y + outer_radius,
                                start=i * 30, extent=30,
                                fill="black" if i in locked_sectors else "white",
                                outline="black", width=1)
        sectors.append(arc)

    center_circle = canvas.create_oval(center_x - center_radius, center_y - center_radius,
                                       center_x + center_radius, center_y + center_radius,
                                       fill="white", outline="black", width=1)
    canvas.tag_raise(center_circle)

    wheel_info = tk.Frame(wheel_frame, bg=bg)
    wheel_info.pack(pady=(10, 0))
    tk.Button(wheel_info, text="Save Color", command=save_color, **BUTTON_STYLE).pack(pady=(0, 5))
    tk.Button(wheel_info, text="Reset", command=reset_all, **BUTTON_STYLE).pack(pady=(0, 5))
    tk.Label(wheel_info, text="RGB", font=(font_family, font_size + 2, "bold"), bg=bg, fg=fg).pack()
    rgb_value_label = tk.Label(wheel_info, text="RGB(255, 255, 255)", font=font, bg=bg, fg=fg)
    rgb_value_label.pack()

    # === Grid ===
    controls_frame = tk.Frame(content_frame, bg=bg)
    controls_frame.grid(row=0, column=1, pady=(155, 0), sticky="n")
    editable_indexes = [i for i in range(12) if i not in locked_sectors]

    for idx, sector_index in enumerate(editable_indexes):
        row, col = idx // 5, idx % 5
        frame = tk.Frame(controls_frame, bg=bg, padx=4, pady=4)
        frame.grid(row=row * 3, column=col, padx=4, pady=4)

        tk.Label(frame, text=f"Sector {idx+1}", font=(font_family, font_size, "bold"), bg=bg, fg=fg).pack()

        entry = tk.Entry(frame, width=10, **ENTRY_STYLE)
        entry.pack()
        entry.bind("<Return>", lambda event, i=sector_index: update_sector(i))
        inputs.insert(sector_index, entry)

        p_frame = tk.Frame(frame, bg=bg)
        p_frame.pack(pady=1)

        tk.Button(p_frame, text="-", command=lambda i=sector_index: update_sector(i, False), **BUTTON_STYLE).pack(side=tk.LEFT)
        potency = tk.IntVar(value=1)
        potencies.insert(sector_index, potency)

        label = tk.Label(p_frame, text="1", font=(font_family, font_size), bg=bg, fg=fg, width=2)
        label.pack(side=tk.LEFT)
        potency_labels.insert(sector_index, label)

        tk.Button(p_frame, text="+", command=lambda i=sector_index: update_sector(i, True), **BUTTON_STYLE).pack(side=tk.LEFT)

    for i in locked_sectors:
        inputs.insert(i, None)
        potencies.insert(i, tk.IntVar(value=1))
        potency_labels.insert(i, None)

    # Load prefilled sectors if mixer_input.txt exists
    if os.path.exists(MIXER_INPUT_FILE):
        try:
            with open(MIXER_INPUT_FILE, "r") as file:
                for idx, line in enumerate(file.readlines()):
                    if idx >= 12:
                        break
                    parts = line.strip().split("|")
                    if len(parts) == 3 and parts[0] == "RGB":
                        color_str, potency = parts[1], int(parts[2])
                        rgb = parse_rgb_input(color_str)
                        if rgb and idx not in locked_sectors:
                            inputs[idx].insert(0, color_str)
                            potencies[idx].set(potency)
                            potency_labels[idx].config(text=str(potency))
                            hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
                            canvas.itemconfig(sectors[idx], fill=hex_color)
        except Exception as e:
            print("Error loading mixer input:", e)
        update_center_color()

    # Back Button
    tk.Button(rgb_window, text="Back", width=20, command=lambda: open_general_color_mixer(rgb_window), **BUTTON_STYLE).pack(pady=20)

    rgb_window.protocol("WM_DELETE_WINDOW", delete_temp_file)
    rgb_window.mainloop()

if __name__ == "__main__":
    open_rgb_page()

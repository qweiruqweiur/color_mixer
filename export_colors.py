import tkinter as tk
from tkinter import messagebox, filedialog
import os
import json
import subprocess
from PIL import Image, ImageTk

TEMP_FILE = "temp_saved_colors.txt"
SETTINGS_FILE = "appearance_settings.json"
SAVE_ICON_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/save.png"

# === Appearance ===
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
    settings = load_appearance()
    font_sizes = {"small": 10, "medium": 12, "large": 14, "extra large": 16}
    return settings["font_family"], font_sizes.get(settings["font_size"], 12), settings["theme"]

# === Load & Conversion ===
def load_saved_colors():
    if os.path.exists(TEMP_FILE):
        with open(TEMP_FILE, "r") as f:
            return [json.loads(line.strip()) for line in f if line.strip()]
    return []

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip("#")
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}".upper()

def rgb_to_cmyk(rgb):
    r, g, b = [x / 255 for x in rgb]
    k = 1 - max(r, g, b)
    if k == 1: return "CMYK(0, 0, 0, 100)"
    c = round((1 - r - k) / (1 - k) * 100)
    m = round((1 - g - k) / (1 - k) * 100)
    y = round((1 - b - k) / (1 - k) * 100)
    return f"CMYK({c}, {m}, {y}, {round(k * 100)})"

def convert_any_to_hex(color_str):
    try:
        if color_str.startswith("CMYK"):
            c, m, y, k = map(int, color_str[5:-1].split(","))
            c, m, y, k = c / 100, m / 100, y / 100, k / 100
            r = round(255 * (1 - c) * (1 - k))
            g = round(255 * (1 - m) * (1 - k))
            b = round(255 * (1 - y) * (1 - k))
            return rgb_to_hex((r, g, b))
        elif color_str.startswith("RGB"):
            return rgb_to_hex(eval(color_str[3:]))  # Assumes well-formed
        elif color_str.startswith("#"):
            return color_str
        else:
            return color_str  # Allow named colors
    except:
        return "white"

def calculate_mixed_rgb(components):
    total = sum(p for _, p in components)
    if total == 0:
        return (255, 255, 255)
    r = sum(hex_to_rgb(c)[0] * p for c, p in components) // total
    g = sum(hex_to_rgb(c)[1] * p for c, p in components) // total
    b = sum(hex_to_rgb(c)[2] * p for c, p in components) // total
    return (r, g, b)

# === Export Function ===
def export_color_to_file(name, sectors, fmt):
    mixed_rgb = calculate_mixed_rgb([(convert_any_to_hex(s["color"]), s["potency"]) for s in sectors])

    if fmt == "RGB":
        output = f"RGB{mixed_rgb}"
    elif fmt == "HEX":
        output = rgb_to_hex(mixed_rgb)
    elif fmt == "CMYK":
        output = rgb_to_cmyk(mixed_rgb)
    else:
        return

    path = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text Files", "*.txt")],
                                        title="Save Exported Color")
    if path:
        with open(path, "w") as f:
            f.write(json.dumps({"name": name, "sectors": sectors}) + "\n")
            f.write(output + "\n")
        messagebox.showinfo("Saved", f"Color saved to {path}")

# === Export Page ===
def open_export_colors_page():
    font_family, font_size, theme = get_font_settings()
    font = (font_family, font_size)
    bg = "#000000" if theme == "dark" else "white"
    fg = "white" if theme == "dark" else "black"

    saved_colors = load_saved_colors()
    color_names = [entry["name"] for entry in saved_colors]

    export_window = tk.Tk()
    export_window.title("Export Colors")
    export_window.geometry("950x700")
    export_window.configure(bg=bg)

    selected_name = tk.StringVar(export_window, value=color_names[0] if color_names else "")
    format_choice = tk.StringVar(export_window)

    # === Top Header ===
    header = tk.Frame(export_window, bg=bg)
    header.pack(padx=20, pady=20, anchor="nw")

    try:
        icon_img = Image.open(SAVE_ICON_PATH).resize((40, 40)).rotate(180)
        icon = ImageTk.PhotoImage(icon_img)
        tk.Label(header, image=icon, bg=bg).pack(side=tk.LEFT, padx=(0, 10))
    except:
        pass

    tk.Label(header, text="Select Saved Color:", font=font, bg=bg, fg=fg).pack(side=tk.LEFT)
    dropdown = tk.OptionMenu(header, selected_name, *color_names)
    dropdown.config(font=font)
    dropdown.pack(side=tk.LEFT, padx=10)

    # === Format Buttons ===
    format_frame = tk.Frame(export_window, bg=bg)
    format_frame.pack(padx=30, pady=(0, 10), anchor="w")

    tk.Label(format_frame, text="Export As:", font=font, bg=bg, fg=fg).pack(side=tk.LEFT)
    for fmt in ["RGB", "HEX", "CMYK"]:
        tk.Radiobutton(format_frame, text=fmt, variable=format_choice, value=fmt,
                       font=font, bg=bg, fg=fg, selectcolor="gray" if theme == "dark" else "white"
                       ).pack(side=tk.LEFT, padx=10)

    # === Sector Grid and Color Preview ===
    content_frame = tk.Frame(export_window, bg=bg)
    content_frame.pack()

    wheel = tk.Canvas(content_frame, width=400, height=400, bg="white", highlightthickness=0)
    wheel.grid(row=0, column=0, padx=20)
    center_x, center_y = 200, 200
    outer_radius, center_radius = 150, 50
    sectors = []
    for i in range(10):
        arc = wheel.create_arc(
            center_x - outer_radius, center_y - outer_radius,
            center_x + outer_radius, center_y + outer_radius,
            start=i * 36, extent=36,
            fill="white", outline="black"
        )
        sectors.append(arc)
    center_circle = wheel.create_oval(
        center_x - center_radius, center_y - center_radius,
        center_x + center_radius, center_y + center_radius,
        fill="white", outline="black"
    )
    wheel.tag_raise(center_circle)

    result_label = tk.Label(content_frame, text="", font=font, bg="white", fg="black")
    result_label.grid(row=1, column=0, pady=10)

    control_frame = tk.Frame(content_frame, bg=bg)
    control_frame.grid(row=0, column=1, padx=20)

    grid_labels = []
    for r in range(5):
        for c in range(2):
            lbl = tk.Label(control_frame, text=" ", width=20, height=2,
                           bg="white", relief="ridge", font=font)
            lbl.grid(row=r, column=c, padx=8, pady=4)
            grid_labels.append(lbl)

    # === Confirm Button Logic ===
    def confirm_selection():
        name = selected_name.get()
        entry = next((e for e in saved_colors if e["name"] == name), None)
        if not entry:
            return

        sectors_data = entry["sectors"]
        for i, label in enumerate(grid_labels):
            if i < len(sectors_data):
                color = sectors_data[i]["color"]
                potency = sectors_data[i]["potency"]
                hex_color = convert_any_to_hex(color)
                label.config(text=f"{color}\n(p{potency})", bg=hex_color)
                wheel.itemconfig(sectors[i], fill=hex_color)
            else:
                label.config(text=" ", bg="white")
                wheel.itemconfig(sectors[i], fill="white")

        mixed_rgb = calculate_mixed_rgb([(convert_any_to_hex(s["color"]), s["potency"]) for s in sectors_data])
        hex_color = rgb_to_hex(mixed_rgb)
        wheel.itemconfig(center_circle, fill=hex_color)

        if format_choice.get() == "RGB":
            result_label.config(text=f"RGB{mixed_rgb}")
        elif format_choice.get() == "HEX":
            result_label.config(text=hex_color)
        elif format_choice.get() == "CMYK":
            result_label.config(text=rgb_to_cmyk(mixed_rgb))

    def clear_all():
        if messagebox.askyesno("Clear", "Clear all saved colors?"):
            open(TEMP_FILE, "w").close()
            selected_name.set("")
            dropdown["menu"].delete(0, "end")

    def go_back():
        export_window.destroy()
        subprocess.run(["python", "external_data.py"])

    # === Buttons ===
    btn_style = {"bg": "#e0e0e0", "font": font, "bd": 1, "relief": "raised", "padx": 8, "pady": 4}
    button_bar = tk.Frame(export_window, bg=bg)
    button_bar.pack(pady=20)

    tk.Button(button_bar, text="Confirm", command=confirm_selection, **btn_style).pack(side=tk.LEFT, padx=10)
    tk.Button(button_bar, text="Export", command=lambda: export_color_to_file(
        selected_name.get(),
        next((e["sectors"] for e in saved_colors if e["name"] == selected_name.get()), []),
        format_choice.get()), **btn_style).pack(side=tk.LEFT, padx=10)
    tk.Button(button_bar, text="Clear Saved Colors", command=clear_all, **btn_style).pack(side=tk.LEFT, padx=10)
    tk.Button(export_window, text="Back", command=go_back, **btn_style).pack(pady=10)

    export_window.mainloop()

if __name__ == "__main__":
    open_export_colors_page()

import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import json
import re
import subprocess

SETTINGS_FILE = "appearance_settings.json"
TEMP_FILE = "temp_saved_colors.txt"

# === Compatible Named Colors ===
COMPATIBLE_COLORS_CMYK = {
    "red": (0, 100, 100, 0),
    "green": (100, 0, 100, 0),
    "blue": (100, 100, 0, 0),
    "yellow": (0, 0, 100, 0),
    "cyan": (100, 0, 0, 0),
    "magenta": (0, 100, 0, 0),
    "black": (0, 0, 0, 100),
    "white": (0, 0, 0, 0),
    "gray": (0, 0, 0, 50),
    "orange": (0, 50, 100, 0),
    "purple": (50, 100, 0, 0),
    "pink": (0, 25, 0, 0)
}

# === Appearance ===
def load_appearance():
    default = {"theme": "light", "font_size": "medium", "font_family": "Arial"}
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            try:
                return json.load(file)
            except:
                return default
    return default

def get_font_settings():
    settings = load_appearance()
    font_sizes = {"small": 10, "medium": 12, "large": 14, "extra large": 16}
    return (
        settings.get("font_family", "Arial"),
        font_sizes.get(settings.get("font_size", "medium"), 12),
        settings.get("theme", "light")
    )

# === Parse + Convert ===
def parse_cmyk_input(text):
    text = text.lower().strip()
    if text in COMPATIBLE_COLORS_CMYK:
        return COMPATIBLE_COLORS_CMYK[text]
    match = re.match(r"\(?\s*(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\s*\)?", text)
    if match:
        c, m, y, k = map(int, match.groups())
        if all(0 <= val <= 100 for val in (c, m, y, k)):
            return (c, m, y, k)
    return None

def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c / 100) * (1 - k / 100)
    g = 255 * (1 - m / 100) * (1 - k / 100)
    b = 255 * (1 - y / 100) * (1 - k / 100)
    return (int(r), int(g), int(b))

def calculate_mixed_cmyk(components):
    total = sum(p for _, p in components)
    if total == 0:
        return (0, 0, 0, 0)
    sum_c = sum(c[0] * p for c, p in components)
    sum_m = sum(c[1] * p for c, p in components)
    sum_y = sum(c[2] * p for c, p in components)
    sum_k = sum(c[3] * p for c, p in components)
    return (
        round(sum_c / total),
        round(sum_m / total),
        round(sum_y / total),
        round(sum_k / total)
    )

def load_saved_colors():
    if os.path.exists(TEMP_FILE):
        with open(TEMP_FILE, "r") as f:
            return [json.loads(line.strip()) for line in f if line.strip()]
    return []

# === Main Page ===
def open_cmyk_page():
    font_family, font_size, theme = get_font_settings()
    font = (font_family, font_size)
    bg = "#000000" if theme == "dark" else "white"
    fg = "white" if theme == "dark" else "black"

    window = tk.Tk()
    window.title("CMYK Color Mixer")
    window.configure(bg=bg)

    tk.Label(window, text="CMYK Color Mixer", font=("Arial", 18, "bold"), bg=bg, fg=fg).pack(pady=10)

    content = tk.Frame(window, bg=bg)
    content.pack()

    # === Wheel ===
    wheel = tk.Frame(content, bg=bg)
    wheel.grid(row=0, column=0, padx=30)

    canvas_size = 500
    canvas = tk.Canvas(wheel, width=canvas_size, height=canvas_size, bg="white", highlightthickness=0)
    canvas.pack()

    center = canvas_size // 2
    outer_r = 200
    center_r = 65
    sectors = []
    locked = [5, 11]

    for i in range(12):
        angle = i * 30
        arc = canvas.create_arc(
            center - outer_r, center - outer_r,
            center + outer_r, center + outer_r,
            start=angle, extent=30,
            fill="black" if i in locked else "white",
            outline="black"
        )
        sectors.append(arc)

    center_circle = canvas.create_oval(center - center_r, center - center_r,
                                       center + center_r, center + center_r,
                                       fill="white", outline="black")
    canvas.tag_raise(center_circle)

    # === Controls ===
    right = tk.Frame(content, bg=bg)
    right.grid(row=0, column=1, pady=(155, 0))

    inputs, potencies, potency_labels = [], [], []
    editable = [i for i in range(12) if i not in locked]

    def update_sector(i, inc=None):
        if i in locked: return
        value = inputs[i].get()
        parsed = parse_cmyk_input(value)
        if not parsed:
            messagebox.showerror("Error", "Format: CMYK or (C,M,Y,K) with 0–100")
            return
        p = potencies[i].get()
        if inc is True and p < 50: potencies[i].set(p + 1)
        elif inc is False and p > 1: potencies[i].set(p - 1)
        r, g, b = cmyk_to_rgb(*parsed)
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.itemconfig(sectors[i], fill=hex_color)
        potency_labels[i].config(text=str(potencies[i].get()))
        update_center_color()

    def update_center_color():
        comps = []
        for i in range(12):
            if i in locked: continue
            text = inputs[i].get()
            parsed = parse_cmyk_input(text)
            if parsed:
                comps.append((parsed, potencies[i].get()))
        final = calculate_mixed_cmyk(comps)
        r, g, b = cmyk_to_rgb(*final)
        canvas.itemconfig(center_circle, fill=f"#{r:02x}{g:02x}{b:02x}")
        result_label.config(text=f"CMYK({final[0]}, {final[1]}, {final[2]}, {final[3]})")

    for idx, sec in enumerate(editable):
        row = idx // 5
        col = idx % 5
        frame = tk.Frame(right, bg=bg)
        frame.grid(row=row * 3, column=col, padx=5, pady=5)

        tk.Label(frame, text=f"Sector {idx+1}", font=(font_family, font_size, "bold"), bg=bg, fg=fg).pack()
        entry = tk.Entry(frame, width=12, font=font)
        entry.pack()
        entry.bind("<Return>", lambda e, i=sec: update_sector(i))
        inputs.insert(sec, entry)

        p = tk.IntVar(value=1)
        potencies.insert(sec, p)

        pf = tk.Frame(frame, bg=bg)
        pf.pack()
        tk.Button(pf, text="-", command=lambda i=sec: update_sector(i, False), font=font).pack(side=tk.LEFT)
        lbl = tk.Label(pf, text="1", font=font, bg=bg, fg=fg, width=2)
        lbl.pack(side=tk.LEFT)
        potency_labels.insert(sec, lbl)
        tk.Button(pf, text="+", command=lambda i=sec: update_sector(i, True), font=font).pack(side=tk.LEFT)

    for i in locked:
        inputs.insert(i, None)
        potencies.insert(i, tk.IntVar(value=1))
        potency_labels.insert(i, None)

    # === Bottom Info ===
    bottom = tk.Frame(wheel, bg=bg)
    bottom.pack(pady=10)
    result_label = tk.Label(bottom, text="CMYK(0, 0, 0, 0)", font=font, bg=bg, fg=fg)
    result_label.pack()

    def reset_all():
        for i in range(12):
            if i in locked: continue
            inputs[i].delete(0, tk.END)
            potencies[i].set(1)
            potency_labels[i].config(text="1")
            canvas.itemconfig(sectors[i], fill="white")
        canvas.itemconfig(center_circle, fill="white")
        result_label.config(text="CMYK(0, 0, 0, 0)")

    def save_color():
        name = simpledialog.askstring("Save Color", "Enter a name:", initialvalue="Color 1")
        if not name: return
        all_saved = load_saved_colors()
        if any(entry.get("name") == name for entry in all_saved):
            messagebox.showerror("Duplicate", f"A color named '{name}' already exists.")
            return
        sectors_data = []
        for i in range(12):
            if i in locked: continue
            text = inputs[i].get()
            parsed = parse_cmyk_input(text)
            if parsed:
                cmyk_str = f"CMYK({parsed[0]}, {parsed[1]}, {parsed[2]}, {parsed[3]})"
                sectors_data.append({"color": cmyk_str, "potency": potencies[i].get()})
        if not sectors_data:
            messagebox.showerror("Empty", "No sectors have valid input.")
            return
        with open(TEMP_FILE, "a") as f:
            f.write(json.dumps({"name": name, "sectors": sectors_data}) + "\n")
        messagebox.showinfo("Saved", f"Color '{name}' saved!")

    def go_back():
        window.destroy()
        subprocess.run(["python", "general_color_mixer.py"])

    # Footer
    footer = tk.Frame(window, bg=bg)
    footer.pack(pady=20)
    tk.Button(footer, text="Save Color", command=save_color, font=font).pack(side=tk.LEFT, padx=10)
    tk.Button(footer, text="Reset", command=reset_all, font=font).pack(side=tk.LEFT, padx=10)
    tk.Button(footer, text="Back", command=go_back, font=font).pack(side=tk.LEFT, padx=10)

    window.mainloop()

if __name__ == "__main__":
    open_cmyk_page()

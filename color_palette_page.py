import tkinter as tk
from tkinter import messagebox
import re
import os

# Named color support
COMPATIBLE_COLORS_HEX = {
    "red": "#FF0000",
    "orange": "#FFA500",
    "yellow": "#FFFF00",
    "green": "#008000",
    "blue": "#0000FF",
    "purple": "#800080",
    "pink": "#FFC0CB",
    "black": "#000000",
    "brown": "#A52A2A",
    "white": "#FFFFFF",
}

PALETTE_SAVE_FILE = "saved_palette.txt"

# CMYK to HEX via RGB
def cmyk_to_rgb(c, m, y, k):
    c /= 100
    m /= 100
    y /= 100
    k /= 100
    r = round(255 * (1 - c) * (1 - k))
    g = round(255 * (1 - m) * (1 - k))
    b = round(255 * (1 - y) * (1 - k))
    return f"#{r:02X}{g:02X}{b:02X}"

# === Color Parser ===
def parse_color_input(text):
    """Parse input into a valid HEX color string."""
    text = text.strip().lower()

    # Named color
    if text in COMPATIBLE_COLORS_HEX:
        return COMPATIBLE_COLORS_HEX[text]

    # HEX code
    hex_code = text.lstrip("#")
    if re.fullmatch(r"[0-9a-f]{6}", hex_code):
        return f"#{hex_code.upper()}"

    # RGB tuple
    rgb_match = re.match(r"\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", text)
    if rgb_match:
        r, g, b = map(int, rgb_match.groups())
        if all(0 <= v <= 255 for v in (r, g, b)):
            return f"#{r:02X}{g:02X}{b:02X}"

    # CMYK tuple
    cmyk_match = re.match(r"\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", text)
    if cmyk_match:
        c, m, y, k = map(int, cmyk_match.groups())
        if all(0 <= val <= 100 for val in (c, m, y, k)):
            return cmyk_to_rgb(c, m, y, k)

    return None

# === Main App ===
def open_color_palette_page():
    def apply_color(index):
        color_text = entries[index].get()
        hex_color = parse_color_input(color_text)
        if hex_color:
            color_boxes[index].config(bg=hex_color)
        else:
            messagebox.showerror(
                "Invalid Input",
                "Enter a valid color name, hex code (#RRGGBB), RGB value (R, G, B), or CMYK (C, M, Y, K)"
            )

    def save_palette():
        colors = [box.cget("bg").upper() for box in color_boxes]
        with open(PALETTE_SAVE_FILE, "w") as f:
            for color in colors:
                f.write(color + "\n")
        messagebox.showinfo("Saved", "Palette saved successfully!")

    def go_back():
        window.destroy()
        import tools
        tools.open_tools_page()

    # === GUI Setup ===
    window = tk.Tk()
    window.title("Color Palette")
    window.configure(bg="white")

    BUTTON_STYLE = {
        "bg": "#e0e0e0",
        "fg": "black",
        "font": ("Arial", 11, "bold"),
        "bd": 1,
        "relief": "raised",
        "padx": 8,
        "pady": 4
    }
    ENTRY_STYLE = {
        "bg": "white",
        "fg": "black",
        "font": ("Arial", 10),
        "bd": 1,
        "relief": "solid"
    }

    # Title
    tk.Label(window, text="Color Palette", font=("Arial", 18, "bold"), bg="white", fg="black").pack(pady=(10, 5))

    # Save Button
    tk.Button(window, text="Save Palette", command=save_palette, **BUTTON_STYLE).pack(pady=(0, 10))

    # === Color Grid ===
    grid_frame = tk.Frame(window, bg="white")
    grid_frame.pack()

    entries = []
    color_boxes = []

    for row in range(2):  # 2 rows
        for col in range(5):  # 5 columns
            index = row * 5 + col

            box_frame = tk.Frame(grid_frame, bg="white", padx=8, pady=8)
            box_frame.grid(row=row * 2, column=col, padx=5, pady=5)

            if row == 0:
                entry = tk.Entry(box_frame, width=12, **ENTRY_STYLE)
                entry.pack(pady=(0, 5))
            else:
                entry = None  # Placeholder, will define below

            box = tk.Label(box_frame, bg="white", width=12, height=6, relief="ridge", bd=2)
            box.pack()

            if row == 1:
                entry = tk.Entry(box_frame, width=12, **ENTRY_STYLE)
                entry.pack(pady=(5, 0))

            entry.bind("<Return>", lambda event, i=index: apply_color(i))

            entries.append(entry)
            color_boxes.append(box)

    # Back Button
    tk.Button(window, text="Back", width=20, command=go_back, **BUTTON_STYLE).pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    open_color_palette_page()

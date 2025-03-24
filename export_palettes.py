import tkinter as tk
from tkinter import messagebox, filedialog
import os
import json
import subprocess
from PIL import Image, ImageTk

TEMP_PALETTE_FILE = "temp_saved_palettes.txt"
SAVE_ICON_PATH = "/Users/rohanshankar/Documents/Coding/CompSciHL/color_mixer/save.png"

def load_saved_palettes():
    if os.path.exists(TEMP_PALETTE_FILE):
        with open(TEMP_PALETTE_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def rgb_to_hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}".upper()

def rgb_to_cmyk(rgb):
    r, g, b = rgb[0]/255, rgb[1]/255, rgb[2]/255
    k = 1 - max(r, g, b)
    if k == 1:
        return "CMYK(0, 0, 0, 100)"
    c = (1 - r - k) / (1 - k) * 100
    m = (1 - g - k) / (1 - k) * 100
    y = (1 - b - k) / (1 - k) * 100
    return f"CMYK({round(c)}, {round(m)}, {round(y)}, {round(k * 100)})"

def format_color_label(rgb, fmt):
    if fmt == "RGB":
        return f"RGB({rgb[0]}, {rgb[1]}, {rgb[2]})"
    elif fmt == "HEX":
        return rgb_to_hex(rgb)
    elif fmt == "CMYK":
        return rgb_to_cmyk(rgb)
    return ""

def show_palette():
    name = palette_var.get()
    fmt = format_var.get()
    if not name or name == "No saved palettes":
        messagebox.showerror("Error", "Please select a palette.")
        return
    if not fmt:
        messagebox.showerror("Error", "Please select a format.")
        return

    palettes = load_saved_palettes()
    selected = next((p for p in palettes if p["name"] == name), None)
    if not selected:
        messagebox.showerror("Error", "Palette not found.")
        return

    colors = selected["colors"]
    for i, cell in enumerate(color_cells):
        if i < len(colors):
            rgb = colors[i]["RGB"]
            hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
            cell.config(bg=hex_color)
            label = format_color_label(rgb, fmt)
            if i < 5:
                top_labels[i].config(text=label)
            else:
                bottom_labels[i - 5].config(text=label)
        else:
            cell.config(bg="white")
            if i < 5:
                top_labels[i].config(text="")
            else:
                bottom_labels[i - 5].config(text="")

def save_palette():
    name = palette_var.get()
    fmt = format_var.get()
    if not name or name == "No saved palettes":
        messagebox.showerror("Error", "Please select a palette.")
        return
    if not fmt:
        messagebox.showerror("Error", "Please select a format.")
        return

    palettes = load_saved_palettes()
    selected = next((p for p in palettes if p["name"] == name), None)
    if not selected:
        messagebox.showerror("Error", "Palette not found.")
        return

    converted = []
    for c in selected["colors"]:
        rgb = c["RGB"]
        converted.append(format_color_label(rgb, fmt))

    path = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text Files", "*.txt")],
                                        initialfile=name,
                                        title="Save Palette")
    if path:
        with open(path, "w") as f:
            f.write(name + "\n")
            for line in converted:
                f.write(line + "\n")
        messagebox.showinfo("Success", f"Palette '{name}' exported to:\n{path}")

def clear_saved_palettes():
    if messagebox.askyesno("Confirm", "Are you sure you want to delete all saved palettes?"):
        open(TEMP_PALETTE_FILE, "w").close()
        palette_var.set("No saved palettes")
        palette_dropdown["menu"].delete(0, "end")
        palette_dropdown["menu"].add_command(label="No saved palettes", command=tk._setit(palette_var, "No saved palettes"))

def go_back():
    export_window.destroy()
    subprocess.Popen(["python", "external_data.py"])

def open_export_palettes_page():
    global export_window, palette_var, format_var, palette_dropdown, color_cells, top_labels, bottom_labels

    export_window = tk.Tk()
    export_window.title("Export Palettes")
    export_window.configure(bg="white")

    BUTTON_STYLE = {
        "bg": "#e0e0e0", "fg": "black", "font": ("Arial", 11, "bold"),
        "bd": 1, "relief": "raised", "padx": 8, "pady": 4
    }

    # --- Top Bar ---
    top_frame = tk.Frame(export_window, bg="white")
    top_frame.pack(padx=20, pady=10, anchor="nw")

    try:
        save_img = Image.open(SAVE_ICON_PATH).resize((40, 40)).rotate(180)
        save_icon = ImageTk.PhotoImage(save_img)
        icon_label = tk.Label(top_frame, image=save_icon, bg="white")
        icon_label.image = save_icon
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
    except Exception as e:
        print("Save icon load failed:", e)

    tk.Label(top_frame, text="Select Saved Palette:", font=("Arial", 11), bg="white", fg="black").pack(side=tk.LEFT)

    saved = load_saved_palettes()
    names = [p["name"] for p in saved]
    default_name = names[0] if names else "No saved palettes"

    palette_var = tk.StringVar()
    palette_var.set(default_name)

    palette_dropdown = tk.OptionMenu(top_frame, palette_var, *names if names else ["No saved palettes"])
    palette_dropdown.config(width=30)
    palette_dropdown.pack(side=tk.LEFT, padx=10)

    tk.Button(top_frame, text="Confirm", command=show_palette, **BUTTON_STYLE).pack(side=tk.LEFT, padx=5)
    tk.Button(top_frame, text="Download", command=save_palette, **BUTTON_STYLE).pack(side=tk.LEFT, padx=5)

    # --- Format Selection ---
    format_frame = tk.Frame(export_window, bg="white")
    format_frame.pack(anchor="w", padx=30)

    tk.Label(format_frame, text="Select Format:", font=("Arial", 11), bg="white", fg="black").pack(side=tk.LEFT)
    format_var = tk.StringVar()
    for fmt in ["RGB", "HEX", "CMYK"]:
        tk.Radiobutton(format_frame, text=fmt, variable=format_var, value=fmt,
                       bg="white", fg="black", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)

    # --- Labels + Color Grid ---
    grid_wrapper = tk.Frame(export_window, bg="white")
    grid_wrapper.pack(pady=20)

    # Top row of labels
    top_labels = []
    label_row_top = tk.Frame(grid_wrapper, bg="white")
    label_row_top.pack()
    for _ in range(5):
        lbl = tk.Label(label_row_top, text="", font=("Arial", 9), bg="white", fg="black", width=18)
        lbl.pack(side=tk.LEFT, padx=6)
        top_labels.append(lbl)

    # Color grid (2x5)
    color_cells = []
    grid_frame = tk.Frame(grid_wrapper, bg="white")
    grid_frame.pack()
    for row in range(2):
        for col in range(5):
            frame = tk.Frame(grid_frame, width=80, height=80, bg="white", highlightthickness=1, highlightbackground="black")
            frame.grid(row=row, column=col, padx=10, pady=10)
            label = tk.Label(frame, bg="white", width=12, height=6, relief="solid", bd=1)
            label.pack(fill="both", expand=True)
            color_cells.append(label)

    # Bottom row of labels
    bottom_labels = []
    label_row_bottom = tk.Frame(grid_wrapper, bg="white")
    label_row_bottom.pack()
    for _ in range(5):
        lbl = tk.Label(label_row_bottom, text="", font=("Arial", 9), bg="white", fg="black", width=18)
        lbl.pack(side=tk.LEFT, padx=6)
        bottom_labels.append(lbl)

    # --- Bottom Buttons ---
    bottom_frame = tk.Frame(export_window, bg="white")
    bottom_frame.pack(pady=20)

    tk.Button(bottom_frame, text="Clear Saved Palettes", command=clear_saved_palettes,
              fg="red", font=("Arial", 11, "bold")).pack(pady=5)
    tk.Button(bottom_frame, text="Back", command=go_back, width=20, **BUTTON_STYLE).pack(pady=5)

    export_window.mainloop()

if __name__ == "__main__":
    open_export_palettes_page()

import tkinter as tk
from tkinter import messagebox
import re
import os
import json

TEMP_PALETTE_FILE = "temp_saved_palettes.txt"

# Supported color formats
def parse_color_input(input_text):
    """Parse input as RGB, HEX, or CMYK and convert to RGB for display."""
    match_hex = re.match(r"^#([0-9a-fA-F]{6})$", input_text)
    if match_hex:
        hex_value = match_hex.group(1)
        return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))

    match_rgb = re.match(r"\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", input_text)
    if match_rgb:
        r, g, b = map(int, match_rgb.groups())
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            return (r, g, b)

    match_cmyk = re.match(r"\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", input_text)
    if match_cmyk:
        c, m, y, k = map(int, match_cmyk.groups())
        if 0 <= c <= 100 and 0 <= m <= 100 and 0 <= y <= 100 and 0 <= k <= 100:
            r = int(255 * (1 - c / 100) * (1 - k / 100))
            g = int(255 * (1 - m / 100) * (1 - k / 100))
            b = int(255 * (1 - y / 100) * (1 - k / 100))
            return (r, g, b)

    return None  # Invalid format

# Load Saved Palettes
def load_saved_palettes():
    """Loads saved palettes from the temp file."""
    if os.path.exists(TEMP_PALETTE_FILE):
        with open(TEMP_PALETTE_FILE, "r") as file:
            try:
                return json.load(file)  # Load as structured data
            except json.JSONDecodeError:
                return []  # Return empty list if corrupted
    return []

# Clear Palettes (Triggered when the Home Page Closes)
def clear_temp_palettes():
    """Clears the temporary palettes file when the home page closes."""
    if os.path.exists(TEMP_PALETTE_FILE):
        open(TEMP_PALETTE_FILE, "w").close()  # Clears the file

# Generate next available palette name
def get_next_palette_name(saved_palettes):
    """Finds the next available palette number."""
    existing_numbers = {int(palette["name"].split(" ")[1]) for palette in saved_palettes if palette["name"].startswith("Palette")}

    num = 1
    while num in existing_numbers:
        num += 1
    return f"Palette {num}"

# Main function to open the Color Palette Page
def open_color_palette_page():
    def update_color(index):
        """Update the color box based on the input."""
        input_text = inputs[index].get()
        color_rgb = parse_color_input(input_text)
        if color_rgb:
            color_boxes[index].config(bg=f"#{color_rgb[0]:02x}{color_rgb[1]:02x}{color_rgb[2]:02x}")
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid color in RGB, HEX, or CMYK format.")

    def save_palette():
        """Saves the current palette to `temp_saved_palettes.txt` in structured format."""
        colors = []
        for i in range(10):
            color_text = inputs[i].get()
            if color_text:
                color_rgb = parse_color_input(color_text)
                if color_rgb:
                    colors.append({"RGB": (color_rgb[0], color_rgb[1], color_rgb[2])})

        if not colors:
            messagebox.showerror("Error", "No valid colors to save.")
            return

        # Load existing palettes
        saved_palettes = load_saved_palettes()
        palette_name = get_next_palette_name(saved_palettes)

        # Store as structured JSON data
        saved_palettes.append({"name": palette_name, "colors": colors})
        with open(TEMP_PALETTE_FILE, "w") as file:
            json.dump(saved_palettes, file, indent=2)

        messagebox.showinfo("Saved!", f"{palette_name} saved successfully!")

    def go_back():
        """Close the Palette Page and open the Tools Page."""
        palette_window.destroy()
        import tools
        tools.open_tools_page()

    # GUI Setup
    palette_window = tk.Tk()
    palette_window.title("Color Palette")

    # Palette Title
    tk.Label(palette_window, text="Color Palette", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

    # Color Boxes and Inputs
    global color_boxes, inputs
    color_boxes = []
    inputs = []

    for i in range(10):
        row_frame = tk.Frame(palette_window)
        row_frame.grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")

        color_box = tk.Label(row_frame, width=10, height=2, bg="white", relief="solid")
        color_box.pack(side=tk.LEFT, padx=5)
        color_boxes.append(color_box)

        input_field = tk.Entry(row_frame, width=20)
        input_field.pack(side=tk.LEFT)
        inputs.append(input_field)

        tk.Button(row_frame, text="Enter", command=lambda idx=i: update_color(idx)).pack(side=tk.LEFT, padx=5)

    # Save Palette Button (Now Functional)
    tk.Button(palette_window, text="Save Palette", command=save_palette, width=15).grid(row=12, column=0, pady=10, columnspan=2)

    # Back Button
    tk.Button(palette_window, text="Back", command=go_back).grid(row=13, column=0, pady=10, columnspan=2)

    palette_window.mainloop()

# Run Color Palette Page
if __name__ == "__main__":
    open_color_palette_page()

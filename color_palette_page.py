import tkinter as tk
from tkinter import messagebox
import re

# Supported color formats
def parse_color_input(input_text):
    """Parse input as RGB, HEX, or CMYK and convert to RGB for display."""
    # Check for HEX format
    match_hex = re.match(r"^#([0-9a-fA-F]{6})$", input_text)
    if match_hex:
        hex_value = match_hex.group(1)
        return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))

    # Check for RGB format (e.g., (255, 0, 0))
    match_rgb = re.match(r"\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", input_text)
    if match_rgb:
        r, g, b = map(int, match_rgb.groups())
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            return (r, g, b)

    # Check for CMYK format (e.g., (0, 100, 100, 0))
    match_cmyk = re.match(r"\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", input_text)
    if match_cmyk:
        c, m, y, k = map(int, match_cmyk.groups())
        if 0 <= c <= 100 and 0 <= m <= 100 and 0 <= y <= 100 and 0 <= k <= 100:
            r = int(255 * (1 - c / 100) * (1 - k / 100))
            g = int(255 * (1 - m / 100) * (1 - k / 100))
            b = int(255 * (1 - y / 100) * (1 - k / 100))
            return (r, g, b)

    # If none match, return None
    return None

# Main function to open the Color Palette Page
def open_color_palette_page():
    def update_color(index):
        """Update the color box based on the input."""
        input_text = inputs[index].get()
        color_rgb = parse_color_input(input_text)
        if color_rgb:
            # Update the color box background with the parsed color
            color_boxes[index].config(bg=f"#{color_rgb[0]:02x}{color_rgb[1]:02x}{color_rgb[2]:02x}")
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid color in RGB, HEX, or CMYK format.")
    
    def go_back():
        """Close the General Color Mixer and open the Tools Page."""
        palette_window.destroy()
        import tools
        tools.open_tools_page()

    # GUI Setup
    palette_window = tk.Tk()
    palette_window.title("Color Palette")

    # Palette Title
    tk.Label(palette_window, text="Color Palette", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

    # Color Boxes and Inputs
    color_boxes = []
    inputs = []

    for i in range(10):
        # Row for each color box and input
        row_frame = tk.Frame(palette_window)
        row_frame.grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")

        # Color box
        color_box = tk.Label(row_frame, width=10, height=2, bg="white", relief="solid")
        color_box.pack(side=tk.LEFT, padx=5)
        color_boxes.append(color_box)

        # Input field
        input_field = tk.Entry(row_frame, width=20)
        input_field.pack(side=tk.LEFT)
        inputs.append(input_field)

        # Submit button
        tk.Button(row_frame, text="Enter", command=lambda idx=i: update_color(idx)).pack(side=tk.LEFT, padx=5)

    # Save Button (non-functional for now)
    tk.Button(palette_window, text="Save Palette", state="disabled", width=15).grid(row=12, column=0, pady=10, columnspan=2)

    # Back Button
    tk.Button(palette_window, text="Back", command=go_back).grid(row=13, column=0, pady=10, columnspan=2)

    palette_window.mainloop()

# Run Color Palette Page
if __name__ == "__main__":
    open_color_palette_page()


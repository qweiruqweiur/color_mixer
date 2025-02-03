import tkinter as tk
from tkinter import messagebox
import re
import subprocess

# Supported color names and their HEX equivalents
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

# Parse user input for HEX or color name
def parse_hex_input(input_text):
    # Check if it's a valid HEX value
    match = re.match(r"^#([0-9a-fA-F]{6})$", input_text)
    if match:
        hex_value = match.group(1)
        return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))
    # Check if it's a supported color name
    if input_text.lower() in COMPATIBLE_COLORS_HEX:
        hex_value = COMPATIBLE_COLORS_HEX[input_text.lower()].lstrip("#")
        return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))
    return None

# Calculate the mixed color from all inputs
def calculate_mixed_hex(colors_and_potencies):
    red_sum = green_sum = blue_sum = total_potency = 0
    for color, potency in colors_and_potencies:
        red_sum += color[0] * potency
        green_sum += color[1] * potency
        blue_sum += color[2] * potency
        total_potency += potency
    if total_potency == 0:
        return (255, 255, 255)  # Default to white if no colors
    avg_red = red_sum // total_potency
    avg_green = green_sum // total_potency
    avg_blue = blue_sum // total_potency
    return avg_red, avg_green, avg_blue

# Main function to open the HEX page
def open_hex_page():
    def update_cell(index, increase=None):
        # Get user input and parse it
        hex_input = inputs[index].get()
        rgb_values = parse_hex_input(hex_input)
        if rgb_values:
            # Handle potency adjustment
            if increase is True and potencies[index].get() < 5:  # Increase potency
                potencies[index].set(potencies[index].get() + 1)
            elif increase is False and potencies[index].get() > 1:  # Decrease potency
                potencies[index].set(potencies[index].get() - 1)

            # Update cell background color
            cells[index].config(bg=f"#{rgb_values[0]:02x}{rgb_values[1]:02x}{rgb_values[2]:02x}")
            potency_labels[index].config(text=f"{potencies[index].get()}")
            update_center_color()
        else:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid color name or HEX value (e.g., red or #FF5733)."
            )

    def update_center_color():
        # Calculate mixed color from all inputs
        colors_and_potencies = [
            (parse_hex_input(inputs[i].get()), potencies[i].get())
            for i in range(10)
            if parse_hex_input(inputs[i].get())
        ]
        mixed_rgb = calculate_mixed_hex(colors_and_potencies)
        mixed_hex = f"#{mixed_rgb[0]:02x}{mixed_rgb[1]:02x}{mixed_rgb[2]:02x}"
        center_color_label.config(bg=mixed_hex)
        center_hex_label.config(text=mixed_hex)
        
    def go_back():
        """Close the current window and open the General Color Mixer."""
        hex_window.destroy()  # Close the RGB page
        subprocess.run(["python", "general_color_mixer.py"])  # Open the General Color Mixer

    # GUI Setup
    hex_window = tk.Tk()
    hex_window.title("HEX Color Mixer")

    # Final Color Display
    center_frame = tk.Frame(hex_window)
    center_frame.grid(row=0, column=0, padx=10, pady=10)

    center_color_label = tk.Label(center_frame, text=" ", width=20, height=10, bg="white")
    center_color_label.pack()

    center_hex_label = tk.Label(center_frame, text="#FFFFFF")
    center_hex_label.pack(pady=5)

    # Color Wheel and Inputs
    wheel_frame = tk.Frame(hex_window)
    wheel_frame.grid(row=0, column=1, padx=10, pady=10)

    cells = []
    inputs = []
    potencies = []
    potency_labels = []

    for i in range(10):
        frame = tk.Frame(wheel_frame)
        frame.grid(row=i // 5, column=i % 5, padx=5, pady=5)

        # Display area
        cell = tk.Label(frame, width=10, height=5, bg="white")
        cell.pack()
        cells.append(cell)

        # Input field
        input_field = tk.Entry(frame, width=15)
        input_field.pack()
        inputs.append(input_field)
        input_field.bind("<Return>", lambda event, idx=i: update_cell(idx))

        # Potency slider
        potency = tk.IntVar(value=1)
        potencies.append(potency)

        # "+" and "-" Buttons
        plus_button = tk.Button(frame, text="+", command=lambda idx=i: update_cell(idx, True))
        plus_button.pack(side=tk.LEFT, padx=2)

        minus_button = tk.Button(frame, text="-", command=lambda idx=i: update_cell(idx, False))
        minus_button.pack(side=tk.RIGHT, padx=2)

        # Potency label
        potency_label = tk.Label(frame, text="1")
        potency_label.pack()
        potency_labels.append(potency_label)

    # Back Button
    back_button = tk.Button(hex_window, text="Back", command=go_back)
    back_button.grid(row=1, column=0, columnspan=2, pady=10)

    hex_window.mainloop()

# Run HEX Page
if __name__ == "__main__":
    open_hex_page()

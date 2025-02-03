import tkinter as tk
from tkinter import messagebox
import re
import subprocess


# Supported color names and their RGB equivalents
COMPATIBLE_COLORS_RGB = {
    "red": (255, 0, 0),
    "orange": (255, 165, 0),
    "yellow": (255, 255, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 255),
    "purple": (128, 0, 128),
    "pink": (255, 192, 203),
    "black": (0, 0, 0),
    "brown": (165, 42, 42),
    "white": (255, 255, 255),
}

# Parse user input for RGB or color name
def parse_rgb_input(input_text):
    # Check if it's a supported color name
    if input_text.lower() in COMPATIBLE_COLORS_RGB:
        return COMPATIBLE_COLORS_RGB[input_text.lower()]
    # Check if it's an RGB value in the format (R, G, B)
    match = re.match(r"\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", input_text)
    if match:
        r, g, b = map(int, match.groups())
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            return r, g, b
    return None

# Calculate the mixed color from all inputs
def calculate_mixed_rgb(colors_and_potencies):
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

# Main function to open the RGB page
def open_rgb_page():
    def update_cell(index, increase=None):
        # Get user input and parse it
        rgb_input = inputs[index].get()
        rgb_values = parse_rgb_input(rgb_input)
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
                "Please enter a valid color name or RGB value (e.g., red or (255, 0, 0))."
            )

    def update_center_color():
        # Calculate mixed color from all inputs
        colors_and_potencies = [
            (parse_rgb_input(inputs[i].get()), potencies[i].get())
            for i in range(10)
            if parse_rgb_input(inputs[i].get())
        ]
        mixed_rgb = calculate_mixed_rgb(colors_and_potencies)
        mixed_rgb_str = f"RGB({mixed_rgb[0]}, {mixed_rgb[1]}, {mixed_rgb[2]})"
        center_color_label.config(bg=f"#{mixed_rgb[0]:02x}{mixed_rgb[1]:02x}{mixed_rgb[2]:02x}")
        center_rgb_label.config(text=mixed_rgb_str)
        
    def go_back():
        """Close the current window and open the General Color Mixer."""
        rgb_window.destroy()  # Close the RGB page
        subprocess.run(["python", "general_color_mixer.py"])  # Open the General Color Mixer


    # GUI Setup
    rgb_window = tk.Tk()
    rgb_window.title("RGB Color Mixer")

    # Final Color Display
    center_frame = tk.Frame(rgb_window)
    center_frame.grid(row=0, column=0, padx=10, pady=10)

    center_color_label = tk.Label(center_frame, text=" ", width=20, height=10, bg="white")
    center_color_label.pack()

    center_rgb_label = tk.Label(center_frame, text="RGB(255, 255, 255)")
    center_rgb_label.pack(pady=5)

    # Color Wheel and Inputs
    wheel_frame = tk.Frame(rgb_window)
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
    back_button = tk.Button(rgb_window, text="Back", command=go_back)
    back_button.grid(row=1, column=0, columnspan=2, pady=10)

    rgb_window.mainloop()

# Run RGB Page
if __name__ == "__main__":
    open_rgb_page()

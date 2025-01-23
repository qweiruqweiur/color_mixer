import tkinter as tk
from tkinter import messagebox
import re

# Define compatible colors
COMPATIBLE_COLORS = {
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

# Function to parse RGB input
def parse_rgb_input(input_text):
    if input_text.lower() in COMPATIBLE_COLORS:
        return COMPATIBLE_COLORS[input_text.lower()]
    match = re.match(r"\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", input_text)
    if match:
        r, g, b = map(int, match.groups())
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            return (r, g, b)
    return None

# Function to calculate mixed color
def calculate_mixed_color(colors_and_potencies):
    red_sum = green_sum = blue_sum = total_potency = 0
    for color, potency in colors_and_potencies:
        red_sum += color[0] * potency
        green_sum += color[1] * potency
        blue_sum += color[2] * potency
        total_potency += potency
    if total_potency == 0:
        return (255, 255, 255)  # Default to white if no colors
    return (
        min(255, red_sum // total_potency),
        min(255, green_sum // total_potency),
        min(255, blue_sum // total_potency),
    )

# Main function
def open_rgb_color_mixer():
    def update_cell(index, increase):
        """Update the color and potency for a cell on the wheel."""
        color_input = inputs[index].get()
        potency = potencies[index]
        rgb_color = parse_rgb_input(color_input)
        if rgb_color:
            if increase and potency.get() < 5:
                potency.set(potency.get() + 1)
            elif not increase and potency.get() > 1:
                potency.set(potency.get() - 1)

            cells[index].config(bg=f"#{rgb_color[0]:02x}{rgb_color[1]:02x}{rgb_color[2]:02x}")
            potency_labels[index].config(text=f"{potency.get()}")
            calculate_and_update_center()
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid color name or RGB value (e.g., (255, 0, 0)).")

    def calculate_and_update_center():
        """Calculate and update the mixed color in the center."""
        colors_and_potencies = [
            (parse_rgb_input(inputs[i].get()), potencies[i].get())
            for i in range(10)
            if parse_rgb_input(inputs[i].get())
        ]
        mixed_color = calculate_mixed_color(colors_and_potencies)
        center_color_label.config(bg=f"#{mixed_color[0]:02x}{mixed_color[1]:02x}{mixed_color[2]:02x}")
        rgb_value_label.config(text=f"RGB({mixed_color[0]}, {mixed_color[1]}, {mixed_color[2]})")

    # GUI Setup
    mixer_window = tk.Tk()
    mixer_window.title("RGB Color Mixer")

    # Final Color Display on the Left
    left_frame = tk.Frame(mixer_window)
    left_frame.grid(row=0, column=0, padx=10, pady=10)

    # Header
    header_label = tk.Label(left_frame, text="RGB", font=("Arial", 14), fg="dark blue")
    header_label.pack(pady=5)

    # Center Color Display
    center_color_label = tk.Label(left_frame, width=20, height=10, bg="white")
    center_color_label.pack()

    # RGB Value Label
    rgb_value_label = tk.Label(left_frame, text="RGB(255, 255, 255)")
    rgb_value_label.pack(pady=5)

    # Color Wheel and Inputs on the Right
    wheel_frame = tk.Frame(mixer_window)
    wheel_frame.grid(row=0, column=1, padx=10, pady=10)

    inputs = []
    potencies = []
    cells = []
    potency_labels = []

    for i in range(10):
        frame = tk.Frame(wheel_frame)
        frame.grid(row=i // 5, column=i % 5, padx=5, pady=5)

        # Display area
        cell = tk.Label(frame, width=10, height=5, bg="white")
        cell.pack()
        cells.append(cell)

        # Input field
        input_field = tk.Entry(frame, width=10)
        input_field.pack()
        inputs.append(input_field)

        # Potency label
        potency_label = tk.Label(frame, text="1")
        potency_label.pack()
        potency_labels.append(potency_label)

        # Potency slider
        potency = tk.IntVar(value=1)
        potencies.append(potency)

        # "+" Button
        plus_button = tk.Button(frame, text="+", command=lambda idx=i: update_cell(idx, True))
        plus_button.pack(side=tk.LEFT, padx=2)

        # "-" Button
        minus_button = tk.Button(frame, text="-", command=lambda idx=i: update_cell(idx, False))
        minus_button.pack(side=tk.RIGHT, padx=2)

    # Back Button
    back_button = tk.Button(mixer_window, text="Back", command=mixer_window.destroy)
    back_button.grid(row=1, column=0, columnspan=2, pady=10)

    mixer_window.mainloop()

# Run the RGB Color Mixer
if __name__ == "__main__":
    open_rgb_color_mixer()


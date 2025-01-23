import tkinter as tk
from tkinter import messagebox
import re

# Define supported color names and their CMYK equivalents
COMPATIBLE_COLORS_CMYK = {
    "red": (0, 100, 100, 0),
    "orange": (0, 50, 100, 0),
    "yellow": (0, 0, 100, 0),
    "green": (100, 0, 100, 0),
    "blue": (100, 100, 0, 0),
    "purple": (50, 100, 0, 0),
    "pink": (0, 50, 0, 0),
    "black": (0, 0, 0, 100),
    "brown": (30, 60, 60, 30),
    "white": (0, 0, 0, 0),
}

# Convert CMYK to RGB (for cell colors)
def cmyk_to_rgb(c, m, y, k):
    r = int(255 * (1 - c / 100) * (1 - k / 100))
    g = int(255 * (1 - m / 100) * (1 - k / 100))
    b = int(255 * (1 - y / 100) * (1 - k / 100))
    return r, g, b

# Parse user input for CMYK or color name
def parse_cmyk_input(input_text):
    # Check if it's a color name
    if input_text.lower() in COMPATIBLE_COLORS_CMYK:
        return COMPATIBLE_COLORS_CMYK[input_text.lower()]
    # Check if it's a CMYK value in the format (C, M, Y, K)
    match = re.match(r"\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", input_text)
    if match:
        c, m, y, k = map(int, match.groups())
        if 0 <= c <= 100 and 0 <= m <= 100 and 0 <= y <= 100 and 0 <= k <= 100:
            return (c, m, y, k)
    return None

# Calculate the mixed color from all inputs
def calculate_mixed_cmyk(colors_and_potencies):
    c_sum = m_sum = y_sum = k_sum = total_potency = 0
    for color, potency in colors_and_potencies:
        c_sum += color[0] * potency
        m_sum += color[1] * potency
        y_sum += color[2] * potency
        k_sum += color[3] * potency
        total_potency += potency
    if total_potency == 0:
        return 0, 0, 0, 0  # Default to pure white in CMYK
    avg_c = c_sum / total_potency
    avg_m = m_sum / total_potency
    avg_y = y_sum / total_potency
    avg_k = k_sum / total_potency
    return round(avg_c, 2), round(avg_m, 2), round(avg_y, 2), round(avg_k, 2)

# Main function to open the CMYK page
def open_cmyk_page():
    def update_cell(index, increase=False):
        # Get user input and parse it
        cmyk_input = inputs[index].get()
        cmyk_values = parse_cmyk_input(cmyk_input)
        if cmyk_values:
            if not increase:  # Enter key auto-sets potency to 1
                potencies[index].set(1)
            elif increase and potencies[index].get() < 5:
                potencies[index].set(potencies[index].get() + 1)
            elif not increase and potencies[index].get() > 1:
                potencies[index].set(potencies[index].get() - 1)

            # Update cell background color
            rgb_color = cmyk_to_rgb(*cmyk_values)
            cells[index].config(bg=f"#{rgb_color[0]:02x}{rgb_color[1]:02x}{rgb_color[2]:02x}")
            potency_labels[index].config(text=f"{potencies[index].get()}")
            update_center_color()
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid color name or CMYK value (e.g., (0, 100, 100, 0)).")

    def update_center_color():
        # Calculate mixed color from all inputs
        colors_and_potencies = [
            (parse_cmyk_input(inputs[i].get()), potencies[i].get())
            for i in range(10)
            if parse_cmyk_input(inputs[i].get())
        ]
        mixed_cmyk = calculate_mixed_cmyk(colors_and_potencies)
        center_color_label.config(bg=f"#{cmyk_to_rgb(*mixed_cmyk)[0]:02x}{cmyk_to_rgb(*mixed_cmyk)[1]:02x}{cmyk_to_rgb(*mixed_cmyk)[2]:02x}")
        center_cmyk_label.config(text=f"CMYK({mixed_cmyk[0]}, {mixed_cmyk[1]}, {mixed_cmyk[2]}, {mixed_cmyk[3]})")

    # GUI Setup
    cmyk_window = tk.Tk()
    cmyk_window.title("CMYK Color Mixer")

    # Final Color Display
    center_frame = tk.Frame(cmyk_window)
    center_frame.grid(row=0, column=0, padx=10, pady=10)

    center_color_label = tk.Label(center_frame, text=" ", width=20, height=10, bg="white")
    center_color_label.pack()

    center_cmyk_label = tk.Label(center_frame, text="CMYK(0, 0, 0, 0)")
    center_cmyk_label.pack(pady=5)

    # Color Wheel and Inputs
    wheel_frame = tk.Frame(cmyk_window)
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
    back_button = tk.Button(cmyk_window, text="Back", command=cmyk_window.destroy)
    back_button.grid(row=1, column=0, columnspan=2, pady=10)

    cmyk_window.mainloop()

# Run CMYK Page
if __name__ == "__main__":
    open_cmyk_page()


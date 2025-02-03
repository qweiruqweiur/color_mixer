import tkinter as tk
from tkinter import messagebox

# Function to redirect to specific pages
def open_rgb_page():
    import rgb_page
    rgb_page.open_rgb_page()

def open_cmyk_page():
    import cmyk_page
    cmyk_page.open_cmyk_page()

def open_hex_page():
    import hex_page
    hex_page.open_hex_page()

# Main function to open the General Color Mixer Page
def open_general_color_mixer():
    def block_interaction():
        """Show an error message when interaction is attempted without a format selection."""
        messagebox.showerror(
            "Select Format",
            "Please select a color format before interacting with components!"
        )

    def redirect_to_format(format_choice):
        """Redirect the user to the specified format page."""
        mixer_window.destroy()
        if format_choice == "RGB":
            open_rgb_page()
        elif format_choice == "CMYK":
            open_cmyk_page()
        elif format_choice == "HEX":
            open_hex_page()
    
    def go_back():
        """Close the General Color Mixer and open the Tools Page."""
        mixer_window.destroy()
        import tools
        tools.open_tools_page()

    # GUI Setup
    mixer_window = tk.Tk()
    mixer_window.title("General Color Mixer")

    # Final Color Display
    center_frame = tk.Frame(mixer_window)
    center_frame.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    center_color_label = tk.Label(center_frame, text=" ", width=20, height=10, bg="white")
    center_color_label.pack()

    # Format Selection Buttons
    button_frame = tk.Frame(mixer_window)
    button_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    tk.Button(button_frame, text="RGB", width=10, command=lambda: redirect_to_format("RGB")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="CMYK", width=10, command=lambda: redirect_to_format("CMYK")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="HEX", width=10, command=lambda: redirect_to_format("HEX")).pack(side=tk.LEFT, padx=5)

    # Color Wheel and Inputs
    wheel_frame = tk.Frame(mixer_window)
    wheel_frame.grid(row=2, column=0, padx=10, pady=10)

    cells = []
    inputs = []
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
        input_field.bind("<FocusIn>", lambda event: block_interaction())

        # Potency label
        potency_label = tk.Label(frame, text="1")
        potency_label.pack()
        potency_labels.append(potency_label)

        # "+" and "-" Buttons
        tk.Button(frame, text="+", command=block_interaction).pack(side=tk.LEFT, padx=2)
        tk.Button(frame, text="-", command=block_interaction).pack(side=tk.RIGHT, padx=2)

    # Back Button
    back_button = tk.Button(mixer_window, text="Back", command=go_back)
    back_button.grid(row=3, column=0, columnspan=2, pady=10)

    mixer_window.mainloop()

# Run General Color Mixer
if __name__ == "__main__":
    open_general_color_mixer()


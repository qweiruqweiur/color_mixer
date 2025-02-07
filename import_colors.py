import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import re

# Function to parse imported color data
def parse_color_data(file_path, format_choice):
    """Reads the selected file and extracts colors in the chosen format."""
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        colors = []
        for line in lines:
            line = line.strip()
            if format_choice == "RGB":
                match = re.match(r"\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", line)
                if match:
                    r, g, b = map(int, match.groups())
                    if all(0 <= val <= 255 for val in (r, g, b)):
                        colors.append((r, g, b))
            elif format_choice == "HEX":
                match = re.match(r"^#([0-9a-fA-F]{6})$", line)
                if match:
                    colors.append(line)
            elif format_choice == "CMYK":
                match = re.match(r"\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", line)
                if match:
                    c, m, y, k = map(int, match.groups())
                    if all(0 <= val <= 100 for val in (c, m, y, k)):
                        colors.append((c, m, y, k))

        return colors
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read file: {e}")
        return []

# Function to open file dialog and load colors
def load_colors():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return
    
    format_choice = format_var.get()
    if not format_choice:
        messagebox.showerror("Error", "Please select a format before importing.")
        return
    
    colors = parse_color_data(file_path, format_choice)
    
    if colors:
        # Display imported colors
        for i, color in enumerate(colors[:10]):  # Limit display to 10 colors
            if format_choice == "HEX":
                color_display[i].config(bg=color, text=color)
            else:
                rgb = color if format_choice == "RGB" else (
                    int(255 * (1 - color[0] / 100) * (1 - color[3] / 100)),
                    int(255 * (1 - color[1] / 100) * (1 - color[3] / 100)),
                    int(255 * (1 - color[2] / 100) * (1 - color[3] / 100))
                )
                color_display[i].config(bg=f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}", text=str(color))
    else:
        messagebox.showwarning("No Colors Found", "No valid colors found in the file.")

# Function to go back to External Data Page
def go_back():
    import_window.destroy()
    subprocess.run(["python", "external_data.py"])

# Main function to open Import Colors Page
def open_import_colors_page():
    global import_window, format_var, color_display

    # GUI Setup
    import_window = tk.Tk()
    import_window.title("Import Colors")

    # Title
    title_label = tk.Label(import_window, text="Import Colors", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Format Selection
    format_var = tk.StringVar()

    format_frame = tk.Frame(import_window)
    format_frame.pack(pady=10)

    tk.Label(format_frame, text="Select Format:").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(format_frame, text="RGB", variable=format_var, value="RGB").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(format_frame, text="HEX", variable=format_var, value="HEX").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(format_frame, text="CMYK", variable=format_var, value="CMYK").pack(side=tk.LEFT, padx=5)

    # Load Colors Button
    load_button = tk.Button(import_window, text="Import Colors", command=load_colors, width=20)
    load_button.pack(pady=10)

    # Color Display Section
    color_frame = tk.Frame(import_window)
    color_frame.pack(pady=10)

    color_display = []
    for i in range(10):
        label = tk.Label(color_frame, text=" ", width=20, height=2, bg="white", relief="solid")
        label.pack(pady=2)
        color_display.append(label)

    # Back Button
    back_button = tk.Button(import_window, text="Back", command=go_back)
    back_button.pack(pady=10)

    import_window.mainloop()

# Run Import Colors Page
if __name__ == "__main__":
    open_import_colors_page()


import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import os

TEMP_FILE = "temp_saved_colors.txt"

# Load saved colors from the temporary file
def load_saved_colors():
    """Loads saved colors from the temp file."""
    if os.path.exists(TEMP_FILE):
        with open(TEMP_FILE, "r") as file:
            return [line.strip() for line in file.readlines()]
    return []

# Convert RGB to HEX
def rgb_to_hex(rgb):
    """Converts an RGB string (e.g., 'RGB(255, 0, 0)') to HEX."""
    r, g, b = map(int, rgb[4:-1].split(", "))  # Extract numbers
    return f"#{r:02x}{g:02x}{b:02x}".upper()

# Convert RGB to CMYK
def rgb_to_cmyk(rgb):
    """Converts an RGB string to CMYK."""
    r, g, b = map(int, rgb[4:-1].split(", "))
    r, g, b = r / 255, g / 255, b / 255
    k = 1 - max(r, g, b)
    if k == 1:
        return "CMYK(0, 0, 0, 100)"
    c = (1 - r - k) / (1 - k) * 100
    m = (1 - g - k) / (1 - k) * 100
    y = (1 - b - k) / (1 - k) * 100
    return f"CMYK({round(c)}, {round(m)}, {round(y)}, {round(k * 100)})"

# Function to save the selected color
def save_color():
    """Saves the selected color in the chosen format."""
    selected_color = color_var.get()
    format_choice = format_var.get()

    if not selected_color or selected_color == "No saved colors":
        messagebox.showerror("Error", "No color selected to export.")
        return

    if not format_choice:
        messagebox.showerror("Error", "Please select a format before exporting.")
        return

    # Convert color to the selected format
    if format_choice == "RGB":
        output_color = selected_color
    elif format_choice == "HEX":
        output_color = rgb_to_hex(selected_color)
    elif format_choice == "CMYK":
        output_color = rgb_to_cmyk(selected_color)
    else:
        output_color = selected_color  # Fallback (should never happen)

    # Save to file
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")],
                                             title="Save Color")
    if file_path:
        with open(file_path, "w") as file:
            file.write(output_color)
        messagebox.showinfo("Success", f"Color {output_color} saved to {file_path}!")

# Function to clear saved colors
def clear_saved_colors():
    """Deletes all saved colors and updates the dropdown."""
    confirm = messagebox.askyesno("Clear Colors", "Are you sure you want to delete all saved colors?")
    if confirm:
        open(TEMP_FILE, "w").close()  # Clears the file
        messagebox.showinfo("Cleared", "All saved colors have been deleted.")

        # Update the dropdown to show "No saved colors"
        color_var.set("No saved colors")
        color_dropdown["menu"].delete(0, "end")  # Clear dropdown menu
        color_dropdown["menu"].add_command(label="No saved colors", command=tk._setit(color_var, "No saved colors"))

def go_back():
    """Closes the export window and returns to the external data page."""
    export_window.destroy()
    subprocess.run(["python", "external_data.py"])

# Main function to open Export Colors Page
def open_export_colors_page():
    """Launches the Export Colors UI."""
    global export_window, color_var, format_var, color_dropdown

    export_window = tk.Tk()
    export_window.title("Export Colors")

    tk.Label(export_window, text="Export Colors", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(export_window, text="Select a Color to Export:").pack()

    # Load saved colors
    saved_colors = load_saved_colors()
    default_value = saved_colors[0] if saved_colors else "No saved colors"

    # Dropdown for saved colors
    color_var = tk.StringVar(value=default_value)
    color_dropdown = tk.OptionMenu(export_window, color_var, *saved_colors if saved_colors else ["No saved colors"])
    color_dropdown.pack(pady=5)

    # Format Selection
    format_var = tk.StringVar()
    format_frame = tk.Frame(export_window)
    format_frame.pack(pady=10)

    tk.Label(format_frame, text="Select Export Format:").pack()
    tk.Radiobutton(format_frame, text="RGB", variable=format_var, value="RGB").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(format_frame, text="HEX", variable=format_var, value="HEX").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(format_frame, text="CMYK", variable=format_var, value="CMYK").pack(side=tk.LEFT, padx=5)

    # Export, Clear, and Back Buttons
    tk.Button(export_window, text="Export Color", command=save_color, width=20).pack(pady=5)
    tk.Button(export_window, text="Clear Saved Colors", command=clear_saved_colors, width=20, fg="red").pack(pady=5)
    tk.Button(export_window, text="Back", command=go_back, width=20).pack(pady=5)

    export_window.mainloop()

if __name__ == "__main__":
    open_export_colors_page()

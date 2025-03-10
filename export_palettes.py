import tkinter as tk
from tkinter import messagebox, filedialog
import os
import json
import re

TEMP_PALETTE_FILE = "temp_saved_palettes.txt"

# Load saved palettes from JSON file
def load_saved_palettes():
    """Loads palettes from the JSON file."""
    if os.path.exists(TEMP_PALETTE_FILE):
        with open(TEMP_PALETTE_FILE, "r") as file:
            try:
                return json.load(file)  # Read as structured data
            except json.JSONDecodeError:
                return []  # Return empty list if corrupted
    return []

# Convert RGB to HEX
def rgb_to_hex(rgb):
    """Converts an RGB tuple to HEX."""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}".upper()

# Convert RGB to CMYK
def rgb_to_cmyk(rgb):
    """Converts an RGB tuple to CMYK."""
    r, g, b = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
    k = 1 - max(r, g, b)
    if k == 1:
        return "CMYK(0, 0, 0, 100)"
    c = (1 - r - k) / (1 - k) * 100
    m = (1 - g - k) / (1 - k) * 100
    y = (1 - b - k) / (1 - k) * 100
    return f"CMYK({round(c)}, {round(m)}, {round(y)}, {round(k * 100)})"

# Function to save the selected palette
def save_palette():
    """Saves the selected palette in the chosen format."""
    selected_palette_name = palette_var.get()
    format_choice = format_var.get()

    if not selected_palette_name or selected_palette_name == "No saved palettes":
        messagebox.showerror("Error", "No palette selected to export.")
        return

    if not format_choice:
        messagebox.showerror("Error", "Please select a format before exporting.")
        return

    # Retrieve the selected palette data
    saved_palettes = load_saved_palettes()
    selected_palette = next((p for p in saved_palettes if p["name"] == selected_palette_name), None)

    if not selected_palette:
        messagebox.showerror("Error", "Selected palette not found.")
        return

    # Convert colors based on format selection
    converted_colors = []
    for color in selected_palette["colors"]:
        rgb = color["RGB"]
        if format_choice == "RGB":
            converted_colors.append(f"RGB({rgb[0]}, {rgb[1]}, {rgb[2]})")
        elif format_choice == "HEX":
            converted_colors.append(rgb_to_hex(rgb))
        elif format_choice == "CMYK":
            converted_colors.append(rgb_to_cmyk(rgb))

    # Save to file
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")],
                                             initialfile=selected_palette_name,
                                             title="Save Palette")
    if file_path:
        with open(file_path, "w") as file:
            file.write(f"{selected_palette_name}\n")
            file.writelines(f"{color}\n" for color in converted_colors)
        messagebox.showinfo("Success", f"Palette {selected_palette_name} saved to {file_path}!")

def show_palette_contents(event):
    """Displays the colors of the selected palette when right-clicked."""
    selected_palette_name = palette_var.get()
    if selected_palette_name and selected_palette_name != "No saved palettes":
        saved_palettes = load_saved_palettes()
        selected_palette = next((p for p in saved_palettes if p["name"] == selected_palette_name), None)

        if selected_palette:
            color_lines = "\n".join([f"RGB({c['RGB'][0]}, {c['RGB'][1]}, {c['RGB'][2]})" for c in selected_palette["colors"]])
            messagebox.showinfo(selected_palette_name, f"Colors:\n{color_lines}")

def clear_saved_palettes():
    """Clears all saved palettes from temp file."""
    confirm = messagebox.askyesno("Clear Palettes", "Are you sure you want to delete all saved palettes?")
    if confirm:
        open(TEMP_PALETTE_FILE, "w").close()  # Clears the file
        messagebox.showinfo("Cleared", "All saved palettes have been deleted.")
        
        # Update the dropdown to reflect that no palettes exist
        palette_var.set("No saved palettes")
        palette_dropdown["menu"].delete(0, "end")  # Clear dropdown menu
        palette_dropdown["menu"].add_command(label="No saved palettes", command=tk._setit(palette_var, "No saved palettes"))

def go_back():
    """Closes the export window and returns to the external data page."""
    export_window.destroy()
    import external_data
    external_data.open_external_data()

# Main function to open Export Palettes Page
def open_export_palettes_page():
    """Launches the Export Palettes UI."""
    global export_window, palette_var, format_var, palette_dropdown

    export_window = tk.Tk()
    export_window.title("Export Palettes")

    tk.Label(export_window, text="Export Palettes", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(export_window, text="Select a Palette to Export:").pack()

    # Load saved palettes
    saved_palettes = load_saved_palettes()
    palette_names = [p["name"] for p in saved_palettes]
    default_value = palette_names[0] if palette_names else "No saved palettes"

    # Dropdown for saved palettes
    palette_var = tk.StringVar(value=default_value)
    palette_dropdown = tk.OptionMenu(export_window, palette_var, *palette_names if palette_names else ["No saved palettes"])
    palette_dropdown.pack(pady=5)

    # Right-click to view palette contents
    palette_dropdown.bind("<Button-3>", show_palette_contents)

    # Format Selection
    format_var = tk.StringVar()
    format_frame = tk.Frame(export_window)
    format_frame.pack(pady=10)

    tk.Label(format_frame, text="Select Export Format:").pack()
    tk.Radiobutton(format_frame, text="RGB", variable=format_var, value="RGB").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(format_frame, text="HEX", variable=format_var, value="HEX").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(format_frame, text="CMYK", variable=format_var, value="CMYK").pack(side=tk.LEFT, padx=5)

    # Export, Clear, and Back Buttons
    tk.Button(export_window, text="Export Palette", command=save_palette, width=20).pack(pady=5)
    tk.Button(export_window, text="Clear Saved Palettes", command=clear_saved_palettes, width=20, fg="red").pack(pady=5)
    tk.Button(export_window, text="Back", command=go_back, width=20).pack(pady=5)

    export_window.mainloop()

if __name__ == "__main__":
    open_export_palettes_page()

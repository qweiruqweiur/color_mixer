import tkinter as tk
from tkinter import messagebox
import json
import os

# === Appearance ===
SETTINGS_FILE = "appearance_settings.json"

def load_appearance():
    default = {"theme": "light", "font_size": "medium", "font_family": "Arial"}
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return default
    return default

def get_font_settings():
    appearance = load_appearance()
    font_sizes = {
        "small": 10, "medium": 12, "large": 14, "extra large": 16
    }
    font_size = font_sizes.get(appearance.get("font_size", "medium"), 12)
    font_family = appearance.get("font_family", "Arial")
    theme = appearance.get("theme", "light")
    return font_family, font_size, theme

# === Navigation Functions ===
def open_rgb_page():
    import rgb_page
    rgb_page.open_rgb_page()

def open_cmyk_page():
    import cmyk_page
    cmyk_page.open_cmyk_page()

def open_hex_page():
    import hex_page
    hex_page.open_hex_page()

def open_general_color_mixer():
    font_family, font_size, theme = get_font_settings()
    font = (font_family, font_size)

    bg_color = "#333" if theme == "dark" else "white"
    fg_color = "white" if theme == "dark" else "black"

    BUTTON_STYLE = {
        "bg": "#e0e0e0", "fg": "black", "font": font,
        "bd": 1, "relief": "raised", "padx": 8, "pady": 4
    }
    ENTRY_STYLE = {
        "bg": "white", "fg": "black", "font": font,
        "bd": 1, "relief": "solid"
    }

    selected_format = [None]

    def block_interaction():
        messagebox.showerror("Select Format", "Please select a color format before interacting with components!")

    def redirect_to_format(format_choice):
        mixer_window.destroy()
        if format_choice == "RGB":
            open_rgb_page()
        elif format_choice == "CMYK":
            open_cmyk_page()
        elif format_choice == "HEX":
            open_hex_page()

    def go_back():
        mixer_window.destroy()
        import tools
        tools.open_tools_page()

    mixer_window = tk.Tk()
    mixer_window.title("General Color Mixer")
    mixer_window.configure(bg=bg_color)

    tk.Label(mixer_window, text="General Color Mixer", font=("Arial", 18, "bold"), bg=bg_color, fg=fg_color).pack(pady=10)

    content_frame = tk.Frame(mixer_window, bg=bg_color)
    content_frame.pack()

    # === Wheel (left) ===
    wheel_frame = tk.Frame(content_frame, bg=bg_color)
    wheel_frame.grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="n")

    canvas_size = 500
    canvas = tk.Canvas(wheel_frame, width=canvas_size, height=canvas_size, bg=bg_color, highlightthickness=0)
    canvas.pack()

    center_x = canvas_size // 2
    center_y = canvas_size // 2
    outer_radius = 200
    center_radius = 65

    sectors = []
    locked_sectors = [5, 11]

    for i in range(12):
        start_angle = i * 30
        arc = canvas.create_arc(
            center_x - outer_radius, center_y - outer_radius,
            center_x + outer_radius, center_y + outer_radius,
            start=start_angle, extent=30,
            fill="black" if i in locked_sectors else "white",
            outline="black", width=1
        )
        sectors.append(arc)

    center_circle = canvas.create_oval(
        center_x - center_radius, center_y - center_radius,
        center_x + center_radius, center_y + center_radius,
        fill="white", outline="black", width=1
    )
    canvas.tag_raise(center_circle)

    # === Format Selection ===
    wheel_info = tk.Frame(wheel_frame, bg=bg_color)
    wheel_info.pack(pady=(10, 0))

    tk.Label(wheel_info, text="Choose Data Format", font=("Arial", 14, "bold"), bg=bg_color, fg=fg_color).pack(pady=(0, 5))

    format_button_frame = tk.Frame(wheel_info, bg=bg_color)
    format_button_frame.pack()

    tk.Button(format_button_frame, text="RGB", width=10, font=("Arial", 12), command=lambda: redirect_to_format("RGB")).pack(side=tk.LEFT, padx=10)
    tk.Button(format_button_frame, text="HEX", width=10, font=("Arial", 12), command=lambda: redirect_to_format("HEX")).pack(side=tk.LEFT, padx=10)
    tk.Button(format_button_frame, text="CMYK", width=10, font=("Arial", 12), command=lambda: redirect_to_format("CMYK")).pack(side=tk.LEFT, padx=10)

    example_frame = tk.Frame(wheel_info, bg=bg_color)
    example_frame.pack(pady=(5, 10))

    tk.Label(example_frame, text="(255, 0, 0)", font=("Arial", 10), bg=bg_color, fg=fg_color).pack(side=tk.LEFT, padx=43)
    tk.Label(example_frame, text="#FF0000", font=("Arial", 10), bg=bg_color, fg=fg_color).pack(side=tk.LEFT, padx=43)
    tk.Label(example_frame, text="(0, 100, 100, 0)", font=("Arial", 10), bg=bg_color, fg=fg_color).pack(side=tk.LEFT, padx=43)

    # === Controls (right) ===
    controls_frame = tk.Frame(content_frame, bg=bg_color)
    controls_frame.grid(row=0, column=1, pady=(155, 0), sticky="n")

    inputs = []
    potencies = []
    potency_labels = []

    editable_indexes = [i for i in range(12) if i not in locked_sectors]

    for idx, sector_index in enumerate(editable_indexes):
        row = idx // 5
        col = idx % 5
        frame = tk.Frame(controls_frame, bg=bg_color, padx=4, pady=4)
        frame.grid(row=row * 3, column=col, padx=4, pady=4)

        label = tk.Label(frame, text=f"Sector {idx+1}", font=("Arial", 11, "bold"), bg=bg_color, fg=fg_color)
        label.pack()

        entry = tk.Entry(frame, width=10, **ENTRY_STYLE)
        entry.pack()
        entry.bind("<FocusIn>", lambda event: block_interaction())
        inputs.append(entry)

        p_frame = tk.Frame(frame, bg=bg_color)
        p_frame.pack(pady=1)

        minus_btn = tk.Button(p_frame, text="-", command=block_interaction, **BUTTON_STYLE)
        minus_btn.pack(side=tk.LEFT)

        potency = tk.IntVar(value=1)
        potencies.append(potency)

        potency_label = tk.Label(p_frame, text="1", font=("Arial", 10), bg=bg_color, fg=fg_color, width=2)
        potency_label.pack(side=tk.LEFT)
        potency_labels.append(potency_label)

        plus_btn = tk.Button(p_frame, text="+", command=block_interaction, **BUTTON_STYLE)
        plus_btn.pack(side=tk.LEFT)

    for i in locked_sectors:
        inputs.insert(i, None)
        potencies.insert(i, tk.IntVar(value=1))
        potency_labels.insert(i, None)

    # === Back Button ===
    back_button = tk.Button(mixer_window, text="Back", width=20, command=go_back, **BUTTON_STYLE)
    back_button.pack(pady=20)

    mixer_window.mainloop()

# Run
if __name__ == "__main__":
    open_general_color_mixer()

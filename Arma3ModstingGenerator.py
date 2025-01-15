import tkinter as tk
from tkinter import filedialog, messagebox
import re
from html import unescape

# Function to sanitize filenames
invalid_chars = r'[<>:"/\\|?*]'


def sanitize_filename(name):
    sanitized_name = unescape(name)  # Decode HTML entities like &amp; to &
    sanitized_name = re.sub(invalid_chars, '-', sanitized_name)
    return sanitized_name


# Function to extract IDs and DisplayNames from the .html file
def extract_ids():
    # Ask user to select the .html file
    file_path = filedialog.askopenfilename(title="Select an Arma 3 Preset .html File",
                                           filetypes=[("HTML Files", "*.html")])

    if not file_path:
        return  # User canceled

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            global extracted_data, sanitized_mods
            extracted_data = []
            sanitized_mods = []
            x = '?id='
            for line in f:
                if 'data-type="DisplayName"' in line:
                    display_name = line.split('>')[1].split('<')[0]
                if x in line:
                    id_value = ''
                    lines = (line[line.find(x) + len(x):])
                    for z in lines:
                        if z == '"':
                            break
                        else:
                            id_value += z
                    sanitized_name = sanitize_filename(display_name)
                    if sanitized_name != display_name and "&" not in display_name:
                        sanitized_mods.append((display_name, sanitized_name))
                    extracted_data.append((sanitized_name, id_value))

        display_ids()
        show_sanitized_mods()
        save_button.config(state=tk.NORMAL)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to display IDs and DisplayNames in the text box based on the selected format
def display_ids():
    if not extracted_data:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Output will appear here...")
        return

    include_at = include_at_var.get()
    show_names = show_names_var.get()
    format_option = format_var.get()
    output_text.delete(1.0, tk.END)

    formatted_entries = []
    for name, mod_id in extracted_data:
        entry = f"@{name}" if include_at else name
        if not show_names:
            entry = f"@{mod_id}" if include_at else mod_id
        formatted_entries.append(entry)

    if format_option == "Newline":
        output_text.insert(tk.END, '\n'.join(formatted_entries))
    elif format_option == "Semicolon":
        output_text.insert(tk.END, ';'.join(formatted_entries))
    elif format_option == "Comma":
        output_text.insert(tk.END, ','.join(formatted_entries))


# Function to display sanitized mods in a separate text box
def show_sanitized_mods():
    sanitized_text.delete(1.0, tk.END)
    if not sanitized_mods:
        sanitized_text.insert(tk.END, "No mods required sanitization.")
    else:
        for original, sanitized in sanitized_mods:
            sanitized_text.insert(tk.END, f"Original: {original}\nSanitized: {sanitized}\n\n")


# Function to save the extracted data to a file
def save_list():
    include_at = include_at_var.get()
    show_names = show_names_var.get()
    format_option = format_var.get()
    savefile = filedialog.asksaveasfilename(title="Save List", defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt")])
    if savefile:
        with open(savefile, "w", encoding='utf-8') as file:
            formatted_entries = []
            for name, mod_id in extracted_data:
                entry = f"@{name}" if include_at else name
                if not show_names:
                    entry = f"@{mod_id}" if include_at else mod_id
                formatted_entries.append(entry)

            if format_option == "Newline":
                file.write('\n'.join(formatted_entries))
            elif format_option == "Semicolon":
                file.write(';'.join(formatted_entries))
            elif format_option == "Comma":
                file.write(','.join(formatted_entries))
        messagebox.showinfo("Success", f"List saved to {savefile}")


# Create the GUI
root = tk.Tk()
root.title("Arma 3 Mod ID Extractor")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Include "@" option
include_at_var = tk.BooleanVar(value=False)
include_at_check = tk.Checkbutton(frame, text="Include '@' before each entry", variable=include_at_var,
                                  command=display_ids)
include_at_check.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="w")

# Show names or IDs option
show_names_var = tk.BooleanVar(value=True)
show_names_check = tk.Checkbutton(frame, text="Show Names (instead of only IDs)", variable=show_names_var,
                                  command=display_ids)
show_names_check.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="w")

# Format selection
format_var = tk.StringVar(value="Newline")
format_label = tk.Label(frame, text="Select Output Format:")
format_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

newline_radio = tk.Radiobutton(frame, text="Newline", variable=format_var, value="Newline", command=display_ids)
newline_radio.grid(row=2, column=1, padx=5, pady=5)
semicolon_radio = tk.Radiobutton(frame, text="Semicolon", variable=format_var, value="Semicolon", command=display_ids)
semicolon_radio.grid(row=2, column=2, padx=5, pady=5)
comma_radio = tk.Radiobutton(frame, text="Comma", variable=format_var, value="Comma", command=display_ids)
comma_radio.grid(row=2, column=3, padx=5, pady=5)

# Buttons
load_button = tk.Button(frame, text="Load .html File", command=extract_ids)
load_button.grid(row=3, column=0, padx=5, pady=5)

save_button = tk.Button(frame, text="Save List", state=tk.DISABLED, command=save_list)
save_button.grid(row=3, column=1, padx=5, pady=5, columnspan=3)

# Output Text Box
output_text = tk.Text(frame, height=15, width=60)
output_text.grid(row=4, column=0, columnspan=4, padx=5, pady=5)
output_text.insert(tk.END, "Output will appear here...")

# Sanitized Mods Text Box
sanitized_label = tk.Label(frame, text="Sanitized Mods:")
sanitized_label.grid(row=5, column=0, columnspan=4, sticky="w")
sanitized_text = tk.Text(frame, height=10, width=60)
sanitized_text.grid(row=6, column=0, columnspan=4, padx=5, pady=5)
sanitized_text.insert(tk.END, "No mods required sanitization.")

# Detailed Instructions
instructions = tk.Label(frame, text=(
    "1. Load an .html file to extract mod names and IDs.\n"
    "2. Names will be sanitized for file compatibility.\n"
    "Note:\n - Sanitized Mod Names may not be reliable for loading mods in Arma 3.\n"
    "  - It is recommended to use Workshop IDs for loading mods.\n"
    "4. Choose the desired output format and save the list."
), wraplength=400, justify="left")
instructions.grid(row=7, column=0, columnspan=4, padx=5, pady=10)

# Author signature
author_label = tk.Label(root, text="Developed by Waldo", font=("Arial", 10, "italic"))
author_label.pack(pady=5)

# Initialize extracted data variable
extracted_data = []
sanitized_mods = []

# Start the GUI event loop
root.mainloop()

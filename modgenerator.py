import tkinter as tk
from tkinter import filedialog, messagebox


# Function to extract IDs from the .html file
def extract_ids():
    # Ask user to select the .html file
    file_path = filedialog.askopenfilename(title="Select an Arma 3 Preset .html File",
                                           filetypes=[("HTML Files", "*.html")])

    if not file_path:
        return  # User canceled

    try:
        with open(file_path, 'r') as f:
            x = '?id='
            ids = []
            for line in f:
                if x in line:
                    lines = (line[line.find(x) + len(x):])
                    id_value = ''
                    for z in lines:
                        if z == '"':
                            break
                        else:
                            id_value += z
                    ids.append(id_value)

        # Store IDs and update display
        global extracted_ids
        extracted_ids = ids
        display_ids()

        # Enable saving button
        save_button.config(state=tk.NORMAL)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to display IDs in the text box based on the selected format
def display_ids():
    format_option = format_var.get()
    if format_option == "Newline":
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, '\n'.join(extracted_ids))
    elif format_option == "Semicolon":
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, ';'.join(extracted_ids))
    elif format_option == "Comma":
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, ','.join(extracted_ids))


# Function to save the selected format to a file
def save_list():
    format_option = format_var.get()
    savefile = filedialog.asksaveasfilename(title=f"Save {format_option} List", defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt")])
    if savefile:
        with open(savefile, "w") as file:
            if format_option == "Newline":
                file.write('\n'.join(extracted_ids))
            elif format_option == "Semicolon":
                file.write(';'.join(extracted_ids))
            elif format_option == "Comma":
                file.write(','.join(extracted_ids))
        messagebox.showinfo("Success", f"{format_option} list saved to {savefile}")


# Create the GUI
root = tk.Tk()
root.title("Arma 3 Mod ID Extractor")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Format selection
format_var = tk.StringVar(value="Newline")
format_label = tk.Label(frame, text="Select Output Format:")
format_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

newline_radio = tk.Radiobutton(frame, text="Newline", variable=format_var, value="Newline", command=display_ids)
newline_radio.grid(row=0, column=1, padx=5, pady=5)
semicolon_radio = tk.Radiobutton(frame, text="Semicolon", variable=format_var, value="Semicolon", command=display_ids)
semicolon_radio.grid(row=0, column=2, padx=5, pady=5)
comma_radio = tk.Radiobutton(frame, text="Comma", variable=format_var, value="Comma", command=display_ids)
comma_radio.grid(row=0, column=3, padx=5, pady=5)

# Buttons
load_button = tk.Button(frame, text="Load .html File", command=extract_ids)
load_button.grid(row=1, column=0, padx=5, pady=5)

save_button = tk.Button(frame, text="Save List", state=tk.DISABLED, command=save_list)
save_button.grid(row=1, column=1, padx=5, pady=5, columnspan=3)

# Output Text Box
output_text = tk.Text(frame, height=15, width=60)
output_text.grid(row=2, column=0, columnspan=4, padx=5, pady=5)
output_text.insert(tk.END, "Output will appear here...")

# Detailed Instructions
instructions = tk.Label(frame,
                        text="Load an .html file to extract mod IDs. The IDs will be displayed in the selected format.\nYou can then save the list in the desired format to a text file.",
                        wraplength=400, justify="left")
instructions.grid(row=3, column=0, columnspan=4, padx=5, pady=10)

# Author signature
author_label = tk.Label(root, text="Developed by Waldo", font=("Arial", 10, "italic"))
author_label.pack(pady=5)

# Initialize extracted IDs variable
extracted_ids = []

# Start the GUI event loop
root.mainloop()

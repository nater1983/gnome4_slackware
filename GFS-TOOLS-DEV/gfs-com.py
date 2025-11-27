import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Function to navigate to the selected folder
def navigate_to_folder():
    folder_name = entry.get()
    matching_paths = find_folder_path(folder_name, os.path.abspath(".."))

    if matching_paths:
        folder_path = matching_paths[0]
        os.chdir(folder_path)
        open_folder(folder_path)
        status_label.config(text=f"Opened directory: {folder_path}")
        history.append(folder_path)  # Add to history
        update_history_menu()
    else:
        status_label.config(text=f"Folder '{folder_name}' not found in the parent directory")

# Function to open the "order" folder, if available
def open_order_folder():
    folder_name = entry.get()
    matching_paths = find_folder_path(folder_name, os.path.abspath(".."))

    if matching_paths:
        order_path = os.path.join(os.path.dirname(matching_paths[0]), "order")
        if os.path.exists(order_path):
            os.chdir(order_path)
            open_folder(order_path)
            status_label.config(text=f"Opened 'order' folder: {order_path}")
            history.append(order_path)  # Add to history
            update_history_menu()
        else:
            status_label.config(text=f"'order' folder not found for '{folder_name}'")
    else:
        status_label.config(text=f"Folder '{folder_name}' not found in the parent directory")

# Function to search for the specified folder name on the system, starting from a given directory
def find_folder_path(folder_name, start_directory):
    matching_paths = []

    # Recursively search for the folder name starting from the specified directory
    for root, dirs, _ in os.walk(start_directory):
        if folder_name in dirs:
            matching_paths.append(os.path.join(root, folder_name))

    return matching_paths

# Function to open a folder using the default file manager
def open_folder(folder_path):
    os.system(f"nautilus {folder_path}")

# Function to gracefully close the application
def close_application(event=None):
    root.destroy()

# Function to update the history menu with the recently visited folders
def update_history_menu():
    history_menu.delete(0, tk.END)
    for i, path in enumerate(history[-10:], start=1):  # Display the last 10 items in history
        history_menu.add_command(label=f"{i}. {os.path.basename(path)}", command=lambda p=path: navigate_to_history(p))

# Function to navigate to a folder from the history menu
def navigate_to_history(path):
    os.chdir(path)
    open_folder(path)
    status_label.config(text=f"Opened directory: {path}")

# Function to navigate to the selected subfolder
def navigate_to_selected_folder():
    selected_folder = folder_var.get()
    folder_path = os.path.join(parent_folder, selected_folder)
    os.chdir(folder_path)
    open_folder(folder_path)
    status_label.config(text=f"Opened directory: {folder_path}")
    history.append(folder_path)  # Add to history
    update_history_menu()

# Create the main application window
root = tk.Tk()
root.title("Multi-Folder Navigator")

# Set the initial window size (width x height)
root.geometry("400x400")

# Create and configure the entry widget
entry_label = ttk.Label(root, text="Enter folder name:")
entry_label.pack()
entry = ttk.Entry(root)
entry.pack()

# Create and configure the navigate button
navigate_button = ttk.Button(root, text="Navigate", command=navigate_to_folder)
navigate_button.pack()

# Create and configure the open "order" button
open_order_button = ttk.Button(root, text="Open 'order' folder", command=open_order_folder)
open_order_button.pack()

# Create a label to display the current directory or file information
status_label = ttk.Label(root, text="")
status_label.pack()

# Create a history menu
history = []  # Store visited folder paths in history
history_menu = tk.Menu(root, tearoff=0)
root.config(menu=history_menu)

# Bind the <Control-c> event to close the application
root.bind("<Control-c>", close_application)

# Load and display a logo image (change 'logo.png' to your image file path)
logo_path = "./gfs-logo.png"  # Change this to the path of your logo image
if os.path.exists(logo_path):
    logo_image = Image.open(logo_path)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = ttk.Label(root, image=logo_photo)
    logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
    logo_label.pack()

# Define the parent folder where you want to navigate its subfolders
# Use os.path.expanduser to correctly handle the tilde (~) character
parent_folder = os.path.expanduser("/mnt/www/linux/gnome/46.x/source")  # Change this to the actual path

# Get a list of subdirectories within the parent folder
subfolder_names = [name for name in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, name))]

# Create a dropdown menu for selecting subfolders
folder_var = tk.StringVar(root)
folder_var.set(subfolder_names[0])  # Default selection
folder_menu = ttk.OptionMenu(root, folder_var, *subfolder_names)
folder_menu.pack()

# Create a button to navigate to the selected subfolder
navigate_folder_button = ttk.Button(root, text="Navigate to Selected Subfolder", command=navigate_to_selected_folder)
navigate_folder_button.pack()

# Start the Tkinter main loop
root.mainloop()


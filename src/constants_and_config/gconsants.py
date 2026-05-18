import os
import sys
from pathlib import Path

# Try to load .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def get_path_via_gui(title, file_type=None, is_folder=False):
    """Opens a GUI file/folder selector and returns the chosen path."""
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()  # Hide the main window
        root.attributes('-topmost', True)  # Bring to front

        if is_folder:
            path = filedialog.askdirectory(title=title)
        else:
            filetypes = [("Files", file_type)] if file_type else [("All Files", "*.*")]
            path = filedialog.askopenfilename(title=title, filetypes=filetypes)

        root.destroy()
        return path if path else None
    except Exception as e:
        print(f"Error opening file selector: {e}")
        return None

def save_to_env(key, value):
    """Saves a key-value pair to the .env file."""
    env_path = Path(".env")
    lines = []
    if env_path.exists():
        lines = env_path.read_text().splitlines()

    found = False
    new_lines = []
    for line in lines:
        if line.startswith(f"{key}="):
            new_lines.append(f'{key}="{value}"')
            found = True
        else:
            new_lines.append(line)

    if not found:
        new_lines.append(f'{key}="{value}"')

    env_path.write_text("\n".join(new_lines) + "\n")

def get_config_with_fallback(key, title, file_type=None, is_folder=False):
    """Gets config from env, or asks user via GUI if not found/invalid."""
    # Reload env each time to pick up previous saves in same session if needed
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except:
        pass

    path = os.getenv(key)

    # If path is missing or doesn't exist, ask the user
    if not path or not os.path.exists(path):
        print(f"{key} not set or invalid. Please select it via the file selector...")
        path = get_path_via_gui(title, file_type, is_folder)

        if not path:
            print(f"Error: No path selected for {key}. Exiting.")
            sys.exit(1)

        # Save it so we don't have to ask again
        save_to_env(key, path)

    return path
# --- Configuration Paths ---

# DOLPHIN_PATH: The executable itself
DOLPHIN_PATH = get_config_with_fallback(
    "DOLPHIN_PATH",
    "Select Dolphin Executable",
    file_type="*.app;Dolphin" if sys.platform == "darwin" else "*.exe"
)

# ISO_PATH: The Melee ISO file
ISO_PATH = get_config_with_fallback(
    "ISO_PATH",
    "Select Super Smash Bros. Melee ISO",
    file_type="*.iso"
)

# DATA_FOLDER: Where training data is stored
DATA_FOLDER = get_config_with_fallback(
    "DATA_FOLDER",
    "Select Folder for Training Data",
    is_folder=True
)

# DOLPHIN_HOME_PATH: The "User" directory for Dolphin settings/login
DOLPHIN_HOME_PATH = get_config_with_fallback(
    "DOLPHIN_HOME_PATH",
    "Select Dolphin User/Home Directory",
    is_folder=True
)

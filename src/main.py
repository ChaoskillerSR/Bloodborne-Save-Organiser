import tkinter as tk
from tkinter import filedialog
import json
import os
import ctypes
import config
import save_management
import profile_management

CONFIG_FILE = "config.json"


def save_config(profile_listbox, profile_entry):
    """Saves the directories for saves, profiles, and dark mode state."""
    data = {
        "save_directory": save_entry.get(),
        "profile_directory": profile_entry.get(),
        "dark_mode": dark_mode_var.get(),
        "load_save_keybind": load_save_keybind,
        "create_save_keybind": create_save_keybind
    }
    with open(CONFIG_FILE, "w") as file:
        json.dump(data, file)
    profile_management.load_profiles(profile_listbox, profile_entry)


def load_config():
    """Loads saved directories and dark mode state from config file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            data = json.load(file)
            save_entry.insert(0, data.get("save_directory", ""))
            profile_entry.insert(0, data.get("profile_directory", ""))
            dark_mode_var.set(data.get("dark_mode", True))
            apply_theme()


def apply_theme():
    """Applies the light or dark theme based on dark_mode_var."""
    if dark_mode_var.get():
        root.config(bg="#2e2e2e")
        save_entry.config(bg="#3c3c3c", fg="#ffffff")
        profile_entry.config(bg="#3c3c3c", fg="#ffffff")
        profile_listbox.config(bg="#3c3c3c", fg="#ffffff")
        savestate_listbox.config(bg="#3c3c3c", fg="#ffffff")
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg="#2e2e2e", fg="#ffffff")
            elif isinstance(widget, tk.Button):
                widget.config(bg="#555555", fg="#ffffff")
            elif isinstance(widget, tk.Checkbutton):
                widget.config(bg="#2e2e2e", fg="#ffffff")
    else:
        root.config(bg="#ffffff")
        save_entry.config(bg="#ffffff", fg="#000000")
        profile_entry.config(bg="#ffffff", fg="#000000")
        profile_listbox.config(bg="#ffffff", fg="#000000")
        savestate_listbox.config(bg="#ffffff", fg="#000000")
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg="#ffffff", fg="#000000")
            elif isinstance(widget, tk.Button):
                widget.config(bg="#f0f0f0", fg="#000000")
            elif isinstance(widget, tk.Checkbutton):
                widget.config(bg="#ffffff", fg="#000000")


def toggle_dark_mode(profile_listbox, profile_entry):
    """Toggles the dark mode state."""
    dark_mode_var.set(not dark_mode_var.get())
    apply_theme()
    save_config(profile_listbox, profile_entry)


def browse_save():
    """Opens a directory dialog for the game save folder."""
    path = filedialog.askdirectory()
    if path:
        save_entry.delete(0, tk.END)
        save_entry.insert(0, path)
        save_config(profile_listbox, profile_entry)


def browse_profile():
    """Opens a directory dialog for the profile folder."""
    path = filedialog.askdirectory()
    if path:
        profile_entry.delete(0, tk.END)
        profile_entry.insert(0, path)
        profile_management.load_profiles(profile_listbox, profile_entry)
        save_config(profile_listbox, profile_entry)


# ------------------------- GUI SETUP -------------------------

root = tk.Tk()
root.title("Bloodborne Save Manager")
root.geometry("380x540")

myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
root.iconbitmap("appicon.ico")

tk.Label(root, text="Game Save Directory:").pack()
save_entry = tk.Entry(root, width=50)
save_entry.pack()
tk.Button(root, text="Browse", command=browse_save).pack()

tk.Label(root, text="Profile Directory:").pack()
profile_entry = tk.Entry(root, width=50)
profile_entry.pack()
tk.Button(root, text="Browse", command=browse_profile).pack()

dark_mode_var = tk.BooleanVar(value=True)
dark_mode_button = tk.Button(root, text="Switch to Light/Dark Mode", command=toggle_dark_mode)
dark_mode_button.pack()

keybinds_button = tk.Button(root, text="Set Keybinds", command=lambda: config.open_config_window(root, dark_mode_var))
keybinds_button.pack()

tk.Label(root, text="Profiles:").pack()
profile_listbox = tk.Listbox(root, height=5)
profile_listbox.pack()

tk.Button(root, text="Create Profile", command=lambda: profile_management.create_profile(profile_listbox,
                                                                                         profile_entry)).pack()
tk.Button(root, text="Delete Profile", command=lambda: profile_management.delete_profile(profile_listbox,
                                                                                         savestate_listbox,
                                                                                         profile_entry)).pack()

tk.Label(root, text="Savestates:").pack()
savestate_listbox = tk.Listbox(root, height=5)
savestate_listbox.pack()

tk.Button(root, text="Create Savestate", command=lambda: save_management.create_savestate(root,
                                                                                          savestate_listbox,
                                                                                          profile_listbox,
                                                                                          profile_entry,
                                                                                          save_entry,
                                                                                          notification)).pack()
tk.Button(root, text="Load Savestate", command=lambda: save_management.load_selected_savestate(root,
                                                                                               profile_listbox,
                                                                                               savestate_listbox,
                                                                                               profile_entry,
                                                                                               save_entry,
                                                                                               notification)).pack()
tk.Button(root, text="Delete Savestate", command=lambda: save_management.delete_savestate(root,
                                                                                          dark_mode_var,
                                                                                          profile_listbox,
                                                                                          savestate_listbox,
                                                                                          profile_entry,
                                                                                          notification)).pack()

notification = tk.Label(root, text=f"")
notification.config(fg="#ffffff", bg="#2e2e2e")
notification.pack()

load_config()
root.after(100, profile_management.load_profiles(profile_listbox, profile_entry))
profile_listbox.bind("<ButtonRelease-1>", lambda event: save_management.update_savestates(root,
                                                                                          savestate_listbox,
                                                                                          profile_listbox,
                                                                                          profile_entry))

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    load_save_keybind = config_data["load_save_keybind"]
    create_save_keybind = config_data["create_save_keybind"]
    config.set_keybinds(root, savestate_listbox, profile_listbox, profile_entry, save_entry, notification)

dark_mode_button.configure(command=lambda: toggle_dark_mode(profile_listbox, profile_entry))
keybinds_button.configure(command=lambda: config.open_config_window(root, dark_mode_var, savestate_listbox,
                                                                    profile_listbox, profile_entry, save_entry, notification))

root.mainloop()

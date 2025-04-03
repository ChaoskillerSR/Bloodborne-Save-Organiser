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
        "global_hotkeys_enabled": global_hotkeys_enabled.get(),
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

        save_setup_frame.config(bg="#2e2e2e")
        profile_setup_frame.config(bg="#2e2e2e")
        listboxes_frame.config(bg="#2e2e2e")
        profile_listbox_frame.config(bg="#2e2e2e")
        savestate_listbox_frame.config(bg="#2e2e2e")
        config_frame.config(bg="#2e2e2e")
        save_entry_frame.config(bg="#2e2e2e")
        profile_entry_frame.config(bg="#2e2e2e")

        save_directory_label.config(bg="#2e2e2e", fg="#ffffff")
        profile_directory_label.config(bg="#2e2e2e", fg="#ffffff")
        profile_listbox_label.config(bg="#2e2e2e", fg="#ffffff")
        savestate_listbox_label.config(bg="#2e2e2e", fg="#ffffff")
        notification.config(bg="#2e2e2e", fg="#ffffff")

        for widget in root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg="#555555", fg="#ffffff")

        for widget in profile_entry_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg="#555555", fg="#ffffff")

        for widget in save_entry_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg="#555555", fg="#ffffff")

        for widget in savestate_listbox_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg="#555555", fg="#ffffff")

        for widget in profile_listbox_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg="#555555", fg="#ffffff")

        for widget in config_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg="#555555", fg="#ffffff")

    else:
        root.config(bg="#ffffff")

        save_entry.config(bg="#ffffff", fg="#000000")
        profile_entry.config(bg="#ffffff", fg="#000000")

        profile_listbox.config(bg="#ffffff", fg="#000000")
        savestate_listbox.config(bg="#ffffff", fg="#000000")

        save_setup_frame.config(bg="#ffffff")
        profile_setup_frame.config(bg="#ffffff")
        listboxes_frame.config(bg="#ffffff")
        profile_listbox_frame.config(bg="#ffffff")
        savestate_listbox_frame.config(bg="#ffffff")
        config_frame.config(bg="#ffffff")
        save_entry_frame.config(bg="#ffffff")
        profile_entry_frame.config(bg="#ffffff")

        save_directory_label.config(bg="#ffffff", fg="#000000")
        profile_directory_label.config(bg="#ffffff", fg="#000000")
        profile_listbox_label.config(bg="#ffffff", fg="#000000")
        savestate_listbox_label.config(bg="#ffffff", fg="#000000")
        notification.config(bg="#ffffff", fg="#000000")

        for widget in root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg="#f0f0f0", fg="#000000")

        for widget in profile_entry_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg="#f0f0f0", fg="#000000")

        for widget in save_entry_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg="#f0f0f0", fg="#000000")

        for widget in savestate_listbox_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg="#f0f0f0", fg="#000000")

        for widget in profile_listbox_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg="#f0f0f0", fg="#000000")

        for widget in config_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg="#f0f0f0", fg="#000000")



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
root.title("Bloodborne Save Organiser")

myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
root.iconbitmap("appicon.ico")

save_setup_frame = tk.Frame(root)
save_setup_frame.pack()

save_directory_label = tk.Label(save_setup_frame, text="Game Save Directory:")
save_directory_label.pack(anchor='w', padx=(10, 0))

save_entry_frame = tk.Frame(save_setup_frame)
save_entry_frame.pack()

save_entry = tk.Entry(save_entry_frame, width=50)
save_entry.pack(side='left', padx=(10, 10))
tk.Button(save_entry_frame, text="Browse", command=browse_save).pack(side='right', padx=(10, 10))

profile_setup_frame = tk.Frame(root)
profile_setup_frame.pack()

profile_directory_label = tk.Label(profile_setup_frame, text="Profile Directory:")
profile_directory_label.pack(anchor='w', padx=(10, 0))

profile_entry_frame = tk.Frame(profile_setup_frame)
profile_entry_frame.pack()

profile_entry = tk.Entry(profile_entry_frame, width=50)
profile_entry.pack(side='left', padx=(10, 10))
tk.Button(profile_entry_frame, text="Browse", command=browse_profile).pack(side='right', padx=(10, 10))

dark_mode_var = tk.BooleanVar(value=True)
global_hotkeys_enabled = tk.BooleanVar(value=False)

listboxes_frame = tk.Frame(root)
listboxes_frame.pack(fill='both', expand=True)

profile_listbox_frame = tk.Frame(listboxes_frame)
profile_listbox_frame.pack(side='left', padx=(0, 20), fill='both', expand=True)

savestate_listbox_frame = tk.Frame(listboxes_frame)
savestate_listbox_frame.pack(side='right', padx=(20, 0), fill='both',
                             expand=True)

profile_listbox_label = tk.Label(profile_listbox_frame, text="Profiles:")
profile_listbox_label.pack(side='top')

profile_listbox = tk.Listbox(profile_listbox_frame, height=15)
profile_listbox.pack(fill='both', padx=5, pady=5)

create_profile_button = tk.Button(profile_listbox_frame, text="Create Profile",
                                  command=lambda: profile_management.create_profile(profile_listbox, profile_entry))
create_profile_button.pack(fill='x', padx=5, pady=2)

delete_profile_button = tk.Button(profile_listbox_frame, text="Delete Profile",
                                  command=lambda: profile_management.delete_profile(profile_listbox,
                                                                                    savestate_listbox,
                                                                                    profile_entry))
delete_profile_button.pack(fill='x', padx=5, pady=2)

savestate_listbox_label = tk.Label(savestate_listbox_frame, text="Savestates:")
savestate_listbox_label.pack(side='top')

savestate_listbox = tk.Listbox(savestate_listbox_frame, height=15)
savestate_listbox.pack(fill='both', padx=5, pady=5)

create_savestate_button = tk.Button(savestate_listbox_frame, text="Create Savestate",
                                    command=lambda: save_management.create_savestate(root,
                                                                                     savestate_listbox,
                                                                                     profile_listbox,
                                                                                     profile_entry,
                                                                                     save_entry,
                                                                                     notification))
create_savestate_button.pack(fill='x', padx=5, pady=2)

load_savestate_button = tk.Button(savestate_listbox_frame, text="Load Savestate",
                                  command=lambda: save_management.load_selected_savestate(root,
                                                                                          profile_listbox,
                                                                                          savestate_listbox,
                                                                                          profile_entry,
                                                                                          save_entry,
                                                                                          notification))
load_savestate_button.pack(fill='x', padx=5, pady=2)

delete_savestate_button = tk.Button(savestate_listbox_frame, text="Delete Savestate",
                                    command=lambda: save_management.delete_savestate(root,
                                                                                     dark_mode_var,
                                                                                     profile_listbox,
                                                                                     savestate_listbox,
                                                                                     profile_entry,
                                                                                     notification))
delete_savestate_button.pack(fill='x', padx=5, pady=2)

config_frame = tk.Frame(root)
config_frame.pack()

dark_mode_button = tk.Button(config_frame, text="Switch to Light/Dark Mode", command=toggle_dark_mode)
dark_mode_button.pack(fill='x', padx=5, pady=2)

keybinds_button = tk.Button(config_frame, text="Set Keybinds",
                            command=lambda: config.open_config_window(root, dark_mode_var))
keybinds_button.pack(fill='x', padx=5, pady=2)

notification = tk.Label(root, text=f"")
notification.config()
notification.pack()

load_config()
root.after(100, profile_management.load_profiles(profile_listbox, profile_entry))
profile_listbox.bind("<ButtonRelease-1>", lambda event: save_management.update_savestates(root,
                                                                                          savestate_listbox,
                                                                                          profile_listbox,
                                                                                          profile_entry))

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    global_hotkeys_enabled.set(config_data["global_hotkeys_enabled"])
    load_save_keybind = config_data["load_save_keybind"]
    create_save_keybind = config_data["create_save_keybind"]
    config.set_keybinds(root, savestate_listbox, profile_listbox, profile_entry, save_entry, notification)

dark_mode_button.configure(command=lambda: toggle_dark_mode(profile_listbox, profile_entry))
keybinds_button.configure(command=lambda: config.open_config_window(root, dark_mode_var, savestate_listbox,
                                                                    profile_listbox, profile_entry, save_entry,
                                                                    notification))

root.mainloop()

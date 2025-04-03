import tkinter as tk
import save_management
import json
import keyboard

CONFIG_FILE = "config.json"


def toggle_global_keybinds(root, savestate_listbox, profile_listbox, profile_entry, save_entry, notification, toggle_button):
    with open(CONFIG_FILE, "r") as file:
        data = json.load(file)
        global_hotkeys_enabled = data.get("global_hotkeys_enabled")

        if global_hotkeys_enabled:
            data["global_hotkeys_enabled"] = False
            toggle_button.config(text="Global Hotkeys OFF")
        else:
            data["global_hotkeys_enabled"] = True
            toggle_button.config(text="Global Hotkeys ON")

        with open(CONFIG_FILE, "w") as file:
            json.dump(data, file)

        set_keybinds(root, savestate_listbox, profile_listbox, profile_entry, save_entry, notification)


def set_keybinds(root, savestate_listbox, profile_listbox, profile_entry, save_entry, notification):
    """Binds the configured keybinds for all functions on launch and when keybinds are remapped"""
    with open(CONFIG_FILE, "r") as file:
        data = json.load(file)

        load_save_keybind = data.get("load_save_keybind")
        create_save_keybind = data.get("create_save_keybind")
        global_hotkeys_enabled = data.get("global_hotkeys_enabled")

        if global_hotkeys_enabled:
            if load_save_keybind:
                root.unbind(load_save_keybind)
                keyboard.add_hotkey(load_save_keybind, lambda: root.after(10, save_management.load_selected_savestate,
                                                                          root, profile_listbox, savestate_listbox,
                                                                          profile_entry, save_entry, notification))

            if create_save_keybind:
                root.unbind(create_save_keybind)
                keyboard.add_hotkey(create_save_keybind, lambda: root.after(10, save_management.create_savestate,
                                                                            root, savestate_listbox, profile_listbox,
                                                                            profile_entry, save_entry, notification))
        else:
            try:
                keyboard.remove_all_hotkeys()
            except AttributeError:
                pass

            if load_save_keybind:
                root.bind(load_save_keybind, lambda event: root.after(10, save_management.load_selected_savestate,
                                                                      root, profile_listbox, savestate_listbox,
                                                                      profile_entry, save_entry, notification))

            if create_save_keybind:
                root.bind(create_save_keybind, lambda event: root.after(10, save_management.create_savestate,
                                                                        root, savestate_listbox, profile_listbox,
                                                                        profile_entry, save_entry, notification))


def record_keybind(root, savestate_listbox, profile_listbox, profile_entry,
                   save_entry, dark_mode_var, function, keybind_text, notification):
    """Opens a window that records a key press and saves it as a keybind."""
    keybind_window = tk.Toplevel(root)
    keybind_window.title("Record Keybind")
    keybind_window.geometry("300x150")
    keybind_window.config(bg="#2e2e2e" if dark_mode_var.get() else "#ffffff")

    keybind = tk.StringVar(value="Press any key...")

    tk.Label(keybind_window, text="Press a key to bind:", bg=keybind_window["bg"],
             fg="#ffffff" if dark_mode_var.get() else "#555555").pack(pady=10)

    keybind_entry = tk.Entry(keybind_window, textvariable=keybind, state="readonly", width=20)
    keybind_entry.pack(pady=5)

    def on_key(event):
        """Records the key press and updates the keybind entry."""
        keybind.set(event.keysym)
        keybind_window.after(500, keybind_window.destroy)

        with open("config.json", "r") as file:
            config_data = json.load(file)

        config_data[function] = keybind.get()

        with open("config.json", "w") as file:
            json.dump(config_data, file)

        set_keybinds(root, savestate_listbox, profile_listbox, profile_entry, save_entry, notification)

        keybind_text.set(keybind.get())

    keybind_window.bind("<KeyPress>", on_key)
    keybind_window.focus_force()


def open_config_window(root, dark_mode_var, savestate_listbox, profile_listbox,
                       profile_entry, save_entry, notification):
    """"Opens the keybind configuration window."""
    config_window = tk.Toplevel(root)
    config_window.title("Edit Config")

    config_window.config(bg="#2e2e2e" if dark_mode_var.get() else "#ffffff")

    with open(CONFIG_FILE, "r") as file:
        config_data = json.load(file)

        create_savestate_keybind = config_data.get("create_save_keybind", "None")
        create_savestate_keybind_text = tk.StringVar(value=create_savestate_keybind)

        create_savestate_keybind_label = tk.Label(config_window, text="Create Savestate", bg=config_window["bg"],
                                                  fg="#ffffff" if dark_mode_var.get() else "#555555")
        create_savestate_keybind_label.grid(row=0, column=0)

        create_savestate_keybind_entry = tk.Entry(config_window, textvariable=create_savestate_keybind_text,
                                                  state="disabled", width=20)
        create_savestate_keybind_entry.grid(row=0, column=1)

        create_savestate_keybind_button = tk.Button(config_window, text="Record Keybind",
                                                    command=lambda: record_keybind(root, savestate_listbox,
                                                                                   profile_listbox, profile_entry,
                                                                                   save_entry, dark_mode_var,
                                                                                   "create_save_keybind",
                                                                                   create_savestate_keybind_text,
                                                                                   notification),
                                                    bg="#555555",
                                                    fg="#ffffff")
        create_savestate_keybind_button.grid(row=0, column=2)

        load_savestate_keybind = config_data.get("load_save_keybind", "None")
        load_savestate_keybind_text = tk.StringVar(value=load_savestate_keybind)

        load_savestate_keybind_label = tk.Label(config_window, text="Load Savestate", bg=config_window["bg"],
                                                fg="#ffffff" if dark_mode_var.get() else "#555555")
        load_savestate_keybind_label.grid(row=1, column=0)

        load_savestate_keybind_entry = tk.Entry(config_window, textvariable=load_savestate_keybind_text,
                                                state="disabled", width=20)
        load_savestate_keybind_entry.grid(row=1, column=1)

        load_savestate_keybind_button = tk.Button(config_window, text="Record Keybind",
                                                  command=lambda: record_keybind(root, savestate_listbox,
                                                                                 profile_listbox, profile_entry,
                                                                                 save_entry, dark_mode_var,
                                                                                 "load_save_keybind",
                                                                                 load_savestate_keybind_text,
                                                                                 notification),
                                                  bg="#555555",
                                                  fg="#ffffff")
        load_savestate_keybind_button.grid(row=1, column=2)

        global_hotkey_toggle = tk.Button(config_window,
                                         text="Global Hotkeys ON" if config_data.get(
                                             "global_hotkeys_enabled") == True else "Global Hotkeys OFF",
                                         bg="#555555" if dark_mode_var.get() else "#f0f0f0",
                                         fg="#ffffff" if dark_mode_var.get() else "#000000",
                                         command=lambda: toggle_global_keybinds(root, savestate_listbox, profile_listbox, profile_entry, save_entry, notification, global_hotkey_toggle))
        global_hotkey_toggle.grid(row=2, column=0)

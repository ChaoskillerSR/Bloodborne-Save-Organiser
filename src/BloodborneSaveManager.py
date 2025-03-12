import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json
import os
import shutil
import ctypes

CONFIG_FILE = "config.json"


def record_keybind(function, keybind_text):
    """Opens a window that records a key press and saves it as a keybind."""
    keybind_window = tk.Toplevel(root)
    keybind_window.title("Record Keybind")
    keybind_window.geometry("300x150")
    keybind_window.config(bg="#2e2e2e" if dark_mode_var.get() else "#ffffff")

    keybind = tk.StringVar(value="Press any key...")

    tk.Label(keybind_window, text="Press a key to bind:", bg=keybind_window["bg"], fg="#ffffff" if dark_mode_var.get() else "#555555").pack(pady=10)

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

        set_keybinds()

        keybind_text.set(keybind.get())

    keybind_window.bind("<KeyPress>", on_key)
    keybind_window.focus_force()


def open_config_window():
    config_window = tk.Toplevel(root)
    config_window.title("Edit Config")

    config_window.config(bg="#2e2e2e" if dark_mode_var.get() else "#ffffff")

    with open(CONFIG_FILE, "r") as file:
        config_data = json.load(file)

        create_savestate_keybind = config_data.get("create_save_keybind", "None")
        create_savestate_keybind_text = tk.StringVar(value=create_savestate_keybind)

        create_savestate_keybind_label = tk.Label(config_window, text="Create Savestate", bg=config_window["bg"], fg="#ffffff" if dark_mode_var.get() else "#555555")
        create_savestate_keybind_label.grid(row=0, column=0)

        create_savestate_keybind_entry = tk.Entry(config_window, textvariable=create_savestate_keybind_text, state="disabled", width=20)
        create_savestate_keybind_entry.grid(row=0, column=1)

        create_savestate_keybind_button = tk.Button(config_window, text="Record Keybind", command=lambda: record_keybind(function="create_save_keybind", keybind_text=create_savestate_keybind_text), bg="#555555", fg="#ffffff")
        create_savestate_keybind_button.grid(row=0, column=2)

        load_savestate_keybind = config_data.get("load_save_keybind", "None")
        load_savestate_keybind_text = tk.StringVar(value=load_savestate_keybind)

        load_savestate_keybind_label = tk.Label(config_window, text="Load Savestate", bg=config_window["bg"], fg="#ffffff" if dark_mode_var.get() else "#555555")
        load_savestate_keybind_label.grid(row=1, column=0)

        load_savestate_keybind_entry = tk.Entry(config_window, textvariable=load_savestate_keybind_text, state="disabled", width=20)
        load_savestate_keybind_entry.grid(row=1, column=1)

        load_savestate_keybind_button = tk.Button(config_window, text="Record Keybind", command=lambda: record_keybind(function="load_save_keybind", keybind_text=load_savestate_keybind_text), bg="#555555", fg="#ffffff")
        load_savestate_keybind_button.grid(row=1, column=2)


def save_config():
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
    load_profiles()


def set_keybinds():
    with open(CONFIG_FILE, "r") as file:
        data = json.load(file)
        root.bind(data.get("load_save_keybind"), lambda event: load_selected_savestate())
        root.bind(data.get("create_save_keybind"), lambda event: create_savestate())


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


def toggle_dark_mode():
    """Toggles the dark mode state."""
    dark_mode_var.set(not dark_mode_var.get())
    apply_theme()
    save_config()


def browse_save():
    """Opens a directory dialog for the game save folder."""
    path = filedialog.askdirectory()
    if path:
        save_entry.delete(0, tk.END)
        save_entry.insert(0, path)
        save_config()


def browse_profile():
    """Opens a directory dialog for the profile folder."""
    path = filedialog.askdirectory()
    if path:
        profile_entry.delete(0, tk.END)
        profile_entry.insert(0, path)
        load_profiles()
        save_config()


def load_profiles():
    """Loads the list of available profiles."""
    profile_listbox.delete(0, tk.END)
    profile_dir = profile_entry.get()

    if os.path.exists(profile_dir):
        profiles = [f for f in os.listdir(profile_dir) if os.path.isdir(os.path.join(profile_dir, f))]
        for profile in profiles:
            profile_listbox.insert(tk.END, profile)


def create_profile():
    """Creates a new save profile folder."""
    profile_dir = profile_entry.get()
    if not profile_dir:
        messagebox.showerror("Error", "Set the profile directory first!")
        return

    profile_name = simpledialog.askstring("Create Profile", "Enter profile name:")
    if not profile_name:
        return

    new_profile_path = os.path.join(profile_dir, profile_name)
    if os.path.exists(new_profile_path):
        messagebox.showerror("Error", "Profile already exists!")
        return

    os.makedirs(new_profile_path)
    load_profiles()
    messagebox.showinfo("Success", f"Profile '{profile_name}' created!")


def delete_profile():
    """Deletes the selected profile folder."""
    selected_profile = profile_listbox.get(tk.ACTIVE)
    if not selected_profile:
        messagebox.showerror("Error", "Select a profile first!")
        return

    confirm = messagebox.askyesno("Delete Profile", f"Are you sure you want to delete '{selected_profile}'?")
    if not confirm:
        return

    profile_path = os.path.join(profile_entry.get(), selected_profile)
    shutil.rmtree(profile_path)
    load_profiles()
    savestate_listbox.delete(0, tk.END)
    messagebox.showinfo("Deleted", f"Profile '{selected_profile}' deleted.")


def update_savestates(event=None):
    """Ensures the savestate list updates when switching profiles."""
    root.after(100, load_savestates)


def load_savestates(event=None):
    """Loads savestates when a profile is selected."""
    savestate_listbox.delete(0, tk.END)

    try:
        selected_profile = profile_listbox.get(profile_listbox.curselection())
    except:
        return

    profile_path = os.path.join(profile_entry.get(), selected_profile)

    if os.path.exists(profile_path):
        savestates = [f for f in os.listdir(profile_path) if os.path.isdir(os.path.join(profile_path, f))]
        for save in savestates:
            savestate_listbox.insert(tk.END, save)


def create_savestate():
    """Creates a new savestate inside the selected profile."""
    selected_profile = profile_listbox.get(tk.ACTIVE)
    if not selected_profile:
        messagebox.showerror("Error", "Select a profile first!")
        return

    profile_path = os.path.join(profile_entry.get(), selected_profile)
    save_path = save_entry.get()

    if not os.path.exists(save_path):
        messagebox.showerror("Error", "Invalid save directory!")
        return

    savestate_name = simpledialog.askstring("Create Savestate", "Enter savestate name:")
    if not savestate_name:
        return

    savestate_path = os.path.join(profile_path, savestate_name)
    if os.path.exists(savestate_path):
        messagebox.showerror("Error", "Savestate already exists!")
        return

    shutil.copytree(save_path, savestate_path)
    update_savestates()
    messagebox.showinfo("Success", f"Savestate '{savestate_name}' created!")


def delete_savestate():
    """Deletes a selected savestate."""
    selected_profile = profile_listbox.get(tk.ACTIVE)
    selected_savestate = savestate_listbox.get(tk.ACTIVE)

    if not selected_profile or not selected_savestate:
        messagebox.showerror("Error", "Select a profile and a savestate first!")
        return

    confirm = messagebox.askyesno("Delete Savestate", f"Delete '{selected_savestate}'?")
    if not confirm:
        return

    savestate_path = os.path.join(profile_entry.get(), selected_profile, selected_savestate)
    shutil.rmtree(savestate_path)
    update_savestates()
    messagebox.showinfo("Deleted", f"Savestate '{selected_savestate}' deleted.")


def load_selected_savestate():
    """Loads the selected savestate into the game save folder."""
    selected_profile = profile_listbox.get(tk.ACTIVE)
    selected_savestate = savestate_listbox.get(tk.ACTIVE)

    if not selected_profile or not selected_savestate:
        messagebox.showerror("Error", "Select a profile and a savestate first!")
        return

    profile_path = os.path.join(profile_entry.get(), selected_profile)
    savestate_path = os.path.join(profile_path, selected_savestate)
    save_path = save_entry.get()

    if os.path.exists(save_path):
        shutil.rmtree(save_path)
        shutil.copytree(savestate_path, save_path)
        messagebox.showinfo("Success", f"Savestate '{selected_savestate}' loaded!")
    else:
        messagebox.showerror("Error", "Invalid game save directory!")

# ------------------------- GUI SETUP -------------------------

root = tk.Tk()
root.title("Bloodborne Save Manager")

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

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    load_save_keybind = config_data["load_save_keybind"]
    create_save_keybind = config_data["create_save_keybind"]
    set_keybinds()
keybinds_button = tk.Button(root, text="Set Keybinds", command=lambda: open_config_window())
keybinds_button.pack()

tk.Label(root, text="Profiles:").pack()
profile_listbox = tk.Listbox(root, height=5)
profile_listbox.pack()
profile_listbox.bind("<ButtonRelease-1>", update_savestates)

tk.Button(root, text="Create Profile", command=create_profile).pack()
tk.Button(root, text="Delete Profile", command=delete_profile).pack()

tk.Label(root, text="Savestates:").pack()
savestate_listbox = tk.Listbox(root, height=5)
savestate_listbox.pack()

tk.Button(root, text="Create Savestate", command=create_savestate).pack()
tk.Button(root, text="Delete Savestate", command=delete_savestate).pack()

load_config()

root.mainloop()

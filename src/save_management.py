import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import shutil


def update_savestates(root, savestate_listbox, profile_listbox, profile_entry):
    """Ensures the savestate list updates when switching profiles."""
    root.after(100, load_savestates(savestate_listbox, profile_listbox, profile_entry))


def load_savestates(savestate_listbox, profile_listbox, profile_entry):
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


def create_savestate(root, savestate_listbox, profile_listbox, profile_entry, save_entry, notification):
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
    if os.listdir(save_path) == ['1']:
        savestate_name = simpledialog.askstring("Create Savestate", "Enter savestate name:")
        if not savestate_name:
            return

        savestate_path = os.path.join(profile_path, savestate_name)
        if os.path.exists(savestate_path):
            messagebox.showerror("Error", "Savestate already exists!")
            return

        shutil.copytree(save_path, savestate_path)
        update_savestates(root, savestate_listbox, profile_listbox, profile_entry)
        notification.config(text=f"Savestate '{savestate_name}' created!")
    else:
        messagebox.showerror("Error", "Selected game save directory is not a Bloodborne save directory!")


def delete_savestate(root, dark_mode_var, profile_listbox, savestate_listbox, profile_entry, notification):
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
    update_savestates(root, savestate_listbox, profile_listbox, profile_entry)
    notification.config(text=f"Savestate '{selected_savestate}' deleted.")
    # root.after(3000, lambda: notification.config(text=""))


def load_selected_savestate(root, profile_listbox, savestate_listbox, profile_entry, save_entry, notification):
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
        # The save directory contains a single folder named "1", which I use to check if the folder is valid
        if os.listdir(save_path) == ['1']:
            shutil.rmtree(save_path)
            shutil.copytree(savestate_path, save_path)
            notification.config(text=f"Savestate '{selected_savestate}' loaded successfully!")
        else:
            messagebox.showerror("Error", "Selected game save directory is not a Bloodborne save directory!")
    else:
        messagebox.showerror("Error", "Invalid game save directory!")

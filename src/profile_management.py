import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import shutil


def load_profiles(profile_listbox, profile_entry):
    """Loads the list of available profiles."""
    profile_listbox.delete(0, tk.END)
    profile_dir = profile_entry.get()

    if os.path.exists(profile_dir):
        profiles = [f for f in os.listdir(profile_dir) if os.path.isdir(os.path.join(profile_dir, f))]
        for profile in profiles:
            profile_listbox.insert(tk.END, profile)


def create_profile(profile_listbox, profile_entry):
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
    load_profiles(profile_listbox, profile_entry)
    messagebox.showinfo("Success", f"Profile '{profile_name}' created!")


def delete_profile(profile_listbox, savestate_listbox, profile_entry):
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
    load_profiles(profile_listbox, profile_entry)
    savestate_listbox.delete(0, tk.END)
    messagebox.showinfo("Deleted", f"Profile '{selected_profile}' deleted.")

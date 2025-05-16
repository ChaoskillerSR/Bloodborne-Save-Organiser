import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os
import shutil
import time
import zipfile
import save_management

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


def export_profile(profile_listbox, profile_entry):
    selected_profile = profile_listbox.get(tk.ACTIVE)
    if not selected_profile:
        messagebox.showerror("Error", "Select a profile first!")
        return

    profile_path = os.path.join(profile_entry.get(), selected_profile)

    zip_path = tk.filedialog.asksaveasfilename(
        defaultextension=".zip",
        filetypes=[("Zip files", "*.zip")],
        title="Export Profile As...",
        initialfile=selected_profile + ".zip"
    )

    if not zip_path:
        return

    try:
        base_name = os.path.splitext(zip_path)[0]
        shutil.make_archive(base_name, 'zip', root_dir=profile_path)
        messagebox.showinfo("Success", f"Profile exported to:\n{base_name}.zip")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to export profile:\n{e}")


def import_profile(savestate_listbox, profile_listbox, profile_entry):
    import_zip = filedialog.askopenfilename()
    if not import_zip:
        return

    profiles_path = profile_entry.get()
    profile_name = os.path.splitext(os.path.basename(import_zip))[0]
    imported_profile_path = os.path.join(profiles_path, profile_name)
    temp_folder_suffix = time.strftime("%Y%m%d_%H%M%S")
    temp_folder = os.path.join(profiles_path, f"__import__{temp_folder_suffix}")

    os.mkdir(temp_folder)

    with zipfile.ZipFile(import_zip, 'r') as zip_ref:
        zip_ref.extractall(temp_folder)

    if os.path.isdir(imported_profile_path):
        for savestate in os.listdir(temp_folder):
            savestate_path = os.path.join(temp_folder, savestate)
            if not os.path.isdir(savestate_path):
                continue

            try:
                shutil.copytree(savestate_path, os.path.join(imported_profile_path, savestate))

            except FileExistsError:
                count = 1
                while True:
                    if os.path.isdir(os.path.join(imported_profile_path, f"{savestate}({count})")):
                        count += 1
                    else:
                        shutil.copytree(savestate_path, os.path.join(imported_profile_path, f"{savestate}({count})"))
                        break

    else:
        shutil.copytree(temp_folder, imported_profile_path)

    shutil.rmtree(temp_folder)
    load_profiles(profile_listbox, profile_entry)
    profile_names = profile_listbox.get(0, tk.END)
    if profile_name in profile_names:
        index = profile_names.index(profile_name)
        profile_listbox.selection_clear(0, tk.END)
        profile_listbox.selection_set(index)
        profile_listbox.activate(index)
        profile_listbox.see(index)
    save_management.load_savestates(savestate_listbox, profile_listbox, profile_entry)
    messagebox.showinfo("Success", f"Profile {profile_name} imported successfully!")

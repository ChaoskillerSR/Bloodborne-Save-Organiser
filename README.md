# Bloodborne Save Manager  

**NOTE:** This program can be falsely flagged as malware by antivirus software, as it can modify files (copy, paste, and overwrite when loading saves). However, the program is **perfectly safe to use**.

The **Bloodborne Save Manager** is designed to help players efficiently manage their save files for **Bloodborne**. It provides an easy-to-use interface for **backing up, restoring, and organizing multiple game saves**, allowing users to:  

- Switch between different progress states.  
- Practice specific areas and bosses.  
- Retry sections of the game effortlessly.  

---

## Features  

### **Profile-Based Save Management**  
- Players can create separate profiles, each containing different sets of save files.  
- Profiles help in organizing **multiple playthroughs, character builds, or progression states**.  

### **Save State Backup and Loading**  
- Users can create savestates (snapshots of their current save files) within a selected profile.  
- At any time, a savestate can be loaded back into the game, restoring progress to a previous point.  
- Savestates are stored as **complete copies** of the save directory, ensuring no data loss.  

---

## How It Works  

### **Setup Save and Profile Directories**  
1. To run the program, run **bloodborne_save_manager.exe** inside of the **dist** folder.
2. On first launch, select:  
   - The **game’s save directory** (typically found inside `user/savedata` within your `ShadPS4` folder).  
   - A **profile directory** (any folder of your choice).  
3. These paths are stored in the **configuration file (`config.json`)** for future sessions.  

### **Creating and Managing Profiles**  
- Click **"Create Profile"** to make a new profile folder.  
- Each profile acts as a **container** for different game save backups, useful for creating categories or groups of savestates.  

### **Saving and Restoring Progress**  
- Select a profile and click **"Create Savestate"** to make a snapshot of your current save.  
- Select a saved state and click **"Load Savestate"** to restore the selected save.  
- Click **"Delete Savestate"** to remove an unwanted save.  

### **Theme Customization**  
- Click the theme toggle button to switch between Dark Mode and Light Mode.  
- The app remembers your preference for future launches.  

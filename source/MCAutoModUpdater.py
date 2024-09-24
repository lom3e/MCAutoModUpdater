import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os
import requests

# Get user's profile path
user_profile = os.getenv("USERPROFILE")

# Default Minecraft mods folder path
MODS_FOLDER = os.path.join(user_profile, "AppData", "Roaming", ".minecraft", "mods")

# Dictionary of mod names and their Modrinth IDs
MODS = {
    "Continuity": "continuity",
    "Fabric API": "fabric-api",
    "Indium": "indium",
    "Iris Fabric": "iris",
    "Malilib Fabric": "malilib",
    "MiniHUD Fabric": "minihud",
    "Sodium Extra Fabric": "sodium-extra",
    "Tweakeroo Fabric": "tweakeroo",
    "WI Zoom": "wi-zoom",
    "Dynamic Lights": "dynamic-lights",  
}

# List of Minecraft versions from 1.7 onwards (no snapshots)
MINECRAFT_VERSIONS = [
    "1.21.1", "1.21", "1.20.6", "1.20.5", "1.20.4", "1.20.3", "1.19.4", "1.19.3",
    "1.19.2", "1.19", "1.18.2", "1.18.1", "1.18", "1.17.1", "1.17", "1.16.5", 
    "1.16.4", "1.16.3", "1.16.2", "1.16.1", "1.16", "1.15.2", "1.15.1", "1.14.4", 
    "1.14.3", "1.14.2", "1.14.1", "1.13.2", "1.13.1", "1.13", "1.12.2", "1.12.1", 
    "1.12", "1.11.2", "1.11.1", "1.11", "1.10.2", "1.9.4", "1.9", "1.8.9", 
    "1.8.8", "1.8.7", "1.8.6", "1.7.10", "1.7.9", "1.7.8", "1.7.2"
]

# Platforms
MOD_PLATFORMS = ["Fabric", "Forge", "Quilt", "NeoForge"]

# Function to check for the latest mod version on Modrinth
def check_latest_version(mod_id, target_version, platform):
    response = requests.get(f"https://api.modrinth.com/v2/project/{mod_id}/version")
    if response.status_code == 200:
        versions = response.json()
        compatible_version = None
        
        sorted_versions = sorted(versions, key=lambda v: v["version_number"], reverse=True)
        
        for version in sorted_versions:
            minecraft_versions = version['game_versions']
            loaders = version['loaders']
            if target_version in minecraft_versions and platform.lower() in loaders:
                return version  # Return the exact version if found
            elif not compatible_version and any(v < target_version for v in minecraft_versions):
                compatible_version = version  # Keep track of the latest compatible version
        
        if compatible_version:
            use_previous_version = messagebox.askyesno(
                "Version Not Available",
                f"The version {target_version} is not available for {mod_id}. Would you like to use the previous version ({compatible_version['version_number']})?"
            )
            if use_previous_version:
                return compatible_version  # User accepted the previous version
            else:
                return None  # User declined the previous version
        else:
            print(f"No compatible version found for {mod_id}.")
            return None
    else:
        print(f"Error fetching data for mod {mod_id}.")
        return None

# Function to download and save the mod
def download_mod(mod_info, mod_name):
    download_url = mod_info["files"][0]["url"]
    filename = mod_info["files"][0]["filename"]
    response = requests.get(download_url)

    if not os.path.exists(MODS_FOLDER):
        os.makedirs(MODS_FOLDER)

    with open(os.path.join(MODS_FOLDER, filename), "wb") as f:
        f.write(response.content)
    print(f"{mod_name} updated to version {mod_info['version_number']}.")

# Function to update selected mods
def update_mods(selected_mods, target_version, platform):
    for mod_name, mod_id in MODS.items():
        if selected_mods[mod_name].get():
            latest_version = check_latest_version(mod_id, target_version, platform)
            if latest_version:
                download_mod(latest_version, mod_name)
            else:
                print(f"Mod {mod_name} not updated for version {target_version}.")
    messagebox.showinfo("Update", "Mod update completed!")

# Function to select the mods folder
def select_mod_folder():
    global MODS_FOLDER
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        MODS_FOLDER = folder_selected
        print(f"Mods folder selected: {MODS_FOLDER}")

# GUI Creation with modernized interface
def create_gui():
    root = tk.Tk()
    root.title("Minecraft Auto Mod Updater")
    root.iconbitmap("Icona-ridimensionata.ico")
    root.configure(bg="#3c3f41")
    root.geometry("500x600")

    style = ttk.Style()
    
    # Configure button style (rounded corners and black text)
    style.configure("TButton", padding=6, relief="flat", background="#61afef", foreground="black", borderwidth=1)
    style.map("TButton", background=[("active", "#4da3db")])
    
    # Adding rounded corners to buttons (via element option in ttk if supported by OS)
    style.element_create("RoundedButton", "from", "clam")
    style.layout("RoundedButton.TButton", 
                 [('Button.button', {'children': [('Button.padding', 
                 {'children': [('Button.label', {'sticky': 'nswe'})], 'sticky': 'nswe'})], 'sticky': 'nswe'})])
    
    # Configure other elements like labels and checkbuttons
    style.configure("TLabel", background="#3c3f41", foreground="white", font=("Arial", 12))
    style.configure("TCheckbutton", background="#3c3f41", foreground="white", font=("Arial", 10), focuscolor="none")
    
    # Combobox with rounded corners
    style.configure("TCombobox", padding=5, relief="flat", fieldbackground="#e0e0e0", borderwidth=1)
    style.map("TCombobox", fieldbackground=[("readonly", "#e0e0e0")], background=[("active", "#cccccc")])
    
    # Main title
    title_label = ttk.Label(root, text="Minecraft Auto Mod Updater", font=("Arial", 16, "bold"))
    title_label.pack(pady=20)

    # Minecraft version selection
    ttk.Label(root, text="Select Minecraft Version:").pack(pady=10)

    version_var = tk.StringVar()
    version_combobox = ttk.Combobox(root, textvariable=version_var, font=("Arial", 10), width=15, state="readonly")  # Set state to readonly
    version_combobox['values'] = MINECRAFT_VERSIONS  # Specific version list
    version_combobox.pack(pady=5)
    version_combobox.current(0)  # Default version selection

    # Mod platform selection
    ttk.Label(root, text="Select Mod Platform:").pack(pady=10)

    platform_var = tk.StringVar()
    platform_combobox = ttk.Combobox(root, textvariable=platform_var, font=("Arial", 10), width=15, state="readonly")  # Set state to readonly
    platform_combobox['values'] = MOD_PLATFORMS
    platform_combobox.pack(pady=5)
    platform_combobox.current(0)  # Default platform selection

    # Mods folder selection button
    select_folder_button = ttk.Button(root, text="Select mods folder", command=select_mod_folder, style="RoundedButton.TButton")
    select_folder_button.pack(pady=15)

    # Mod selection
    ttk.Label(root, text="Select mods to update:").pack(pady=10)

    selected_mods = {mod: tk.BooleanVar() for mod in MODS}

    mods_frame = tk.Frame(root, bg="#3c3f41")
    mods_frame.pack(pady=10)

    for mod_name in MODS:
        ttk.Checkbutton(mods_frame, text=mod_name, variable=selected_mods[mod_name]).pack(anchor='w')

    # Mod update button
    update_button = ttk.Button(root, text="Update mods", command=lambda: update_mods(selected_mods, version_var.get(), platform_var.get()), style="RoundedButton.TButton")
    update_button.pack(pady=20)

    root.mainloop()

# Entry point
if __name__ == "__main__":
    create_gui()

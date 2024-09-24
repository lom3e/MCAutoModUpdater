
---

# Minecraft Auto Mod Updater

**Minecraft Auto Mod Updater** is a Python application with a graphical user interface (GUI) that automates the process of updating Minecraft mods. Users can select their Minecraft version and mod platform (Fabric, Forge, Quilt, NeoForge) and automatically download the latest compatible mod versions.

## Features

- Select your Minecraft version (from 1.7 up to the latest stable release).
- Supports multiple modding platforms: **Fabric**, **Forge**, **Quilt**, and **NeoForge**.
- Checks for the latest mod versions using the [Modrinth](https://modrinth.com/) API.
- Option to use a previous version of the mod if the exact version isn't available.
- Allows users to choose their mods folder for flexible mod management.
- Simple, modern GUI with rounded elements.

## How It Works

1. **Select Minecraft Version**: Choose your target version from a dropdown list of all major Minecraft releases (no snapshots).
2. **Select Modding Platform**: Choose the modding platform you're using (Fabric, Forge, Quilt, NeoForge).
3. **Select Mods to Update**: Pick the mods you'd like to update from a list of popular mods.
4. **Automatic Download**: The app automatically checks for the latest compatible versions of each selected mod and downloads them to your mods folder.

## Setup and Installation

### Prerequisites

- **Python 3.x** installed on your system.
- Required Python libraries (install using `pip`):
  ```bash
  pip install requests tkinter
  ```

### Running the Application

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/lom3e/MCAutoModUpdater.git
   ```

2. Navigate to the project folder

3. Run the program: Click on the file MCAutoModUpdater.exe

## Usage

1. Run the app and select the **Minecraft version** and **modding platform**.
2. Choose the mods you wish to update.
3. Select your mods folder if it's different from the default Minecraft mods folder.
4. Click the "Update mods" button to automatically download and update the mods.

## Customizing

- You can add more mods by editing the `MODS` dictionary in the code and adding the corresponding Modrinth project ID.

## Contributions

Contributions are welcome! Feel free to submit issues or pull requests to improve the functionality or add new features.

## License

This project is licensed under the MIT License.

---

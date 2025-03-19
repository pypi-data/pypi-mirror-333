import os
import sys
import subprocess
import platform

# Windows-specific imports
if sys.platform.startswith("win"):
    import ctypes
    import winreg

# Paths
ICON_PATH = os.path.join(os.path.dirname(__file__), "icon.ico")  # Path to the icon file
INTERPRETER_PATH = sys.executable  # Path to Python interpreter

def register_qx_file_windows():
    """Register .qx file association on Windows."""
    try:
        # Check for admin privileges
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("Please run as administrator to register file associations on Windows.")
            return False

        # Register .qx extension
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, ".qx") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "QuantumXFile")

        # Set friendly name for the file type
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "QuantumXFile") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "QuantumX Source File")

        # Set the icon for .qx files
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"QuantumXFile\DefaultIcon") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, ICON_PATH)

        # Set the open command
        with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"QuantumXFile\shell\open\command") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f'"{INTERPRETER_PATH}" -m quantumx "%1"')

        print("QuantumX .qx file association registered successfully on Windows!")
        return True
    except Exception as e:
        print(f"Error registering file association on Windows: {e}")
        return False

def register_qx_file_linux():
    """Register .qx file association on Linux using xdg utilities."""
    try:
        # Ensure xdg-mime and xdg-icon-resource are available
        if not shutil.which("xdg-mime") or not shutil.which("xdg-icon-resource"):
            print("Error: 'xdg-mime' and 'xdg-icon-resource' are required. Install 'xdg-utils' package.")
            return False

        # Define paths for Linux
        home_dir = os.path.expanduser("~")
        mime_dir = os.path.join(home_dir, ".local/share/mime/packages")
        applications_dir = os.path.join(home_dir, ".local/share/applications")
        icons_dir = os.path.join(home_dir, ".local/share/icons/hicolor/48x48/apps")

        # Create directories if they don't exist
        os.makedirs(mime_dir, exist_ok=True)
        os.makedirs(applications_dir, exist_ok=True)
        os.makedirs(icons_dir, exist_ok=True)

        # Define MIME type for .qx files
        mime_xml = """
        <?xml version="1.0" encoding="UTF-8"?>
        <mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
            <mime-type type="application/x-quantumx">
                <comment>QuantumX Source File</comment>
                <glob pattern="*.qx"/>
            </mime-type>
        </mime-info>
        """
        mime_file = os.path.join(mime_dir, "application-x-quantumx.xml")
        with open(mime_file, "w") as f:
            f.write(mime_xml)

        # Create a .desktop file for QuantumX
        desktop_entry = f"""
        [Desktop Entry]
        Type=Application
        Name=QuantumX
        Exec={INTERPRETER_PATH} -m quantumx %F
        Icon=quantumx
        Terminal=false
        MimeType=application/x-quantumx;
        """
        desktop_file = os.path.join(applications_dir, "quantumx.desktop")
        with open(desktop_file, "w") as f:
            f.write(desktop_entry)

        # Copy the icon to the appropriate location (48x48 is a common size for desktop icons)
        icon_dest = os.path.join(icons_dir, "quantumx.ico")
        if os.path.exists(ICON_PATH):
            shutil.copyfile(ICON_PATH, icon_dest)
        else:
            print(f"Warning: Icon file {ICON_PATH} not found. Skipping icon installation.")

        # Update the MIME database
        subprocess.run(["xdg-mime", "install", mime_file], check=True)
        subprocess.run(["xdg-mime", "default", "quantumx.desktop", "application/x-quantumx"], check=True)

        # Update the icon cache
        if os.path.exists(icon_dest):
            subprocess.run(["xdg-icon-resource", "install", "--size", "48", icon_dest, "quantumx"], check=True)

        # Update the desktop database
        subprocess.run(["update-desktop-database", os.path.join(home_dir, ".local/share/applications")], check=True)

        print("QuantumX .qx file association registered successfully on Linux!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running xdg commands on Linux: {e}")
        return False
    except Exception as e:
        print(f"Error registering file association on Linux: {e}")
        return False

def main():
    """Register .qx file association based on the platform."""
    if sys.platform.startswith("win"):
        register_qx_file_windows()
    elif sys.platform.startswith("linux"):
        register_qx_file_linux()
    else:
        print(f"Platform {sys.platform} not supported for file association.")

if __name__ == "__main__":
    main()

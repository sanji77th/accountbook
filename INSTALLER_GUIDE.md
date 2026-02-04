# How to Create the AccountBook Installer

Since this is a Windows application, we use the industry-standard **Inno Setup** to create a professional `Setup.exe` installer.

### Prerequisites
1.  **Build the EXE first**:
    ```bash
    python build_exe.py
    ```
    Ensure `dist/AccountBook.exe` exists.

2.  **Install Inno Setup**:
    - Download and install [Inno Setup](https://jrsoftware.org/isdl.php).

### Steps to Compile Installer
1.  **Right-click** on the file `setup.iss` in this folder.
2.  Select **Compile**.
3.  Wait for the process to finish.
4.  The installer will be generated in the `Output` folder named `AccountBook_Setup.exe`.

### What the Installer Does
- Installs `AccountBook.exe` to the user's `AppData\Local\Programs` folder (no Admin rights needed by default).
- Creates a **Desktop Shortcut**.
- Creates a **Start Menu** entry.
- Adds an uninstaller in Control Panel.

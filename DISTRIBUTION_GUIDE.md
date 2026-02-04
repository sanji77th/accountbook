# How to Distribute "AccountBook" to Outsiders

You have successfully compiled the installer! Here is how to give it to others.

## What to Send
You only need to send **ONE** file:
> `Output/AccountBook_Setup.exe`

## How the User Installs It
1.  **Receive File**: The user downloads the `AccountBook_Setup.exe` you sent them.
2.  **Run Installer**: They double-click the file.
    - They will be asked where to save it (e.g., `C:\Users\Name\AppData\Local\Programs\AccountBook`).
    - They can choose to create a Desktop Shortcut.
3.  **Launch**: They double-click the **AccountBook** icon on their desktop.

## Common Questions describing the "Outsider" Experience

**Q: Do they need Python installed?**
A: **No.** The installer contains everything needed (Python, Flask, Libraries) inside it.

**Q: Do they need to install a database?**
A: **No.** The application automatically creates a fresh `accounting.db` file the first time they run it.

**Q: What if they want to uninstall it?**
A: They can go to **Control Panel > Programs and Features** and uninstall "AccountBook" just like any other Windows app.

**Q: Can they share data with me?**
A: Yes. If they want to send you their data, they should send you the `accounting.db` file located in their installation folder.

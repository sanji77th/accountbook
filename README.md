# AccountBook

**AccountBook** is a professional, local desktop accounting application featuring double-entry bookkeeping, role-based access control, and a modern dashboard.

---

## 🚀 Setup & Installation

### 1. Developer Setup (Running from source)
If you are a developer and want to run the project locally:
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the App**:
    ```bash
    python main.py
    ```
    - The first time you run this, a `.env` file will be created in your project folder.
    - Default Admin: `admin` / `admin1234`

---

### 2. User Installation (Using the Installer)
If you have received the `AccountBook_Setup.exe` installer:
1.  Run the installer and follow the on-screen instructions.
2.  Once installed, launch **AccountBook** from your Desktop or Start Menu.
3.  The installation folder will stay clean—no configuration files will clutter your program directory.

---

## ⚙️ Configuration (Post-Installation)

AccountBook stores its data and security settings in a hidden system folder to keep your installation professional and clean.

### Where is my data?
To find your database, logs, or change your password:
1.  Press `Win + R` on your keyboard.
2.  Type **`%APPDATA%\AccountBook`** and press Enter.
3.  Inside this folder, you will find:
    - **`accounting.db`**: Your local database file.
    - **`.env`**: Your security configuration.
    - **`app_debug.log`**: Technical logs (useful for troubleshooting).

### Changing the Admin Password
To change the main Admin password after installation:
1.  Navigate to the `%APPDATA%\AccountBook` folder.
2.  Open the **`.env`** file with Notepad.
3.  Change the `ADMIN_PASSWORD` value and Save.
4.  Restart the application.

---

## 📦 Building the Project

This project is ready for professional distribution.

1.  **Generate EXE**: Run `python build_exe.py` to package the app into the `dist` folder.
2.  **Generate Installer**: Open `setup.iss` with **Inno Setup** and click **Compile**.
    - This creates a professional Windows installer in the `Output` folder.

---

## 🌟 Key Features
- **Clean Interface**: Professional dark-mode dashboard with real-time charting.
- **Double-Entry Engine**: Every transaction automatically generates balanced Journal Entries.
- **User Management**: Admins can create and manage Accountant accounts.
- **Role-Based Security**: Accountants can record transactions; Admins can edit rules and manage staff.
- **Privacy-First**: All data is stored locally on your machine—never in the cloud.

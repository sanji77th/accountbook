# AccountBook

**AccountBook** is a professional, local desktop accounting application featuring double-entry bookkeeping, role-based access control, and a modern dashboard.

---

##  Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
python main.py
```
This will:
- Initialize the database (`accounting.db`) automatically.
- Open your default web browser to `http://127.0.0.1:5000`.

### 3. Log In
Use these default credentials:
- **Admin**: `admin` / `admin123`
- **Accountant**: `user` / `user123`

---

## 📦 Building the Installer (setup.iss)

This project includes a **`setup.iss`** file, which is a configuration script for **Inno Setup**.

**Inno Setup** is a free tool used to create professional Windows installers (`.exe`). The `setup.iss` script in this repository is pre-configured to:
1.  Package the compiled `AccountBook.exe`.
2.  Create a standard Windows Installation Wizard.
3.  Add Desktop Shortcuts and Start Menu entries.
4.  Handle Uninstallation automatically.

### How to use it:
1.  Run `python build_exe.py` to generate the standalone executable in the `dist/` folder.
2.  Open `setup.iss` with Inno Setup Compiler.
3.  Click **Compile** to generate the final `Option/AccountBook_Setup.exe` installer.

---

## 🌟 Features
- **Dashboard**: View real-time income/expense charts.
- **Double-Entry Engine**: Transactions are automatically converted to Journal Entries.
- **Role-Based Access**: Admins control data; Accountants can only view.
- **Reporting**: Full Ledger, Journal, and Drill-down Account functionality.
- **Security**: Local SQLite database and role-based permissions.

# AccountBook

**AccountBook** is a professional, local desktop accounting application featuring double-entry bookkeeping, role-based access control, and a modern dashboard.

---

## 📚 Documentation
We have detailed guides for everything you need:

| Guide | Description |
| :--- | :--- |
| **[User Manual](USER_MANUAL.md)** | **For End Users**. How to login, record transactions, and start reporting. |
| **[Distribution Guide](DISTRIBUTION_GUIDE.md)** | **For You**. How to share the app with outsiders (just send one file!). |
| **[Installer Guide](INSTALLER_GUIDE.md)** | **For Developers**. How to build the professional Windows Installer (`setup.exe`). |
| **[Icon Guide](ICON_GUIDE.md)** | How to customize the application icon. |
| **[Project Structure](PROJECT_STRUCTURE.md)** | Technical breakdown of every file in the codebase. |

---

## 🚀 Quick Start (for Developers)

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

### 4. Build EXE
To create a standalone executable:
```bash
python build_exe.py
```
To create the **Installer**, follow the [Installer Guide](INSTALLER_GUIDE.md).

---

## 🌟 Features
- **Dashboard**: View real-time income/expense charts.
- **Double-Entry Engine**: Transactions are automatically converted to Journal Entries.
- **Role-Based Access**: Admins control data; Accountants can only view.
- **Reporting**: Full Ledger, Journal, and Drill-down Account functionality.
- **Security**: Local SQLite database and role-based permissions.

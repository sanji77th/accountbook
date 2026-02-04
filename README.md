# AccountBook

**AccountBook** is a professional, local desktop accounting application featuring double-entry bookkeeping, role-based access control, and a modern dashboard.

---

## 🚀 Setup Instructions

Follow these steps to set up the application for the first time.

### 1. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
The application uses a `.env` file to store sensitive configuration like the **Admin Password**.

1. Create a file named **`.env`** in the root directory of the project.
2. Add the following content to the file:
```text
# Main Admin Credentials
ADMIN_PASSWORD=your_secure_password_here

# Flask Secret Key (Random string for security)
SECRET_KEY=any_random_long_string_here
```
> [!IMPORTANT]
> The `ADMIN_PASSWORD` you set here will be the password for the `admin` account. The application will always prioritize this password.

### 3. Run the Application
```bash
python main.py
```
This will:
- Initialize the database (`accounting.db`) automatically.
- Open your default web browser to `http://127.0.0.1:5000`.

### 4. Manage Users
Once logged in as **`admin`**, you can go to the **Users** tab to create accounts for other staff members (Accountants). These users are managed in-app and saved to the database.

---

## 📦 Building the Installer (setup.iss)

This project includes a **`setup.iss`** file for creating a professional Windows installer using **Inno Setup**.

1. Run `python build_exe.py` to generate the standalone executable.
2. Compile `setup.iss` using Inno Setup to create the final installer.

---

## 🌟 Features
- **Dashboard**: Real-time income/expense charting.
- **Double-Entry Engine**: Automated journalizing.
- **Role-Based Access**: Admins manage users and data; Accountants have restricted access.
- **Reporting**: Full Ledger and Journal with date filtering.
- **Security**: Environment-based Admin authentication and hashed database passwords for others.

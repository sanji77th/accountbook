# Vibe Accounting App

## Quick Start

### 1. Install Dependencies
If you haven't already:
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

### 4. Build EXE (Optional)
To create a standalone executable for distribution:
```bash
python build_exe.py
```
The `.exe` will be located in the `dist/` folder.

## Features
- **Dashboard**: View real-time income/expense charts.
- **Transactions**: Double-entry bookkeeping.
- **Rules**: Map transaction types to debit/credit accounts.
- **Journal**: View the general ledger.
- **Dark Mode**: Toggle in the top bar.

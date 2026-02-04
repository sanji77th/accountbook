# AccountBook User Manual

**Version**: 1.0  
**Last Updated**: February 2026

---

## 1. Introduction
Welcome to **AccountBook**, your professional desktop accounting solution. This application helps you track income, expenses, and automated double-entry journal records in a secure, local environment.

## 2. Getting Started

### Launching the App
Double-click the **AccountBook** icon on your Desktop. The application will open in your default web browser automatically.

### Login
Enter your credentials to access the dashboard. There are two types of users:

| Role | Username | Password (Default) | Access Level |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `admin123` | **Full Access**: Can Edit/Delete transactions, manage Rules, and export data. |
| **Accountant** | `user` | `user123` | **Restricted**: Can Record transactions and View reports. Cannot Delete or Edit. |

> **Note**: Your administrator may have changed these passwords.

---

## 3. Dashboard
The Dashboard gives you a real-time financial snapshot:
- **Total Income**: Sum of all Sales/Revenue.
- **Total Expenses**: Sum of all expenses.
- **Net Profit**: Income minus Expenses.
- **Charts**: Visual breakdown of your finances.
- **Recent Activity**: The 5 most recent transactions.

---

## 4. Managing Transactions

### Recording a New Transaction
1. Go to the **Transactions** tab.
2. Fill in the form:
   - **Description**: What happened? (e.g., "Sold Services to Client X").
   - **Amount**: The value in dollars.
   - **Type**: Choose the category (e.g., Sales, Expense, Salary).
     * *Note: The "Type" determines which accounts are Debited and Credited automatically.*
3. Click **Record Transaction**.

### Editing a Transaction (Admin Only)
1. In the **Transaction History** list, find the row you want to change.
2. Click the **Blue Pen Icon**.
3. Update the Description, Amount, Date, or Type.
4. Click **Update**.
   * *Warning: Changing the Type will regenerate the Journal Entries for this transaction.*

### Deleting a Transaction (Admin Only)
1. Click the **Red Trash Icon** next to any transaction.
2. Confirm the warning. This will remove the transaction and its associated Journal Entries.

### Exporting Data
Click the **Export CSV** button at the top of the history table to download an Excel-compatible file.

---

## 5. Reports & Auditing

### General Journal
- Accessible via the **Journal** tab.
- Shows the raw **Debit** and **Credit** lines for every transaction.
- Use the **Date Filter** at the top to see records for a specific month or year.

### Ledger (Account Summary)
- Accessible via the **Ledger** tab.
- Shows a list of all accounts (e.g., Cash, Inventory, Sales Revenue) and their current balances.
- **Drill-Down**: Click on any **Account Name** (e.g., "Cash") to see a detailed statement of every transaction affecting that account, along with a running balance.

---

## 6. Administration (Admin Only)

### Rules Engine
Go to the **Rules** tab. Here you define how the automation works:
- **Transaction Type**: The name that appears in the dropdown (e.g., "Internet Bill").
- **Debit Account**: The account that increases (e.g., "Utilities Expense").
- **Credit Account**: The account that decreases (e.g., "Cash").

### Server Control
To close the application properly, click the **Shutdown Server** link at the bottom of the page. This ensures the database is saved safely before closing.

---

## 7. Troubleshooting

**Q: The browser didn't open automatically.**  
A: Open your web browser and type `http://127.0.0.1:5000` in the address bar.

**Q: I can't see the Edit button.**  
A: Ensure you are logged in as `admin`. The `user` account is read-only for history.

**Q: How do I backup my data?**  
A: Copy the `accounting.db` file from the application folder to a safe location (like a USB drive).

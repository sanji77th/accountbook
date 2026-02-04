from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify, Response
from flask_login import login_user, logout_user, login_required, current_user
import functools
from extensions import db
from models import User, Transaction, Rule, JournalEntry
from datetime import datetime
import os
import signal
import csv
import io

main_bp = Blueprint('main', __name__)

def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
@login_required
def dashboard():
    sales = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.transaction_type == 'Sales').scalar() or 0
    expenses = db.session.query(db.func.sum(Transaction.amount)).filter(Transaction.transaction_type == 'Expense').scalar() or 0
    
    recent_transactions = Transaction.query.order_by(Transaction.date.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                           income=sales, 
                           expense=expenses, 
                           recent_transactions=recent_transactions)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user:
            is_correct = user.check_password(password)
            if is_correct:
                login_user(user)
                return redirect(url_for('main.dashboard'))
            else:
                flash('Invalid password', 'danger')
        else:
            flash('User not found in database', 'danger')
    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main_bp.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    rules = Rule.query.all()
    
    # Date Filtering
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Transaction.query
    if start_date:
        query = query.filter(Transaction.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Transaction.date <= datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))
        
    if request.method == 'POST':
        try:
            desc = request.form.get('description')
            amount = float(request.form.get('amount'))
            t_type = request.form.get('type')
            
            rule = Rule.query.filter_by(transaction_type=t_type).first()
            if not rule:
                flash('Invalid transaction type', 'danger')
                return redirect(url_for('main.transactions'))

            new_tx = Transaction(
                description=desc,
                amount=amount,
                transaction_type=t_type,
                created_by=current_user.id
            )
            db.session.add(new_tx)
            db.session.flush()

            dr_entry = JournalEntry(transaction_id=new_tx.id, account=rule.debit_account, debit=amount, credit=0)
            cr_entry = JournalEntry(transaction_id=new_tx.id, account=rule.credit_account, debit=0, credit=amount)
            
            db.session.add(dr_entry)
            db.session.add(cr_entry)
            db.session.commit()
            flash('Transaction recorded successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    all_tx = query.order_by(Transaction.date.desc()).all()
    return render_template('transactions.html', transactions=all_tx, rules=rules, start_date=start_date, end_date=end_date)

@main_bp.route('/delete_transaction/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_transaction(id):
    tx = Transaction.query.get_or_404(id)
    try:
        db.session.delete(tx)
        db.session.commit()
        flash('Transaction deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting transaction.', 'danger')
        
    return redirect(request.referrer or url_for('main.transactions'))

@main_bp.route('/rules', methods=['GET', 'POST'])
@login_required
@admin_required
def rules():
    if request.method == 'POST':
        t_type = request.form.get('transaction_type')
        dr = request.form.get('debit_account')
        cr = request.form.get('credit_account')
        
        if Rule.query.filter_by(transaction_type=t_type).first():
            flash('Rule already exists for this type', 'warning')
        else:
            new_rule = Rule(transaction_type=t_type, debit_account=dr, credit_account=cr)
            db.session.add(new_rule)
            db.session.commit()
            flash('Rule added.', 'success')
            
    all_rules = Rule.query.all()
    return render_template('rules.html', rules=all_rules)

@main_bp.route('/journal')
@login_required
def journal():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = JournalEntry.query.join(Transaction)
    
    if start_date:
        query = query.filter(JournalEntry.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(JournalEntry.date <= datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))

    entries = query.order_by(JournalEntry.date.desc()).all()
    return render_template('journal.html', entries=entries, start_date=start_date, end_date=end_date)

@main_bp.route('/edit_transaction/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_transaction(id):
    tx = Transaction.query.get_or_404(id)
    rules = Rule.query.all()
    
    if request.method == 'POST':
        try:
            # Update basic fields
            tx.description = request.form.get('description')
            tx.amount = float(request.form.get('amount'))
            new_type = request.form.get('type')
            new_date_str = request.form.get('date')
            tx.date = datetime.strptime(new_date_str, '%Y-%m-%dT%H:%M')
            
            # If Type changed or simple update, easier to regenerate journal entries
            # Check if type changed
            type_changed = (tx.transaction_type != new_type)
            tx.transaction_type = new_type
            
            # Fetch Rule
            rule = Rule.query.filter_by(transaction_type=new_type).first()
            if not rule:
                 flash('Invalid transaction type', 'danger')
                 return render_template('edit_transaction.html', transaction=tx, rules=rules)

            # Regenerate Journal Entries
            # Delete old entries
            JournalEntry.query.filter_by(transaction_id=tx.id).delete()
            
            # Create new entries
            dr_entry = JournalEntry(
                transaction_id=tx.id, 
                account=rule.debit_account, 
                debit=tx.amount, 
                credit=0,
                date=tx.date
            )
            cr_entry = JournalEntry(
                transaction_id=tx.id, 
                account=rule.credit_account, 
                debit=0, 
                credit=tx.amount,
                date=tx.date
            )
            
            db.session.add(dr_entry)
            db.session.add(cr_entry)
            db.session.commit()
            flash('Transaction updated successfully.', 'success')
            return redirect(url_for('main.transactions'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating transaction: {str(e)}', 'danger')

    return render_template('edit_transaction.html', transaction=tx, rules=rules)

# --- USER MANAGEMENT ---
@main_bp.route('/users')
@login_required
@admin_required
def users():
    # Only show 'accountant' users, or all users. Let's show all except myself maybe?
    # Or just show all.
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

@main_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'accountant')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
        else:
            try:
                new_user = User(username=username, role=role)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                flash(f'User {username} created successfully.', 'success')
                return redirect(url_for('main.users'))
            except Exception as e:
                flash(f'Error creating user: {str(e)}', 'danger')
                
    return render_template('create_user.html')

@main_bp.route('/delete_user/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.username == 'admin':
        flash('Cannot delete the Admin user.', 'danger')
        return redirect(url_for('main.users'))
        
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
    except Exception as e:
        flash(f'Error deleting user: {str(e)}', 'danger')
    return redirect(url_for('main.users'))

@main_bp.route('/ledger')
@login_required
def ledger():
    # Account Summary View
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = db.session.query(
        JournalEntry.account,
        db.func.sum(JournalEntry.debit).label('total_debit'),
        db.func.sum(JournalEntry.credit).label('total_credit')
    )
    
    if start_date:
        query = query.filter(JournalEntry.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(JournalEntry.date <= datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))
        
    results = query.group_by(JournalEntry.account).order_by(JournalEntry.account).all()
    
    accounts = []
    for row in results:
        net = row.total_debit - row.total_credit
        accounts.append({
            'name': row.account,
            'debit': row.total_debit,
            'credit': row.total_credit,
            'balance': net
        })
        
    return render_template('ledger.html', accounts=accounts, start_date=start_date, end_date=end_date)

@main_bp.route('/ledger/<path:account_name>')
@login_required
def account_details(account_name):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = JournalEntry.query.join(Transaction).filter(JournalEntry.account == account_name)
    
    if start_date:
        query = query.filter(JournalEntry.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(JournalEntry.date <= datetime.strptime(end_date + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))
    
    # Order by date
    entries = query.order_by(JournalEntry.date.asc(), JournalEntry.id.asc()).all()
    
    # Calculate Running Balance
    running_balance = 0.0
    entry_data = []
    
    for entry in entries:
        # Simple heuristic: Debits increase balance, Credits decrease (Asset nature).
        # OR: Just show Dr - Cr.
        # Let's assume Dr is positive, Cr is negative for visual simplicity.
        net = entry.debit - entry.credit
        running_balance += net
        entry_data.append({
            'obj': entry,
            'balance': running_balance
        })
        
    # Reverse for display if desired (showing newest first), but running balance makes sense chronologically.
    # Let's show Chronological (Oldest First) for Ledger, or Newest First?
    # Standard Bank Statements are Newest First, but Running Balance is calculated Oldest First.
    # We will display Chronological (Oldest at top) or Newest at top with correct balance.
    # Let's do Newest at top, but we calculated strictly chronological.
    
    entry_data.reverse()

    return render_template('account_details.html', 
                           account_name=account_name, 
                           entries=entry_data, 
                           start_date=start_date, 
                           end_date=end_date)

@main_bp.route('/export/<type>')
@login_required
def export_csv(type):
    output = io.StringIO()
    writer = csv.writer(output)
    
    if type == 'transactions':
        writer.writerow(['ID', 'Date', 'Description', 'Type', 'Amount', 'Created By'])
        items = Transaction.query.all()
        for i in items:
            writer.writerow([i.id, i.date, i.description, i.transaction_type, i.amount, i.created_by])
            
    elif type == 'journal':
        writer.writerow(['ID', 'Transaction ID', 'Date', 'Account', 'Debit', 'Credit'])
        items = JournalEntry.query.order_by(JournalEntry.date.desc()).all()
        for i in items:
            writer.writerow([i.id, i.transaction_id, i.date, i.account, i.debit, i.credit])
            
    elif type == 'ledger':
        writer.writerow(['Account', 'Total Debit', 'Total Credit', 'Net Balance'])
        results = db.session.query(
            JournalEntry.account,
            db.func.sum(JournalEntry.debit).label('total_debit'),
            db.func.sum(JournalEntry.credit).label('total_credit')
        ).group_by(JournalEntry.account).all()
        for row in results:
            writer.writerow([row.account, row.total_debit, row.total_credit, row.total_debit - row.total_credit])
            
    else:
        return "Invalid type", 400

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={type}_{datetime.now().strftime('%Y%m%d')}.csv"}
    )

@main_bp.route('/shutdown', methods=['POST'])
@login_required
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    return 'Server shutting down...'

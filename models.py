from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='accountant') # 'admin' or 'accountant'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(100), unique=True, nullable=False)
    debit_account = db.Column(db.String(100), nullable=False)
    credit_account = db.Column(db.String(100), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(100), db.ForeignKey('rule.transaction_type'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationship to Journal Entries
    journal_entries = db.relationship('JournalEntry', backref='transaction', lazy=True, cascade="all, delete-orphan")

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    account = db.Column(db.String(100), nullable=False)
    debit = db.Column(db.Float, default=0.0)
    credit = db.Column(db.Float, default=0.0)
    date = db.Column(db.DateTime, default=datetime.utcnow)

def init_db_data():
    from datetime import timedelta
    import random
    
    # Helper to create initial data
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
    
    if not User.query.filter_by(username='user').first():
        user = User(username='user', role='accountant')
        user.set_password('user123')
        db.session.add(user)

    # Default Rules
    default_rules = [
        ('Sales', 'Cash', 'Sales Revenue'),
        ('Expense', 'General Expense', 'Cash'),
        ('Purchase', 'Inventory', 'Accounts Payable'),
        ('Salary', 'Salary Expense', 'Cash'),
        ('Rent', 'Rent Expense', 'Cash')
    ]
    
    existing_rules = {}
    for t_type, dr, cr in default_rules:
        rule = Rule.query.filter_by(transaction_type=t_type).first()
        if not rule:
            rule = Rule(transaction_type=t_type, debit_account=dr, credit_account=cr)
            db.session.add(rule)
        existing_rules[t_type] = rule
    
    # Commit users and rules first
    db.session.commit()

    # Generate Sample Transactions if none exist
    if Transaction.query.count() == 0:
        print("Generating sample data...")
        admin_user = User.query.filter_by(username='admin').first()
        base_date = datetime.utcnow() - timedelta(days=30)
        
        sample_data = [
            ('Sales', 1000, 5000),
            ('Expense', 50, 200),
            ('Purchase', 500, 2000),
            ('Salary', 2000, 2000),
            ('Rent', 1500, 1500)
        ]

        for _ in range(20):
            t_type, min_amt, max_amt = random.choice(sample_data)
            days_offset = random.randint(0, 30)
            tx_date = base_date + timedelta(days=days_offset)
            amount = round(random.uniform(min_amt, max_amt), 2)
            
            rule = Rule.query.filter_by(transaction_type=t_type).first()
            if not rule: 
                # Fallback refetch
                rule = Rule.query.filter_by(transaction_type=t_type).first()

            desc = f"Sample {t_type} #{random.randint(100, 999)}"
            
            new_tx = Transaction(
                date=tx_date,
                description=desc,
                amount=amount,
                transaction_type=t_type,
                created_by=admin_user.id
            )
            db.session.add(new_tx)
            db.session.flush()

            # Debit
            db.session.add(JournalEntry(
                transaction_id=new_tx.id,
                account=rule.debit_account,
                debit=amount,
                credit=0,
                date=tx_date
            ))
            # Credit
            db.session.add(JournalEntry(
                transaction_id=new_tx.id,
                account=rule.credit_account,
                debit=0,
                credit=amount,
                date=tx_date
            ))
        
        db.session.commit()

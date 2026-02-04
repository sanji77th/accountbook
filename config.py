import os
import sys
from dotenv import load_dotenv

# Detect if we are running as a bundled EXE or regular Python
if getattr(sys, 'frozen', False):
    # Use AppData for persistent storage (DB, .env)
    appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
    basedir = os.path.join(appdata, 'AccountBook')
    if not os.path.exists(basedir):
        os.makedirs(basedir)
else:
    basedir = os.path.abspath(os.path.dirname(__file__))

env_path = os.path.join(basedir, '.env')
# Load env; if missing, we'll create it in main.py
load_dotenv(env_path, override=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'AccountBookDefaultSecret_9988'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin1234')
    
    BASE_DIR = basedir
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'accounting.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.path.join(basedir, '.env')
load_dotenv(env_path, override=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key_super_secret_123'
    BASE_DIR = basedir
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'accounting.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

import sys
import os
import webbrowser
from threading import Timer
from flask import Flask
from config import Config
from extensions import db, login_manager
from models import init_db_data, User
from routes import main_bp

def create_app():
    if getattr(sys, 'frozen', False):
        # PyInstaller Mode
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        static_folder = os.path.join(sys._MEIPASS, 'static')
        app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    else:
        # Dev Mode
        app = Flask(__name__)

    app.config.from_object(Config)
    
    # Patch database URI for frozen app to store DB in AppData or local folder instead of temp
    if getattr(sys, 'frozen', False):
        # Use executable directory for DB
        exe_dir = os.path.dirname(sys.executable)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(exe_dir, 'accounting.db')

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_blueprint(main_bp)

    with app.app_context():
        # Create DB if not exists
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if not os.path.exists(db_path):
            db.create_all()
            init_db_data()
            print("Database initialized.")

    return app

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
    app = create_app()

    # Timer to open browser to prevent blocking
    if not os.environ.get("WERKZEUG_RUN_MAIN"): 
        Timer(1.5, open_browser).start()

    app.run(debug=False, port=5000)

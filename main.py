import sys
import os
import webbrowser
from threading import Timer
from flask import Flask
import logging
from config import Config
from extensions import db, login_manager
from models import init_db_data, User
from routes import main_bp

# Set up logging to AppData directory
log_path = os.path.join(Config.BASE_DIR, 'app_debug.log')
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

logging.info("--- App Starting ---")
logging.info(f"Data and Log directory: {Config.BASE_DIR}")

# Ensure a default .env exists in the data directory if missing
env_path = os.path.join(Config.BASE_DIR, '.env')
if not os.path.exists(env_path):
    with open(env_path, 'w') as f:
        f.write("# Admin Credentials - Change these for security!\n")
        f.write("ADMIN_PASSWORD=admin1234\n")
        f.write("SECRET_KEY=secure_key_placeholder_789\n")
    logging.info(f"Created default .env at {env_path}")
    # Reload environment after creation
    from dotenv import load_dotenv
    load_dotenv(env_path, override=True)

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
    
    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_blueprint(main_bp)

    with app.app_context():
        try:
            # Ensure database and core data (Admin user) exist
            logging.info("Checking/Creating database tables...")
            db.create_all()
            logging.info("Initializing database data (rules/admin)...")
            init_db_data()
            logging.info("Initialization complete.")
        except Exception as e:
            logging.exception("FAILED TO INITIALIZE DATABASE:")

    return app

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000')

if __name__ == '__main__':
    app = create_app()

    # Timer to open browser to prevent blocking
    if not os.environ.get("WERKZEUG_RUN_MAIN"): 
        Timer(1.5, open_browser).start()

    app.run(debug=False, port=5000)

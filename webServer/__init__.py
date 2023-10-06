from flask import Flask
from flask_login import LoginManager
from sorm.orm import ORM
from .authHandling.sessions import Session
import os



db = ORM()

def create_app(CONFIG_TYPE=None):
    # Create the Flask app object
    app = Flask(__name__)

    # Load the config file
    if not CONFIG_TYPE:
        CONFIG_TYPE = os.getenv(
            'CONFIG_TYPE',
            default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)
    
    # Set up the database
    SETTINGS = {
            'type': app.config['DB_TYPE'],
            'databaseURI': app.config['DATABASE_URI'],
            'isolation_level': app.config['ISOLATION_LEVEL']
        }  
    db.config(SETTINGS)

    # Set up the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # Set up the session manager
    sess = Session()
    sess.init_app(app)
    
    # Import the User model
    from .models import User
    # Set up the user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id)[0]

    # Import and register the blueprints
    from .webManagement.admin.core import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .webManagement.auth.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .webManagement.manageData import mangData as manageData_blueprint
    app.register_blueprint(manageData_blueprint)

    from .pythonInterface.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .codeManagement.gitUpdate import gitUpdate as gitUpdate_blueprint
    app.register_blueprint(gitUpdate_blueprint, url_prefix='/gitUpdate')

    from .mandelbrot.mandelbrotPages import mandelbrot as mandelbrot_blueprint
    app.register_blueprint(mandelbrot_blueprint, url_prefix='/mandelbrot')

    return app

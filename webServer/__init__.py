# init.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 

from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from config import Config 
import os


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app(CONFIG_TYPE=None):
    app = Flask(__name__)

    if not CONFIG_TYPE:
        CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)

    db.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
 

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .webManagement.admin.core import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    
    from .webManagement.auth.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .webManagement.manageData import mangData as manageData_blueprint
    app.register_blueprint(manageData_blueprint)
    
    from .pythonInterface.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    from .codeManagement.gitUpdate import gitUpdate as gitUpdate_blueprint
    app.register_blueprint(gitUpdate_blueprint, url_prefix='/gitUpdate')


    return app
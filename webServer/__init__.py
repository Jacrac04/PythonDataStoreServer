# init.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 

from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    
    admin = Admin(app, name='Admin', template_mode='bootstrap3')

    from .models import User
    from .pythonInterface.models import PythonData
    from .dataManagment.models import PythonDataAuthTokens

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(PythonData, db.session))
    admin.add_view(ModelView(PythonDataAuthTokens, db.session))
    # # blueprint for auth routes in our app
    from .webManagement.auth.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .pythonInterface.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')


    return app
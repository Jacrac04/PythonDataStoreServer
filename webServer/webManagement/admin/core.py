from flask_admin.contrib.sqla import ModelView 
from flask_admin import Admin, AdminIndexView
import flask_login as login
from ... import db
from ...models import User, PythonData, PythonDataAuthTokens, Project
from flask import url_for, redirect, request
import flask_login as login
from flask import Blueprint

class AdminBlueprint(Blueprint):
    views=None

    def __init__(self,*args, **kargs):
        self.views = []
        return super(AdminBlueprint, self).__init__('admin2', __name__,url_prefix='/admin2',static_folder='static', static_url_path='/static/admin')

    def add_view(self, view):
        self.views.append(view)

    def register(self,app, options, first_registration=False):
        admin = Admin(app, name='Admin', template_mode='bootstrap3', index_view=HomeAdminView())

        for v in self.views:
            admin.add_view(v)

        return super(AdminBlueprint, self).register(app, options)



class PythonDataView(ModelView):
    form_columns = ['id', 'name', 'dataJson', 'authTokens','project']
    def is_accessible(self):
        if login.current_user.is_authenticated:
            return login.current_user.is_admin
        return False
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))
    
class UserView(ModelView):
    form_columns = ['id', 'email', 'password', 'name', 'admin', 'projects']
    def is_accessible(self):
        if login.current_user.is_authenticated:
            return login.current_user.is_admin
        return False
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))

class PythonDataAuthTokensView(ModelView):
    form_columns = ['id', 'authToken', 'tokenType', 'pythonData']
    def is_accessible(self):
        if login.current_user.is_authenticated:
            return login.current_user.is_admin
        return False
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))

class ProjectView(ModelView):
    form_columns = ['id', 'name', 'pythonData', 'owner']
    def is_accessible(self):
        if login.current_user.is_authenticated:
            return login.current_user.is_admin
        return False
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))
    
class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        if login.current_user.is_authenticated:
            return login.current_user.is_admin
        return False
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login', next=request.url))
    
# with app.app_context():
admin = AdminBlueprint(name='admin', url_prefix='/admin')
admin.add_view(UserView(User, db.session))
admin.add_view(PythonDataView(PythonData, db.session))
admin.add_view(PythonDataAuthTokensView(PythonDataAuthTokens, db.session))           
admin.add_view(ProjectView(Project, db.session))   
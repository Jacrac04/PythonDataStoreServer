from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask import Blueprint, render_template
from ...models import Project, PythonData, PythonDataAuthTokens, User
from webServer.authHandling.loginUtils import admin_required

admin = Blueprint('admin', __name__, 
                  url_prefix='/admin',
                  template_folder='templates',
                  static_folder='static',)


@admin.route('/')
@admin_required
def index():
    
    return render_template('admin_home.html')

# A route to display all users
# Admin only
@admin.route('/users', methods=['GET'])
@admin_required
def users():
    # Get all users
    users = User.query.filter_by()
    # Render the manageUsers page
    return render_template('manageUsers.html', users=users)

# A route to delete a user
# Admin only
@admin.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    # Get the user to delete
    user = User.query.filter_by(id=user_id).first()
    # Delete all projects, data and AuthTokens associated with the user
    for project in user.projects:
        for data in project.pythonData:
            for token in data.authTokens:
                PythonDataAuthTokens.query.delete(id=token.id)
            PythonData.query.delete(id=data.id)
        Project.query.delete(id=project.id)
    # Delete the user
    User.query.delete(id=user_id)
    # Redirect to the manageUsers page
    return redirect(url_for('admin.users'))

# A route to toggle a user's admin status
# Admin only
@admin.route('/users/<int:user_id>/toggleAdmin', methods=['POST'])
@admin_required
def toggle_admin(user_id):
    # Get the user to toggle
    user = User.query.filter_by(id=user_id).first()
    # Toggle the user's admin status
    if user.admin:
        user.admin = False
    else:
        user.admin = True
    # redirect to the manageUsers page
    return redirect(url_for('admin.users'))


# A route to display all projects
# Admin only
@admin.route('/projects', methods=['GET'])
@admin_required
def projects():
    # Get all projects 
    projects = Project.query.filter_by()
    # Render and return the manageDataHome.html template
    return render_template('manageProjects.html', projects=projects)


# A route to delete a project
# Admin only
@admin.route('/projects/<int:project_id>/delete', methods=['POST'])
@admin_required
def delete_project(project_id):
    # Get the project to delete
    project = Project.query.filter_by(id=project_id).first()
    # Delete all data and AuthTokens associated with the project
    for data in project.pythonData:
        for token in data.authTokens:
            PythonDataAuthTokens.query.delete(id=token.id)
        PythonData.query.delete(id=data.id)            
    # Delete the project
    Project.query.delete(id=project_id)
    # Redirect to the manageDataHome page
    return redirect(url_for('admin.projects'))

# A route to display all data
# Admin only
@admin.route('/data', methods=['GET'])
@admin_required
def data():
    # Get all data
    datas = PythonData.query.filter_by()
    # Render and return the manageData.html template
    return render_template('manageData.html', datas=datas)


# A route to delete a data
# Admin only
@admin.route('/data/<int:data_id>/delete', methods=['POST'])
@admin_required
def delete_data(data_id):
    # Get the data to delete
    data = PythonData.query.filter_by(id=data_id).first()
    # Delete all AuthTokens associated with the data
    for token in data.authTokens:
        PythonDataAuthTokens.query.delete(id=token.id)
    # Delete the data
    PythonData.query.delete(id=data_id)
    # Redirect to the manageData page
    return redirect(url_for('admin.data'))

# A route to display all authTokens
# Admin only
@admin.route('/authTokens', methods=['GET'])
@admin_required
def authTokens():
    # Get all authTokens
    tokens = PythonDataAuthTokens.query.filter_by()
    # Render and return the manageAuthTokens.html template
    return render_template('manageAuthTokens.html', tokens=tokens)


# A route to delete a authToken
# Admin only
@admin.route('/authTokens/<int:token_id>/delete', methods=['POST'])
@admin_required
def delete_token(token_id):
    # Get the authToken to delete
    PythonDataAuthTokens.query.delete(id=token_id)
    # Redirect to the manageAuthTokens page
    return redirect(url_for('admin.authTokens'))

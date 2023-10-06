from flask import Blueprint, render_template, redirect, url_for, request, flash
from ..models import PythonData, PythonDataAuthTokens, Project
from webServer.authHandling.loginUtils import current_user, login_required
from wtforms import Form, StringField, SelectField, validators
from wtforms.widgets import TextArea
from webServer import db


# Create a form class for the project form
class ProjectForm(Form):
    # Create a string field for the project name
    # It has a minimum length of 1 and a maximum length of 50
    name = StringField('Name', [validators.Length(min=1, max=50)])
    # Create a string field for the project description
    # It has a minimum length of 1 and a maximum length of 1000
    # It uses a TextArea widget which when rendered has a bigger area to edit
    description = StringField(
        'Description', [
            validators.Length(
                min=1, max=1000)], widget=TextArea())

# Create a form class for the data form
class DataForm(Form):
    # Create a string field for the data name
    # It has a minimum length of 1 and a maximum length of 50
    name = StringField('Name', [validators.Length(min=1, max=50)])
    # Create a string field for the data description
    # It has a minimum length of 1 and a maximum length of 1000
    # It uses a TextArea widget which when rendered has a bigger area to edit
    dataJson = StringField(
        'DataJson', [
            validators.Length(
                min=1, max=10000)], widget=TextArea())


# Create a form class for the auth token form
class AuthTokenForm(Form):
    # A temp variable used as the id for the select field
    counter = 1
    # Create a string field for the auth token name
    # It has a minimum length of 1 and a maximum length of 50
    name = StringField('Name', [validators.Length(min=1, max=50)])
    # Create a string field for the auth token
    # It has a minimum length of 1 and a maximum length of 50
    authToken = StringField('Token', [validators.Length(min=1, max=50)])
    # Define the choices for the auth token type select field
    choices = ['r', 'a', 'w', 'a+']
    # Create a select field for the auth token type
    # It uses the choices defined above
    # It uses the temp variable as the id however this is changed in the __init__ method
    tokenType = SelectField('Token Type', choices=choices, id=f"form{counter}")

    def __init__(self, *args, **kwargs):
        # Call the parent class's __init__ method
        Form.__init__(self, *args, **kwargs)
        # Change the id of the select field to select + the id passed in
        self.tokenType.id = f"select{kwargs['id']}"
        # Pop the id from the kwargs
        kwargs.pop('id')
        # Increment the temp variable
        self.counter += 1


mangData = Blueprint(
    'manageData',
    __name__,
    template_folder='templates',
    static_folder='static')


# Add a route to the manage data blueprint
@mangData.route('/projects')
@login_required
def projects():
    # Get all projects owned by the current user from the database
    projects = Project.query.filter_by(ownerId=current_user.id)
    # Render and return the manageDataHome.html template
    return render_template('manageDataHome.html', projects=projects)


# Add a route to the manage data blueprint
# The route takes a parameter of project_id which is found in the URL
@mangData.route('/projects/<int:project_id>', methods=['GET', 'POST'])
@login_required
def project(project_id):
    # The project_id is used to get the project from the database
    project = Project.query.filter_by(id=project_id).first()
    # If the project does not belong to the current user, redirect to the projects page
    if project.owner != current_user:
        flash('You do not have permission to view this project', 'danger')
        return redirect(url_for('manageData.projects'))
    # Create a form object from the ProjectForm class
    form = ProjectForm(request.form)
    # If the request method is POST and the form is valid, update the project
    if request.method == 'POST' and form.validate():
        project.name = form.name.data
        project.description = form.description.data
        # db.session.commit()
        # Flash a success message
        flash('Project updated', 'success')
        # Redirect to the project's with the project_id page
        return redirect(url_for('manageData.project', project_id=project_id))
    # Set the form's data to the project's data
    form.name.data = project.name
    form.description.data = project.description
    # Render and return the manageDataProject.html template
    return render_template(
        'manageDataProject.html',
        form=form,
        project=project)


# Add a route to the manage data blueprint
# The route takes a parameter of data_id which is found in the URL
@mangData.route('/data/<int:data_id>', methods=['GET', 'POST'])
@login_required
def data(data_id):
    # The data_id is used to get the data from the database
    data = PythonData.query.filter_by(id=data_id).first()
    # If the data does not belong to the current user, redirect to the projects page
    if data.project.owner != current_user:
        flash('You do not have permission to view this data', 'danger')
        return redirect(url_for('manageData.projects'))
    # Create a form object from the DataForm class
    form = DataForm(request.form)
    # Create a dictionary of form objects from the AuthTokenForm class
    forms = dict()
    # For each auth token in the data, create a form object and add it to the dictionary
    for dataAuthToken in data.authTokens:
        x = AuthTokenForm(request.form, id=dataAuthToken.id)
        x.tokenType.data = dataAuthToken.tokenType
        forms[dataAuthToken.id] = x
    # If the request method is POST and the form is valid, update the data
    if request.method == 'POST':
        data.name = form.name.data
        data.dataJson = form.dataJson.data
        flash('Data updated', 'success')
        return redirect(url_for('manageData.data', data_id=data_id))
    # Set the form's data to the data's data
    form.name.data = data.name
    form.dataJson.data = data.dataJson
    # Render and return the manageDataData.html template
    return render_template(
        'manageDataData.html',
        form=form,
        forms=forms,
        data=data)


@mangData.route('/projects/new', methods=['GET', 'POST'])
@login_required
def createProject():
    # Create a form object from the ProjectForm class
    form = ProjectForm(request.form)
    # If the request method is POST and the form is valid, create the project
    if request.method == 'POST' and form.validate():
        # Get the data from the form
        name = form.name.data
        description = form.description.data
        # Create a project object
        project = Project(
            name=name,
            ownerId=current_user.id,
            description=description)
        # db.session.add(project)
        # db.session.commit()
        # Flash a success message and redirect to the projects page
        flash('Project created', 'success')
        return redirect(url_for('manageData.projects'))
    # Render and return the editDataProject.html template in create mode
    return render_template('editDataProject.html', form=form, keyword='Create')


@mangData.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def editProject(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if project.owner != current_user:
        flash('You do not have permission to edit this project', 'danger')
        return redirect(url_for('manageData.projects'))
    form = ProjectForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        description = form.description.data
        project.name = name
        project.description = description
        # db.session.commit()
        flash('Project edited', 'success')
        return redirect(url_for('manageData.projects'))
    form.name.data = project.name
    form.description.data = project.description
    return render_template('editDataProject.html', form=form, keyword='Edit')


# Add a route to the manage data blueprint
# The route takes a parameter of project_id which is found in the URL
@mangData.route('/projects/<int:project_id>/newData', methods=['GET', 'POST'])
@login_required
def createData(project_id):
    # Get the project from the database
    project = Project.query.filter_by(id=project_id).first()
    # If the project does not belong to the current user, redirect to the projects page
    if project.owner != current_user:
        flash('You do not have permission to add data to this project', 'danger')
        return redirect(url_for('manageData.projects'))
    # Create a form object from the DataForm class
    form = DataForm(request.form)
    # If the request method is POST and the form is valid, create the data
    if request.method == 'POST' and form.validate():
        # Get the data from the form
        name = form.name.data
        dataJson = form.dataJson.data
        # Create a data object
        data = PythonData(name=name, dataJson=dataJson, projectId=project_id)
        # db.session.add(data)
        # db.session.commit()
        # Flash a success message and redirect to the data page
        flash('Data created', 'success')
        return redirect(url_for('manageData.data', data_id=data.id))
    # Render and return the editDataData.html template in create mode
    return render_template('editDataData.html', form=form, keyword='Create')


@mangData.route('/data/<int:data_id>/edit', methods=['GET', 'POST'])
@login_required
def editData(data_id):
    data = PythonData.query.filter_by(id=data_id).first()
    if data.project.owner != current_user:
        flash('You do not have permission to view this data', 'danger')
        return redirect(url_for('manageData.projects'))
    form = DataForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        dataJson = form.dataJson.data
        data.name = name
        data.dataJson = dataJson
        # db.session.commit()
        flash('Data edited', 'success')
        return redirect(
            url_for(
                'manageData.project',
                project_id=data.projectId))
    form.name.data = data.name
    form.dataJson.data = data.dataJson
    return render_template('editDataData.html', form=form, keyword='Edit')


@mangData.route('/authToken/<int:authToken_id>', methods=['GET', 'POST'])
@login_required
def authToken(authToken_id):
    authToken = PythonDataAuthTokens.query.filter_by(id=authToken_id).first()
    if authToken.data.project.owner != current_user:
        flash('You do not have permission to view this authToken', 'danger')
        return redirect(url_for('manageData.projects'))
    return render_template('manageDataAuthToken.html', authToken=authToken)


# Delete AuthToken
# Add a route to the manage data blueprint
# The route takes a parameter of authToken_id whicj is found in the url
@mangData.route('/authToken/<int:authToken_id>/delete', methods=['POST'])
@login_required
def deleteAuthToken(authToken_id):
    # Get the authToken from the database
    authToken = PythonDataAuthTokens.query.filter_by(id=authToken_id).first()
    # Check if the authToken's project owner is the current user
    if authToken.pythonData.project.owner != current_user:
        # If not, flash a message and redirect to the projects page
        flash('You do not have permission to delete this authToken', 'danger')
        return redirect(url_for('manageData.projects'))
    # Delete the authToken from the database
    PythonDataAuthTokens.query.delete(id=authToken_id)
    # Flash a message and redirect to the previous page
    flash('AuthToken deleted', 'success')
    return redirect(request.referrer)

# Delete Data
# Add a route to the manage data blueprint
# The route takes a parameter of data_id which is found in the url
@mangData.route('/data/<int:data_id>/delete', methods=['POST'])
@login_required
def deleteData(data_id):
    # Get the data from the database
    data = PythonData.query.filter_by(id=data_id).first()
    # Check if the data's project owner is the current user
    if data.project.owner != current_user:
        # If not, flash a message and redirect to the projects page
        flash('You do not have permission to delete this data', 'danger')
        return redirect(url_for('manageData.projects'))
    # Loop through the data's authTokens and delete them
    for authToken in data.authTokens:
        PythonDataAuthTokens.query.delete(id=authToken.id)
    # Delete the data from the database
    PythonData.query.delete(id=data_id)
    # Flash a message and redirect to the previous page
    flash('Data deleted', 'success')
    return redirect(request.referrer)

# Delete Project
# Add a route to the manage data blueprint
# The route takes a parameter of project_id which is found in the url
@mangData.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def deleteProject(project_id):
    # Get the project from the database
    project = Project.query.filter_by(id=project_id).first()
    # Check if the project's owner is the current user
    if project.owner != current_user:
        # If not, flash a message and redirect to the projects page
        flash('You do not have permission to delete this project', 'danger')
        return redirect(url_for('manageData.projects'))
    # Loop through the project's data
    for data in project.pythonData:
        # Loop through the data's authTokens and delete them
        for authToken in data.authTokens:
            PythonDataAuthTokens.query.delete(id=authToken.id)
        # Delete the data from the database
        PythonData.query.delete(id=data.id)
    # Delete the project from the database
    Project.query.delete(id=project_id)
    # Flash a message and redirect to the projects page
    flash('Project deleted', 'success')
    return redirect(url_for('manageData.projects'))

@mangData.route('/authToken/<int:authToken_id>/update', methods=['POST'])
@login_required
def updateAuthToken(authToken_id):
    authToken = PythonDataAuthTokens.query.filter_by(id=authToken_id).first()
    if authToken.pythonData.project.owner != current_user:
        flash('You do not have permission to update this authToken', 'danger')
        return redirect(url_for('manageData.projects'))
    authToken.tokenType = request.form['tokenType']
    # db.session.commit()
    flash('AuthToken updated', 'success')
    return redirect(request.referrer)

@mangData.route('/data/<int:data_id>/new', methods=['POST'])
@login_required
def createAuthToken(data_id):
    data = PythonData.query.filter_by(id=data_id).first()
    if data.project.owner != current_user:
        flash(
            'You do not have permission to create an authToken for this data',
            'danger')
        return redirect(url_for('manageData.projects'))
    authToken = PythonDataAuthTokens(pythonDataId=data.id, tokenType='r')
    # db.session.add(authToken)
    # db.session.commit()
    flash('AuthToken created', 'success')
    return redirect(request.referrer)

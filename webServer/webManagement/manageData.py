from calendar import day_abbr
from flask import Blueprint, render_template, redirect, url_for, request, flash
from ..models import PythonData, PythonDataAuthTokens, Project
from flask_login import current_user
from wtforms import Form, StringField, SelectField, validators
from wtforms.widgets import TextArea
from webServer import db


class ProjectForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    description = StringField(
        'Description', [
            validators.Length(
                min=1, max=1000)], widget=TextArea())


class DataForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    dataJson = StringField(
        'DataJson', [
            validators.Length(
                min=1, max=10000)], widget=TextArea())


class AuthTokenForm(Form):
    counter = 1
    name = StringField('Name', [validators.Length(min=1, max=50)])
    authToken = StringField('Token', [validators.Length(min=1, max=50)])
    choices = ['r', 'a', 'w', 'a+']
    tokenType = SelectField('Token Type', choices=choices, id=f"form{counter}")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.tokenType.id = f"select{kwargs['id']}"
        kwargs.pop('id')


mangData = Blueprint(
    'manageData',
    __name__,
    template_folder='templates',
    static_folder='static')


@mangData.route('/projects')
def projects():
    projects = Project.query.filter_by(ownerId=current_user.id).all()
    return render_template('manageDataHome.html', projects=projects)


@mangData.route('/projects/<int:project_id>', methods=['GET', 'POST'])
def project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if project.owner != current_user:
        flash('You do not have permission to view this project', 'danger')
        return redirect(url_for('manageData.projects'))
    form = ProjectForm(request.form)
    if request.method == 'POST' and form.validate():
        project.name = form.name.data
        project.description = form.description.data
        db.session.commit()
        flash('Project updated', 'success')
        return redirect(url_for('manageData.project', project_id=project_id))
    form.name.data = project.name
    form.description.data = project.description
    return render_template(
        'manageDataProject.html',
        form=form,
        project=project)


@mangData.route('/data/<int:data_id>', methods=['GET', 'POST'])
def data(data_id):
    data = PythonData.query.filter_by(id=data_id).first()
    if data.project.owner != current_user:
        flash('You do not have permission to view this data', 'danger')
        return redirect(url_for('manageData.projects'))
    form = DataForm(request.form)
    forms = dict()
    for dataAuthToken in data.authTokens:
        x = AuthTokenForm(request.form, id=dataAuthToken.id)
        x.tokenType.data = dataAuthToken.tokenType
        forms[dataAuthToken.id] = x
    if request.method == 'POST':
        data.name = form.name.data
        data.dataJson = form.dataJson.data
        db.session.commit()

        # flash('Data updated', 'success')
        return redirect(url_for('manageData.data', data_id=data_id))
    form.name.data = data.name
    form.dataJson.data = data.dataJson
    return render_template(
        'manageDataData.html',
        form=form,
        forms=forms,
        data=data)


@mangData.route('/projects/new', methods=['GET', 'POST'])
def createProject():
    form = ProjectForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        description = form.description.data
        project = Project(
            name=name,
            ownerId=current_user.id,
            description=description)
        db.session.add(project)
        db.session.commit()
        flash('Project created', 'success')
        return redirect(url_for('manageData.projects'))
    return render_template('editDataProject.html', form=form, keyword='Create')


@mangData.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
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
        db.session.commit()
        flash('Project edited', 'success')
        return redirect(url_for('manageData.projects'))
    form.name.data = project.name
    form.description.data = project.description
    return render_template('editDataProject.html', form=form, keyword='Edit')


@mangData.route('/projects/<int:project_id>/newData', methods=['GET', 'POST'])
def createData(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if project.owner != current_user:
        flash('You do not have permission to add data to this project', 'danger')
        return redirect(url_for('manageData.projects'))
    form = DataForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        dataJson = form.dataJson.data
        data = PythonData(name=name, dataJson=dataJson, projectId=project_id)
        db.session.add(data)
        db.session.commit()
        flash('Data created', 'success')
        return redirect(url_for('manageData.data', data_id=data.id))
    return render_template('editDataData.html', form=form, keyword='Create')


@mangData.route('/data/<int:data_id>/edit', methods=['GET', 'POST'])
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
        db.session.commit()
        flash('Data edited', 'success')
        return redirect(
            url_for(
                'manageData.project',
                project_id=data.projectId))
    form.name.data = data.name
    form.dataJson.data = data.dataJson
    return render_template('editDataData.html', form=form, keyword='Edit')


@mangData.route('/authToken/<int:authToken_id>', methods=['GET', 'POST'])
def authToken(authToken_id):
    authToken = PythonDataAuthTokens.query.filter_by(id=authToken_id).first()
    if authToken.data.project.owner != current_user:
        flash('You do not have permission to view this authToken', 'danger')
        return redirect(url_for('manageData.projects'))
    return render_template('manageDataAuthToken.html', authToken=authToken)


@mangData.route('/authToken/<int:authToken_id>/delete', methods=['POST'])
def deleteAuthToken(authToken_id):
    authToken = PythonDataAuthTokens.query.filter_by(id=authToken_id).first()
    if authToken.pythonData.project.owner != current_user:
        flash('You do not have permission to delete this authToken', 'danger')
        return redirect(url_for('manageData.projects'))
    db.session.delete(authToken)
    db.session.commit()
    flash('AuthToken deleted', 'success')
    return redirect(request.referrer)


@mangData.route('/authToken/<int:authToken_id>/update', methods=['POST'])
def updateAuthToken(authToken_id):
    authToken = PythonDataAuthTokens.query.filter_by(id=authToken_id).first()
    if authToken.pythonData.project.owner != current_user:
        flash('You do not have permission to update this authToken', 'danger')
        return redirect(url_for('manageData.projects'))
    authToken.tokenType = request.form['tokenType']
    db.session.commit()
    flash('AuthToken updated', 'success')
    return redirect(request.referrer)


@mangData.route('/data/<int:data_id>/new', methods=['POST'])
def createAuthToken(data_id):
    data = PythonData.query.filter_by(id=data_id).first()
    if data.project.owner != current_user:
        flash(
            'You do not have permission to create an authToken for this data',
            'danger')
        return redirect(url_for('manageData.projects'))
    authToken = PythonDataAuthTokens(pythonDataId=data.id, tokenType='r')
    db.session.add(authToken)
    db.session.commit()
    flash('AuthToken created', 'success')
    return redirect(request.referrer)

from calendar import day_abbr
from flask import Blueprint, render_template, redirect, url_for, request, flash
from ..models import PythonData, PythonDataAuthTokens, Project
from flask_login import current_user
from wtforms import Form, StringField, PasswordField, validators
from wtforms.widgets import TextArea
from webServer import db



class ProjectForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    description = StringField('Description', [validators.Length(min=1, max=1000)], widget=TextArea())
    
class DataForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    dataJson = StringField('DataJson', [validators.Length(min=1, max=10000)], widget=TextArea())

# class UpdateData(Form):
#     dataJson = StringField('DataJson', [validators.Length(min=1, max=10000)], widget=TextArea())
    
    



mangData = Blueprint('manageData', __name__, template_folder='templates', static_folder='static')


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
    return render_template('manageDataProject.html', form=form, project=project)

@mangData.route('/data/<int:data_id>', methods=['GET', 'POST'])
def data(data_id):
    data = PythonData.query.filter_by(id=data_id).first()
    if data.project.owner != current_user:
        flash('You do not have permission to view this data', 'danger')
        return redirect(url_for('manageData.projects'))
    form = DataForm(request.form)
    if request.method == 'POST':
        data.name = form.name.data
        data.dataJson = form.dataJson.data
        db.session.commit()
        # flash('Data updated', 'success')
        return redirect(url_for('manageData.data', data_id=data_id))
    form.name.data = data.name
    form.dataJson.data = data.dataJson
    return render_template('manageDataData.html', form=form, data=data)

@mangData.route('/projects/new', methods=['GET', 'POST'])
def createProject():
    form = ProjectForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        description = form.description.data
        project = Project(name=name, ownerId=current_user.id, description=description)
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
        return redirect(url_for('manageData.project', project_id=data.projectId))
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
    
    


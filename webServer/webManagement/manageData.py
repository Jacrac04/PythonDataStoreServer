from flask import Blueprint, render_template, redirect, url_for, request, flash
from ..models import PythonData, PythonDataAuthTokens, Project
from flask_login import current_user

mangData = Blueprint('manageData', __name__, template_folder='templates', static_folder='static')


@mangData.route('/projects')
def projects():
    projects = Project.query.filter_by(ownerId=current_user.id).all()
    return render_template('manageDataHome.html', projects=projects)
    
@mangData.route('/projects/<int:project_id>')
def project(project_id):
    project = Project.query.filter_by(id=project_id).first()
    if project.owner != current_user:
        flash('You do not have permission to view this project', 'danger')
        return redirect(url_for('manageData.projects'))
    return render_template('manageDataProject.html', project=project)

@mangData.route('/data/<int:data_id>')
def data(data_id):
    data = PythonData.query.filter_by(id=data_id).first()
    if data.project.owner != current_user:
        flash('You do not have permission to view this data', 'danger')
        return redirect(url_for('manageData.projects'))
    return render_template('manageDataData.html', data=data)
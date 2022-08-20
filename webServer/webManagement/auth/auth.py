from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from webServer.models import User
from webServer import db
from wtforms import Form, StringField, PasswordField, validators

auth = Blueprint(
    'auth',
    __name__,
    template_folder='templates',
    static_folder='static')


class Registerform(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])

    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_candidate = request.form['password']
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(
                user.password, password_candidate):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():

    form = Registerform(request.form)

    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data

        if not name:
            name = username

        # if this returns a user, then the email already exists in database
        user = User.query.filter_by(email=email).first()

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.register'))

        # create new user with the form data. Hash the password so plaintext
        # version isn't saved.
        new_user = User(email=email, name=name, password=password)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

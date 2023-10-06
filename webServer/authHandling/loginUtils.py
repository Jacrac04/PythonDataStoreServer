from flask import redirect, url_for, request, session, has_request_context, flash
from werkzeug.local import LocalProxy
from functools import wraps
from ..models import User

current_user = LocalProxy(lambda: get_user_from_session())


def wrapper_context_needed(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not has_request_context():
            print('No request context')
            return None
        return func(*args, **kwargs)
    return wrapped
        

@wrapper_context_needed
def get_user_from_session():
    if not '_user_id' in session:
        print('No user in session')
        return None
    print('here')
    user = User.query.filter_by(id=session['_user_id'])[0]
    return user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if '_user_id' not in session:
            flash('You need to be logged in to view that page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)    
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if '_user_id' not in session:
            flash('You need to be logged in to view that page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        if not current_user.is_admin:
            flash('You need to be an admin to view that page.', 'warning')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)    
    return decorated_function
    
    
@wrapper_context_needed
def login_user(user, remember=False):
    session['_user_id'] = user.id
    session.permanent = remember
    

@wrapper_context_needed
def logout_user():
    if session.get('_user_id'):
        session.pop('_user_id', None)
    
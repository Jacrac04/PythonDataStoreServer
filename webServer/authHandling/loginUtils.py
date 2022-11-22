from flask import redirect, url_for, request, session, has_request_context
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
    user = User.query.filter_by(id=session['_user_id']).first()
    return user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if '_user_id' not in session:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)    
    return decorated_function
    
    
@wrapper_context_needed
def login_user(user, remember=False):
    session['_user_id'] = user.id
    session.permanent = remember
    

@wrapper_context_needed        
def logout_user():
    session.pop('_user_id', None)
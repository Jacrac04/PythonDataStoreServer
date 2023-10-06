from flask.sessions import SessionInterface as FlaskSessionInterface
from flask.sessions import SessionMixin
from werkzeug.datastructures import CallbackDict
from itsdangerous import Signer, BadSignature, want_bytes
from cachelib.file import FileSystemCache
import os 
from uuid import uuid4

def total_seconds(td):
    return td.days * 60 * 60 * 24 + td.seconds


class ServerSideSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None, permanent=None):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        if permanent:
            self.permanent = permanent
        self.modified = False
 
class FileBasedSession(ServerSideSession):
    pass

class FileBasedSessionInterface(FlaskSessionInterface):
    session_class = FileBasedSession
    
    def __init__(self, cache_dir, threshold, mode, key_prefix, use_signer=False, permanent=True):
        self.cache = FileSystemCache(cache_dir, threshold=threshold, mode=mode)
        self.key_prefix = key_prefix
        self.use_signer = use_signer
        self.permanent = permanent
        self.has_same_site_capability = hasattr(self, "get_cookie_samesite")

     
    def open_session(self, app, request):
        # Get the session ID from the request's cookies
        sid = request.cookies.get(app.session_cookie_name)
        # If no session ID, create one
        if not sid:
            sid = self._generate_sid()
            return self.session_class(sid=sid, permanent=self.permanent)
        # If the session ID was signed, unsign it
        if self.use_signer:
            signer = self._get_signer(app)
            if signer is None:
                return None
            try:
                sid_as_bytes = signer.unsign(sid)
                sid = sid_as_bytes.decode()
            except BadSignature:
                sid = self._generate_sid()
                return self.session_class(sid=sid, permanent=self.permanent)
        # Get the session data from the cache
        data = self.cache.get(self.key_prefix + sid)
        # If no session data, create a new session
        if data is not None:
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, permanent=self.permanent)

    def save_session(self, app, session, response):
        # Get the domain and path for the cookie
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        # If there is no session, delete the cookie from the response
        if not session:
            if session.modified:
                self.cache.delete(self.key_prefix + session.sid)
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain, path=path)
            return

        # Create the cookie parameters
        conditional_cookie_kwargs = {}
        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        if self.has_same_site_capability:
            conditional_cookie_kwargs["samesite"] = self.get_cookie_samesite(app)
        expires = self.get_expiration_time(app, session)
        # Get the data for the session
        data = dict(session)
        # Store the session data in the cache
        self.cache.set(self.key_prefix + session.sid, data,
                       total_seconds(app.permanent_session_lifetime))
        # If the signer should be used, sign the session id
        if self.use_signer:
            session_id = self._get_signer(app).sign(want_bytes(session.sid))
        else:
            session_id = session.sid
        # Set the cookie in the response
        response.set_cookie(app.session_cookie_name, session_id,
                            expires=expires, httponly=httponly,
                            domain=domain, path=path, secure=secure,
                            **conditional_cookie_kwargs)
        
    def _generate_sid(self):
        return str(uuid4())

    def _get_signer(self, app):
        if not app.secret_key:
            return None
        return Signer(app.secret_key, salt='flask-session',
                        key_derivation='hmac')


        
        
class Session(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.session_interface = self._get_interface(app)

    def _get_interface(self, app):
        config = app.config.copy()
        config.setdefault('SESSION_TYPE', 'null')
        config.setdefault('SESSION_PERMANENT', True)
        config.setdefault('SESSION_USE_SIGNER', True)
        config.setdefault('SESSION_KEY_PREFIX', 'session:')
        config.setdefault('SESSION_FILE_DIR',
                          os.path.join(os.getcwd(), 'flask_session'))
        config.setdefault('SESSION_FILE_THRESHOLD', 500)
        config.setdefault('SESSION_FILE_MODE', 384)


        session_interface = FileBasedSessionInterface(
            config['SESSION_FILE_DIR'], config['SESSION_FILE_THRESHOLD'],
            config['SESSION_FILE_MODE'], config['SESSION_KEY_PREFIX'],
            config['SESSION_USE_SIGNER'], config['SESSION_PERMANENT'])


        return session_interface
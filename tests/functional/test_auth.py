from webServer import create_app

def test_home_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data
    assert b'Login' in response.data
    assert b'Register' in response.data
    
class TestLogin():
    def test_login_page(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/login' page is requested (GET)
        THEN check that the response is valid
        """
        response = test_client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data
        assert b'Email' in response.data
        assert b'Password' in response.data
    
    def test_login_post(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/login' page is requested (POST)
        THEN check that the response is valid
        """
        response = test_client.post(
            '/login', data={
                'email': 'test@test.com',
                'password': 'Test'
            })
        assert response.status_code == 302
        assert 'Set-Cookie' in response.headers
        assert self._test_after_login(test_client)
        

    def _test_after_login(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/login' page is requested (POST)
        THEN check that the response is valid
        """
        response = test_client.get('/profile')
        assert b'Test' in response.data
        return True
    
    def test_logout(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/logout' page is requested (POST)
        THEN check that the response is valid
        """
        response = test_client.get('/logout')
        assert response.status_code == 302
        assert self._test_after_logout(test_client)
        
    def _test_after_logout(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/login' page is requested (POST)
        THEN check that the response is valid
        """
        response = test_client.get('/profile')
        assert response.status_code == 302
        return True
    
class TestRegister():
    def test_register_page(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/register' page is requested (GET)
        THEN check that the response is valid
        """
        response = test_client.get('/register')
        assert response.status_code == 200
        assert b'Register' in response.data
        assert b'Email' in response.data
        assert b'Password' in response.data
    
    def test_register_post(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/register' page is requested (POST)
        THEN check that the response is valid
        """
        response = test_client.post(
            '/register', data={
                'name': 'Test Register',
                'email': 'register@test.com',
                'username': 'testregister',
                'password': 'TestRegister',
                'confirm': 'TestRegister'
            })
        assert response.status_code == 302
        assert self._test_after_register(test_client)
        
    def _test_after_register(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/register' page is requested (POST)
        THEN check that the response is valid
        """
        response = test_client.get('/login')
        assert b'registered' in response.data
        return True
        
    def test_register_post_fail(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/register' page is requested (POST)
        THEN check for error
        """
        response = test_client.post(
            '/register', data={
                'name': 'Test Register',
                'email': 'test@test.com',
                'username': 'testregister',
                'password': 'TestRegister',
                'confirm': 'TestRegister'
            })
        assert response.status_code == 302
        assert self._test_after_register_fail(test_client)

    def _test_after_register_fail(self, test_client):
        """
        GIVEN a Flask application configured for testing
        WHEN the '/register' page is requested (POST)
        THEN check that the response is valid
        """
        response = test_client.get('/login')
        assert b'already' in response.data
        return True
from webServer import models

def test_user_model():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check that the email and password fields are defined correctly
    """
    user = models.User('test@test.com', 'test', 'test')
    assert user.email == 'test@test.com'
    assert user.password != 'test'
    
def test_pythonData_model():
    """
    GIVEN a PythonData model
    WHEN a new PythonData is created
    THEN check that the dataJson field is defined correctly
    """
    pythonData = models.PythonData(dataJson='[1,2,3]')
    assert pythonData.dataJson == '[1,2,3]'
                                
def test_pythonDataAuthTokens_model():
    """
    GIVEN a PythonDataAuthTokens model
    WHEN a new PythonDataAuthTokens is created
    THEN check that the authToken field is defined correctly and unique and the tokenType field is defined correctly
    """
    pythonDataAuthTokens1 = models.PythonDataAuthTokens('r', 1)
    pythonDataAuthTokens2 = models.PythonDataAuthTokens('w', 1)
    assert pythonDataAuthTokens1.tokenType == 'r'
    assert pythonDataAuthTokens1.authToken != pythonDataAuthTokens2.authToken
                                
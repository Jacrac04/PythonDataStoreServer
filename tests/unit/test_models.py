from webServer import models


def test_user_model(newUser):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check that the email and password fields are defined correctly
    """
    # user = models.User('test@test.com', 'test', 'test')
    assert newUser.email == 'test@test.com'
    assert newUser.password != 'test'


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
    THEN check that the authToken field is defined correctly and unique
        and the tokenType field is defined correctly
    """
    pythonDataAuthTokens1 = models.PythonDataAuthTokens('r', 1)
    pythonDataAuthTokens2 = models.PythonDataAuthTokens('w', 1)
    assert pythonDataAuthTokens1.tokenType == 'r'
    assert pythonDataAuthTokens1.authToken != pythonDataAuthTokens2.authToken


def test_Project_model():
    """
    GIVEN a Project model
    WHEN a new Project is created
    THEN check that the projectName field is defined correctly
    """
    project = models.Project('test', 1, 'testDescription')
    assert project.name == 'test'

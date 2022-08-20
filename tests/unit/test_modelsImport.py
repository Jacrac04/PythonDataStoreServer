from webServer.models import User
from webServer.dataManagment.models import PythonDataAuthTokens, Project
from webServer.pythonInterface.models import PythonData


def test_modelsImport():
    """
    GIVEN a User model
    WHEN imported
    THEN check that it has imported
    """
    assert User is not None
    assert PythonData is not None
    assert PythonDataAuthTokens is not None
    assert Project is not None

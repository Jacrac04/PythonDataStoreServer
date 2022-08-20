class TestProjectPage:
    def test_project_page(self, authed_client):
        response = authed_client.get('/projects')
        assert response.status_code == 200
        assert b'Projects' in response.data
        assert b'Test' in response.data
        assert b'Lorem' in response.data

    def test_create_project(self, authed_client):
        response = authed_client.post(
            '/projects/new', data={
                'name': 'Test2',
                'description': 'Lorem2'
            })
        assert response.status_code == 302
        self._after_create_project(authed_client)

    def _after_create_project(self, authed_client):
        response = authed_client.get('/projects')
        assert response.status_code == 200
        assert b'Test2' in response.data
        assert b'Lorem2' in response.data


class TestManageProject:
    def test_manage_project(self, authed_client):
        response = authed_client.get('/projects/2')
        assert response.status_code == 200
        assert b'Test Data' in response.data
        assert b'Test' in response.data
        assert b'Lorem ipsum dolor sit amet, consectetur adipiscing' \
            in response.data

    def test_create_data_page(self, authed_client):
        response = authed_client.get('/projects/2/newData')
        assert response.status_code == 200
        assert b'Create Data' in response.data

    def test_create_data(self, authed_client):
        response = authed_client.post(
            '/projects/2/newData', data={
                'name': 'Test Data 2',
                'dataJson': '{"TesttseT"}'
            })
        assert response.status_code == 302
        self._after_create_data(authed_client, response.headers['Location'])

    def _after_create_data(self, authed_client, url):
        response = authed_client.get(url)
        assert response.status_code == 200
        assert b'Test Data 2' in response.data
        assert b'Type' in response.data
        assert b'TesttseT' in response.data

    def test_update_project(self, authed_client):
        response = authed_client.post(
            '/projects/2', data={
                'name': 'Test 3',
                'description': 'Lorem2'
            })
        assert response.status_code == 302
        self._after_update_project(authed_client)

    def _after_update_project(self, authed_client):
        response = authed_client.get('/projects/2')
        assert response.status_code == 200
        assert b'Test 3' in response.data
        response = authed_client.post(
            '/projects/2', data={
                'name': 'Test',
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing'
            })

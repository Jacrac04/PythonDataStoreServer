from webServer import create_app


import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = create_app()

if __name__ == '__main__':
    app.run()

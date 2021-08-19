import os
# Basically configures the file structure for Flask
# Look at my current file, what is the path

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "You shall not pass..."
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
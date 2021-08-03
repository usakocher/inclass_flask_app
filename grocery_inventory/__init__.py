# This initializes everything in the parent folder. Just like an __init__ in a Python Class
# Indicates app folder

from flask import Flask
# from config import Config
from .site.routes import site

app = Flask(__name__)

# registering blueprint
app.register_blueprint(site)
from flask import Blueprint, render_template

# This is telling us where our bluprints are located
site = Blueprint('site', __name__, template_folder='site_templates')

# Providing a call for the blueprints?
@site.route('/')
def home():
    return render_template('index.html')
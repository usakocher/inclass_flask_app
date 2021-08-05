from flask import Blueprint, render_template
from flask_login import login_required

# This is telling us where our bluprints are located
site = Blueprint('site', __name__, template_folder='site_templates')

# Providing a call for the blueprints?
@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
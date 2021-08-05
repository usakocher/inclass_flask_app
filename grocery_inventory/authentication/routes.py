from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from grocery_inventory.forms import UserLoginForm
from grocery_inventory.models import User, db, check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print([email, password])

        user = User(email, password)
        db.session.add(user)
        db.session.commit()

        flash(f'You have successfully created a user account {email}', 'user-created')


        return redirect(url_for('auth.signin'))

    return render_template('signup.html', form = form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print([email, password])

        
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash('You were successfully logged in.', 'auth-success')
            return redirect(url_for('site.home'))
        else:
            flash('Your Email or Password was not correct.', 'auth-failed')
            return redirect(url_for('auth.signin'))
    return render_template('signin.html', form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were successfully logged out.', 'logout')
    return redirect(url_for('auth.signin'))
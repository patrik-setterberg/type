from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm
from app.forms import EditEmailForm, EditPasswordForm, EditUsernameForm
from datetime import datetime
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash


# Home
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


# Survive game
@app.route('/survive')
def survive():
    return render_template('survive.html', title='Survive: Type or die!')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Sign in', form=form)


# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You're already registered and logged in.")
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data) # NIFTY
        db.session.add(user)
        db.session.commit()

        flash('Success! You are now a registered user.')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


# User page
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    return render_template('user.html', title='Profile: ' + user.username,
                           user=user)


# Edit user
@app.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    user_form = EditUsernameForm(current_user.username)
    mail_form = EditEmailForm(current_user.email)
    pass_form = EditPasswordForm()

    # Change username
    if user_form.validate_on_submit():
        if len(user_form.username.data) < 3 or len(user_form.username.data) > 20:
            flash('Username must be between 3 and 20 characters.')
            return redirect(url_for('edit_user'))
        current_user.username = user_form.username.data
        db.session.commit()
        flash('Username updated successfully!')
        return redirect(url_for('edit_user'))
    # Change email
    elif mail_form.validate_on_submit():
        # NEED EMAIL FORMAT VALIDATION
        # A LITTLE BIT OF REGEXP MAYBE. 
        # IF NOT alpha @ alphas . alphas
        current_user.email = mail_form.email.data
        db.session.commit()
        flash('Email updated successfully!')
        return redirect(url_for('edit_user'))
    # Change password
    elif pass_form.validate_on_submit():
        if len(pass_form.password.data) < 5 or len(pass_form.password.data) > 40:
            flash('password must be between 5 and 40 characters.')
            return redirect(url_for('edit_user'))
        elif pass_form.password.data != pass_form.password2.data:
            flash('Passwords do not match. Please try again.')
            return redirect(url_for('edit_user'))
        else:
            current_user.password_hash = generate_password_hash(pass_form.password.data)
            db.session.commit()
            flash('Password changed successfully!')
            return redirect(url_for('edit_user'))
    elif request.method == 'GET':
        user_form.username.data = current_user.username
        mail_form.email.data = current_user.email
    
    return render_template('edit_user.html', title='Edit user details',
                           user_form=user_form, mail_form=mail_form,
                           pass_form=pass_form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
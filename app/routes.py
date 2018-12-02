from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User, SentenceModel, WordList
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm
from app.forms import EditEmailForm, EditPasswordForm, EditUsernameForm, SentenceForm, WordForm
from app.forms import ResetPasswordForm
from app.sentence_generator import generate_sentence, add_word
from app.sentence_gen_statics import WORDLIST_TAGS_ALLOWED
from datetime import datetime
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
from app.email import send_password_reset_email


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
    if user_form.submit_username.data and user_form.validate():
        current_user.username = user_form.username.data
        db.session.commit()
        flash('Username updated successfully!')
        return redirect(url_for('edit_user'))
        
    # Change email
    elif mail_form.submit_email.data and mail_form.validate():
        current_user.email = mail_form.email.data
        db.session.commit()
        flash('Email updated successfully!')
        return redirect(url_for('edit_user'))

    # Change password
    elif pass_form.submit_password.data and pass_form.validate():
        current_user.password_hash = generate_password_hash(pass_form.password.data)
        db.session.commit()
        flash('Password updated successfully!')
        return redirect(url_for('edit_user'))
            
    return render_template('edit_user.html', title='Edit user details',
                           user_form=user_form, mail_form=mail_form,
                           pass_form=pass_form)


# Reset password request
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = ResetPasswordRequestForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for instructions to reset your password.')
        return redirect(url_for('login'))
        
    return render_template('reset_password_request.html', 
                           title='Reset Password', form=form)


# Reset password
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)


# test sentence generator, TEMPORARY
@app.route('/sentence', methods=['GET', 'POST'])
def sentence():

    sentence = generate_sentence()

    return render_template('sentence.html', sentence=sentence)


# Manage word list
@app.route('/admin/manage_words', methods=['GET', 'POST'])
@login_required
def manage_words():

    if current_user.username != 'admin':
        flash('Restricted area!')
        return redirect(url_for('index'))

    form = WordForm()

    # add new word (word, tag)
    if form.submit_word.data and form.validate():
        word = add_word(form.word.data, form.tag.data)

        # (possibly) assign article (a/an)
        if form.article.data:
            word.article = form.article.data

        # assign gender
        if form.gender.data:
            word.gender = form.gender.data

        # assign irregular status
        if form.irregular.data:
            word.irregular = form.irregular.data

        # assign syllables
        if form.syllables.data:
            word.syllables = form.syllables.data

        # assign categories
        if form.categories.data:
           word.categories = form.categories.data

        # assign associations
        if form.noun_assoc.data:
            word.noun_assoc = form.noun_assoc.data
        if form.adj_assoc.data:
            word.adj_assoc = form.adj_assoc.data
        if form.verb_assoc.data:
            word.verb_assoc = form.verb_assoc.data

        # assign subtype 
        if form.subtype.data:
            word.subtype = form.subtype.data

        db.session.add(word)
        db.session.commit()

        flash('Word added.')
        return redirect(url_for('manage_words'))


    words = WordList.query.order_by(WordList.tag.asc()).all()

    return render_template('manage_words.html',
                           form=form, 
                           words=words,
                           tags=WORDLIST_TAGS_ALLOWED,
                           title='Sentence generator word list')


# Manage sentence models
@app.route('/admin/manage_sentences', methods=['GET', 'POST'])
@login_required
def manage_sentences():

    if current_user.username != 'admin':
        flash('Restricted area!')
        return redirect(url_for('index'))

    sentence_form = SentenceForm()

    # add sentence model
    if sentence_form.submit_sentence.data and sentence_form.validate():
        sentence = SentenceModel(sentence=sentence_form.sentence.data)
        db.session.add(sentence)
        db.session.commit()

        flash('Sentence model added')
        return redirect(url_for('manage_sentences'))

    sentences = SentenceModel.query.all()

    return render_template('manage_sentences.html',
                           sentence_form=sentence_form,
                           sentences=sentences,
                           title='Sentence generator models')


# Delete item from database
@app.route('/admin/delete_item/<item>/<id>', methods=['GET'])
@login_required
def delete_item(item, id):

    if item == 'sentence':
        db_table = SentenceModel
    elif item == 'word':
        db_table = WordList

    del_item = db_table.query.filter_by(id=int(id)).first_or_404()

    db.session.delete(del_item)
    db.session.commit()

    flash(item.capitalize() + ' deleted.')

    return redirect(url_for('manage_sentences'))


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()




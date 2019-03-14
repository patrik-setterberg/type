from flask import render_template, flash, redirect, request, url_for 
from flask import session, make_response
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User, SentenceModel, WordList
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm
from app.forms import EditEmailForm, EditPasswordForm, EditUsernameForm
from app.forms import SentenceForm, ResetPasswordForm, NounForm, AdjectiveForm
from app.forms import VerbForm, AdverbForm, ProperNounForm, SpecialForm
from app.forms import ContactForm
from app.sentence_generator import generate_sentence
from datetime import datetime
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
from app.email import send_password_reset_email, send_contact_me_message
from config import SECRET_HIGH_SCORE_KEY, COOKIE_MAX_AGE, Config
from config import ADMIN_USER, ADMIN_EMAIL
from sqlalchemy import func
import json
import os


# Home
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='Home')


# High score list
@app.route('/high_scores', methods=['GET'])
def high_scores():
    scores = list(User.query.order_by(User.high_score.desc()).limit(25))

    return render_template('high_scores.html', title='High Scores', scores=scores)


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
        app.logger.info('[LOGIN] User signed in: (' + 
                        str(user.id) + ') //')
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Sign in', form=form)


# Logout
@app.route('/logout')
def logout():
    """ Logout user, add event to log and clear session. """

    resp = make_response(redirect(url_for('index')))

    if current_user:
        app.logger.info('[LOGOUT] User signed out: (' + 
                        str(current_user.id) + ') //')

        resp.set_cookie('remember_token', '', max_age=0)
        logout_user()
        session.clear()
    return resp


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("You're already registered and logged in.")
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        app.logger.info('[REGISTRATION] New user registered: (' + 
                        str(user.id) + ') //')

        flash('Success! You are now a registered user.')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


# User page
@app.route('/user/<username>')
@login_required
def user(username):
    """ Display user information, as well as links to settings
        on user's own user page. """

    user = User.query.filter_by(username=username).first_or_404()
    high_scores = User.query.order_by(User.high_score.desc()).all()

    name_list = []
    for player in high_scores:
        name_list.append(player.username)

    user.high_score_pos = name_list.index(username) + 1
    
    return render_template('user.html', title='Profile: ' + user.username, user=user, admin=ADMIN_USER)


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
        app.logger.info('[EDIT_USER] User changed their username: (' + 
                        str(current_user.id) + ') //')
        flash('Username updated successfully!')
        return redirect(url_for('edit_user'))
        
    # Change email
    elif mail_form.submit_email.data and mail_form.validate():
        current_user.email = mail_form.email.data
        db.session.commit()
        app.logger.info('[EDIT_USER] User changed their email address: (' + 
                        str(current_user.id) + ') //')
        flash('Email updated successfully!')
        return redirect(url_for('edit_user'))

    # Change password
    elif pass_form.submit_password.data and pass_form.validate():
        current_user.password_hash = generate_password_hash(pass_form.password.data)
        db.session.commit()
        app.logger.info('[EDIT_USER] User changed their password: (' + 
                        str(current_user.id) + ') //')
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
            app.logger.info(
                '[PASSWORD_RESET] User requested a password reset: (' + 
                str(user.id) + ') //')
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
        app.logger.info(
                '[PASSWORD_RESET] User reset their password: (' + 
                str(user.id) + ') //')
        flash('Your password has been reset.')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)


# Delete account page
@app.route('/delete_account', methods=['GET'])
@login_required
def delete_account():
    """ Page asking for deletion confirmation """

    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    return render_template('delete_account.html')

    
# Delete user route
@app.route('/delete_user', methods=['GET'])
@login_required
def delete_user():
    """ Log out user, delete user account, redirect to index. """

    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        user_id = current_user.id
        logout_user()

        del_user = User.query.filter_by(id=user_id).first_or_404()

        if del_user:
            app.logger.info(
                '[DELETE_ACCOUNT] User deöeted their account: (' +
                str(del_user.id) + ') //')
            db.session.delete(del_user)
            db.session.commit()
            flash('User account deleted.')

        return redirect(url_for('index'))


@app.route('/get_name_and_score', methods=['GET'])
def get_name_and_score():
    """ Get username and score. Also make sure user 'anonymous' exists. """

    user_info = {}
    if current_user.is_authenticated:
        user_info['username'] = current_user.username
        try:
            user_info['high_score'] = current_user.high_score
        except:
            user_info['high_score'] = 0
    else:
        try:
            user = User.query.filter_by(username='anonymous').first()
            try:
                user_info['username'] = user.username
                user_info['high_score'] = user.high_score
            except:
                user_info['username'] = 'anonymous'
                user_info['high_score'] = 0
        except:
            anon = User(username='anonymous')
            db.session.add(anon)
            db.session.commit()

            user_info['username'] = 'anonymous'
            user_info['high_score'] = 0

    return json.dumps(user_info)


# Get best score achieved by any user
@app.route('/get_high_score', methods=['GET'])
def get_high_score():
    score_dict = {}
    try:
        leader = User.query.order_by(User.high_score.desc()).first()
        score_dict['high_score'] = leader.high_score
    except:
        score_dict['high_score'] = 0

    return json.dumps(score_dict)


@app.route('/get_high_score_key', methods=['GET'])
def get_high_score_key():
    """ Get secret high score key. """

    secret = {'high_score_key': SECRET_HIGH_SCORE_KEY}
    return json.dumps(secret)


@app.route('/update_user_score/<high_score_cypher>/<score>', methods=['GET'])
def update_user_score(high_score_cypher, score):
    """ Update user score. To prevent users from being able to
        update scores manually by simply visiting e.g.
        /update_user_score/2000 a weak security measure was added.
        Scores are multiplied by a static number stored in app.config
        and verified in this route. Not secure but good enough for
        current app. """

    score = int(score)
    deciphered = int(high_score_cypher) / SECRET_HIGH_SCORE_KEY

    if deciphered == score:
        if current_user.is_authenticated:
            user = current_user
        else:
            try:
                user = (User.query.filter_by(username='anonymous')
                        .first())
            except Exception as e:
                print(e)

        user.times_played = int(user.times_played) + 1

        if score > user.high_score:
            user.high_score = score
            app.logger.info(
                '[HIGH_SCORE] User set new personal high score: (' + 
                str(user.id) + ') //')

        db.session.commit()
        
    return str(score)  # Do I have to return something here?


# test sentence generator, TEMPORARY
@app.route('/sentence', methods=['GET', 'POST'])
def sentence():
    
    return render_template('sentence.html')


@app.route('/get_sent', methods=['GET'])
def get_sent():
    """ Get and return a sentence from sentence_generator.py """

    sentence = generate_sentence()
    
    return sentence


# Admin panel
@app.route('/admin', methods=['GET'])
@login_required
def admin():
    """ Administrator control panel. """

    if not current_user.username == ADMIN_USER:
        flash('Restricted area!')
        return redirect(url_for('index'))
    
    users = db.session.query(User).all()

    # Get user count, remove 2 to account for users admin and anonymous
    user_count = len(users) - 2

    times_played = 0 + sum([int(user.times_played) for user in users])

    return render_template('admin.html',
                           title='Admin panel',
                           user_count=user_count,
                           times_played=times_played,
                           admin=ADMIN_USER)


# Manage word list
@app.route('/admin/manage_words', methods=['GET', 'POST'])
@login_required
def manage_words():

    if current_user.username != ADMIN_USER:
        flash('Restricted area!')
        return redirect(url_for('index'))

    noun_form = NounForm()
    adj_form = AdjectiveForm()
    verb_form = VerbForm()
    adv_form = AdverbForm()
    prop_noun_form = ProperNounForm()
    special_form = SpecialForm()

    # POST
    if request.method == 'POST':

        # Add noun
        if noun_form.submit_noun.data and noun_form.validate():
            new_word = WordList(word=noun_form.word.data,
                                tag='NN',
                                article=noun_form.article.data,
                                irregular=noun_form.irregular.data,
                                gender=noun_form.gender.data,
                                categories=noun_form.categories.data,
                                adj_assoc=noun_form.adj_assoc.data,
                                verb_assoc=noun_form.verb_assoc.data)
            db.session.add(new_word)
            db.session.commit()
        
            flash('Word added.')
            return redirect(url_for('manage_words'))
        # Add adjective
        elif adj_form.submit_adj.data and adj_form.validate():
            new_word = WordList(word=adj_form.word.data,
                                tag='JJ',
                                irregular=adj_form.irregular.data,
                                mult_syll=adj_form.mult_syll.data,
                                categories=adj_form.categories.data,
                                noun_assoc=adj_form.noun_assoc.data)
            db.session.add(new_word)
            db.session.commit()
        
            flash('Word added.')
            return redirect(url_for('manage_words'))
        # Add verb
        elif verb_form.submit_verb.data and verb_form.validate():
            new_word = WordList(word=verb_form.word.data,
                                tag='VB',
                                irregular=verb_form.irregular.data,
                                mult_syll=verb_form.mult_syll.data,
                                categories=verb_form.categories.data,
                                noun_assoc=verb_form.noun_assoc.data,
                                subtype=verb_form.subtype.data)
            db.session.add(new_word)
            db.session.commit()
        
            flash('Word added.')
            return redirect(url_for('manage_words'))
        # Add adverb
        elif adv_form.submit_adv.data and adv_form.validate():
            new_word = WordList(word=adv_form.word.data,
                                tag='RB',
                                irregular=adv_form.irregular.data,
                                categories=adv_form.categories.data,
                                subtype=adv_form.subtype.data)
            db.session.add(new_word)
            db.session.commit()
        
            flash('Word added.')
            return redirect(url_for('manage_words'))
        # Add proper noun
        elif prop_noun_form.submit_prop_noun.data and prop_noun_form.validate():
            new_word = WordList(word=prop_noun_form.word.data,
                                tag='NP',
                                gender=prop_noun_form.gender.data)
            db.session.add(new_word)
            db.session.commit()
        
            flash('Word added.')
            return redirect(url_for('manage_words'))
        # Add special word
        elif special_form.submit_spec.data and special_form.validate():
            new_word = WordList(word=special_form.word.data,
                                tag='SPEC')
            db.session.add(new_word)
            db.session.commit()
        
            flash('Word added.')
            return redirect(url_for('manage_words'))        
        
    else:
        nouns = WordList.query.filter_by(tag='NN')
        adjectives = WordList.query.filter_by(tag='JJ')
        verbs = WordList.query.filter_by(tag='VB')
        adverbs = WordList.query.filter_by(tag='RB')
        proper_nouns = WordList.query.filter_by(tag='NP')
        special_words = WordList.query.filter_by(tag='SPEC')

        return render_template('manage_words.html',
                            noun_form=noun_form,
                            adj_form=adj_form,
                            verb_form=verb_form,
                            adv_form=adv_form,
                            prop_noun_form=prop_noun_form,
                            special_form=special_form,
                            nouns=nouns,
                            adjectives=adjectives,
                            verbs=verbs,
                            adverbs=adverbs,
                            proper_nouns=proper_nouns,
                            special_words=special_words,
                            title='Word database management')


# Manage sentence models
@app.route('/admin/manage_sentences', methods=['GET', 'POST'])
@login_required
def manage_sentences():

    if current_user.username != ADMIN_USER:
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


# Manage users
@app.route('/admin/manage_users', methods=['GET'])
@login_required
def manage_users():
    
    if not current_user.username == ADMIN_USER:
        flash('Restricted area')
        return redirect(url_for('index'))

    users = User.query.order_by(User.id.asc()).all()

    return render_template('manage_users.html',
                           users=users,
                           title='Manage users',
                           admin=ADMIN_USER)


# Get all user data
@app.route('/admin/get_data/<user_id>', methods=['GET'])
@login_required
def get_data(user_id):
    """ To allow users to exercise their right of access to data,
        get all their user info and all lines in log files
        where their usernames and email addresses occur. """

    if not current_user.username == ADMIN_USER:
        return redirect(url_for('index'))

    try:
        user = User.query.filter_by(id=user_id).first_or_404()
    except:
        flash('No user with that ID')
        return redirect(url_for('manage_users'))

    if user:
        try:
            response_str = (
                "*** USER DATA***<br>" +
                "User ID: " + str(user.id) + "<br>" +
                "Username: " + user.username + "<br>" +
                "Email address: " + user.email + "<br>" +
                "Registered: " + user.registered.strftime("%A, %b %d, %Y") +
                "<br>" +
                "Last seen: " + user.last_seen.strftime("%A, %b %d, %Y") +
                "<br>" +
                "High score: " + str(user.high_score) + "<br>" +
                "Times played: " + str(user.times_played) + "<br><br>" +
                "*** IN LOGS ***<br>")
        except:
            response_str = 'Something went wrong. Probably a value missing.'

        logfiles = os.listdir(app.config['LOGS_DIR'])

        for current_file in logfiles:
            with open(app.config['LOGS_DIR'] + current_file) as f:
                lines = []
                for line in f:
                    if '(' + str(user_id) + ')' in line:
                        lines.append(line.split('//')[0] + "<br>")
                lines.reverse()
                for line in lines:
                    response_str += line

        return response_str


# Delete item from database
@app.route('/admin/delete_item/<item>/<id>', methods=['GET'])
@login_required
def delete_item(item, id):

    if not current_user.username == ADMIN_USER:
        flash("You can't do that.")
        return redirect(url_for('index'))

    if item == 'sentence':
        db_table = SentenceModel
        redir = 'manage_sentences'
    elif item == 'word':
        db_table = WordList
        redir = 'manage_words'
    elif item == 'user':
        db_table = User
        redir = 'manage_users'
    else:
        return redirect(url_for('admin'))

    del_item = db_table.query.filter_by(id=int(id)).first_or_404()

    try:
        if del_item.username == current_user.username:
            flash("Don't delete yourself, bro.")
            return redirect(url_for('admin'))
    except AttributeError:
        pass
    else:
        pass

    if item == 'user':
        app.logger.info('[ADMIN] Admin deleted user: (' + 
                        str(del_item.id) + ') //')

    db.session.delete(del_item)
    db.session.commit()

    flash(item.capitalize() + ' deleted.')

    return redirect(url_for(redir))


# About page
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html', title='About this place')


# Contact form
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """ Send an email to website administrator with a message
        from a website visitor containing their name, email address
        and the message body. """

    form = ContactForm()

    if form.validate_on_submit():
        send_contact_me_message(form.name.data,
                                form.email.data,
                                form.message.data)
        flash('Message sent. Thank you!')
        app.logger.info('[MESSAGE] Visitor sent a message through \
            contact form.')
        return redirect(url_for('contact'))

    return render_template('contact.html', title='Contact', form=form)


# Site privacy policy
@app.route('/privacy_policy', methods=['GET'])
def privacy_policy():
    return render_template('privacy_policy.html', title='Privacy Policy')


# Site cookie policy
@app.route('/cookie_policy', methods=['GET'])
def cookie_policy():
    return render_template('cookie_policy.html', title='Cookie Policy')


# Clear cookies and session
@app.route('/clear_cookies', methods=['GET'])
def clear_cookies():
    all_cookies = [cookie for cookie in request.cookies]
    # only available from /cookie_policy so redirects there
    resp = make_response(redirect(url_for('cookie_policy')))

    for cookie in all_cookies:
        resp.set_cookie(cookie, '', expires=0)
    
    return resp


# Toggle Analytics consent
@app.route('/toggle_ga', methods=['GET'])
def toggle_ga():
    resp = make_response(redirect(url_for('cookie_policy')))
    if request.cookies.get('ga_consent') == 'true':
        resp.set_cookie('ga_consent', 'false', max_age=COOKIE_MAX_AGE)
    else:
        resp.set_cookie('ga_consent', 'true', max_age=COOKIE_MAX_AGE)
    
    return resp


@app.before_first_request
def ensure_admin_anon():
    """ Make sure that users 'admin' and 'Anonymous' exist on
        app startup. """

    anon = User.query.filter_by(username='anonymous').first()
    if not anon:
        new_anon = User(username='anonymous', email='anon@typemania.net')
        db.session.add(new_anon)
        db.session.commit()

    admin = User.query.filter_by(username=ADMIN_USER).first()
    if not admin:
        new_admin = User(username=ADMIN_USER, email=ADMIN_EMAIL)
        new_admin.set_password('admin')
        db.session.add(new_admin)
        db.session.commit()


@app.before_request
def before_request():
    """ Update user last seen. """

    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.after_request
def after_request(response):
    """ Clear session after request unless users have consented
        to cookies to make sure no session cookie is created
        illegaly. """
    resp = make_response(response)

    if request.cookies.get('cookie_consent') == 'true':
        pass
    else:
        session.clear()

    return resp


# Check cookies consent
# Thanks: https://stackoverflow.com/a/51935872
@app.context_processor
def inject_template_scope():
    injections = dict()

    def cookies_check():
        """ Check if users have consented to cookies """
        value = request.cookies.get('cookie_consent')
        return value == 'true'
    injections.update(cookies_check=cookies_check)

    def analytics_check():
        """ Check if users opted out of Google Analytics tracking """
        value = request.cookies.get('ga_consent')
        return value == 'true'
    injections.update(analytics_check=analytics_check)

    return injections

from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.models import User, SentenceModel, WordList
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm
from app.forms import EditEmailForm, EditPasswordForm, EditUsernameForm, SentenceForm
from app.forms import ResetPasswordForm, NounForm, AdjectiveForm, VerbForm, AdverbForm
from app.forms import ProperNounForm, SpecialForm
from app.sentence_generator import generate_sentence
from datetime import datetime
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
from app.email import send_password_reset_email
from config import SECRET_HIGH_SCORE_KEY, ADMIN_USER
import json


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


# Survive game ######## KANSKE TA BORT HELT OCH HÅLLET EN GÅNG FÖR ALLA????????
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
        user = (current_user if current_user.is_authenticated
                else User.query.filter_by(username='anonymous').first_or_404())

        user.times_played = int(user.times_played) + 1

        if score > user.high_score:
            user.high_score = score

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
        words = WordList.query.order_by(WordList.tag.asc()).all()
        return render_template('manage_words.html',
                            noun_form=noun_form,
                            adj_form=adj_form,
                            verb_form=verb_form,
                            adv_form=adv_form,
                            prop_noun_form=prop_noun_form,
                            special_form=special_form,
                            words=words,
                            title='Sentence generator word list')


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

    if del_item.username == current_user.username:
        flash("Don't delete yourself, bro.")
        return redirect(url_for('admin'))

    db.session.delete(del_item)
    db.session.commit()

    flash(item.capitalize() + ' deleted.')

    return redirect(url_for(redir))


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()




from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from time import time
import jwt


# Users table 
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    high_score = db.Column(db.Integer, index=True, default=0)
    times_played = db.Column(db.Integer, index=True, default=0)
    registered = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                             algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Sentence models
class SentenceModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.String(120), index=True, unique=True)


# Words
class WordList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(32), index=True)
    tag = db.Column(db.String(16), index=True)
    # Indefinite article, a / an for nouns
    article = db.Column(db.String(5), nullable=True)
    # Proper nouns need gender to assign correct pronouns
    gender = db.Column(db.String(16), nullable=True, index=True)
    # Irregular forms of words, e.g. adverbs, verbs, 1 or 0
    irregular = db.Column(db.Integer, nullable=True, index=True)
    # Syllable count is needed for verbs and adjectives for proper conjugation
    # mult(iple) syll(ables), 1 for true, 0 for false (i.e. 1 syllable)
    mult_syll = db.Column(db.Integer, nullable=True, index=True)
    # Categories aid in word selection, used for nouns, adjectives ????
    categories = db.Column(db.String(120), nullable=True, index=True)
    # Associations help select common objects or actions for words
    noun_assoc = db.Column(db.String(120), nullable=True, index=True)
    adj_assoc = db.Column(db.String(120), nullable=True, index=True)
    verb_assoc = db.Column(db.String(120), nullable=True, index=True)
    # Subtypes (e.g. 'time' for adverbs of time, 'emotion' for verb of
    # emotion). NOTE, VERBS: enter stative property, e.g. perception, opinion,
    # the senses, emotion, possession, and state, OR 'action' if action verb.
    subtype = db.Column(db.String(16), nullable=True, index=True)
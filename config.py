import os
import datetime
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'application.secret_key'

    # "Remember me"-token max age
    REMEMBER_COOKIE_DURATION = datetime.timedelta(days=7)

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['min@email.se']

    # Logs directory
    LOGS_DIR = 'logs/'

# Secret high score key
SECRET_HIGH_SCORE_KEY = 4738

# Administrator username
ADMIN_USER = 'admin'

# Max age of cookies 'cookie_consent' and 'ga_consent'
COOKIE_MAX_AGE = 604800  # one week in seconds
#! /usr/bin/python3.6

import os
import logging
import sys
from dotenv import load_dotenv


# load environment variables
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/spacedoctor/typemania/type/')
from app import app as application
application.secret_key = os.environ.get('SECRET_KEY')
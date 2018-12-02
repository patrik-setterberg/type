from flask import render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo 
from wtforms.validators import Length, ValidationError
from app.models import User, WordList, SentenceModel
from app.sentence_generator import check_word_tag, check_sentence_tags
from app.sentence_gen_statics import WORD_BLACKLIST, ALLOWED_CHARS
import re

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                           Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(),
                        Length(min=5, max=50)])
    password = PasswordField('Password', validators=[DataRequired(),
                             Length(min=6, max=50)])
    password2 = PasswordField('Repeat Password', validators=[
                              DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    

class EditUsernameForm(FlaskForm):
    username = StringField('Change Username', validators=[DataRequired(),
                           Length(min=3, max=20)])
    submit_username = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditUsernameForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class EditEmailForm(FlaskForm):
    email = StringField('Change E-Mail Address', validators=[DataRequired(),
                        Email(), Length(min=5, max=50)])
    submit_email = SubmitField('Submit')

    def __init__(self, original_email, *args, **kwargs):
        super(EditEmailForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            mail = User.query.filter_by(email=self.email.data).first()
            if mail is not None:
                raise ValidationError('Please choose a different e-mail address.')
                

class EditPasswordForm(FlaskForm):
    password = PasswordField('Change Password', validators=[DataRequired(),
                             Length(min=6, max=50)])
    password2 = PasswordField('Repeat Password', validators=[
                              DataRequired(), EqualTo('password')])
    submit_password = SubmitField('Submit')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(),
                             Length(min=6, max=50)])
    password2 = PasswordField('Repeat Password', validators=[
                              DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class SentenceForm(FlaskForm):
    sentence = StringField('Sentence tags', validators=[DataRequired(), 
                           Length(min=6, max=120)])
    submit_sentence = SubmitField('Add sentence model')

    def validate_sentence(self, sentence):
        # check model formatting
        pattern = '([' + ALLOWED_CHARS + ']+\/)+[' + ALLOWED_CHARS + ']+'
        if not re.match(pattern, sentence.data):
            raise ValidationError('Sentence model formatted incorrectly.')
        # check tags
        tag = check_sentence_tags(sentence.data)
        if tag != 'allowed':
            raise ValidationError('Sentence model contains illegal tag: ' + tag)
        # check duplicates
        existing_sentence = SentenceModel.query.filter_by(sentence=sentence.data).first()
        if existing_sentence is not None:
            raise ValidationError('Sentence model already exists in database.')


class WordForm(FlaskForm):
    word = StringField('Word', validators=[DataRequired(),
                       Length(min=1, max=32)])
    tag = StringField('Tag', validators=[DataRequired(),
                      Length(min=1, max=16)])
    article = RadioField('Article (a or an)', choices=[('a','a'),('an','an')])
    gender = RadioField('Gender', choices=[('MM','Male'),('FF','Female'),
                        ('NN','Neutral')])
    irregular = RadioField('Word regularity', 
                           choices=[(0,'Regular'),(1,'Irregular')])
    mult_syll = RadioField('Syllables count',
                           choices=[(0,'One syllable'),(1,'Multiple syllables')])
    categories = StringField('Categories')
    noun_assoc = StringField('Noun associations')
    adj_assoc = StringField('Adjective associations')
    verb_assoc = StringField('Verb associations')
    subtype = StringField('Subtype')
    submit_word = SubmitField('Add word')

    def validate_word(self, word):
        for letter in word.data:
            if not re.match('[a-zA-Z0-9]+', letter):
                raise ValidationError('Only letters and numbers allowed')
        
        if word.data in WORD_BLACKLIST:  ##### MAKE SURE WORD_BLACKLIST IS THERE
            raise ValidationError('Word banned. Sorry...')

        existing_word = WordList.query.filter_by(word=word.data).first()
        if existing_word is not None:
            raise ValidationError('Word already exists in database.')

    def validate_tag(self, tag):
        if not check_word_tag(tag.data):
            raise ValidationError('Tag nog allowed. Check spelling or \
                                  add tag to ALLOWED_TAGS')
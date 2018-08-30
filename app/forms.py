from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo 
from wtforms.validators import Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
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
    username = StringField('Change Username')
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditUsernameForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                flash('Please use a different username.')
                return redirect(url_for('edit_user'))


class EditEmailForm(FlaskForm):
    email = StringField('Change E-Mail Address', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def __init__(self, original_email, *args, **kwargs):
        super(EditEmailForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            mail = User.query.filter_by(email=self.email.data).first()
            if mail is not None:
                flash('Please choose a different e-mail address.')
                return redirect(url_for('edit_user'))


class EditPasswordForm(FlaskForm):
    password = PasswordField('Change Password')
    password2 = PasswordField('Repeat Password')
    submit = SubmitField('Submit')

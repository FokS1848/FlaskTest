from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


class Form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Enter')


class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Enter')


class Blog1(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Blog', validators=[DataRequired()])
    submit = SubmitField('Enter')


class CommentForm(FlaskForm):
    text = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Enter')


class Update(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Blog', validators=[DataRequired()])
    submit = SubmitField('Enter')


class ChangeForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Enter')

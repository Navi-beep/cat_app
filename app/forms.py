from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo 

class Create_accountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()

class CatForm(FlaskForm):
    fav_cat_breed = StringField('Favorite Cat Breed or color', validators=[DataRequired()])
    fav_int_cat = StringField('Favorite Famous Cat', validators=[DataRequired()])
    fav_cat_fact = StringField('Favorite fact or thing about Cats', validators=[DataRequired()])
    submit = SubmitField()      



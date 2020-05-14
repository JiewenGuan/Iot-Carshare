from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import requests
from wtforms.fields.html5 import DateField, TimeField
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        r = requests.get('https://192.168.1.109:10100/uniq/{}'.format(username.data), verify=False)
        if 'error' in r.json():
            raise ValidationError('Please use a different username.')

class CarSearchForm(FlaskForm):
    body_type = SelectField('Car Type',coerce=int,validate_choice=False)
    colour = SelectField('Color',coerce=int,validate_choice=False)
    make = StringField(render_kw={"placeholder": "Make"})
    seats = IntegerField(render_kw={"placeholder": "Seats"})
    status = HiddenField(1)
    submit = SubmitField('Search')

class BookingForm(FlaskForm):
    car_id = HiddenField(validators=[DataRequired()])
    user_id = HiddenField(validators=[DataRequired()])
    date = DateField(validators=[DataRequired()])
    time = TimeField(validators=[DataRequired()])
    duration = IntegerField(validators=[DataRequired()],render_kw={"placeholder": "Hours"})
    submit = SubmitField('Book')


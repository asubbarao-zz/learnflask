from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm): 
  first_name = StringField("First name", validators=[DataRequired("You must enter a first name"), Length(min=2)])
  last_name = StringField("Last name", validators=[DataRequired("You must enter a last name"), Length(min=1)])
  email = StringField("Email", validators=[DataRequired("You must enter an email"), Email("must be an email")])
  password = PasswordField("Password", validators=[DataRequired("You must enter a password"), Length(min=6)])
  submit = SubmitField("Sign up")

#Form is a base FlaskForm
class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired("Enter email"), Email("Enter Email" )])
	password = PasswordField("Password", validators=[DataRequired("Enter password")])
	submit = SubmitField("Sign in")

class AddressForm(FlaskForm):
	address = StringField('Address', validators=[DataRequired("Enter an address")])
	submit = SubmitField("Search")
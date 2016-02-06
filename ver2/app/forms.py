from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from wtforms.validators import DataRequired, Length
from models import db, User

class EditForm(Form):
    firstname = StringField('firstname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

class SigninForm(Form):
  andrewid = TextField("Email",  [validators.Required("Please enter your andrewid.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(andrewid = self.andrewid.data.lower()).first()
    if user and user.password == self.password.data:
      return True
    else:
      self.andrewid.errors.append("Invalid id or password")
      return False


class SignUpForm(Form):
  firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
  lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
  andrewid = TextField("Andrew id",  [validators.Required("Please enter your andrewid.")])
  password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(andrewid = self.andrewid.data.lower()).first()
    if user:
      self.andrewid.errors.append("That andrew id is already taken")
      return False
    else:
      return True

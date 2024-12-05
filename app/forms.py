from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

class SignUpForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Firstname"})
    surname = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Surname"})
    email = StringField(validators=[InputRequired(), Length(min=5, max=49)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Sign up")

class EditForm(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Firstname"})
    surname = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Surname"})
    email = StringField(validators=[InputRequired(), Length(min=5, max=49)], render_kw={"placeholder": "Email"})
    submit = SubmitField("Update")

class PasswordForm(FlaskForm):
    old_password = PasswordField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Current password"})
    new_password = PasswordField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "New password"})
    submit = SubmitField("Change")

class SearchForm(FlaskForm):
    search = StringField(render_kw={"placeholder": "Search..."})
    submit = SubmitField("Go")

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=5, max=49)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class CheckoutForm(FlaskForm):
    address1 = StringField(validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "Address line 1"})
    address2 = StringField(render_kw={"placeholder": "Address line 2"})
    town = StringField(validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "Town/City"})
    postcode = StringField(validators=[InputRequired(), Length(min=1, max=10)], render_kw={"placeholder": "Postcode"})
    submit = SubmitField("Checkout")
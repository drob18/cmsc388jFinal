from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField,IntegerField,SelectField
from wtforms.validators import (
    InputRequired,
    DataRequired,
    NumberRange,
    Length,
    Email,
    EqualTo,
    ValidationError,
)


from .models import User

class SearchUserForm(FlaskForm):
    query = StringField("Username", validators=[InputRequired(), Length(min=1, max=100)])
    submit = SubmitField("Search")
    
class SearchForm(FlaskForm):
    search_query = StringField( "Query", validators=[InputRequired(), Length(min=1, max=100)])
    submit = SubmitField("Search")


class MovieReviewForm(FlaskForm):
    text = TextAreaField("Comment", validators=[InputRequired(), Length(min=5, max=500)])
    score = IntegerField("Score",validators=[NumberRange(min=1,max=5,message="Between 1 & 5")])
    submit = SubmitField("Enter Comment")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=40)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    accountType = SelectField("Account Type", choices=[('Terp Critic', 'Terp Critic'), ('Normal Critic', 'Normal Critic')])
    password = PasswordField("Password", validators=[InputRequired(),Length(min=5, max=20, message = 'Password must be at least 5 characters')])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")
    def validate_password(self,password):
        checkSpecials = '!@#$%^&*()'
        checkNums = '123456789'
        checkerOne = 0
        checkerTwo = 0
        print("This is the password: "+password.data)
        for curr in checkSpecials:
            if curr in password.data:
                checkerOne = 1
                break
        for currNum in checkNums:
            if currNum in password.data:
                checkerTwo = 1
        if checkerOne != 1 or checkerTwo != 1:
            raise ValidationError("Special characters and numbers must be included!")



class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class UpdateUsernameForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=40)])
    submit = SubmitField("Update Username")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user is not None:
                raise ValidationError("That username is already taken")

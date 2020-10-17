from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from .models import User


class SignupForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=25),
            Regexp(
                "^[a-zA-Z0-9]*$",
                message="The username should contain only a-z, A-Z, 0-9",
            ),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Length(min=3, max=40),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, max=40),
        ],
    )
    confirm = PasswordField(
        "Verify password",
        [
            DataRequired(),
            EqualTo("password", message="Password must match"),
        ],
    )

    def __init__(self, *args, **kwargs):
        """Create instance"""
        super(SignupForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form"""
        initial_validation = super(SignupForm, self).validate()

        if not initial_validation:
            return False

        user = User.query.filter_by(username=self.username.data).first()

        if user:
            self.username.errors.append("Username already registered")
            return False

        user = User.query.filter_by(email=self.email.data).first()

        if user:
            self.email.errors.append("Email already registered")
            return False

        return True


class LoginForm(FlaskForm):

    username = StringField("Username or Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        if "@" in self.username.data:
            self.user = User.query.filter_by(email=self.username.data).first()
            if not self.user.check_password_with_email(self.username.data, self.password.data):
                self.password.errors.append("Wrong password.")
                return False
        else:
            self.user = User.query.filter_by(username=self.username.data).first()
            if not self.user.check_password_with_username(self.username.data, self.password.data):
                self.password.errors.append("Wrong password.")
                return False

        if not self.user:
            self.username.errors.append("Unknown username or email")
            return False

        return True


class ProfileEditForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=25),
            Regexp(
                "^[a-zA-Z0-9]*$",
                message="The username should contain only a-z, A-Z, 0-9",
            ),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Length(min=3, max=40),
        ],
    )

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(ProfileEditForm, self).validate()

        if not initial_validation:
            return False

        user = User.query.filter_by(username=self.username.data).first()

        if user:
            self.username.errors.append("Username already registered")
            return False

        user = User.query.filter_by(email=self.email.data).first()

        if user:
            self.email.errors.append("Email already registered")
            return False

        return True









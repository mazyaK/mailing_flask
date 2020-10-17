from app import db, login_manager
from passlib.hash import bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.hash(password)

    def __str__(self):
        return self.username

    def get_id(self):
        return self.id

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @classmethod
    def check_password_with_email(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise Exception('Wrong password')
        return user

    @classmethod
    def check_password_with_username(cls, username, password):
        user = cls.query.filter(cls.username == username).one()
        if not bcrypt.verify(password, user.password):
            raise Exception('Wrong password')
        return user



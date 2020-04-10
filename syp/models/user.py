""" User object """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods

from flask import url_for
from flask_login import UserMixin

from syp import db, login_manager
from syp.models.social_media import SocialMedia


@login_manager.user_loader
def load_user(user_id):
    """ Required by the login manager, which uses it internally. """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pw = db.Column(db.String(60), nullable=False)
    birth_date = db.Column(db.DateTime)
    intro = db.Column(db.Text)

    recipes = db.relationship('Recipe', backref='user', lazy=True)
    media = db.relationship('SocialMedia', backref='user', lazy=True)

    def image_path(self):
        """Returns the path for the user image. """
        return url_for(
            'static', filename=f'images/users/{self.username}.jpg'
        )
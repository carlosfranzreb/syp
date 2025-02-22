""" Social media usernames of users. """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods


from syp import db
from syp.models.web import Web


class SocialMedia(db.Model):
    __tablename__ = 'social_media'
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    id_web = db.Column(db.Integer, db.ForeignKey('webs.id'), primary_key=True)
    username = db.Column(db.String(100), nullable=False)

    web = db.relationship('Web', backref='media', lazy=True)

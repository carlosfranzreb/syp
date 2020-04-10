""" Social media webs. """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods


from syp import db


class Web(db.Model):
    __tablename__ = 'webs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    link = db.Column(db.String(200), unique=True, nullable=False)
    users = db.relationship('SocialMedia', backref='web', lazy=True)

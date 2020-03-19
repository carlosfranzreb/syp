""" Models for the DB used by SQLAlchemy. """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods


from syp import db


class Unit(db.Model):
    __tablename__ = 't_units'
    id = db.Column(db.Integer, primary_key=True)
    singular = db.Column(db.String(20), nullable=False)
    plural = db.Column(db.String(20), nullable=False)
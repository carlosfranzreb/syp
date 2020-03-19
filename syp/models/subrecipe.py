""" Subrecipe: this can be a sauce, a side-dish, etc. 
It is not a recipe itself; it belongs to a recipe. """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods


from syp import db


class Subrecipe(db.Model):
    __tablename__ = 'subrecipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    steps = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    case_fem = db.Column(db.Boolean, nullable=False)  # 0=masc., 1=fem.
    steps = db.relationship('SubrecipeStep', backref='subrecipe', lazy=True)
    ingredients = db.relationship('Subquantity', backref='subrecipe', lazy=True)
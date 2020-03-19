""" Season of the recipe. """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods


from syp import db


class Season(db.Model):
    __tablename__ = 'seasons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    recipes = db.relationship('Recipe', backref='season', lazy=True)

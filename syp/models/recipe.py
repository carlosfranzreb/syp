""" Recipe. """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods

from datetime import datetime as dt
from flask import url_for

from syp import db
from syp.models.recipe_state import RecipeState


class Recipe(db.Model):
    # TODO: add function that gets url from name automatically.
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    url = db.Column(db.String(100), nullable=False, unique=True)
    time_prep = db.Column(db.Integer)
    time_cook = db.Column(db.Integer)
    intro = db.Column(db.Text)
    text = db.Column(db.Text)
    link_video = db.Column(db.String(100))
    health = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.now())
    changed_at = db.Column(db.DateTime)
    id_season = db.Column(db.Integer, db.ForeignKey('seasons.id'))
    id_state = db.Column(db.Integer, db.ForeignKey('recipe_states.id'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    steps = db.relationship('RecipeStep', backref='recipe', lazy=True, cascade='delete')
    ingredients = db.relationship('Quantity', backref='recipe', lazy=True, cascade='delete')

    def image_path(self, folder):
        """Returns the path for the recipe image in the given size. """
        return url_for(
            'static', filename=f'images/recipes/{folder}/{self.url}.jpg'
        )



""" Recipe. """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods


from syp import db
from syp.models.recipe_state import RecipeState


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    url = db.Column(db.String(100), nullable=False, unique=True)
    time_prep = db.Column(db.Integer, nullable=False)
    time_cook = db.Column(db.Integer, nullable=False)
    intro = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    link_video = db.Column(db.String(100), nullable=False)
    health = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    id_season = db.Column(db.Integer, db.ForeignKey('seasons.id'), nullable=False)
    id_state = db.Column(db.Integer, db.ForeignKey('recipe_states.id'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    steps = db.relationship('RecipeStep', backref='recipe', lazy=True)
    ingredients = db.relationship('Quantity', backref='recipe', lazy=True)


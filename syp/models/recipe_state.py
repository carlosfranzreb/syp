""" State of the recipe: unfinished, unpublished, published, deleted. """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods


from syp import db


class RecipeState(db.Model):
    __tablename__ = 'recipe_states'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False)
    label = db.Column(db.String(100))
    recipes = db.relationship('Recipe', backref='state', lazy=True)


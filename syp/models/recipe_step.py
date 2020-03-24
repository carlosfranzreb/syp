""" Step of a recipe. Consists of a number indicating its order and a string. """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods


from syp import db


class RecipeStep(db.Model):
    __tablename__ = 'recipe_steps'
    id = db.Column(db.Integer, primary_key=True)
    step_nr = db.Column(db.Integer, nullable=False)
    step = db.Column(db.String(500), nullable=False)
    id_recipe = db.Column(db.Integer, db.ForeignKey('recipes.id'),
                          nullable=False)

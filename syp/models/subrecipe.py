""" Subrecipe: this can be a sauce, a side-dish, etc. 
It is not a recipe itself; it belongs to a recipe. """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods


from sqlalchemy.sql.functions import now

from syp import db
from syp.models.subrecipe_step import SubrecipeStep
from syp.models.recipe_step import RecipeStep
from syp.models.subquantity import Subquantity


class Subrecipe(db.Model):
    __tablename__ = 'subrecipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    url = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=now())
    changed_at = db.Column(db.DateTime)
    is_feminine = db.Column(db.Boolean, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    steps = db.relationship('SubrecipeStep', backref='subrecipe', lazy=True, cascade='delete')
    ingredients = db.relationship('Subquantity', backref='subrecipe', lazy=True, cascade='delete')

    def uses(self):
        """ Returns the number of recipes on which the given subrecipe appears. """
        return RecipeStep.query.filter_by(step=str(self.id)).count()


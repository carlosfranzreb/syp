""" Models for the DB used by SQLAlchemy. """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods

from syp.models.quantity import Quantity
from syp.models.subquantity import Subquantity
from syp import db


class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    url = db.Column(db.String(100), nullable=False, unique=True)
    health = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)  # nullable not necessary because of default.
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    changed_at = db.Column(db.DateTime)  # nullable not necessary because of default.
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_valid = db.Column(db.Boolean, default=False)

    creator = db.relationship(
        'User', backref='ingredient', foreign_keys='Ingredient.created_by', lazy=True
    )

    def __repr__(self):
        return self.name

    def uses(self):
        """ Returns the amount of recipes and subrecipes that use it. """
        recipe_count = Quantity.query.filter_by(id_ingredient=self.id).count()
        subrecipe_count = Subquantity.query.filter_by(id_ingredient=self.id).count()
        return recipe_count + subrecipe_count


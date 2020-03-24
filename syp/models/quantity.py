""" Quantities represent ingredients within recipes, with their corresponding
amounts and units. """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods


from syp import db


class Quantity(db.Model):
    __tablename__ = 'ingredients_in_recipe'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    id_recipe = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    id_ingredient = db.Column(
        db.Integer, db.ForeignKey('ingredients.id'), nullable=False
    )
    id_unit = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)

    ingredient = db.relationship('Ingredient', lazy=True)
    unit = db.relationship('Unit', lazy=True)

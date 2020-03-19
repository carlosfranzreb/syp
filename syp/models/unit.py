""" Unit of the quantity of an ingredient in a recipe or subrecipe.
Here are the names of the units in singular and plural.  """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods


from syp import db


class Unit(db.Model):
    __tablename__ = 'units'
    id = db.Column(db.Integer, primary_key=True)
    singular = db.Column(db.String(20), nullable=False)
    plural = db.Column(db.String(20), nullable=False)
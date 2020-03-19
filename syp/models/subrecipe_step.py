""" Step of a subrecipe. Consists of a number indicating its order and a string. """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods


from syp import db


class SubrecipeStep(db.Model):
    __tablename__ = 'subrecipe_steps'
    id = db.Column(db.Integer, primary_key=True)
    step_nr = db.Column(db.Integer, nullable=False)
    step = db.Column(db.String(500), nullable=False)
    id_subrecipe = db.Column(db.Integer, db.ForeignKey('subrecipes.id'),
                             nullable=False)
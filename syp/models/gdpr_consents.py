""" Quantities represent ingredients within recipes, with their corresponding
amounts and units. """
# pylint: disable=no-member, missing-class-docstring, too-few-public-methods


from datetime import datetime as dt
from syp import db


class GDPR(db.Model):
    __tablename__ = 'gdpr_consents'
    ip = db.Column(db.Integer, primary_key=True)
    has_consented = db.Column(db.Boolean, nullable=False)
    asked_at = db.Column(db.DateTime, nullable=False, default=dt.now()) 

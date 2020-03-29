""" Functions to create new ingredients. """


from flask_login import current_user

from syp.recipes.utils import get_url_from_name
from syp.models.ingredient import Ingredient
from syp import db


def save_ingredient(form):
    """ Save the newly created ingredient. """
    db.session.add(Ingredient(
        name=form.name.data,
        url=get_url_from_name(form.name.data),
        health=form.health.data,
        created_by=current_user.id,
    ))
    db.session.commit()

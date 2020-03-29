
from datetime import datetime as dt

from syp.recipes.utils import get_url_from_name
from syp import db


def update_ingredient(ingredient, form):
    """ Updates name, ingredients and steps of ingredient. """
    ingredient.changed_at = dt.now()
    if ingredient.name != form.name.data:
        new_name = form.name.data
        ingredient.name = new_name
        ingredient.url = get_url_from_name(new_name)
    if ingredient.health != form.health.data:
        ingredient.health = form.health.data
    db.session.commit()

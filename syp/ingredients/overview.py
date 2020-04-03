""" Functions related to the list of ingredients shown to users. """


from flask import request
from flask_login import current_user
# from sqlalchemy import func

from syp.models.ingredient import Ingredient


def sort_by_name(desc, limit=None, items=9):
    """ Sort overview ingredient by name. """
    page = request.args.get('page', 1, type=int)
    if desc == 'True':
        recipes = Ingredient.query \
            .order_by(Ingredient.name.desc()) \
            .limit(limit).paginate(page=page, per_page=items)
    else:
        recipes = Ingredient.query \
            .order_by(Ingredient.name) \
            .limit(limit).paginate(page=page, per_page=items)
    return (page, recipes)


def sort_by_date(desc, limit=None, items=9):
    """ Sort overview ingredient by name. """
    page = request.args.get('page', 1, type=int)
    if desc == 'True':
        recipes = Ingredient.query \
            .order_by(Ingredient.created_at.desc()) \
            .limit(limit).paginate(page=page, per_page=items)
    else:
    # .order_by(func.coalesce(Recipe.changed_at, Recipe.created_at)) \
        recipes = Ingredient.query \
            .order_by(Ingredient.created_at) \
            .limit(limit).paginate(page=page, per_page=items)
    return (page, recipes)


def search_name(name, limit=None, items=9):
    """ Search ingredient list. """
    page = request.args.get('page', 1, type=int)
    recipes = Ingredient.query \
        .filter(Ingredient.name.contains(name)) \
        .order_by(Ingredient.name) \
        .limit(limit).paginate(page=page, per_page=items)
    return (page, recipes)

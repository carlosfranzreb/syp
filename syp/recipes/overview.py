""" Functions related to the list of owned recipes shown to users. """


from flask import request
from flask_login import current_user
# from sqlalchemy import func

from syp.models.recipe import Recipe


def sort_by_name(desc, limit=None, items=9):
    """ Sort overview recipes by name. """
    page = request.args.get('page', 1, type=int)
    if desc == 'True':
        recipes = Recipe.query \
            .filter_by(id_user=current_user.id) \
            .order_by(Recipe.name.desc()) \
            .limit(limit).paginate(page=page, per_page=items)
    else:
        recipes = Recipe.query \
            .filter_by(id_user=current_user.id) \
            .order_by(Recipe.name) \
            .limit(limit).paginate(page=page, per_page=items)
    return (page, recipes)


def sort_by_date(desc, limit=None, items=9):
    """ Sort overview recipes by name. """
    page = request.args.get('page', 1, type=int)
    if desc == 'True':
        recipes = Recipe.query \
            .filter_by(id_user=current_user.id) \
            .order_by(Recipe.created_at.desc()) \
            .limit(limit).paginate(page=page, per_page=items)
    else:
    # .order_by(func.coalesce(Recipe.changed_at, Recipe.created_at)) \
        recipes = Recipe.query \
            .filter_by(id_user=current_user.id) \
            .order_by(Recipe.created_at) \
            .limit(limit).paginate(page=page, per_page=items)
    return (page, recipes)


def sort_by_state(desc, limit=None, items=9):
    """ Sort overview recipes by state. """
    page = request.args.get('page', 1, type=int)
    if desc == 'True':
        recipes = Recipe.query \
            .filter_by(id_user=current_user.id) \
            .order_by(Recipe.id_state.desc()) \
            .limit(limit).paginate(page=page, per_page=items)
    else:
        recipes = Recipe.query \
            .filter_by(id_user=current_user.id) \
            .order_by(Recipe.id_state) \
            .limit(limit).paginate(page=page, per_page=items)
    return (page, recipes)

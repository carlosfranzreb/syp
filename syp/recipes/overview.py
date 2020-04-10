""" Functions related to the list of owned recipes shown to users. """


from flask import request
from flask_login import current_user
from sqlalchemy import func

from syp.models.recipe import Recipe


def sort(order, desc, limit, items):
    """ Return recipes sorted with the given order. """
    if desc == 'True':
        order = order.desc()
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query \
        .filter_by(id_user=current_user.id) \
        .order_by(order) \
        .limit(limit).paginate(page=page, per_page=items)
    return (page, recipes)


def sort_by_name(desc, limit=None, items=9):
    """ Sort overview recipes by name. """
    return sort(Recipe.name, desc, limit, items)


def sort_by_date(desc, limit=None, items=9):
    """ Sort overview recipes by name. """
    order = func.coalesce(Recipe.changed_at, Recipe.created_at)
    return sort(order, desc, limit, items)


def sort_by_state(desc, limit=None, items=9):
    """ Sort overview recipes by state. """
    return sort(Recipe.id_state, desc, limit, items)


def search_name(name, limit=None, items=9):
    """ Search recipe list. """
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query \
        .filter_by(id_user=current_user.id) \
        .filter(Recipe.name.contains(name)) \
        .order_by(Recipe.name) \
        .limit(limit).paginate(page=page, per_page=items)
    return (page, recipes)

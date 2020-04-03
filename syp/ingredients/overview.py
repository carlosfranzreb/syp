""" Functions related to the list of ingredients shown to users. """


from flask import request
from sqlalchemy import func

from syp.models.ingredient import Ingredient


def sort(order, desc, limit, items):
    """ Return ingredients sorted with the given order. """
    if desc == 'True':
        order = order.desc()
    page = request.args.get('page', 1, type=int)
    ingredients = Ingredient.query \
        .order_by(order) \
        .limit(limit).paginate(page=page, per_page=items)
    return (page, ingredients)


def sort_by_name(desc, limit=None, items=9):
    """ Sort overview ingredient by name. """
    return sort(Ingredient.name, desc, limit, items)


def sort_by_date(desc, limit=None, items=9):
    """ Sort overview ingredient by date. """
    order = func.coalesce(Ingredient.changed_at, Ingredient.created_at)
    return sort(order, desc, limit, items)


def sort_by_creator(desc, limit=None, items=9):
    """ Sort overview ingredient by date. """
    order = Ingredient.creator.name
    return sort(order, desc, limit, items)


def search_name(name, limit=None, items=9):
    """ Search ingredient list. """
    page = request.args.get('page', 1, type=int)
    recipes = Ingredient.query \
        .filter(Ingredient.name.contains(name)) \
        .order_by(Ingredient.name) \
        .limit(limit).paginate(page=page, per_page=items)
    return (page, recipes)

""" Functions related to the list of owned subrecipes shown to users. """


from flask import request
from flask_login import current_user
from sqlalchemy import func

from syp.models.subrecipe import Subrecipe


def sort(order, desc, limit, items):
    """ Return subrecipes sorted with the given order. """
    if desc == 'True':
        order = order.desc()
    page = request.args.get('page', 1, type=int)
    subrecipes = Subrecipe.query \
        .order_by(order) \
        .limit(limit).paginate(page=page, per_page=items)
    return (page, subrecipes)


def sort_by_name(desc, limit=None, items=9):
    """ Sort overview subrecipes by name. """
    return sort(Subrecipe.name, desc, limit, items)


def sort_by_date(desc, limit=None, items=9):
    """ Sort overview subrecipes by name. """
    order = func.coalesce(Subrecipe.changed_at, Subrecipe.created_at)
    return sort(order, desc, limit, items)


def search_name(name, limit=None, items=9):
    """ Search recipe list. """
    page = request.args.get('page', 1, type=int)
    recipes = Subrecipe.query \
        .filter_by(id_user=current_user.id) \
        .filter(Subrecipe.name.contains(name)) \
        .order_by(Subrecipe.name) \
        .limit(limit).paginate(page=page, per_page=items)
    return (page, recipes)

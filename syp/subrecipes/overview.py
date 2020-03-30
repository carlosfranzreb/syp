""" Functions related to the list of owned subrecipes shown to users. """


from flask import request
from flask_login import current_user
# from sqlalchemy import func

from syp.models.subrecipe import Subrecipe


def sort_by_name(desc, limit=None, items=9):
    """ Sort overview subrecipes by name. """
    page = request.args.get('page', 1, type=int)
    if desc == 'True':
        recipes = Subrecipe.query \
            .filter_by(id_user=current_user.id) \
            .order_by(Subrecipe.name.desc()) \
            .limit(limit).paginate(page=page, per_page=items)
    else:
        recipes = Subrecipe.query \
            .filter_by(id_user=current_user.id) \
            .order_by(Subrecipe.name) \
            .limit(limit).paginate(page=page, per_page=items)
    return (page, recipes)


def sort_by_date(desc, limit=None, items=9):
    """ Sort overview subrecipes by name. """
    page = request.args.get('page', 1, type=int)
    if desc == 'True':
        recipes = Subrecipe.query \
            .filter_by(id_user=current_user.id) \
            .order_by(Subrecipe.created_at.desc()) \
            .limit(limit).paginate(page=page, per_page=items)
    else:
    # .order_by(func.coalesce(Recipe.changed_at, Recipe.created_at)) \
        recipes = Subrecipe.query \
            .filter_by(id_user=current_user.id) \
            .order_by(Subrecipe.created_at) \
            .limit(limit).paginate(page=page, per_page=items)
    return (page, recipes)


def search_name(name, limit=None, items=9):
    """ Search recipe list. """
    page = request.args.get('page', 1, type=int)
    recipes = Subrecipe.query \
        .filter_by(id_user=current_user.id) \
        .filter(Subrecipe.name.contains(name)) \
        .order_by(Subrecipe.name) \
        .limit(limit).paginate(page=page, per_page=items)
    return (page, recipes)

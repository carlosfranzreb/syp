""" Help functions for ingredients. """
# pylint: disable = missing-function-docstring


from flask import abort, request

from syp.models.ingredient import Ingredient
from syp.search.utils import get_default_keywords


def get_ingredient_by_name(name):
    ing = Ingredient.query.filter_by(name=name).first()
    if ing is None:
        return abort(404)
    return ing


def get_ingredient_by_url(url):
    ing = Ingredient.query.filter_by(url=url).first()
    if ing is None:
        return abort(404)
    return ing


def get_all_ingredients():
    """ returns name of all ingredients as a list of tuples """
    return Ingredient.query.with_entities(Ingredient.name) \
                           .order_by(Ingredient.name).all()


def get_paginated_ingredients(limit=None, items=20):
    """ Returns paginated ingredients. """
    page = request.args.get('page', 1, type=int)
    ingredients = Ingredient.query \
        .order_by(Ingredient.name) \
        .limit(limit) \
        .paginate(page=page, per_page=items)
    return (page, ingredients)


def get_ing_keywords(ing_name=None):
    """ SEO keywords specific to this page. """
    ing_keys = get_default_keywords()
    if ing_name is not None:
        ing_keys += f', receta vegana con {ing_name}, '
        ing_keys += f'receta saludable con {ing_name}, '
        ing_keys += f'receta casera con {ing_name}'
    else:
        ing_keys += 'buscar receta vegana por ingrediente, \
                     buscar receta saludable por ingrediente, \
                     buscar receta casera por ingrediente'

    return ' '.join(ing_keys.split())

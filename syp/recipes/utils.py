from flask import abort, request
from syp.search.utils import get_default_keywords
from syp.models import Recipe, Quantity, Subquantity, Ingredient, Subrecipe
import ast


def get_recipe_by_name(recipe_name):
    recipe = Recipe.query.filter_by(name=recipe_name).first()
    if recipe is None:
        abort(404)
    else:
        # set duplicate method for health comments
        ids = []
        for q in recipe.ingredients:
            q.duplicate = False
            ids.append(q.ingredient.id)
        for sub in recipe.subrecipes:
            for q in sub.ingredients:
                id = q.ingredient.id
                if id not in ids:
                    q.duplicate = False
                    ids.append(id)
                else:
                    q.duplicate = True
        return recipe


def get_recipe_by_url(recipe_url):
    recipe = Recipe.query.filter_by(url=recipe_url).first()
    if recipe is None:
        abort(404)
    else:
        # set duplicate method for health comments
        ids = []
        for q in recipe.ingredients:
            q.duplicate = False
            ids.append(q.ingredient.id)
        for sub in recipe.subrecipes:
            for q in sub.ingredients:
                id = q.ingredient.id
                if id not in ids:
                    q.duplicate = False
                    ids.append(id)
                else:
                    q.duplicate = True
        return recipe


def get_last_recipes(limit=None):
    """ returns recipes starting with the most recent one
        Images are sized 300"""
    recipes = Recipe.query.order_by(Recipe.date_created.desc()) \
                          .limit(limit).all()

    return recipes


def get_paginated_recipes(limit=None, items=9):
    """ returns paginated recipes starting with the most recent one
        Images are medium sized"""
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.date_created.desc()) \
                          .limit(limit).paginate(page=page, per_page=items)

    return (page, recipes)


def get_recipe_keywords(recipe):
    recipe_keys = get_default_keywords() + ', '
    for q in recipe.ingredients:
        name = q.ingredient.name.lower()
        recipe_keys += f'receta vegana con {name}, '
        recipe_keys += f'receta saludable con {name}, '
    return ' '.join(recipe_keys[:-2].split())


def get_all_subrecipes():
    return Subrecipe.query.with_entities(Subrecipe.name) \
                          .order_by(Subrecipe.name).all()


def get_subrecipe(id):
    return Subrecipe.query.filter_by(id=id).first()

""" Help function for recipe-related pages. """
#pylint: disable = missing-function-docstring


from flask import abort, request

from syp.search.utils import get_default_keywords
from syp.models.recipe import Recipe
from syp.models.subrecipe import Subrecipe


def get_recipe_by_name(recipe_name):
    recipe = Recipe.query.filter_by(name=recipe_name).first()
    recipe.subrecipes = get_subrecipes(recipe)
    return discard_duplicates(recipe)


def get_recipe_by_url(recipe_url):
    recipe = Recipe.query.filter_by(url=recipe_url).first()
    recipe.subrecipes = get_subrecipes(recipe)
    return discard_duplicates(recipe)


def discard_duplicates(recipe):
    if recipe is None:
        return abort(404)
    ingredient_ids = []
    for quantity in recipe.ingredients:
        quantity.duplicate = False
        ingredient_ids.append(quantity.ingredient.id)
    for sub in recipe.subrecipes:
        for quantity in sub.ingredients:
            ingredient_id = quantity.ingredient.id
            if ingredient_id not in ingredient_ids:
                quantity.duplicate = False
                ingredient_ids.append(ingredient_id)
            else:
                quantity.duplicate = True
    return recipe


def get_last_recipes(limit=None):
    """ returns recipes starting with the most recent one
        Images are sized 300"""
    recipes = Recipe.query.order_by(Recipe.created_at.desc()) \
                          .limit(limit).all()

    return recipes


def get_paginated_recipes(limit=None, items=9):
    """ returns paginated recipes starting with the most recent one
        Images are medium sized"""
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.created_at.desc()) \
                          .limit(limit).paginate(page=page, per_page=items)

    return (page, recipes)


def get_recipe_keywords(recipe):
    recipe_keys = get_default_keywords() + ', '
    for quantity in recipe.ingredients:
        name = quantity.ingredient.name.lower()
        recipe_keys += f'receta vegana con {name}, '
        recipe_keys += f'receta saludable con {name}, '
    return ' '.join(recipe_keys[:-2].split())


def get_all_subrecipes():
    return Subrecipe.query.with_entities(Subrecipe.name) \
                          .order_by(Subrecipe.name).all()


def get_subrecipe(subrecipe_id):
    return Subrecipe.query.filter_by(id=subrecipe_id).first()


def get_subrecipes(recipe):
    """ Get subrecipes used in the given recipe. 
    If the step consists only of one int, then it is a reference to a subrecipe. """
    subrecipes = list()
    recipe_steps = recipe.steps
    for step in recipe.steps:
        try:  # if the step is an int, it is a subrecipe.
            subrecipe_id = int(step.step)
            subrecipes.append(Subrecipe.query.filter_by(id=subrecipe_id).first())
        except ValueError:  # Step is not a subrecipe.
            continue
    return subrecipes

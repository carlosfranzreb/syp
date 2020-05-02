""" Decorators used for recipes. """


from operator import attrgetter
from flask import abort

from syp.models.subrecipe import Subrecipe


def prepare_recipe(func):
    """ Add subrecipes, sort steps and remove duplicates from ingredients. """
    def prepare(*args, **kwargs):
        recipe = func(*args, **kwargs)
        recipe.subrecipes = get_subrecipes(recipe)
        recipe.steps.sort(key=attrgetter('step_nr'))
        return discard_duplicates(recipe)
    return prepare


def discard_duplicates(recipe):
    """ Discard duplicate ingredients. This happens when an
    ingredient appears in both the recipe and one subrecipe, or in
    multiple subrecipes. Required for the health comments. """
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


def get_subrecipes(recipe):
    """ Get subrecipes used in the given recipe. If the step consists
    only of one int, then it is a reference to a subrecipe. """
    subrecipes = list()
    for step in recipe.steps:
        try:  # if the step is an int, it is a subrecipe.
            subrecipe_id = int(step.step)
            subrecipes.append(
                Subrecipe.query.filter_by(id=subrecipe_id).first()
            )
        except ValueError:  # Step is not a subrecipe.
            continue
    return subrecipes

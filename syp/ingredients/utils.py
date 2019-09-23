from flask import abort, request
from string import Template
from syp.models import Recipe, Subrecipe, Quantity, Subquantity, Ingredient
from syp.search.utils import get_default_keywords


def get_ingredient_by_name(name):
    ing = Ingredient.query.filter_by(name=name).first()
    if ing is None:
        abort(404)
    else:
        return ing


def get_ingredient_by_url(url):
    ing = Ingredient.query.filter_by(url=url).first()
    if ing is None:
        abort(404)
    else:
        return ing


def get_recipes_by_ingredient(ing_name, items=9):
    """ Returns recipes by ingredient, the one that was created last goes first
        (ids in descent).
        If ingredient is in subrecipe, recipes that contain that subrecipe
        will be shown at the end.
        If $name is not an ingredient or a subrecipe, return error message
        If ingredient is found, but there are no recipes with it, that means
        that there was a recipe and it was deleted."""

    recipes = Recipe.query.join(Quantity, Recipe.id == Quantity.id_recipe) \
                          .join(Ingredient, Quantity.id_ingredient
                                == Ingredient.id).filter(Ingredient.name
                                                         .contains(ing_name)) \
                          .with_entities(Recipe.name, Recipe.intro)

    recipes = recipes.union(get_subrecipes_by_ingredient(ing_name))
    page = request.args.get('page', 1, type=int)
    recipes = recipes.paginate(page=page, per_page=items)

    if recipes.items == []:
        recipes = Template('No tenemos recetas con $name. \
                            ¡Prueba con otro ingrediente!') \
                           .substitute(name=ing_name.lower())

    return (page, recipes)


def get_subrecipes_by_ingredient(ing):
    """Returns recipes that contain a subrecipe with the ingredient"""
    subs = Subrecipe.query.join(Subquantity, Subrecipe.id ==
                                Subquantity.id_subrecipe) \
                          .join(Ingredient, Subquantity.id_ingredient ==
                                Ingredient.id).filter(Ingredient.name
                                                      .contains(ing)).all()
    # empty query, to extend in the for loop
    recipes = Recipe.query.filter_by(id=0)
    for subrecipe in subs:
        recipes = recipes.union(Recipe.query.filter(Recipe.subrecipes
                                                    .contains(subrecipe)))

    return recipes.with_entities(Recipe.name, Recipe.intro)


def get_all_ingredients():
    """ returns name of all ingredients as a list of tuples """
    return Ingredient.query.with_entities(Ingredient.name) \
                           .order_by(Ingredient.name).all()


def get_ing_keywords(ing_name=None):
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

""" Help functions for the search-by-name page. """


from string import Template
from flask import request

from syp.models.recipe import Recipe
from syp.models.user import User


def get_recipes_by_name(recipe_name, items=9):
    """ returns published recipes (not subrecipes) that contain 
    the given name. """
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query \
        .filter_by(id_state=3) \
        .filter(Recipe.name.contains(recipe_name)) \
        .order_by(Recipe.created_at.desc()) \
        .paginate(page=page, per_page=items)
    if recipes.items == []:
        recipes = Template(
            'No tenemos recetas llamadas $name. ¡Prueba con otra receta!'
        ).substitute(name=recipe_name.lower())
    return (page, recipes)


def get_user_id(username):
    return User.query.filter_by(username=username).first().id


def all_cook_recipes(username, items=9):
    """ Returns all recipes of a given cook, paginated. """
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query \
        .filter_by(id_user=get_user_id(username)) \
        .filter_by(id_state=3) \
        .order_by(Recipe.created_at.desc()) \
        .paginate(page=page, per_page=items)
    if recipes.items == []:
        recipes = Template(
            '$name no ha publicado una receta todavía. ¡Prueba con otro cocinero!'
        ).substitute(name=username)
    return (page, recipes)


def cook_recipe_names(username):
    """ Returns the names of all recipes of the given username. """
    return Recipe.query \
        .filter_by(id_user=get_user_id(username)) \
        .filter_by(id_state=3) \
        .with_entities(Recipe.name) \
        .order_by(Recipe.name).all()


def cook_recipes(username, recipe_name, items=9):
    """ Returns all recipes of a given cook, paginated. """
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query \
        .filter_by(id_user=get_user_id(username)) \
        .filter_by(id_state=3) \
        .filter(Recipe.name.contains(recipe_name)) \
        .order_by(Recipe.created_at.desc()) \
        .paginate(page=page, per_page=items)
    if recipes.items == []:
        recipes = Template(
            '$name no tiene recetas llamadas "$recipe". ¡Prueba con otra receta!'
        ).substitute(name=username, recipe=recipe_name)
    return (page, recipes)


def get_default_keywords():
    """ SEO keywords. """
    keys = "receta vegana, receta saludable, receta sana, plato vegano, \
            plato saludable, cocina vegana, receta casera vegana, \
            salud y pimienta, syp"
    return ' '.join(keys.split())


def get_search_keywords(recipe_name):
    """ SEO keywords specific for the search page. """
    search_keys = get_default_keywords()
    search_keys += f', {recipe_name} receta vegana, '
    search_keys += f'{recipe_name} receta saludable, '
    search_keys += f'{recipe_name} receta casera'
    return ' '.join(search_keys.split())

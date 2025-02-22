""" Help functions for the search-by-season page. """


from datetime import date
from flask import abort, request

from syp.models.recipe import Recipe
from syp.models.season import Season
from syp.search.utils import get_default_keywords


def get_season_recipes(season_nr=None, items=9):
    """ returns recipes (not subrecipes) of the given season.
        If input is None, gets actual season
        If input is name, gets season number under that name"""
    if season_nr is None:
        season_nr = get_current_season()
    elif isinstance(season_nr, str):
        season_nr = get_season_nr(season_nr)
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query \
        .filter_by(id_state=3) \
        .filter(Recipe.id_season.in_((season_nr, 5))) \
        .order_by(Recipe.id_season) \
        .paginate(page=page, per_page=items)
    return (page, recipes)


def get_season_name(season_nr):
    """ Retrieve season name given its ID. """
    season = Season.query.filter_by(id=season_nr).first()
    return season.name


def get_season_nr(season_name):
    """Returns the number of the given season name
       If input is not a season, abort 404"""
    season = Season.query.filter_by(name=season_name).first()
    if season is not None:
        return season.id
    return abort(404)


def get_current_season():
    """ Output the current season given the current date. """
    month_nr = date.today().month
    return (month_nr % 12 + 3) // 3


def get_current_season_name():
    """ Get name of the current season, using the function get_current_season(). """
    month_nr = get_current_season()
    return get_season_name(month_nr)


def get_season_keywords(season_name):
    """ SEO keywords specific to this page. """
    season_keys = get_default_keywords()
    season_keys += f', receta vegana para {season_name}, '
    season_keys += f'receta saludable para {season_name}, '
    season_keys += f'receta casera para {season_name}'
    return ' '.join(season_keys.split())

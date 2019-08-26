from datetime import date
from flask import abort, request
from syp.models import Recipe
from syp.search.utils import get_default_keywords


def get_season_recipes(season_nr=None, items=9):
    """ returns recipes (not subrecipes) of the given season.
        If input is None, gets actual season
        If input is name, gets season number under that name"""
    if season_nr is None:
        season_nr = get_actual_season()
    elif isinstance(season_nr, str):
        season_nr = get_season_nr(season_nr)

    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.filter(Recipe.id_season.in_((season_nr, 5))) \
                          .order_by(Recipe.id_season) \
                          .paginate(page=page, per_page=items)

    return (page, recipes)


def get_season_name(season_nr):
    seasons = {1: 'invierno', 2: 'primavera', 3: 'verano', 4: 'otoño'}
    return seasons[season_nr]


def get_season_nr(season_name):
    """Returns the number of the given season name
       If input is not a season, abort 404"""
    seasons = {'invierno': 1, 'primavera': 2, 'verano': 3, 'otoño': 4}
    if season_name in seasons:
        return seasons[season_name]
    else:
        abort(404)


def get_actual_season():
    month_nr = date.today().month
    return (month_nr % 12 + 3) // 3


def get_actual_season_name():
    month_nr = get_actual_season()
    return get_season_name(month_nr)


def get_season_keywords(season_name):
    season_keys = get_default_keywords()
    season_keys += f', receta vegana para {season_name}, '
    season_keys += f'receta saludable para {season_name}, '
    season_keys += f'receta casera para {season_name}'

    return ' '.join(season_keys.split())

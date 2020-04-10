from flask import Blueprint, redirect, render_template, url_for
from syp.recipes.utils import get_last_recipes
from syp.search.forms import SearchRecipeForm
from syp.seasons.utils import get_current_season_name, get_season_name, \
                              get_season_recipes, get_season_keywords
from syp.seasons.forms import SeasonForm


seasons = Blueprint('seasons', __name__)


@seasons.route('/temporada')
def search_current_season():
    """ Opens when season searcher is called.
        Looks for current season and redirects """
    current_season_name = get_current_season_name()
    return redirect(url_for(
        'seasons.search_season', season_name=current_season_name
    ))


@seasons.route('/temporada/<season_name>', methods=['GET', 'POST'])
def search_season(season_name):
    if season_name == 'Todo el año':
        return redirect(url_for('seasons.search_current_season'))
    form = SeasonForm()
    if form.is_submitted():
        form_name = get_season_name(int(form.season.data))
        return redirect(url_for('seasons.search_season',
                                season_name=form_name))

    page, recs = get_season_recipes(season_name)
    desc = f'Recetas para {season_name}. Escoge recetas de la temporada \
             actual para cocinar con productos frescos y locales. Apoya a los \
             negocios y agricultores de tu ciudad mientras que le echas una \
             mano al medio ambiente.'
    return render_template(
        'search_season.html',
        title=season_name,
        recipe_form=SearchRecipeForm(),
        form=form,
        season_name=season_name,
        recipes=recs,
        last_recipes=get_last_recipes(4),
        description=' '.join(desc.split()),
        keywords=get_season_keywords(season_name)
    )

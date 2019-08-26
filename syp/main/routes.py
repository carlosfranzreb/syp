from flask import Blueprint, render_template, send_from_directory
from syp.recipes.utils import get_last_recipes
from syp.search.forms import RecipesForm
from syp.search.utils import get_default_keywords


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
@main.route('/inicio', methods=['GET', 'POST'])
def get_home():
    desc = 'Recetas veganas para cualquier ocasión. Nos ajustamos al tiempo \
            que tengas, los ingredientes que tengas por casa, tus antojos, y \
            la temporada. Échale un vistazo a nuestros buscadores, o déjanos \
            inspirarte con la receta de la semana.'
    return render_template('home.html',
                           title='Inicio',
                           recipe_form=RecipesForm(),
                           last_recipes=get_last_recipes(9),
                           description=' '.join(desc.split()),
                           keywords=get_default_keywords())


@main.route('/info')
def get_philosophy():
    desc = 'En este blog queremos demostrar que no hace falta sacrificar el \
            sabor para ser vegano, ni para mantener un buen estado de salud.'
    return render_template('philosophy.html',
                           title='Filosofía',
                           recipe_form=RecipesForm(),
                           last_recipes=get_last_recipes(4),
                           description=' '.join(desc.split()),
                           keywords=get_default_keywords() + ', filosofía')


@main.route('/privacidad')
def get_privacy():
    desc = 'La privacidad de tus datos es muy importante para nosotros. \
            Tanto, que no almacenamos ninguno en nuestras bases de datos'
    return render_template('privacy.html',
                           title='Privacidad',
                           recipe_form=RecipesForm(),
                           last_recipes=get_last_recipes(4),
                           description=' '.join(desc.split()),
                           keywords=get_default_keywords() + ', privacidad')


@main.route('/donar')
def get_donate():
    desc = 'Con vuestras donaciones hacemos de este blog un proyecto \
            sostenible y libre de anuncios.'
    return render_template('donate.html',
                           title='Donar',
                           recipe_form=RecipesForm(),
                           last_recipes=get_last_recipes(4),
                           description=' '.join(desc.split()),
                           keywords=get_default_keywords() + ', donación')


@main.route('/robots.txt')
def get_robots():
    return send_from_directory('static', filename='files/robots.txt')


@main.route('/sitemap.xml')
def get_sitemap():
    return send_from_directory('static', filename='files/sitemap.xml')

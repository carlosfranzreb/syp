from string import Template
from urllib.parse import urlparse
from flask import request

from syp.models.user import User
from syp.models.recipe import Recipe
from syp.search.utils import get_default_keywords


def get_url():
    """ Retrieve only the path not the host. """
    parse = urlparse(request.args.get('url'))
    return parse.path


def get_user(username):
    """ Return user with the given username. """
    return User.query.filter_by(username=username).first()


def last_user_recipes(user_id, limit=8):
    """ Return the last recipes published by the user. """
    return Recipe.query \
        .filter_by(id_user=user_id) \
        .filter_by(id_state=3) \
        .order_by(Recipe.created_at.desc()) \
        .limit(limit).all()


def paginated_cooks(items=8):
    """ returns cooks by username"""
    page = request.args.get('page', 1, type=int)
    cooks = User.query \
        .order_by(User.username) \
        .paginate(page=page, per_page=items)
    return (page, cooks)


def all_usernames():
    """ returns usernames of cooks by username. Used for the
    drop-down list from which to choose a user. """
    return User.query \
        .with_entities(User.username) \
        .order_by(User.username).all()


def get_cooks(username, items=8):
    """ returns cooks by username"""
    page = request.args.get('page', 1, type=int)
    cooks = User.query \
        .filter(User.username.contains(username)) \
        .order_by(User.username) \
        .paginate(page=page, per_page=items)
    if cooks.items == []:
        cooks = Template(
            'No hay cocineros llamados $name. ¡Prueba con otro nombre!'
        ).substitute(name=username.lower())
    return (page, cooks)
   

def get_cook_keywords(username='SyP'):
    """ SEO keywords specific for the search page. """
    search_keys = get_default_keywords()
    search_keys += f', recetas veganas de {username}, '
    search_keys += f'recetas saludables de {username}, '
    search_keys += f'recetas caseras de {username}'
    return ' '.join(search_keys.split())

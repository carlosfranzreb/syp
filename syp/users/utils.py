from urllib.parse import urlparse
from flask import request

from syp.models.user import User
from syp.models.recipe import Recipe


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

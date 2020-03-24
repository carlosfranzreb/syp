""" Help functions for the subrecipes page.
Can only be accessed by logged in chefs. """


from flask import request
from flask_login import current_user

from syp import db
from syp.models.subrecipe import Subrecipe


def get_paginated_subrecipes(limit=None, items=20):
    """ Returns paginated recipes starting with the most recent one. 
    It only returns recipes that have not been deleted. """
    page = request.args.get('page', 1, type=int)
    subrecipes = Subrecipe.query \
        .filter_by(id_user=current_user.id) \
        .filter_by(is_deleted=False) \
        .order_by(Subrecipe.created_at.desc()) \
        .limit(limit).paginate(page=page, per_page=items)
    return (page, subrecipes)


def get_subrecipe_by_url(subrecipe_url):
    """ Return the subrecipe object with the given url. """
    return Subrecipe.query.filter_by(url=subrecipe_url).first()


def delete_subrecipe(subrecipe):
    """ Marks subrecipe as deleted. """
    subrecipe.is_deleted = True
    db.session.commit()


def create_subrecipe():
    """ Creates and returns an empty subrecipe. """
    subrecipe = Subrecipe(
        name="Nueva subreceta",
        url="nueva_subreceta",
        id_user=current_user.id
    )
    return subrecipe

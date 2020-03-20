""" Help functions for the subrecipes page.
Can only be accessed by logged in chefs. """


from flask import request

from syp.models.subrecipe import Subrecipe


def get_paginated_subrecipes(limit=None, items=20):
    """ returns paginated recipes starting with the most recent one"""
    page = request.args.get('page', 1, type=int)
    subrecipes = Subrecipe.query.order_by(Subrecipe.created_at.desc()) \
                          .limit(limit).paginate(page=page, per_page=items)
    return (page, subrecipes)


def get_subrecipe_by_url(subrecipe_url):
    """ Return the subrecipe object with the given url. """
    return Subrecipe.query.filter_by(url=subrecipe_url).first()

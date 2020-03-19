from flask import request

from syp.models import Season, Subrecipe, Unit


def get_paginated_subrecipes(limit=None, items=20):
    """ returns paginated recipes starting with the most recent one"""
    page = request.args.get('page', 1, type=int)
    subrecipes = Subrecipe.query.order_by(Subrecipe.date_created.desc()) \
                          .limit(limit).paginate(page=page, per_page=items)
    return (page, subrecipes)
from urllib.parse import urlparse
from flask import request


def get_url():
    """ Retrieve only the path not the host. """
    parse = urlparse(request.args.get('url'))
    return parse.path
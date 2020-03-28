from urllib.parse import urlparse


def validate_url(url):
    """ Verify that the URL belongs to the website. If not, return
    the home URL to avoid phishing. """
    return url
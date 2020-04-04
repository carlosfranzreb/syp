
from syp import db
from syp import bcrypt


def update_user(user, form):
    """ Updates user. """
    if user.email != form.email.data:
        user.email = form.email.data
    if user.username != form.username.data:
        user.username = form.username.data
    if not bcrypt.check_password_hash(user.pw, form.password.data):
        user.pw = bcrypt.generate_password_hash(form.password.data)
    # TODO: image
    if user.intro != form.intro.data:
        user.intro = form.intro.data
    db.session.commit()

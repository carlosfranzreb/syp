
from syp import db
from syp import bcrypt
from syp.utils import images


def update_user(user, form):
    """ Updates user. """
    if user.email != form.email.data:
        user.email = form.email.data
    if user.username != form.username.data:
        old_username = user.username
        user.username = form.username.data
        if form.image.data:  # new image,  new name
            images.change_image(
                form.image.data, 'users', user.username, old_username
            )
        else:  # same image, new name
            images.change_image(None, 'users', user.username, old_username)
    elif form.image.data:  # new image, same name
        images.change_image(form.image.data, 'users', None, user.username)
    if form.password.data:
        if not bcrypt.check_password_hash(user.pw, form.password.data):
            user.pw = bcrypt.generate_password_hash(form.password.data)
    if user.intro != form.intro.data:
        user.intro = form.intro.data
    db.session.commit()

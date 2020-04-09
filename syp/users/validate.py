from syp.models.user import User


def validate_user(form, user):
    """ Verify that the username and email are unique. """
    errors = list()
    if user.email != form.email.data:
        if User.query.filter_by(email=form.email.data).count() > 0:
            errors.append('Este email pertenece a otra cuenta.')
    if user.username != form.username.data:
        if User.query.filter_by(username=form.username.data).count() > 0:
            errors.append('Ese nombre de usuario ya está ocupado.')
    return errors
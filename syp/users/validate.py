from syp.models.user import User
from syp.models.web import Web


def validate_user(form, user):
    """ Verify that the username and email are unique, and that
    social media websites are used only once. """
    errors = list()
    if user.email != form.email.data:
        if User.query.filter_by(email=form.email.data).count() > 0:
            errors.append('Este email pertenece a otra cuenta.')
    if user.username != form.username.data:
        if User.query.filter_by(username=form.username.data).count() > 0:
            errors.append('Ese nombre de usuario ya está ocupado.')
    used_webs = list()
    for medium in form.media.data:
        if medium['web'] in used_webs:
            web = Web.query.filter_by(id=medium['web']).first()
            errors.append(f'No puedes tener dos cuentas de {web.name}.')
        else:
            used_webs.append(medium['web'])
    return errors

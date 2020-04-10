
from syp import db
from syp import bcrypt
from syp.utils import images
from syp.models.social_media import SocialMedia


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
    update_media(form, user)


def update_media(form, user):
    """ Updates social media. """
    old_media = [w.id_web for w in user.media]
    deleted_media = old_media.copy()
    for subform in form.media:
        id_web = subform.web.data
        if id_web in old_media:  # modify old medium
            deleted_media.remove(id_web)
            medium = user.media[old_media.index(id_web)]
            if medium.username != subform.username.data:
                medium.username = subform.username.data
        else:  # create new medium
            db.session.add(SocialMedia(
                id_user=user.id,
                id_web=subform.web.data,
                username=subform.username.data
            ))
    for medium in deleted_media:  # remove deleted quantities
        db.session.delete(
            SocialMedia.query
            .filter_by(id_user=user.id)
            .filter_by(id_web=medium)
            .first()
        )
    db.session.commit()

from flask import current_app
from flask_mail import Message
from syp import mail
from syp.search.utils import get_default_keywords


def send_veggie_msg(form):
    msg = Message(
        subject=f"Propuesta de {form.name.data}: {form.recipe_name.data}",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[current_app.config["MAIL_USERNAME"]],
        body=form.recipe_info.data
    )
    mail.send(msg)


def get_veggie_keywords():
    veggie_keys = get_default_keywords() + ', convertir receta tradicional en vegana, \
                  versión vegana, versión saludable, convertir a vegana'
    return ' '.join(veggie_keys.split())

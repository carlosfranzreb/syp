from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length


class VeggieForm(FlaskForm):
    name = StringField('Tu nombre',
                       validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    recipe_name = StringField('Nombre de la receta',
                              validators=[DataRequired(),
                                          Length(min=5, max=40)])
    recipe_info = TextAreaField('Dinos todo lo que sepas sobre la receta',
                                validators=[DataRequired(),
                                            Length(min=20, max=1000)])
    privacy = BooleanField('Estoy de acuerdo con la política de privacidad',
                           validators=[DataRequired()])
    recaptcha = RecaptchaField()
    send = SubmitField('Enviar')

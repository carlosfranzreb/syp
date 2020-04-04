""" Forms related to users. """

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, \
    BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileAllowed


class LoginForm(FlaskForm):
    """ Form to login. """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar sesión')


class ProfileForm(FlaskForm):
    """ Form to edit profile data. """
    email = StringField(
        'Email', validators=[DataRequired(), Email()]
    )
    username = StringField(
        'Nombre de usuario', validators=[DataRequired(), Length(max=20)]
    )
    password = PasswordField('Contraseña')
    image = FileField('Foto', validators=[FileAllowed(['jpg', 'png'])])
    intro = TextAreaField('Introducción')
    save = SubmitField('Guardar')

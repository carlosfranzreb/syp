""" Forms related to users. """

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, \
    BooleanField, TextAreaField, SelectField, Form, FieldList, FormField
from wtforms.validators import DataRequired, Email, Length, InputRequired


class LoginForm(FlaskForm):
    """ Form to login. """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar sesión')


class SocialMediaForm(Form):
    """ Used by ProfileForm. """
    web = SelectField('Web', validators=[InputRequired()], coerce=int)
    username = StringField(
        'Nombre de usuario', validators=[DataRequired(), Length(max=100)]
    )


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
    media = FieldList(FormField(SocialMediaForm))
    save = SubmitField('Guardar')


class CookForm(FlaskForm):
    """ Form to search for cooks by username. """
    username = StringField('Nombre', validators=[DataRequired()])
    submit = SubmitField('Buscar')

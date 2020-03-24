from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (
    Form, StringField, SubmitField, IntegerField, SelectField, FieldList,
    FormField, TextAreaField, FloatField
)
from wtforms.validators import DataRequired, InputRequired, Length, Optional
from flask_wtf.file import FileField, FileAllowed


class StepForm(Form):
    step = TextAreaField('Paso:', validators=[DataRequired()])


class IngredientForm(Form):
    ingredient = StringField('Ingrediente:', validators=[DataRequired()])
    amount = FloatField('Cantidad:', validators=[InputRequired()])
    unit = SelectField('Unidad:', validators=[InputRequired()], coerce=int)
    # Why InputRequired: https://github.com/wtforms/wtforms/issues/255


class RecipeForm(FlaskForm):
    name = StringField(
        'Nombre de la receta.',
        validators=[DataRequired(), Length(max=100)]
    )
    image = FileField('Foto del plato.', validators=[FileAllowed(['jpg', 'png'])])
    time_prep = IntegerField('Tiempo de preparación.', validators=[DataRequired()])
    time_cook = IntegerField('Tiempo de cocción.', validators=[DataRequired()])
    season = SelectField('Temporada.', coerce=int)
    state = SelectField('Estado:', coerce=int)
    intro = TextAreaField(
        'Un par de frases para promocionar la receta.',
        validators=[DataRequired(), Length(min=80, max=180)]
    )
    text = TextAreaField(
        'Explicación detallada de la receta.',
        validators=[DataRequired(), Length(min=600, max=1400)]
    )
    steps = FieldList(FormField(StepForm), min_entries=1)
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)
    health = TextAreaField(
        'Descripción de los nutrientes de la receta.',
        validators=[DataRequired(), Length(min=300, max=600)]
    )
    link_video = StringField('Link del vídeo de YouTube.')
    save = SubmitField('Guardar')


class NewRecipeForm(FlaskForm):
    """ Same form but without data requirements, 
    so recipes can be stored unfinished. """
    name = StringField(
        'Nombre de la receta.',
        validators=[DataRequired(), Length(max=100)]
    )
    image = FileField(
        'Foto del plato.',
        validators=[FileAllowed(['jpg', 'png'])]
    )
    time_prep = IntegerField('Tiempo de preparación.', validators=[Optional()])
    time_cook = IntegerField('Tiempo de cocción.', validators=[Optional()])
    season = SelectField('Temporada.', coerce=int)
    state = SelectField('Estado:', coerce=int)
    intro = TextAreaField(
        'Un par de frases para promocionar la receta.',
        validators=[Length(max=180)]
    )
    text = TextAreaField(
        'Explicación detallada de la receta.',
        validators=[Length(max=1400)]
    )
    steps = FieldList(FormField(StepForm))
    ingredients = FieldList(FormField(IngredientForm))
    health = TextAreaField(
        'Descripción de los nutrientes de la receta.',
        validators=[Length(max=600)]
    )
    link_video = StringField(
        'Link del vídeo de YouTube.',
        validators=[Length(max=1400)]
    )
    save = SubmitField('Guardar')

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

from syp.seasons.utils import get_current_season


class SeasonForm(FlaskForm):
    seasons = [(1, 'Invierno'), (2, 'Primavera'), (3, 'Verano'), (4, 'Otoño')]
    season = SelectField('Escoge una temporada', choices=seasons,
                         default=get_current_season())
    submit = SubmitField('Buscar')

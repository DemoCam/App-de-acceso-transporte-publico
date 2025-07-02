from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class ImportForm(FlaskForm):
    """Formulario para importar datos desde archivos"""
    tipo_datos = SelectField('Tipo de Datos', validators=[DataRequired()],
                          choices=[
                              ('paradas', 'Paradas'),
                              ('rutas', 'Rutas'),
                              ('rutas_paradas', 'Asociaciones Ruta-Parada')
                          ])
    archivo = FileField('Archivo JSON', validators=[
        FileRequired(),
        FileAllowed(['json'], 'Solo se permiten archivos JSON')
    ])
    vista_previa = BooleanField('Vista previa (sin guardar)', default=True)
    submit = SubmitField('Importar')

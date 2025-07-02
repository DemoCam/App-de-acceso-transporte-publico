from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from app.models.usuario import Role

class UsuarioForm(FlaskForm):
    """Formulario para la gestión de usuarios por parte del administrador"""
    username = StringField('Nombre de Usuario', validators=[
        DataRequired(),
        Length(min=3, max=64)
    ])
    email = StringField('Correo Electrónico', validators=[
        DataRequired(),
        Email(),
        Length(max=120)
    ])
    nombre = StringField('Nombre', validators=[
        Optional(),
        Length(max=64)
    ])
    apellido = StringField('Apellido', validators=[
        Optional(),
        Length(max=64)
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(),
        Length(min=8)
    ])
    password2 = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(),
        EqualTo('password', message='Las contraseñas deben coincidir')
    ])
    # Usamos 'role' en el formulario pero lo asignamos a 'rol' en el controlador
    role = SelectField('Rol', choices=[
        (Role.ADMIN, 'Administrador'),  # 'admin'
        (Role.USER, 'Usuario'),         # 'user'
        (Role.GUEST, 'Invitado')        # 'guest'
    ])
    is_active = BooleanField('Usuario Activo', default=True)
    submit = SubmitField('Guardar')

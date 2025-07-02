from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app.models.usuario import Usuario

class LoginForm(FlaskForm):
    """Formulario de inicio de sesión"""
    username = StringField('Nombre de usuario', validators=[DataRequired()], 
                          render_kw={"aria-label": "Nombre de usuario", "placeholder": "Nombre de usuario", 
                                    "autocomplete": "username"})
    password = PasswordField('Contraseña', validators=[DataRequired()], 
                           render_kw={"aria-label": "Contraseña", "placeholder": "Contraseña", 
                                     "autocomplete": "current-password"})
    remember_me = BooleanField('Recordarme', 
                              render_kw={"aria-label": "Recordar sesión"})
    submit = SubmitField('Iniciar Sesión', 
                        render_kw={"aria-label": "Botón de inicio de sesión"})

class RegisterForm(FlaskForm):
    """Formulario de registro de usuarios"""
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=3, max=64)], 
                          render_kw={"aria-label": "Nombre de usuario", "placeholder": "Nombre de usuario", 
                                    "autocomplete": "username"})
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()], 
                       render_kw={"aria-label": "Correo electrónico", "placeholder": "correo@ejemplo.com", 
                                 "autocomplete": "email"})
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=64)], 
                        render_kw={"aria-label": "Nombre", "placeholder": "Nombre", 
                                  "autocomplete": "given-name"})
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=64)], 
                          render_kw={"aria-label": "Apellido", "placeholder": "Apellido", 
                                    "autocomplete": "family-name"})
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8)], 
                           render_kw={"aria-label": "Contraseña", "placeholder": "Mínimo 8 caracteres", 
                                     "autocomplete": "new-password"})
    password2 = PasswordField('Repita la contraseña', validators=[DataRequired(), EqualTo('password')], 
                             render_kw={"aria-label": "Repita la contraseña", "placeholder": "Repita la contraseña", 
                                       "autocomplete": "new-password"})
    submit = SubmitField('Registrarse', 
                        render_kw={"aria-label": "Botón de registro"})
    
    def validate_username(self, username):
        """Valida que el nombre de usuario no esté ya en uso"""
        user = Usuario.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Este nombre de usuario ya está en uso. Por favor use otro.')
    
    def validate_email(self, email):
        """Valida que el correo electrónico no esté ya en uso"""
        user = Usuario.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Este correo electrónico ya está registrado. Por favor use otro.')

class ChangePasswordForm(FlaskForm):
    """Formulario para cambiar contraseña"""
    old_password = PasswordField('Contraseña actual', validators=[DataRequired()], 
                                render_kw={"aria-label": "Contraseña actual", 
                                          "autocomplete": "current-password"})
    password = PasswordField('Nueva contraseña', validators=[DataRequired(), Length(min=8)], 
                           render_kw={"aria-label": "Nueva contraseña", 
                                     "autocomplete": "new-password"})
    password2 = PasswordField('Repita la nueva contraseña', 
                             validators=[DataRequired(), EqualTo('password')], 
                             render_kw={"aria-label": "Repita la nueva contraseña", 
                                       "autocomplete": "new-password"})
    submit = SubmitField('Cambiar contraseña', 
                        render_kw={"aria-label": "Botón para cambiar contraseña"})

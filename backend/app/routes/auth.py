from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.usuario import Usuario
from app.forms.auth import LoginForm, RegisterForm, ChangePasswordForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    # Si el usuario ya está autenticado, redirigir a la página principal
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Buscar usuario por nombre de usuario
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        
        # Verificación detallada para depuración
        if usuario is None:
            print(f"Usuario no encontrado: {form.username.data}")
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Imprimir información del usuario para depurar
        print(f"Intento de login para: {usuario.username}, Rol: {usuario.rol}, Activo: {usuario.activo}")
        
        # Verificar que la contraseña es correcta
        if not usuario.check_password(form.password.data):
            print(f"Contraseña incorrecta para: {usuario.username}")
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Verificar que el usuario está activo
        if not usuario.activo:
            print(f"Usuario inactivo: {usuario.username}")
            flash('Esta cuenta ha sido desactivada. Contacta al administrador.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Iniciar sesión
        login_user(usuario, remember=form.remember_me.data)
        
        # Actualizar la fecha de último acceso
        usuario.fecha_ultimo_acceso = db.func.now()
        db.session.commit()
        
        # Redirigir a la página solicitada antes de login o a la página principal
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
            
        flash(f'Bienvenido, {usuario.nombre}!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html', form=form, title='Iniciar Sesión')

@auth.route('/logout')
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro de usuarios"""
    # Si el usuario ya está autenticado, redirigir a la página principal
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        usuario = Usuario(
            username=form.username.data,
            email=form.email.data,
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            activo=True
        )
        usuario.set_password(form.password.data)
        
        try:
            db.session.add(usuario)
            db.session.commit()
            flash('¡Te has registrado correctamente! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar el usuario: {str(e)}', 'danger')
    
    return render_template('auth/register.html', form=form, title='Registro')

@auth.route('/perfil')
@login_required
def perfil():
    """Página de perfil del usuario"""
    return render_template('auth/perfil.html', usuario=current_user, title='Mi Perfil')

@auth.route('/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """Cambiar contraseña del usuario"""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        # Verificar la contraseña actual
        if not current_user.check_password(form.old_password.data):
            flash('La contraseña actual no es correcta.', 'danger')
            return redirect(url_for('auth.cambiar_password'))
        
        # Actualizar contraseña
        current_user.set_password(form.password.data)
        db.session.commit()
        flash('Tu contraseña ha sido actualizada.', 'success')
        return redirect(url_for('auth.perfil'))
    
    return render_template('auth/cambiar_password.html', form=form, title='Cambiar Contraseña')

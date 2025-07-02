from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.transporte import Ruta, Parada, RutaParada
from app.models.usuario import Usuario, Role
from app.forms.transporte import RutaForm, ParadaForm, RutaParadaForm
from app.forms.usuario import UsuarioForm
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from functools import wraps
from werkzeug.security import generate_password_hash

# Definir el blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(func):
    """Decorador para verificar que el usuario es admin"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != Role.ADMIN:
            flash('No tienes permisos de administrador para acceder a esta página.', 'danger')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return decorated_view

@admin.route('/')
@login_required
@admin_required
def index():
    """Página principal del panel de administración"""
    # Contar elementos para el dashboard
    rutas_count = Ruta.query.count()
    paradas_count = Parada.query.count()
    asociaciones_count = RutaParada.query.count()
    usuarios_count = Usuario.query.count()
    
    # Obtener las últimas 5 rutas y paradas
    ultimas_rutas = Ruta.query.order_by(Ruta.id.desc()).limit(5).all()
    ultimas_paradas = Parada.query.order_by(Parada.id.desc()).limit(5).all()
    
    # Crear diccionario de estadísticas para la plantilla
    stats = {
        'total_rutas': rutas_count,
        'total_paradas': paradas_count,
        'total_asociaciones': asociaciones_count,
        'total_usuarios': usuarios_count
    }
    
    return render_template('admin/index.html', 
                          stats=stats, 
                          ultimas_rutas=ultimas_rutas, 
                          ultimas_paradas=ultimas_paradas)

# GESTIÓN DE RUTAS
@admin.route('/rutas/')
@login_required
@admin_required
def gestionar_rutas():
    """Listar todas las rutas"""
    page = request.args.get('page', 1, type=int)
    rutas = Ruta.query.order_by(Ruta.numero).paginate(page=page, per_page=10)
    return render_template('admin/rutas/index.html', rutas=rutas)

@admin.route('/rutas/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_ruta():
    """Crear una nueva ruta"""
    form = RutaForm()
    if form.validate_on_submit():
        ruta = Ruta(
            numero=form.numero.data,
            nombre=form.nombre.data,
            origen=form.origen.data,
            destino=form.destino.data,
            hora_inicio=form.hora_inicio.data,
            hora_fin=form.hora_fin.data,
            frecuencia_minutos=form.frecuencia_minutos.data,
            descripcion=form.descripcion.data,
            activa=form.activa.data,
            tiene_rampa=form.tiene_rampa.data,
            tiene_audio=form.tiene_audio.data,
            tiene_espacio_silla=form.tiene_espacio_silla.data,
            tiene_indicador_visual=form.tiene_indicador_visual.data
        )
        try:
            db.session.add(ruta)
            db.session.commit()
            flash('Ruta creada exitosamente.', 'success')
            return redirect(url_for('admin.gestionar_rutas'))
        except IntegrityError:
            db.session.rollback()
            flash('Error: El número de ruta ya existe.', 'danger')
    return render_template('admin/rutas/form.html', form=form, submit_text='Crear Ruta', legend='Crear Nueva Ruta')

@admin.route('/rutas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_ruta(id):
    """Editar una ruta existente"""
    ruta = Ruta.query.get_or_404(id)
    form = RutaForm(obj=ruta)
    
    if form.validate_on_submit():
        form.populate_obj(ruta)
        try:
            db.session.commit()
            flash('Ruta actualizada exitosamente.', 'success')
            return redirect(url_for('admin.gestionar_rutas'))
        except IntegrityError:
            db.session.rollback()
            flash('Error: El número de ruta ya existe.', 'danger')
    
    return render_template('admin/rutas/form.html', 
                          form=form, 
                          ruta=ruta, 
                          submit_text='Actualizar Ruta', 
                          legend=f'Editar Ruta: {ruta.numero} - {ruta.nombre}')

@admin.route('/rutas/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_ruta(id):
    """Eliminar una ruta"""
    ruta = Ruta.query.get_or_404(id)
    try:
        db.session.delete(ruta)
        db.session.commit()
        flash('Ruta eliminada exitosamente.', 'success')
    except:
        db.session.rollback()
        flash('Error al eliminar la ruta.', 'danger')
    
    return redirect(url_for('admin.gestionar_rutas'))

@admin.route('/rutas/<int:ruta_id>/paradas')
@login_required
@admin_required
def paradas_de_ruta(ruta_id):
    """Ver todas las paradas de una ruta específica"""
    ruta = Ruta.query.get_or_404(ruta_id)
    
    # Obtener paradas de la ruta ordenadas por su posición
    paradas = Parada.query.join(Parada.ruta_paradas).filter(
        RutaParada.ruta_id == ruta_id
    ).order_by(RutaParada.orden).all()
    
    return render_template('admin/rutas/paradas.html', 
                          ruta=ruta, 
                          paradas=paradas)

# GESTIÓN DE PARADAS
@admin.route('/paradas/')
@login_required
@admin_required
def gestionar_paradas():
    """Listar todas las paradas"""
    page = request.args.get('page', 1, type=int)
    paradas = Parada.query.order_by(Parada.nombre).paginate(page=page, per_page=10)
    return render_template('admin/paradas/index.html', paradas=paradas)

@admin.route('/paradas/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_parada():
    """Crear una nueva parada"""
    form = ParadaForm()
    if form.validate_on_submit():
        parada = Parada(
            nombre=form.nombre.data,
            direccion=form.direccion.data,
            latitud=form.latitud.data,
            longitud=form.longitud.data,
            tipo=form.tipo.data,
            tiene_rampa=form.tiene_rampa.data,
            tiene_semaforo_sonoro=form.tiene_semaforo_sonoro.data,
            descripcion=form.descripcion.data
        )
        try:
            db.session.add(parada)
            db.session.commit()
            flash('Parada creada exitosamente.', 'success')
            return redirect(url_for('admin.gestionar_paradas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la parada: {str(e)}', 'danger')
    
    return render_template('admin/paradas/form.html', 
                          form=form, 
                          legend="Crear Nueva Parada", 
                          submit_text="Guardar")

@admin.route('/paradas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_parada(id):
    """Editar una parada existente"""
    parada = Parada.query.get_or_404(id)
    form = ParadaForm(obj=parada)
    
    if form.validate_on_submit():
        form.populate_obj(parada)
        try:
            db.session.commit()
            flash('Parada actualizada exitosamente.', 'success')
            return redirect(url_for('admin.gestionar_paradas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la parada: {str(e)}', 'danger')
    
    return render_template('admin/paradas/form.html', 
                          form=form, 
                          parada=parada,
                          legend=f"Editar Parada: {parada.nombre}", 
                          submit_text="Actualizar")

@admin.route('/paradas/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_parada(id):
    """Eliminar una parada"""
    parada = Parada.query.get_or_404(id)
    try:
        db.session.delete(parada)
        db.session.commit()
        flash('Parada eliminada exitosamente.', 'success')
    except:
        db.session.rollback()
        flash('Error al eliminar la parada. Asegúrate de que no esté asociada a ninguna ruta.', 'danger')
    
    return redirect(url_for('admin.gestionar_paradas'))

# GESTIÓN DE ASOCIACIONES RUTA-PARADA
@admin.route('/rutas-paradas/')
@login_required
@admin_required
def gestionar_rutas_paradas():
    """Listar todas las asociaciones entre rutas y paradas"""
    page = request.args.get('page', 1, type=int)
    ruta_id = request.args.get('ruta_id', None, type=int)
    
    # Consulta base
    query = RutaParada.query.join(Ruta).join(Parada)
    
    # Aplicar filtro si se especificó una ruta
    if ruta_id:
        query = query.filter(RutaParada.ruta_id == ruta_id)
    
    # Ordenar por ruta y luego por orden dentro de la ruta
    rutas_paradas = query.order_by(Ruta.numero, RutaParada.orden).paginate(page=page, per_page=15)
    
    # Obtener todas las rutas para el filtro
    rutas = Ruta.query.order_by(Ruta.numero).all()
    
    return render_template('admin/rutas_paradas/index.html', 
                           rutas_paradas=rutas_paradas,
                           rutas=rutas)

@admin.route('/rutas-paradas/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_ruta_parada():
    """Crear una nueva asociación entre ruta y parada"""
    form = RutaParadaForm()
    
    # Poblar las opciones para los select
    form.ruta_id.choices = [(ruta.id, f"{ruta.numero} - {ruta.nombre}") 
                            for ruta in Ruta.query.order_by(Ruta.numero).all()]
    form.parada_id.choices = [(parada.id, f"{parada.nombre} ({parada.direccion})")
                             for parada in Parada.query.order_by(Parada.nombre).all()]
    
    if form.validate_on_submit():
        # Verificar si ya existe esta asociación
        existe = RutaParada.query.filter_by(
            ruta_id=form.ruta_id.data,
            parada_id=form.parada_id.data
        ).first()
        
        if existe:
            flash('Esta parada ya está asociada a la ruta seleccionada.', 'danger')
            return render_template('admin/rutas_paradas/form.html', form=form)
        
        # Crear la asociación
        ruta_parada = RutaParada(
            ruta_id=form.ruta_id.data,
            parada_id=form.parada_id.data,
            orden=form.orden.data,
            tiempo_estimado=form.tiempo_estimado.data
        )
        
        db.session.add(ruta_parada)
        db.session.commit()
        flash('Asociación creada exitosamente.', 'success')
        return redirect(url_for('admin.gestionar_rutas_paradas'))
    
    return render_template('admin/rutas_paradas/form.html', form=form)

@admin.route('/rutas-paradas/editar/<int:ruta_id>/<int:parada_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_ruta_parada(ruta_id, parada_id):
    """Editar una asociación existente entre ruta y parada"""
    ruta_parada = RutaParada.query.filter_by(ruta_id=ruta_id, parada_id=parada_id).first_or_404()
    
    form = RutaParadaForm(obj=ruta_parada)
    form.ruta_id.choices = [(ruta.id, f"{ruta.numero} - {ruta.nombre}") 
                           for ruta in Ruta.query.order_by(Ruta.numero).all()]
    form.parada_id.choices = [(parada.id, f"{parada.nombre} ({parada.direccion})")
                             for parada in Parada.query.order_by(Parada.nombre).all()]
    
    # Deshabilitar cambios en las llaves primarias
    form.ruta_id.render_kw = {'disabled': 'disabled'}
    form.parada_id.render_kw = {'disabled': 'disabled'}
    
    if form.validate_on_submit():
        # Solo actualizar los campos que no son parte de la clave primaria
        ruta_parada.orden = form.orden.data
        ruta_parada.tiempo_estimado = form.tiempo_estimado.data
        
        db.session.commit()
        flash('Asociación actualizada exitosamente.', 'success')
        return redirect(url_for('admin.gestionar_rutas_paradas'))
    
    return render_template('admin/rutas_paradas/form.html', form=form, ruta_parada=ruta_parada)

@admin.route('/rutas-paradas/eliminar/<int:ruta_id>/<int:parada_id>', methods=['POST'])
@login_required
@admin_required
def eliminar_ruta_parada(ruta_id, parada_id):
    """Eliminar una asociación entre ruta y parada"""
    ruta_parada = RutaParada.query.filter_by(ruta_id=ruta_id, parada_id=parada_id).first_or_404()
    
    db.session.delete(ruta_parada)
    db.session.commit()
    flash('Asociación eliminada exitosamente.', 'success')
    return redirect(url_for('admin.gestionar_rutas_paradas'))

# GESTIÓN DE USUARIOS
@admin.route('/usuarios/')
@login_required
@admin_required
def gestionar_usuarios():
    """Listar todos los usuarios con filtros y búsqueda"""
    page = request.args.get('page', 1, type=int)
    
    # Obtener parámetros de búsqueda y filtro
    busqueda = request.args.get('q', '')
    rol_filtro = request.args.get('rol', '')
    
    # Consulta base
    query = Usuario.query
    
    # Aplicar filtros si existen
    if busqueda:
        # Búsqueda por nombre de usuario o email
        query = query.filter(
            db.or_(
                Usuario.username.ilike(f'%{busqueda}%'),
                Usuario.email.ilike(f'%{busqueda}%'),
                Usuario.nombre.ilike(f'%{busqueda}%'),
                Usuario.apellido.ilike(f'%{busqueda}%')
            )
        )
    
    if rol_filtro:
        # Filtrar por rol (admin o usuario)
        query = query.filter(Usuario.rol == rol_filtro)
    
    # Ordenar y paginar resultados
    usuarios = query.order_by(Usuario.username).paginate(page=page, per_page=10)
    
    return render_template('admin/usuarios/index.html', usuarios=usuarios)

@admin.route('/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_usuario():
    """Crear un nuevo usuario"""
    form = UsuarioForm()
    if form.validate_on_submit():
        # Creamos el usuario con los datos del formulario
        usuario = Usuario(
            username=form.username.data,
            email=form.email.data,
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            rol=form.role.data,  # Esto asigna el valor del enum (admin, user, guest)
            activo=form.is_active.data
        )
        # Establecemos la contraseña
        usuario.set_password(form.password.data)
        
        # Verificación para depurar
        print(f"Creando usuario: {usuario.username}, Rol: {usuario.rol}, Activo: {usuario.activo}")
        
        try:
            db.session.add(usuario)
            db.session.commit()
            flash('Usuario creado exitosamente.', 'success')
            return redirect(url_for('admin.gestionar_usuarios'))
        except IntegrityError as e:
            db.session.rollback()
            print(f"Error al crear usuario: {str(e)}")
            flash('Error: El nombre de usuario o email ya existe.', 'danger')
    
    return render_template('admin/usuarios/form.html', 
                          form=form, 
                          legend="Crear Nuevo Usuario", 
                          submit_text="Crear Usuario")

@admin.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_usuario(id):
    """Editar un usuario existente"""
    # No permitir editar al superadmin
    if id == 1:
        flash('No se puede modificar al superadministrador.', 'danger')
        return redirect(url_for('admin.gestionar_usuarios'))
    
    usuario = Usuario.query.get_or_404(id)
    form = UsuarioForm(obj=usuario)
    
    # No requerir contraseña al editar
    form.password.validators = []
    form.password2.validators = []
    form.password.render_kw = {'placeholder': 'Dejar vacío para mantener la contraseña actual'}
    form.password2.render_kw = {'placeholder': 'Dejar vacío para mantener la contraseña actual'}
    
    if form.validate_on_submit():
        usuario.username = form.username.data
        usuario.email = form.email.data
        usuario.nombre = form.nombre.data
        usuario.apellido = form.apellido.data
        usuario.rol = form.role.data
        usuario.activo = form.is_active.data
        
        # Verificación para depurar
        print(f"Actualizando usuario: {usuario.username}, Rol: {usuario.rol}, Activo: {usuario.activo}")
        
        # Actualizar contraseña solo si se proporcionó una nueva
        if form.password.data:
            usuario.set_password(form.password.data)
            print(f"Contraseña actualizada para: {usuario.username}")
        
        try:
            db.session.commit()
            flash('Usuario actualizado exitosamente.', 'success')
            return redirect(url_for('admin.gestionar_usuarios'))
        except IntegrityError as e:
            db.session.rollback()
            print(f"Error al actualizar usuario: {str(e)}")
            flash('Error: El nombre de usuario o email ya existe.', 'danger')
    
    return render_template('admin/usuarios/form.html', 
                          form=form, 
                          usuario=usuario,
                          legend=f"Editar Usuario: {usuario.username}",
                          submit_text="Actualizar Usuario")

@admin.route('/usuarios/eliminar/<int:id>', methods=['POST'])
@login_required
@admin_required
def eliminar_usuario(id):
    """Eliminar un usuario"""
    # No permitir eliminar al superadmin
    if id == 1:
        flash('No se puede eliminar al superadministrador.', 'danger')
        return redirect(url_for('admin.gestionar_usuarios'))
    
    # No permitir que un admin se elimine a sí mismo
    if id == current_user.id:
        flash('No puedes eliminarte a ti mismo.', 'danger')
        return redirect(url_for('admin.gestionar_usuarios'))
    
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado exitosamente.', 'success')
    return redirect(url_for('admin.gestionar_usuarios'))

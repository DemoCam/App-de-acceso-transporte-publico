"""
Script para administrar tareas administrativas de la aplicación
"""
import os
import sys
import click
from app import create_app, db
from app.models.usuario import Usuario
from app.models.transporte import Ruta, Parada
import json
from datetime import datetime

app = create_app()

@click.group()
def cli():
    """Herramientas de administración para la App de Transporte Accesible Cali."""
    pass

@cli.command()
def reset_admin_password():
    """Reinicia la contraseña del usuario administrador."""
    with app.app_context():
        admin = Usuario.query.filter_by(username='admin').first()
        if admin:
            password = 'admin123'
            admin.set_password(password)
            db.session.commit()
            
            # Verificar que la contraseña se estableció correctamente
            if admin.check_password(password):
                click.echo(f'La contraseña del administrador ha sido reiniciada a: {password}')
                click.echo('✅ Verificación de contraseña exitosa')
            else:
                click.echo('❌ ERROR: La contraseña no se estableció correctamente')
        else:
            click.echo('No se encontró el usuario administrador.')

@cli.command()
@click.option('--username', '-u', required=True, help='Nombre de usuario')
@click.option('--password', '-p', required=True, help='Contraseña')
@click.option('--email', '-e', required=True, help='Correo electrónico')
@click.option('--nombre', '-n', required=True, help='Nombre del usuario')
@click.option('--apellido', '-a', required=True, help='Apellido del usuario')
@click.option('--admin/--no-admin', default=False, help='Establecer como administrador')
def crear_usuario(username, password, email, nombre, apellido, admin):
    """Crea un nuevo usuario."""
    with app.app_context():
        if Usuario.query.filter_by(username=username).first():
            click.echo(f'Error: El usuario {username} ya existe.')
            return
        
        if Usuario.query.filter_by(email=email).first():
            click.echo(f'Error: El email {email} ya está registrado.')
            return
        
        rol = 'admin' if admin else 'usuario'
        usuario = Usuario(
            username=username,
            email=email,
            nombre=nombre,
            apellido=apellido,
            rol=rol,
            activo=True
        )
        usuario.set_password(password)
        
        db.session.add(usuario)
        db.session.commit()
        
        click.echo(f'Usuario {username} creado correctamente como {rol}.')

@cli.command()
def crear_nuevo_admin():
    """Crea un nuevo usuario administrador."""
    with app.app_context():
        # Generar un nombre de usuario único
        base_username = "admin_nuevo"
        username = base_username
        contador = 1
        while Usuario.query.filter_by(username=username).first():
            username = f"{base_username}{contador}"
            contador += 1
        
        # Datos del nuevo administrador
        password = "admin456"
        email = f"{username}@transporte-cali.com"
        nombre = "Nuevo"
        apellido = "Administrador"
        
        # Crear el usuario
        usuario = Usuario(
            username=username,
            email=email,
            nombre=nombre,
            apellido=apellido,
            rol='admin',
            activo=True
        )
        usuario.set_password(password)
        
        db.session.add(usuario)
        db.session.commit()
        
        # Verificar que se creó correctamente
        if usuario.id and usuario.check_password(password):
            click.echo(f'✅ Nuevo administrador creado:')
            click.echo(f'Usuario: {username}')
            click.echo(f'Contraseña: {password}')
            click.echo(f'Email: {email}')
        else:
            click.echo('❌ Error al crear el nuevo administrador')

@cli.command()
@click.option('--output', '-o', default='backup.json', help='Archivo de salida')
def exportar_datos(output):
    """Exporta todos los datos de la aplicación a un archivo JSON."""
    with app.app_context():
        data = {
            'rutas': [],
            'paradas': []
        }
        
        # Exportar rutas
        rutas = Ruta.query.all()
        for ruta in rutas:
            ruta_data = ruta.to_dict(include_paradas=True)
            # Convertir objetos datetime a cadenas
            if 'hora_inicio' in ruta_data:
                ruta_data['hora_inicio'] = ruta_data['hora_inicio']
            if 'hora_fin' in ruta_data:
                ruta_data['hora_fin'] = ruta_data['hora_fin']
            data['rutas'].append(ruta_data)
        
        # Exportar paradas
        paradas = Parada.query.all()
        for parada in paradas:
            data['paradas'].append(parada.to_dict())
        
        # Guardar en archivo
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        click.echo(f'Datos exportados a {output}')
        click.echo(f'Rutas: {len(data["rutas"])}, Paradas: {len(data["paradas"])}')

@cli.command()
@click.option('--input', '-i', required=True, help='Archivo de entrada JSON')
@click.option('--clear/--no-clear', default=False, help='Borrar datos existentes antes de importar')
def importar_datos(input, clear):
    """Importa datos desde un archivo JSON."""
    if not os.path.exists(input):
        click.echo(f'Error: El archivo {input} no existe.')
        return
    
    with open(input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with app.app_context():
        if clear:
            if click.confirm('¿Está seguro de que desea borrar TODOS los datos existentes?'):
                db.session.query(Ruta).delete()
                db.session.query(Parada).delete()
                db.session.commit()
                click.echo('Datos existentes borrados.')
            else:
                click.echo('Operación cancelada.')
                return
        
        # Importar paradas
        paradas_importadas = 0
        for parada_data in data.get('paradas', []):
            try:
                parada = Parada.query.filter_by(nombre=parada_data['nombre']).first()
                if not parada:
                    parada = Parada(
                        nombre=parada_data['nombre'],
                        direccion=parada_data['direccion'],
                        latitud=parada_data['latitud'],
                        longitud=parada_data['longitud'],
                        tipo=parada_data.get('tipo', 'regular'),
                        tiene_rampa=parada_data.get('accesibilidad', {}).get('rampa', False),
                        tiene_semaforo_sonoro=parada_data.get('accesibilidad', {}).get('semaforo_sonoro', False),
                        descripcion=parada_data.get('descripcion', '')
                    )
                    db.session.add(parada)
                    paradas_importadas += 1
            except Exception as e:
                click.echo(f'Error al importar parada {parada_data.get("nombre", "desconocida")}: {str(e)}')
        
        db.session.commit()
        click.echo(f'Paradas importadas: {paradas_importadas}')
        
        # Importar rutas
        rutas_importadas = 0
        for ruta_data in data.get('rutas', []):
            try:
                ruta = Ruta.query.filter_by(numero=ruta_data['numero']).first()
                if not ruta:
                    ruta = Ruta(
                        numero=ruta_data['numero'],
                        nombre=ruta_data['nombre'],
                        origen=ruta_data['origen'],
                        destino=ruta_data['destino'],
                        hora_inicio=datetime.strptime(ruta_data['hora_inicio'], '%H:%M').time(),
                        hora_fin=datetime.strptime(ruta_data['hora_fin'], '%H:%M').time(),
                        frecuencia_minutos=ruta_data['frecuencia_minutos'],
                        descripcion=ruta_data.get('descripcion', '')
                    )
                    db.session.add(ruta)
                    rutas_importadas += 1
            except Exception as e:
                click.echo(f'Error al importar ruta {ruta_data.get("numero", "desconocida")}: {str(e)}')
        
        db.session.commit()
        click.echo(f'Rutas importadas: {rutas_importadas}')

if __name__ == '__main__':
    cli()

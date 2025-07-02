"""
Script para inicializar la base de datos con tablas y un usuario administrador
"""

from app import create_app, db
from app.models.usuario import Usuario
import click

@click.command('init-db')
@click.option('--with-test-data/--no-test-data', default=False, help='Initialize with test data')
def init_db(with_test_data):
    """Inicializa la base de datos con las tablas necesarias y un usuario admin."""
    app = create_app()
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        click.echo('Tablas creadas correctamente.')
        
        # Crear usuario administrador si no existe
        if Usuario.query.filter_by(username='admin').first() is None:
            admin = Usuario(
                username='admin',
                email='admin@transporte-cali.com',
                nombre='Administrador',
                apellido='Sistema',
                rol='admin',
                activo=True
            )
            admin.set_password('admin123')  # ¡Cambiar después de la primera instalación!
            db.session.add(admin)
            db.session.commit()
            click.echo('Usuario administrador creado: admin / admin123')
        else:
            click.echo('El usuario administrador ya existe.')
        
        if with_test_data:
            # Aquí se añadiría código para cargar datos de prueba
            click.echo('No hay datos de prueba para cargar en esta versión.')
        
        click.echo('Inicialización completa.')

if __name__ == '__main__':
    init_db()

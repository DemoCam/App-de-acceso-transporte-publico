"""
Script para verificar el usuario administrador en la base de datos
"""
from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():
    admin = Usuario.query.filter_by(username='admin').first()
    if admin:
        print(f"Usuario administrador encontrado:")
        print(f"ID: {admin.id}")
        print(f"Username: {admin.username}")
        print(f"Email: {admin.email}")
        print(f"Rol: {admin.rol}")
        print(f"Activo: {admin.activo}")
    else:
        print("No se encontró ningún usuario administrador.")

    # Verificar si existe algún usuario con rol de administrador
    admins = Usuario.query.filter_by(rol='admin').all()
    if admins:
        print(f"\nTotal usuarios administradores: {len(admins)}")
        for admin in admins:
            print(f"- {admin.username} ({admin.email})")
    else:
        print("\nNo hay usuarios con rol de administrador.")

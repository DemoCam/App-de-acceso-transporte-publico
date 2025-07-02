"""
Script para verificar la contraseña del usuario administrador
"""
import sys
from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

# Verificar si se proporcionó una contraseña como argumento
if len(sys.argv) < 2:
    print("Uso: python check_password.py <contraseña>")
    sys.exit(1)

password = sys.argv[1]

with app.app_context():
    admin = Usuario.query.filter_by(username='admin').first()
    if admin:
        if admin.check_password(password):
            print(f"✅ La contraseña '{password}' es CORRECTA para el usuario 'admin'")
        else:
            print(f"❌ La contraseña '{password}' es INCORRECTA para el usuario 'admin'")
    else:
        print("No se encontró ningún usuario administrador.")

"""
Script para restablecer las contraseñas de todos los usuarios
"""
from app import create_app, db
from app.models.usuario import Usuario
import sys

app = create_app()

def restablecer_contrasenas():
    """Restablece las contraseñas de todos los usuarios a una contraseña predeterminada"""
    with app.app_context():
        usuarios = Usuario.query.all()
        
        for usuario in usuarios:
            # Contraseña personalizada para cada usuario
            nueva_contrasena = f"Reset2025!"
            
            # Guardar la contraseña anterior para comparación
            hash_anterior = usuario.password_hash
            
            # Establecer nueva contraseña
            usuario.set_password(nueva_contrasena)
            
            # Verificar que la contraseña se actualizó correctamente
            if usuario.check_password(nueva_contrasena):
                print(f"✅ Usuario: {usuario.username}")
                print(f"   Contraseña restablecida a: {nueva_contrasena}")
                print(f"   Hash anterior: {hash_anterior[:30]}...")
                print(f"   Nuevo hash: {usuario.password_hash[:30]}...")
            else:
                print(f"❌ Error al restablecer contraseña para {usuario.username}")
        
        # Confirmar cambios
        db.session.commit()
        print("\n✅ Todas las contraseñas han sido restablecidas.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--confirmar":
        restablecer_contrasenas()
    else:
        print("ADVERTENCIA: Este script restablecerá las contraseñas de TODOS los usuarios.")
        print("Para ejecutarlo, use el parámetro --confirmar")
        print("python reset_all_passwords.py --confirmar")

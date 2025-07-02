"""
Script para listar todos los usuarios y su estado de autenticación
"""
from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

def listar_usuarios():
    """Lista todos los usuarios con información relevante"""
    with app.app_context():
        usuarios = Usuario.query.all()
        
        print(f"\nTotal de usuarios: {len(usuarios)}")
        print("\n{:<5} {:<15} {:<25} {:<15} {:<10}".format(
            "ID", "Usuario", "Email", "Rol", "Activo"))
        print("-" * 70)
        
        for usuario in usuarios:
            print("{:<5} {:<15} {:<25} {:<15} {:<10}".format(
                usuario.id,
                usuario.username,
                usuario.email,
                usuario.rol,
                "Sí" if usuario.activo else "No"
            ))
        
        print("\nDetalles de hash de contraseñas:")
        for usuario in usuarios:
            print(f"\nID {usuario.id}: {usuario.username}")
            if usuario.password_hash:
                hash_type = "Desconocido"
                if usuario.password_hash.startswith('pbkdf2'):
                    hash_type = "pbkdf2"
                elif usuario.password_hash.startswith('scrypt'):
                    hash_type = "scrypt"
                elif usuario.password_hash.startswith('$2b$'):
                    hash_type = "bcrypt"
                
                print(f"  Tipo de hash: {hash_type}")
                print(f"  Hash: {usuario.password_hash[:50]}...")
                
                # Probar si la contraseña por defecto funciona
                default_password = f"{usuario.username}123!"
                if usuario.check_password(default_password):
                    print(f"  ✓ La contraseña por defecto '{default_password}' funciona")
                else:
                    print(f"  × La contraseña por defecto '{default_password}' no funciona")
            else:
                print("  ¡No tiene hash de contraseña!")

if __name__ == "__main__":
    listar_usuarios()

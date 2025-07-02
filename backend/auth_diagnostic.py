"""
Script de diagnóstico para identificar problemas de autenticación
"""
from app import create_app, db
from app.models.usuario import Usuario
from werkzeug.security import check_password_hash
import sys
import getpass

# Crear la aplicación Flask
app = create_app()

def test_authentication(username, password):
    """Prueba la autenticación paso a paso"""
    print(f"\n🔍 Diagnóstico de autenticación para usuario: {username}")
    
    with app.app_context():
        # 1. Verificar si el usuario existe
        print("\n1. Verificando si el usuario existe en la base de datos...")
        usuario = Usuario.query.filter_by(username=username).first()
        
        if not usuario:
            print(f"❌ Error: El usuario '{username}' no existe en la base de datos.")
            return
        
        print(f"✅ Usuario encontrado: ID={usuario.id}, Rol={usuario.rol}, Email={usuario.email}")
        
        # 2. Verificar si el usuario está activo
        print("\n2. Verificando si el usuario está activo...")
        if not usuario.activo:
            print("❌ Error: La cuenta está desactivada.")
            return
        
        print("✅ La cuenta está activa.")
        
        # 3. Verificar la contraseña directamente
        print("\n3. Verificando la contraseña usando el método check_password...")
        if usuario.check_password(password):
            print("✅ La contraseña es correcta usando método check_password.")
        else:
            print("❌ Error: La contraseña es incorrecta usando método check_password.")
        
        # 4. Verificar el hash de contraseña directamente
        print("\n4. Detalles del hash de contraseña almacenado:")
        print(f"Hash almacenado: {usuario.password_hash}")
        print(f"Formato de hash: {'bcrypt' if usuario.password_hash.startswith('$2b$') else 'pbkdf2' if usuario.password_hash.startswith('pbkdf2') else 'desconocido'}")
        
        # 5. Intentar verificar con check_password_hash directamente
        print("\n5. Verificando la contraseña usando check_password_hash directamente...")
        if check_password_hash(usuario.password_hash, password):
            print("✅ La contraseña es correcta usando check_password_hash directamente.")
        else:
            print("❌ Error: La contraseña es incorrecta usando check_password_hash directamente.")
        
        # 6. Verificar la clave secreta de la aplicación
        print("\n6. Verificando la clave secreta de la aplicación...")
        if app.config.get('SECRET_KEY'):
            print(f"✅ La aplicación tiene una clave secreta configurada (primeros 10 caracteres): {app.config.get('SECRET_KEY')[:10]}...")
        else:
            print("❌ Error: La aplicación no tiene una clave secreta configurada.")
        
        print("\n🔍 Diagnóstico completo.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
        if len(sys.argv) > 2:
            password = sys.argv[2]
        else:
            password = getpass.getpass("Contraseña: ")
        test_authentication(username, password)
    else:
        print("Uso: python auth_diagnostic.py <username> [password]")
        print("Si no se proporciona la contraseña, se solicitará de forma segura.")

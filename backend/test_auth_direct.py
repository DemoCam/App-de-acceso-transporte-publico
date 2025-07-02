"""
Script para probar directamente la autenticación con credenciales específicas
"""
import os
import sys
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def probar_autenticacion(username, password):
    """Prueba directamente la autenticación con credenciales específicas"""
    try:
        # Obtener credenciales de la base de datos
        db_user = os.environ.get('DATABASE_USER', 'root')
        db_password = os.environ.get('DATABASE_PASSWORD', '')
        db_host = os.environ.get('DATABASE_HOST', 'localhost')
        db_name = os.environ.get('DATABASE_NAME', 'transporte_accesible_cali')
        
        # Conectar a la base de datos
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            
            # Obtener el usuario y su hash
            cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
            usuario = cursor.fetchone()
            
            if not usuario:
                print(f"❌ No se encontró el usuario '{username}' en la base de datos.")
                return
            
            # Mostrar detalles del usuario
            print(f"ID: {usuario['id']}")
            print(f"Username: {usuario['username']}")
            print(f"Email: {usuario['email']}")
            print(f"Rol: {usuario['rol']}")
            print(f"Activo: {usuario['activo']}")
            print(f"Hash de contraseña: {usuario['password_hash']}")
            
            # Probar verificación de contraseña
            try:
                if check_password_hash(usuario['password_hash'], password):
                    print(f"✅ La contraseña '{password}' es CORRECTA para el usuario '{username}'")
                else:
                    print(f"❌ La contraseña '{password}' es INCORRECTA para el usuario '{username}'")
            except Exception as e:
                print(f"❌ Error al verificar la contraseña: {str(e)}")
            
            # Crear un nuevo hash y probar
            nuevo_hash = generate_password_hash(password)
            print(f"\nNuevo hash generado: {nuevo_hash}")
            try:
                if check_password_hash(nuevo_hash, password):
                    print(f"✅ Verificación con nuevo hash: CORRECTA")
                else:
                    print(f"❌ Verificación con nuevo hash: INCORRECTA")
            except Exception as e:
                print(f"❌ Error al verificar con nuevo hash: {str(e)}")
            
            # Actualizar la contraseña en la base de datos
            respuesta = input("\n¿Quieres actualizar la contraseña en la base de datos? (s/n): ")
            if respuesta.lower() == 's':
                cursor.execute(
                    "UPDATE usuarios SET password_hash = %s WHERE username = %s",
                    (nuevo_hash, username)
                )
                connection.commit()
                print(f"✅ Contraseña actualizada para el usuario '{username}'")
            
    except mysql.connector.Error as e:
        print(f"❌ Error al conectar a MySQL: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\nConexión a MySQL cerrada")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        username = sys.argv[1]
        password = sys.argv[2]
        probar_autenticacion(username, password)
    else:
        print("Uso: python test_auth_direct.py <username> <password>")

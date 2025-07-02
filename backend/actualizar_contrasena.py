"""
Script simplificado para actualizar la contraseña de un usuario
"""
import os
import sys
import mysql.connector
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def actualizar_contrasena(username, password):
    """Actualiza la contraseña de un usuario directamente en la base de datos"""
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
            
            # Comprobar si existe el usuario
            cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
            usuario = cursor.fetchone()
            
            if not usuario:
                print(f"❌ No se encontró el usuario '{username}' en la base de datos.")
                return
            
            # Generar hash con método pbkdf2 que es más compatible
            nuevo_hash = generate_password_hash(password, method='pbkdf2:sha256')
            
            # Mostrar información del usuario
            print(f"Usuario encontrado: {usuario['username']} (ID: {usuario['id']})")
            print(f"Hash anterior: {usuario['password_hash']}")
            print(f"Nuevo hash a usar: {nuevo_hash}")
            
            # Actualizar la contraseña en la base de datos
            cursor.execute(
                "UPDATE usuarios SET password_hash = %s WHERE username = %s",
                (nuevo_hash, username)
            )
            connection.commit()
            print(f"✅ Contraseña actualizada para el usuario '{username}'")
            
            # Verificar que se actualizó correctamente
            cursor.execute("SELECT password_hash FROM usuarios WHERE username = %s", (username,))
            usuario_actualizado = cursor.fetchone()
            print(f"Hash almacenado en la base de datos: {usuario_actualizado['password_hash']}")
            
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
        actualizar_contrasena(username, password)
    else:
        print("Uso: python actualizar_contrasena.py <username> <password>")

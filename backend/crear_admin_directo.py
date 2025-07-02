"""
Script para crear un usuario administrador directamente en la base de datos
sin depender de la aplicación Flask
"""
import mysql.connector
import os
import getpass
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Cargar variables de entorno
load_dotenv()

def crear_admin():
    """Crea un usuario administrador directamente en la base de datos"""
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
            cursor = connection.cursor()
            
            # Verificar si ya existe un usuario administrador con username 'superadmin'
            cursor.execute("SELECT id FROM usuarios WHERE username = %s", ('superadmin',))
            admin_exists = cursor.fetchone()
            
            if admin_exists:
                print("Ya existe un usuario con el nombre 'superadmin'.")
                opcion = input("¿Desea restablecer su contraseña? (s/n): ")
                if opcion.lower() != 's':
                    return
                
                # Solicitar la nueva contraseña
                password = getpass.getpass("Ingrese la nueva contraseña: ")
                password_confirm = getpass.getpass("Confirme la nueva contraseña: ")
                
                if password != password_confirm:
                    print("Las contraseñas no coinciden.")
                    return
                
                # Encriptar la contraseña y actualizar el usuario
                password_hash = generate_password_hash(password)
                cursor.execute(
                    "UPDATE usuarios SET password_hash = %s WHERE username = %s",
                    (password_hash, 'superadmin')
                )
                connection.commit()
                print("La contraseña del usuario 'superadmin' ha sido actualizada correctamente.")
            else:
                # Crear un nuevo usuario administrador
                username = 'superadmin'
                email = 'superadmin@transporte-cali.com'
                nombre = 'Super'
                apellido = 'Admin'
                rol = 'admin'
                
                # Solicitar la contraseña
                password = getpass.getpass("Ingrese la contraseña para el nuevo administrador: ")
                password_confirm = getpass.getpass("Confirme la contraseña: ")
                
                if password != password_confirm:
                    print("Las contraseñas no coinciden.")
                    return
                
                # Encriptar la contraseña
                password_hash = generate_password_hash(password)
                
                # Insertar el nuevo usuario
                cursor.execute(
                    """INSERT INTO usuarios (username, email, nombre, apellido, password_hash, rol, activo) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (username, email, nombre, apellido, password_hash, rol, True)
                )
                connection.commit()
                print(f"Usuario administrador '{username}' creado correctamente.")
                print(f"Email: {email}")
                print("No olvide esta contraseña, ya que está encriptada y no se puede recuperar.")
    
    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a MySQL cerrada")

if __name__ == "__main__":
    crear_admin()

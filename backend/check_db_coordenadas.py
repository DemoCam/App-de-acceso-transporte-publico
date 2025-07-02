"""
Script para verificar la estructura de la tabla rutas y la columna coordenadas
"""

import os
import sys
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Cargar variables de entorno
load_dotenv()

def check_rutas_table():
    """Verifica la estructura de la tabla rutas y la presencia de la columna coordenadas"""
    try:
        # Conectar a MySQL
        connection = mysql.connector.connect(
            host=os.environ.get('DATABASE_HOST', 'localhost'),
            user=os.environ.get('DATABASE_USER', 'root'),
            password=os.environ.get('DATABASE_PASSWORD', ''),
            database=os.environ.get('DATABASE_NAME', 'transporte_accesible_cali')
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            
            # Verificar la estructura de la tabla rutas
            print("Verificando estructura de la tabla rutas...")
            cursor.execute("DESCRIBE rutas")
            columnas = cursor.fetchall()
            
            # Imprimir todas las columnas
            print("\nColumnas en la tabla rutas:")
            coordenadas_exists = False
            for columna in columnas:
                print(f"- {columna['Field']}: {columna['Type']} (Null: {columna['Null']})")
                if columna['Field'] == 'coordenadas':
                    coordenadas_exists = True
            
            if coordenadas_exists:
                print("\n✅ La columna 'coordenadas' existe en la tabla.")
                
                # Verificar si hay rutas con coordenadas
                cursor.execute("SELECT id, numero, nombre, coordenadas FROM rutas")
                rutas = cursor.fetchall()
                
                print(f"\nRutas en la base de datos: {len(rutas)}")
                for ruta in rutas:
                    coordenadas_str = ruta['coordenadas'] if ruta['coordenadas'] else "NULL"
                    print(f"- Ruta {ruta['numero']} ({ruta['nombre']}): coordenadas = {coordenadas_str}")
            else:
                print("\n❌ La columna 'coordenadas' NO existe en la tabla.")
                
                # Intentar añadir la columna si no existe
                print("\nIntentando añadir la columna 'coordenadas'...")
                try:
                    cursor.execute(
                        "ALTER TABLE rutas ADD COLUMN coordenadas TEXT NULL COMMENT 'Arreglo de coordenadas [lat, lng] para el trazado de la ruta'"
                    )
                    connection.commit()
                    print("✅ Columna 'coordenadas' añadida correctamente.")
                except Error as e:
                    print(f"❌ Error al añadir columna: {e}")
            
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("\nConexión a MySQL cerrada")

if __name__ == "__main__":
    check_rutas_table()

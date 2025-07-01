"""
Script para solucionar el problema de SQLAlchemy
"""
import subprocess
import sys
import time

def run_command(command):
    """Ejecuta un comando y muestra la salida"""
    print(f"\n> Ejecutando: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    print(result.stdout)
    if result.stderr:
        print(f"ERRORES: {result.stderr}")
    return result.returncode == 0

def main():
    """Soluciona el problema de SQLAlchemy"""
    print("=== Solucionador de problemas con SQLAlchemy ===")
    
    # 1. Comprobar la versión de pip
    print("\n1. Comprobando versión de pip...")
    run_command("pip --version")
    
    # 2. Desinstalar paquetes relacionados con SQLAlchemy
    print("\n2. Desinstalando paquetes conflictivos...")
    run_command("pip uninstall -y sqlalchemy")
    run_command("pip uninstall -y flask-sqlalchemy")
    
    # 3. Instalar versiones específicas compatibles
    print("\n3. Instalando versiones compatibles...")
    run_command("pip install sqlalchemy==1.4.46")
    run_command("pip install flask-sqlalchemy==2.5.1")
    
    # 4. Verificar instalación
    print("\n4. Verificando instalación...")
    run_command("pip list | findstr sqlalchemy")
    
    # 5. Probar importación
    print("\n5. Probando importación de SQLAlchemy...")
    try:
        import sqlalchemy
        print(f"SQLAlchemy instalado correctamente, versión: {sqlalchemy.__version__}")
        
        import flask_sqlalchemy
        print(f"Flask-SQLAlchemy instalado correctamente")
        
        return True
    except Exception as e:
        print(f"Error al importar SQLAlchemy: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Problema resuelto. Ahora puedes ejecutar la aplicación con 'python run_direct.py'")
    else:
        print("\n❌ No se pudo resolver el problema automáticamente.")
    
    # Mantener la consola abierta
    input("\nPresiona Enter para salir...")

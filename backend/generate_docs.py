#!/usr/bin/env python
"""
Script para generar un paquete de documentación completo para la App de Transporte Accesible Cali.

Este script compila todos los manuales y documentación en un único archivo ZIP descargable.
También verifica que todos los archivos de documentación existan y están actualizados.
"""

import os
import shutil
import zipfile
import datetime
import sys

# Configuración
DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dist')
MANUALES_DIR = os.path.join(DOCS_DIR, 'manuales')
VERSION = "1.0.0"  # Versión del paquete de documentación

# Lista de archivos de documentación esperados
EXPECTED_FILES = [
    os.path.join(MANUALES_DIR, 'manual_usuario.md'),
    os.path.join(MANUALES_DIR, 'manual_instalacion.md'),
    os.path.join(MANUALES_DIR, 'api_reference.md'),
    os.path.join(DOCS_DIR, 'accesibilidad.md'),
    os.path.join(DOCS_DIR, 'solucion_problemas.md'),
]

def check_files_exist():
    """Verifica que todos los archivos esperados existan."""
    missing_files = []
    
    for file_path in EXPECTED_FILES:
        if not os.path.isfile(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("Error: Faltan los siguientes archivos de documentación:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    return True

def create_output_dir():
    """Crea el directorio de salida si no existe."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Directorio creado: {OUTPUT_DIR}")

def create_documentation_package():
    """Crea un paquete ZIP con toda la documentación."""
    # Nombre del archivo con fecha
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    zip_filename = f"documentacion-transporte-accesible-v{VERSION}-{date_str}.zip"
    zip_path = os.path.join(OUTPUT_DIR, zip_filename)
    
    # Crear el archivo ZIP
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Agregar el archivo README.md de la raíz
        readme_path = os.path.join(os.path.dirname(os.path.dirname(DOCS_DIR)), 'README.md')
        if os.path.exists(readme_path):
            zipf.write(readme_path, os.path.basename(readme_path))
        
        # Recorrer el directorio docs y agregar todos los archivos
        for root, dirs, files in os.walk(DOCS_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                # Calcular la ruta relativa dentro del ZIP
                rel_path = os.path.relpath(file_path, os.path.dirname(DOCS_DIR))
                zipf.write(file_path, rel_path)
    
    print(f"Paquete de documentación creado: {zip_path}")
    return zip_path

def copy_to_static(zip_path):
    """Copia el paquete de documentación a la carpeta static para ser descargable desde la web."""
    static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                             'app', 'static', 'docs')
    
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    
    dest_path = os.path.join(static_dir, os.path.basename(zip_path))
    shutil.copy(zip_path, dest_path)
    
    print(f"Paquete copiado a: {dest_path}")
    print(f"URL para descarga: /static/docs/{os.path.basename(zip_path)}")

def main():
    """Función principal."""
    print("=== Generador de paquete de documentación ===")
    
    # Verificar archivos
    if not check_files_exist():
        print("\nPor favor, crea los archivos faltantes antes de generar el paquete.")
        sys.exit(1)
    
    # Crear directorio de salida
    create_output_dir()
    
    # Crear paquete
    zip_path = create_documentation_package()
    
    # Copiar a static (opcional)
    try:
        copy_to_static(zip_path)
    except Exception as e:
        print(f"Advertencia: No se pudo copiar el archivo a static: {e}")
    
    print("\nProceso completado con éxito.")
    print(f"El paquete de documentación está disponible en: {zip_path}")

if __name__ == "__main__":
    main()

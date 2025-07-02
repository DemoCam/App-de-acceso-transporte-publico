import os
import sys
from pathlib import Path
from flask import Flask, render_template

# Obtener la ruta absoluta del proyecto
project_root = Path(__file__).parent.absolute()
app_dir = project_root / 'app'
template_dir = app_dir / 'templates'

# Verificar si las rutas existen
print(f"Proyecto: {project_root} {'(existe)' if project_root.exists() else '(no existe)'}")
print(f"App: {app_dir} {'(existe)' if app_dir.exists() else '(no existe)'}")
print(f"Templates: {template_dir} {'(existe)' if template_dir.exists() else '(no existe)'}")

# Crear aplicación Flask con rutas de plantillas explícitas
app = Flask(__name__, 
            template_folder=str(template_dir),
            static_folder=str(app_dir / 'static'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnostico')
def diagnostico():
    return f"""
    <h1>Diagnóstico de la Aplicación</h1>
    <p>Directorio de la aplicación: {app_dir}</p>
    <p>Directorio de plantillas: {app.template_folder}</p>
    <p>Directorio estático: {app.static_folder}</p>
    <p>Rutas de búsqueda de plantillas: {app.jinja_loader.searchpath}</p>
    """

if __name__ == '__main__':
    app.run(debug=True)

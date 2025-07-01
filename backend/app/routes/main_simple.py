"""
Versión simplificada del archivo de rutas main.py para probar la aplicación
"""
from flask import Blueprint, render_template, jsonify

# Crear un blueprint alternativo
main_simple = Blueprint('main_simple', __name__)

@main_simple.route('/')
def index():
    """Página principal simplificada"""
    return render_template('index_simple.html', title="App Transporte Accesible - Cali (Versión Simple)")

@main_simple.route('/test')
def test():
    """Ruta de prueba que devuelve JSON"""
    return jsonify({
        'status': 'success',
        'message': 'La aplicación Flask está funcionando correctamente'
    })

# Función para registrar este blueprint como alternativa
def register_simple_routes(app):
    app.register_blueprint(main_simple)
    print("Rutas simplificadas registradas correctamente")

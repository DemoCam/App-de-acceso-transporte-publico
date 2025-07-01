from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Página principal de la aplicación"""
    return render_template('index.html', title="App Transporte Accesible - Cali")

@main.route('/rutas')
def rutas():
    """Página para consultar rutas de transporte"""
    return render_template('rutas.html', title="Consulta de Rutas")

@main.route('/paradas')
def paradas():
    """Página para consultar paradas cercanas"""
    return render_template('paradas.html', title="Paradas Cercanas")

@main.route('/ayuda')
def ayuda():
    """Página de ayuda y guías de uso"""
    return render_template('ayuda.html', title="Ayuda y Guía")

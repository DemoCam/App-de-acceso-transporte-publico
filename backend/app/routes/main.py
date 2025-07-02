from flask import Blueprint, render_template, request, jsonify
from app.models.transporte import Ruta, Parada, RutaParada
from app.services.mio_service import MioService

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@main.route('/rutas')
def rutas():
    """Página para visualizar rutas de transporte"""
    # Obtener todas las rutas ordenadas por número
    rutas = Ruta.query.order_by(Ruta.numero).all()
    return render_template('rutas.html', rutas=rutas)

@main.route('/rutas/<int:ruta_id>')
def detalle_ruta(ruta_id):
    """Página para ver detalle de una ruta específica"""
    ruta = Ruta.query.get_or_404(ruta_id)
    
    # Obtener las paradas de la ruta en orden
    paradas = Parada.query.join(Parada.ruta_paradas).filter(
        RutaParada.ruta_id == ruta_id
    ).order_by(RutaParada.orden).all()
    
    return render_template('rutas_detalle.html', ruta=ruta, paradas=paradas)

@main.route('/paradas')
def paradas():
    """Página para visualizar paradas de transporte"""
    # Obtener todas las paradas ordenadas por nombre
    paradas = Parada.query.order_by(Parada.nombre).all()
    return render_template('paradas.html', paradas=paradas)

@main.route('/paradas/<int:parada_id>')
def detalle_parada(parada_id):
    """Página para ver detalle de una parada específica"""
    parada = Parada.query.get_or_404(parada_id)
    
    return render_template('paradas_detalle.html', parada=parada)

@main.route('/mapa')
def mapa():
    """Página para visualizar mapa interactivo"""
    # Obtener todas las rutas y paradas para el mapa
    rutas = Ruta.query.all()
    paradas = Parada.query.all()
    
    return render_template('mapa.html', rutas=rutas, paradas=paradas)

@main.route('/ayuda')
def ayuda():
    """Página de ayuda y accesibilidad"""
    return render_template('ayuda.html')

# Ruta para pruebas de integración con MIO
@main.route('/mio-test')
def mio_test():
    """Página para probar la integración con datos del MIO"""
    # Inicializar el servicio MIO
    mio_service = MioService()
    
    # Obtener rutas y paradas del MIO
    rutas = mio_service.obtener_rutas()
    paradas = mio_service.obtener_paradas()
    
    return render_template('mio_test.html', rutas=rutas, paradas=paradas)

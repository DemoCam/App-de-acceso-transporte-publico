from flask import Blueprint, jsonify, request
from app.services.mio_service import (
    obtener_rutas, obtener_ruta, obtener_paradas, 
    obtener_paradas_cercanas
)

api = Blueprint('api', __name__)

@api.route('/rutas', methods=['GET'])
def get_rutas():
    """API para obtener todas las rutas de transporte"""
    # Parámetro de búsqueda opcional
    busqueda = request.args.get('q', '')
    
    # Obtener todas las rutas
    rutas = obtener_rutas()
    
    # Aplicar filtro de búsqueda si se especificó
    if busqueda:
        busqueda = busqueda.lower()
        rutas = [ruta for ruta in rutas if 
                 busqueda in ruta['numero'].lower() or
                 busqueda in ruta['nombre'].lower() or
                 busqueda in ruta['origen'].lower() or
                 busqueda in ruta['destino'].lower()]
    
    return jsonify({
        'status': 'success',
        'rutas': rutas
    })

@api.route('/rutas/<int:id>', methods=['GET'])
def get_ruta(id):
    """API para obtener información de una ruta específica"""
    ruta = obtener_ruta(id)
    
    if not ruta:
        return jsonify({
            'status': 'error',
            'message': f'No se encontró la ruta con ID {id}'
        }), 404
    
    return jsonify({
        'status': 'success',
        'ruta': ruta
    })

@api.route('/paradas', methods=['GET'])
def get_paradas():
    """API para obtener todas las paradas de transporte"""
    paradas = obtener_paradas()
    
    return jsonify({
        'status': 'success',
        'paradas': paradas
    })

@api.route('/paradas/cercanas', methods=['GET'])
def get_paradas_cercanas():
    """API para obtener paradas cercanas a una ubicación"""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    distancia = request.args.get('distancia', default=500, type=int)
    ruta_filtro = request.args.get('ruta', default='')
    
    if not lat or not lng:
        return jsonify({
            'status': 'error',
            'message': 'Se requieren parámetros de latitud (lat) y longitud (lng)'
        }), 400
    
    # Obtener paradas cercanas
    paradas = obtener_paradas_cercanas(lat, lng, distancia)
    
    # Filtrar por ruta si se especifica
    if ruta_filtro:
        paradas = [parada for parada in paradas if 
                  any(ruta.lower().find(ruta_filtro.lower()) != -1 for ruta in parada['rutas'])]
    
    return jsonify({
        'status': 'success',
        'paradas': paradas
    })

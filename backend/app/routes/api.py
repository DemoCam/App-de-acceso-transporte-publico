from flask import Blueprint, jsonify, request
from app.models.transporte import Ruta, Parada, RutaParada
from app.services.mio_service import MioService
from app import db
from sqlalchemy.orm import joinedload

api = Blueprint('api', __name__)

@api.route('/rutas', methods=['GET'])
def get_rutas():
    """Obtener todas las rutas"""
    rutas = Ruta.query.all()
    return jsonify({
        'status': 'success',
        'data': [ruta.to_dict() for ruta in rutas]
    })

@api.route('/rutas/<int:ruta_id>', methods=['GET'])
def get_ruta(ruta_id):
    """Obtener una ruta específica con sus paradas"""
    ruta = Ruta.query.get_or_404(ruta_id)
    return jsonify({
        'status': 'success',
        'data': ruta.to_dict(include_paradas=True)
    })

@api.route('/paradas', methods=['GET'])
def get_paradas():
    """Obtener todas las paradas"""
    paradas = Parada.query.all()
    return jsonify({
        'status': 'success',
        'data': [parada.to_dict() for parada in paradas]
    })

@api.route('/paradas/<int:parada_id>', methods=['GET'])
def get_parada(parada_id):
    """Obtener una parada específica"""
    parada = Parada.query.get_or_404(parada_id)
    return jsonify({
        'status': 'success',
        'data': parada.to_dict()
    })

@api.route('/paradas/<int:parada_id>/rutas', methods=['GET'])
def get_rutas_por_parada(parada_id):
    """Obtener todas las rutas que pasan por una parada"""
    parada = Parada.query.get_or_404(parada_id)
    rutas = parada.rutas
    return jsonify({
        'status': 'success',
        'data': [ruta.to_dict() for ruta in rutas]
    })

@api.route('/rutas-paradas', methods=['GET'])
def get_rutas_paradas():
    """Obtener todas las asociaciones entre rutas y paradas"""
    ruta_id = request.args.get('ruta_id', type=int)
    parada_id = request.args.get('parada_id', type=int)
    
    query = RutaParada.query.join(Ruta).join(Parada)
    
    if ruta_id:
        query = query.filter(RutaParada.ruta_id == ruta_id)
    if parada_id:
        query = query.filter(RutaParada.parada_id == parada_id)
    
    rutas_paradas = query.all()
    
    return jsonify({
        'status': 'success',
        'data': [{
            'ruta_id': rp.ruta_id,
            'ruta': {
                'numero': rp.ruta.numero,
                'nombre': rp.ruta.nombre
            },
            'parada_id': rp.parada_id,
            'parada': {
                'nombre': rp.parada.nombre,
                'direccion': rp.parada.direccion
            },
            'orden': rp.orden,
            'tiempo_estimado': rp.tiempo_estimado
        } for rp in rutas_paradas]
    })

# Endpoints para integración con MIO
@api.route('/mio/rutas', methods=['GET'])
def get_mio_rutas():
    """Obtener rutas del MIO desde el servicio externo"""
    mio_service = MioService()
    rutas = mio_service.obtener_rutas()
    return jsonify({
        'status': 'success',
        'data': rutas
    })

@api.route('/mio/paradas', methods=['GET'])
def get_mio_paradas():
    """Obtener paradas del MIO desde el servicio externo"""
    mio_service = MioService()
    paradas = mio_service.obtener_paradas()
    return jsonify({
        'status': 'success',
        'data': paradas
    })

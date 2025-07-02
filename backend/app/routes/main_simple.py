"""
Versión simplificada de las rutas principales para cuando fallan los blueprints principales
"""
def register_simple_routes(app):
    """Registra rutas simples en la aplicación Flask directamente"""
    
    @app.route('/')
    def index_simple():
        """Página de inicio simplificada"""
        return render_template('index_simple.html')
    
    @app.route('/rutas')
    def rutas_simple():
        """Listado simple de rutas"""
        try:
            from app.models.transporte import Ruta
            rutas = Ruta.query.order_by(Ruta.numero).all()
            return render_template('index_simple.html', rutas=rutas, 
                                   message="Listado de rutas en modo simplificado")
        except Exception as e:
            return render_template('index_simple.html', 
                                   error=f"Error al cargar rutas: {str(e)}")
    
    @app.route('/paradas')
    def paradas_simple():
        """Listado simple de paradas"""
        try:
            from app.models.transporte import Parada
            paradas = Parada.query.order_by(Parada.nombre).all()
            return render_template('index_simple.html', paradas=paradas, 
                                  message="Listado de paradas en modo simplificado")
        except Exception as e:
            return render_template('index_simple.html', 
                                  error=f"Error al cargar paradas: {str(e)}")
    
    @app.route('/diagnostico')
    def diagnostico():
        """Página de diagnóstico para verificar el estado de la aplicación"""
        try:
            from app import db
            
            diagnostico = {
                'flask': True,
                'database_connection': False,
                'tables': {
                    'rutas': 0,
                    'paradas': 0,
                    'ruta_parada': 0,
                    'usuarios': 0
                }
            }
            
            # Verificar conexión a la base de datos
            try:
                db.session.execute("SELECT 1")
                diagnostico['database_connection'] = True
                
                # Contar registros en tablas
                from app.models.transporte import Ruta, Parada, RutaParada
                from app.models.usuario import Usuario
                
                diagnostico['tables']['rutas'] = Ruta.query.count()
                diagnostico['tables']['paradas'] = Parada.query.count()
                diagnostico['tables']['ruta_parada'] = RutaParada.query.count()
                diagnostico['tables']['usuarios'] = Usuario.query.count()
            except Exception as e:
                diagnostico['database_error'] = str(e)
            
            return render_template('index_simple.html', diagnostico=diagnostico, 
                                  message="Diagnóstico del sistema")
        except Exception as e:
            return f"Error grave: {str(e)}"
            
    print("Rutas simplificadas registradas correctamente")

# Asegurarse de que se pueda importar correctamente
from flask import render_template

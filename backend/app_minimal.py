"""
Una aplicación Flask simplificada sin SQLAlchemy para probar la funcionalidad básica
"""
from flask import Flask, render_template, jsonify

app = Flask(__name__, 
            template_folder="../app/templates",
            static_folder="../app/static")

@app.route('/')
def home():
    """Página principal simplificada"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>App de Transporte - Versión Mínima</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
            .container { max-width: 800px; margin: 0 auto; }
            .header { background-color: #007bff; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; }
            .btn { display: inline-block; background-color: #007bff; color: white; padding: 10px 15px; 
                  text-decoration: none; border-radius: 5px; margin: 10px 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>App de Transporte Accesible - Cali</h1>
                <p>Versión mínima de prueba</p>
            </div>
            <div class="content">
                <h2>La aplicación Flask está funcionando correctamente</h2>
                <p>Esta es una versión simplificada sin base de datos para verificar la instalación de Flask.</p>
                <p>
                    <a href="/api/test" class="btn">Probar API</a>
                    <a href="/about" class="btn">Acerca de</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/about')
def about():
    """Página de acerca de"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Acerca de - App de Transporte</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
            .container { max-width: 800px; margin: 0 auto; }
            .header { background-color: #28a745; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; }
            .btn { display: inline-block; background-color: #007bff; color: white; padding: 10px 15px; 
                  text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Acerca de esta aplicación</h1>
            </div>
            <div class="content">
                <h2>Aplicación de prueba</h2>
                <p>Esta es una versión simplificada de la aplicación para verificar que Flask está funcionando correctamente.</p>
                <p>El próximo paso es resolver los problemas de SQLAlchemy para poder utilizar la base de datos.</p>
                <p><a href="/" class="btn">Volver al inicio</a></p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/api/test')
def api_test():
    """API de prueba"""
    return jsonify({
        'status': 'success',
        'message': 'La API está funcionando correctamente',
        'version': 'minimal-test'
    })

if __name__ == '__main__':
    print("Iniciando aplicación Flask simplificada (sin SQLAlchemy)...")
    print("Visita http://127.0.0.1:5000/ en tu navegador")
    app.run(debug=True, port=5000)

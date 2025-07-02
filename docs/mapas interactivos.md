Guía Técnica: Implementación de Mapas InteractivosEste documento describe el proceso técnico para integrar un sistema de creación y visualización de rutas de transporte en la aplicación "App de Transporte Accesible – Cali", utilizando Flask, MySQL, Bootstrap y Leaflet.js.Visión General de la ArquitecturaEl flujo de datos y la interacción entre componentes será el siguiente:Panel de Admin (Creación de Rutas):Un administrador accederá a una página especial en el panel de administración.Esta página contendrá el mapa interactivo para dibujar (basado en Leaflet.js).Al finalizar el dibujo, las coordenadas (en formato JSON) se enviarán junto con el nombre de la ruta a un endpoint de Flask.Backend (Flask y MySQL):Un endpoint POST recibirá los datos del administrador y los guardará en la tabla rutas de la base de datos MySQL. Las coordenadas se almacenarán en un campo de tipo JSON o TEXT.Se creará un endpoint GET público (ej: /api/rutas) que consultará la base de datos y devolverá una lista de todas las rutas y sus coordenadas en formato JSON.Interfaz de Usuario (Visualización de Rutas):La página principal del usuario (o donde se muestren las rutas) contendrá un mapa de Leaflet.Un script de JavaScript hará una petición fetch al endpoint /api/rutas.Con los datos recibidos, el script dibujará todas las rutas en el mapa, añadiendo información relevante como el nombre de la ruta en un popup.Paso 1: Modificar la Base de Datos (MySQL)Necesitamos un lugar para almacenar las coordenadas de la ruta. La mejor opción es añadir una columna a tu tabla de rutas. Asumiremos que tienes una tabla llamada rutas.Ejecuta el siguiente comando SQL en tu base de datos MySQL. Si usas un ORM como SQLAlchemy (común con Flask), puedes modificar tu modelo.Opción A (Recomendada, si usas MySQL 5.7.8+):Usar el tipo de dato JSON.ALTER TABLE rutas
ADD COLUMN coordenadas JSON NULL COMMENT 'Arreglo de coordenadas [lat, lng] para el trazado de la ruta';
Opción B (Alternativa):Si tu versión de MySQL es más antigua, usa TEXT o LONGTEXT.ALTER TABLE rutas
ADD COLUMN coordenadas TEXT NULL COMMENT 'Arreglo de coordenadas [lat, lng] en formato de texto JSON';
Paso 2: Integración en el Panel de AdministradorAquí es donde el administrador crea las rutas. Debes modificar la plantilla de Flask correspondiente a la creación/edición de rutas.Ubicación del archivo: backend/app/templates/admin/formulario_ruta.html (o como se llame).Integra el código del mapa interactivo que te proporcioné anteriormente. La clave es que el <textarea> donde se generan las coordenadas debe tener un name para que Flask lo reciba en el request.form.<!-- backend/app/templates/admin/formulario_ruta.html -->

{% extends "admin/base.html" %}
{% block content %}
<div class="container mt-4">
    <h2>Crear/Editar Ruta</h2>
    
    <!-- Formulario que enviará los datos a Flask -->
    <form action="{{ url_for('admin.guardar_ruta') }}" method="POST">
        <!-- Campo para el nombre de la ruta -->
        <div class="mb-3">
            <label for="nombre_ruta" class="form-label">Nombre de la Ruta</label>
            <input type="text" class="form-control" id="nombre_ruta" name="nombre_ruta" required>
        </div>

        <!-- Aquí integramos el mapa para dibujar -->
        <div class="mb-3">
            <label class="form-label">Dibuja la ruta en el mapa:</label>
            <!-- Contenedor del mapa con una altura definida -->
            <div id="map-drawer" style="height: 500px; width: 100%;" class="rounded border"></div>
        </div>

        <!-- Textarea OCULTO para almacenar y enviar las coordenadas -->
        <!-- Flask leerá los datos de aquí -->
        <textarea id="coordinates-output" name="coordenadas" class="d-none" required></textarea>

        <button type="submit" class="btn btn-primary">Guardar Ruta</button>
    </form>
</div>

<!-- Scripts de Leaflet y nuestro script de dibujo -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
    // --- LÓGICA DEL MAPA DE DIBUJO ---
    // Este es el mismo script de la herramienta anterior, adaptado ligeramente.
    
    // Coordenadas iniciales para Cali
    const map = L.map('map-drawer').setView([3.4516, -76.5320], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    const coordinatesOutput = document.getElementById('coordinates-output');
    let routePoints = [];
    let currentPolyline = null;

    map.on('click', function(e) {
        routePoints.push([e.latlng.lat, e.latlng.lng]);
        
        if (!currentPolyline) {
            currentPolyline = L.polyline(routePoints, { color: 'blue' }).addTo(map);
        } else {
            currentPolyline.addLatLng(e.latlng);
        }
        
        // Actualiza el textarea oculto con el JSON de las coordenadas
        coordinatesOutput.value = JSON.stringify(routePoints);
    });
</script>
{% endblock %}
Paso 3: Creación de Endpoints en Flask (Backend)Ahora, la lógica en Python para guardar y servir las rutas.Ubicación del archivo: backend/app/routes/admin_routes.py y backend/app/routes/api_routes.py (o donde gestiones tus rutas).A. Endpoint para Guardar la Ruta# backend/app/routes/admin_routes.py (o similar)

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Ruta  # Asumiendo que tienes un modelo Ruta
from app import db
import json

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/rutas/guardar', methods=['POST'])
def guardar_ruta():
    # Aquí iría la lógica para verificar que el usuario es admin
    
    nombre = request.form.get('nombre_ruta')
    coordenadas_json = request.form.get('coordenadas')

    if not nombre or not coordenadas_json:
        flash('Faltan datos para guardar la ruta.', 'danger')
        return redirect(url_for('admin.crear_ruta_form')) # Redirigir al formulario

    # Aquí puedes crear una nueva ruta o actualizar una existente
    # Este es un ejemplo para una nueva ruta
    nueva_ruta = Ruta(
        nombre=nombre,
        coordenadas=coordenadas_json # SQLAlchemy manejará la conversión a JSON/TEXT
    )
    db.session.add(nueva_ruta)
    db.session.commit()

    flash(f'Ruta "{nombre}" guardada con éxito.', 'success')
    return redirect(url_for('admin.dashboard')) # Redirigir al panel de admin
B. Endpoint de API para Servir las RutasEste es el endpoint que tu app de usuario final consumirá.# backend/app/routes/api_routes.py (o similar)

from flask import Blueprint, jsonify
from app.models import Ruta
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/rutas', methods=['GET'])
def obtener_rutas():
    """
    Endpoint público que devuelve todas las rutas con sus coordenadas.
    """
    rutas = Ruta.query.all()
    resultado = []
    
    for ruta in rutas:
        # El campo 'coordenadas' es un string JSON, necesitamos convertirlo a un objeto Python (lista)
        try:
            coordenadas_lista = json.loads(ruta.coordenadas)
        except (TypeError, json.JSONDecodeError):
            coordenadas_lista = [] # Si hay un error o está vacío, devuelve una lista vacía

        resultado.append({
            'id': ruta.id,
            'nombre': ruta.nombre,
            'coordenadas': coordenadas_lista
        })
        
    return jsonify(resultado)
Paso 4: Visualización de Rutas para el Usuario (Frontend)Finalmente, la página donde los usuarios ven las rutas en el mapa.Ubicación del archivo: backend/app/templates/public/mapa_rutas.html (o similar).<!-- backend/app/templates/public/mapa_rutas.html -->

{% extends "public/base.html" %}
{% block content %}
<div class="container mt-4">
    <h1 class="mb-4">Rutas de Transporte Público de Cali</h1>
    
    <!-- Contenedor del mapa de visualización -->
    <div id="map-viewer" style="height: 600px; width: 100%;" class="rounded border shadow-sm"></div>
</div>

<!-- Scripts de Leaflet y nuestro script de visualización -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<!-- Este script debe ir en un archivo .js en tu carpeta static -->
<!-- <script src="{{ url_for('static', filename='js/map_viewer.js') }}"></script> -->
<script>
    document.addEventListener('DOMContentLoaded', function () {
        // 1. Inicializar el mapa centrado en Cali
        const map = L.map('map-viewer').setView([3.4516, -76.5320], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        // 2. Obtener las rutas desde nuestra propia API
        fetch('/api/rutas')
            .then(response => response.json())
            .then(rutas => {
                // 3. Dibujar cada ruta en el mapa
                rutas.forEach(ruta => {
                    if (ruta.coordenadas && ruta.coordenadas.length > 1) {
                        const polyline = L.polyline(ruta.coordenadas, {
                            color: getRandomColor(), // Asigna un color aleatorio a cada ruta
                            weight: 5
                        }).addTo(map);

                        // Añadir un popup con el nombre de la ruta
                        polyline.bindPopup(`<b>Ruta: ${ruta.nombre}</b>`);
                    }
                });
            })
            .catch(error => {
                console.error('Error al cargar las rutas:', error);
                // Podrías mostrar un mensaje de error al usuario aquí
            });

        // Función auxiliar para obtener un color aleatorio para las líneas
        function getRandomColor() {
            const letters = '0123456789ABCDEF';
            let color = '#';
            for (let i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
        }
    });
</script>
{% endblock %}

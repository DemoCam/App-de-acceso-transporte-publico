"""
Servicio para obtener datos de rutas y paradas del MIO de Cali
Utiliza una combinación de datos en caché y posible conexión a APIs externas
"""
import json
import os
import requests
from datetime import datetime
import time
import random
from functools import lru_cache

# Ruta al archivo de datos en caché
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
RUTAS_FILE = os.path.join(DATA_DIR, 'rutas_mio.json')
PARADAS_FILE = os.path.join(DATA_DIR, 'paradas_mio.json')

# URL base para la API del MIO (hipotética, para fines de demostración)
MIO_API_BASE_URL = "https://magicloops.dev/api/loop/f4a3d749-1746-4fdc-a10f-038d097e462c/run?input=Hello+World"

# Asegurarse de que existe el directorio de datos
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@lru_cache(maxsize=1)
def obtener_rutas(force_refresh=False):
    """
    Obtiene todas las rutas del MIO
    
    Args:
        force_refresh (bool): Si es True, fuerza la actualización desde la API
        
    Returns:
        list: Lista de rutas
    """
    # Si ya tenemos datos en caché y no se fuerza actualización, los devolvemos
    if os.path.exists(RUTAS_FILE) and not force_refresh:
        try:
            with open(RUTAS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Comprobar si los datos son recientes (menos de 1 día)
                last_update = data.get('last_update', 0)
                if (time.time() - last_update) < 86400:  # 24 horas
                    print(f"Usando datos de rutas en caché ({len(data['rutas'])} rutas)")
                    return data['rutas']
        except Exception as e:
            print(f"Error al leer datos de rutas en caché: {e}")
    
    # Intentar obtener datos de la API
    try:
        # En una implementación real, aquí se haría una solicitud a la API del MIO
        # response = requests.get(f"{MIO_API_BASE_URL}/rutas")
        # response.raise_for_status()
        # rutas = response.json()
        
        # Como no tenemos acceso real a la API, usamos datos de ejemplo
        rutas = generar_datos_ejemplo_rutas()
        
        # Guardar en caché para uso futuro
        with open(RUTAS_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'rutas': rutas,
                'last_update': time.time()
            }, f, ensure_ascii=False, indent=2)
        
        return rutas
        
    except Exception as e:
        print(f"Error al obtener rutas desde la API: {e}")
        
        # Si hay un error y tenemos datos en caché, los usamos aunque sean antiguos
        if os.path.exists(RUTAS_FILE):
            try:
                with open(RUTAS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"Usando datos de rutas en caché antiguos ({len(data['rutas'])} rutas)")
                    return data['rutas']
            except Exception as f:
                print(f"Error al leer datos de rutas en caché antiguos: {f}")
        
        # Si todo falla, devolvemos un conjunto mínimo de datos de ejemplo
        return generar_datos_ejemplo_rutas(minimal=True)

def obtener_ruta(ruta_id):
    """
    Obtiene información detallada de una ruta específica
    
    Args:
        ruta_id (int): ID de la ruta
        
    Returns:
        dict: Datos de la ruta o None si no existe
    """
    rutas = obtener_rutas()
    
    # Buscar la ruta por ID
    for ruta in rutas:
        if ruta['id'] == ruta_id:
            # Enriquecer con datos de paradas
            ruta['paradas'] = obtener_paradas_ruta(ruta_id)
            return ruta
    
    return None

def obtener_paradas(force_refresh=False):
    """
    Obtiene todas las paradas del MIO
    
    Args:
        force_refresh (bool): Si es True, fuerza la actualización desde la API
        
    Returns:
        list: Lista de paradas
    """
    # Similar a obtener_rutas, primero verificamos la caché
    if os.path.exists(PARADAS_FILE) and not force_refresh:
        try:
            with open(PARADAS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Comprobar si los datos son recientes (menos de 1 día)
                last_update = data.get('last_update', 0)
                if (time.time() - last_update) < 86400:  # 24 horas
                    print(f"Usando datos de paradas en caché ({len(data['paradas'])} paradas)")
                    return data['paradas']
        except Exception as e:
            print(f"Error al leer datos de paradas en caché: {e}")
    
    # Intentar obtener datos de la API
    try:
        # En una implementación real, aquí se haría una solicitud a la API del MIO
        # response = requests.get(f"{MIO_API_BASE_URL}/paradas")
        # response.raise_for_status()
        # paradas = response.json()
        
        # Como no tenemos acceso real a la API, usamos datos de ejemplo
        paradas = generar_datos_ejemplo_paradas()
        
        # Guardar en caché para uso futuro
        with open(PARADAS_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'paradas': paradas,
                'last_update': time.time()
            }, f, ensure_ascii=False, indent=2)
        
        return paradas
        
    except Exception as e:
        print(f"Error al obtener paradas desde la API: {e}")
        
        # Si hay un error y tenemos datos en caché, los usamos aunque sean antiguos
        if os.path.exists(PARADAS_FILE):
            try:
                with open(PARADAS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"Usando datos de paradas en caché antiguos ({len(data['paradas'])} paradas)")
                    return data['paradas']
            except Exception as f:
                print(f"Error al leer datos de paradas en caché antiguos: {f}")
        
        # Si todo falla, devolvemos un conjunto mínimo de datos de ejemplo
        return generar_datos_ejemplo_paradas(minimal=True)

def obtener_paradas_cercanas(lat, lng, distancia_max=500):
    """
    Obtiene las paradas cercanas a una ubicación dada
    
    Args:
        lat (float): Latitud
        lng (float): Longitud
        distancia_max (int): Distancia máxima en metros
        
    Returns:
        list: Lista de paradas cercanas con distancia calculada
    """
    paradas = obtener_paradas()
    paradas_cercanas = []
    
    for parada in paradas:
        # Calcular distancia aproximada (fórmula de Haversine simplificada)
        distancia = calcular_distancia_haversine(
            lat, lng, parada['latitud'], parada['longitud'])
        
        # Si está dentro del radio especificado, la agregamos
        if distancia <= distancia_max:
            # Añadir la distancia calculada al objeto de parada
            parada_con_distancia = parada.copy()
            parada_con_distancia['distancia'] = int(distancia)
            paradas_cercanas.append(parada_con_distancia)
    
    # Ordenar por distancia
    paradas_cercanas.sort(key=lambda p: p['distancia'])
    
    return paradas_cercanas

def obtener_paradas_ruta(ruta_id):
    """
    Obtiene las paradas asociadas a una ruta específica
    
    Args:
        ruta_id (int): ID de la ruta
        
    Returns:
        list: Lista de paradas en la ruta con orden
    """
    # En una implementación real, esto sería una consulta a la API o base de datos
    # para obtener las paradas de una ruta específica con su orden
    
    # Para esta demo, generaremos datos de ejemplo
    paradas = obtener_paradas()
    
    # Seleccionar aleatoriamente algunas paradas para esta ruta
    num_paradas = random.randint(10, 20)
    paradas_seleccionadas = random.sample(paradas, min(num_paradas, len(paradas)))
    
    # Asignar orden a las paradas
    for i, parada in enumerate(paradas_seleccionadas):
        parada_con_orden = parada.copy()
        parada_con_orden['orden'] = i + 1
        parada_con_orden['tiempo_estimado'] = i * 3  # Tiempo en minutos desde origen
        paradas_seleccionadas[i] = parada_con_orden
    
    # Ordenar por el campo 'orden'
    return sorted(paradas_seleccionadas, key=lambda p: p['orden'])

def calcular_distancia_haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia entre dos puntos geográficos usando la fórmula de Haversine
    
    Args:
        lat1, lon1: Latitud y longitud del punto 1
        lat2, lon2: Latitud y longitud del punto 2
        
    Returns:
        float: Distancia en metros
    """
    from math import radians, cos, sin, asin, sqrt
    
    # Convertir grados decimales a radianes
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Fórmula de Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371000  # Radio de la Tierra en metros
    
    return c * r

def generar_datos_ejemplo_rutas(minimal=False):
    """
    Genera datos de ejemplo para las rutas del MIO
    
    Args:
        minimal (bool): Si es True, genera un conjunto mínimo de datos
        
    Returns:
        list: Lista de rutas de ejemplo
    """
    if minimal:
        # Versión mínima con solo unas pocas rutas
        return [
            {
                "id": 1,
                "numero": "T31",
                "nombre": "Troncal Aguablanca",
                "origen": "Terminal Andrés Sanín",
                "destino": "Terminal Calipso",
                "hora_inicio": "04:30",
                "hora_fin": "23:00",
                "frecuencia_minutos": 10,
                "descripcion": "Ruta troncal que conecta el oriente con el centro de la ciudad."
            },
            {
                "id": 2,
                "numero": "P10",
                "nombre": "Pretroncal Floralia",
                "origen": "Terminal La Flora",
                "destino": "Centro",
                "hora_inicio": "05:00",
                "hora_fin": "22:00",
                "frecuencia_minutos": 15,
                "descripcion": "Ruta pretroncal que conecta el norte con el centro de la ciudad."
            }
        ]
    
    # Lista de tipos de rutas y sus prefijos
    tipos_rutas = [
        {"prefijo": "T", "tipo": "Troncal", "frecuencia": range(4, 12)},
        {"prefijo": "P", "tipo": "Pretroncal", "frecuencia": range(8, 20)},
        {"prefijo": "A", "tipo": "Alimentadora", "frecuencia": range(15, 30)},
        {"prefijo": "E", "tipo": "Expresa", "frecuencia": range(10, 25)}
    ]
    
    # Terminales y estaciones importantes
    terminales = [
        "Terminal Andrés Sanín", "Terminal Calipso", "Terminal Menga", 
        "Terminal Paso del Comercio", "Terminal Cañaveralejo", "Estación Unidad Deportiva",
        "Estación Chiminangos", "Estación Universidades"
    ]
    
    # Barrios y zonas de Cali
    zonas = [
        "Centro", "El Peñón", "Granada", "San Antonio", "Versalles", "Ciudad Jardín",
        "Pance", "Limonar", "La Flora", "Aguablanca", "Siloé", "Meléndez", "Caney",
        "Santa Librada", "Calipso", "Salomia", "San Nicolás", "Alfonso López"
    ]
    
    # Generar rutas aleatorias
    rutas = []
    for i in range(1, 41):  # Generar 40 rutas
        tipo_ruta = random.choice(tipos_rutas)
        numero = f"{tipo_ruta['prefijo']}{random.randint(10, 99)}"
        
        # Asegurarnos de que el número sea único
        while any(r["numero"] == numero for r in rutas):
            numero = f"{tipo_ruta['prefijo']}{random.randint(10, 99)}"
        
        origen = random.choice(terminales)
        destino = random.choice(zonas)
        
        # Asegurarnos de que origen y destino sean diferentes
        while destino in origen or origen in destino:
            destino = random.choice(zonas)
        
        # Horas de inicio y fin
        hora_inicio = f"{random.randint(4, 6):02d}:{random.choice(['00', '30'])}"
        hora_fin = f"{random.randint(21, 23):02d}:{random.choice(['00', '30'])}"
        
        # Frecuencia en minutos
        frecuencia = random.choice(tipo_ruta["frecuencia"])
        
        # Descripción
        descripciones = [
            f"Ruta {tipo_ruta['tipo'].lower()} que conecta {origen} con {destino}.",
            f"Servicio de transporte {tipo_ruta['tipo'].lower()} entre {origen} y {destino}.",
            f"Ruta {tipo_ruta['tipo'].lower()} que cubre el trayecto {origen}-{destino}."
        ]
        
        ruta = {
            "id": i,
            "numero": numero,
            "nombre": f"{tipo_ruta['tipo']} {destino}",
            "origen": origen,
            "destino": destino,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "frecuencia_minutos": frecuencia,
            "descripcion": random.choice(descripciones)
        }
        
        rutas.append(ruta)
    
    return rutas

def generar_datos_ejemplo_paradas(minimal=False):
    """
    Genera datos de ejemplo para las paradas del MIO
    
    Args:
        minimal (bool): Si es True, genera un conjunto mínimo de datos
        
    Returns:
        list: Lista de paradas de ejemplo
    """
    if minimal:
        # Versión mínima con solo unas pocas paradas
        return [
            {
                "id": 1,
                "nombre": "Estación Universidades",
                "direccion": "Calle 5 #80-00",
                "latitud": 3.3730,
                "longitud": -76.5320,
                "tipo": "estación",
                "accesibilidad": {
                    "rampa": True,
                    "semaforo_sonoro": True
                },
                "rutas": ["T31", "A11", "A17"]
            },
            {
                "id": 2,
                "nombre": "Parada Centro Comercial Único",
                "direccion": "Calle 52 #3-29",
                "latitud": 3.3750,
                "longitud": -76.5340,
                "tipo": "regular",
                "accesibilidad": {
                    "rampa": True,
                    "semaforo_sonoro": False
                },
                "rutas": ["P10", "P21"]
            }
        ]
    
    # Lista de tipos de paradas
    tipos_parada = ["regular", "estación", "terminal"]
    
    # Calles y carreras de Cali
    calles = [f"Calle {i}" for i in range(1, 85)]
    carreras = [f"Carrera {i}" for i in range(1, 100)]
    avenidas = ["Avenida 6", "Avenida Colombia", "Avenida Roosevelt", "Avenida Pasoancho", 
               "Avenida Guadalupe", "Avenida Simón Bolívar", "Autopista Sur"]
    
    # Combinar todas las vías
    vias = calles + carreras + avenidas
    
    # Nombres para las paradas
    prefijos_parada = ["Parada", "Estación", "Terminal", "Vagón"]
    lugares = [
        "Centro Comercial", "Universidad", "Hospital", "Clínica", "Parque", 
        "Estadio", "Biblioteca", "Colegio", "Plaza", "Mercado", "Puente", "Teatro"
    ]
    nombres_propios = [
        "Único", "Chipichape", "Cosmocentro", "Jardín Plaza", "Palmetto", "La 14",
        "Valle del Lili", "San Fernando", "Santa Librada", "San Bosco", "La Flora",
        "Tequendama", "Siloé", "Menga", "Caney", "Calipso", "Andrés Sanín"
    ]
    
    # Generar coordenadas base para el centro de Cali
    base_lat = 3.45
    base_lng = -76.53
    
    # Generar paradas aleatorias
    paradas = []
    for i in range(1, 201):  # Generar 200 paradas
        tipo = random.choices(tipos_parada, weights=[0.7, 0.2, 0.1], k=1)[0]
        
        # Generar nombre de la parada
        if tipo == "terminal":
            nombre = f"Terminal {random.choice(nombres_propios)}"
        elif tipo == "estación":
            nombre = f"Estación {random.choice(nombres_propios)}"
        else:
            prefijo = random.choice(prefijos_parada)
            if random.random() < 0.5:
                nombre = f"{prefijo} {random.choice(lugares)} {random.choice(nombres_propios)}"
            else:
                nombre = f"{prefijo} {random.choice(nombres_propios)}"
        
        # Generar dirección
        via = random.choice(vias)
        numero = f"#{random.randint(1, 99)}-{random.randint(1, 99)}"
        direccion = f"{via} {numero}"
        
        # Generar coordenadas (variación aleatoria alrededor del centro de Cali)
        lat_variacion = (random.random() - 0.5) * 0.1
        lng_variacion = (random.random() - 0.5) * 0.1
        latitud = round(base_lat + lat_variacion, 6)
        longitud = round(base_lng + lng_variacion, 6)
        
        # Características de accesibilidad
        # Las terminales y estaciones tienen más probabilidad de tener características de accesibilidad
        if tipo == "terminal":
            rampa = True
            semaforo = random.random() < 0.8
        elif tipo == "estación":
            rampa = random.random() < 0.9
            semaforo = random.random() < 0.5
        else:
            rampa = random.random() < 0.3
            semaforo = random.random() < 0.1
        
        # Generar rutas que pasan por esta parada (entre 1 y 8)
        num_rutas = random.randint(1, 8)
        rutas_parada = []
        for _ in range(num_rutas):
            tipo_ruta = random.choice(["T", "P", "A", "E"])
            numero_ruta = f"{tipo_ruta}{random.randint(10, 99)}"
            if numero_ruta not in rutas_parada:
                rutas_parada.append(numero_ruta)
        
        parada = {
            "id": i,
            "nombre": nombre,
            "direccion": direccion,
            "latitud": latitud,
            "longitud": longitud,
            "tipo": tipo,
            "accesibilidad": {
                "rampa": rampa,
                "semaforo_sonoro": semaforo
            },
            "rutas": rutas_parada
        }
        
        paradas.append(parada)
    
    return paradas

# Prueba del servicio si se ejecuta directamente
if __name__ == "__main__":
    print("Prueba del servicio de datos MIO")
    
    print("\n1. Obteniendo rutas...")
    rutas = obtener_rutas()
    print(f"Se obtuvieron {len(rutas)} rutas")
    
    if rutas:
        print("\n2. Detalle de la primera ruta:")
        primera_ruta = rutas[0]
        print(json.dumps(primera_ruta, ensure_ascii=False, indent=2))
        
        print("\n3. Obteniendo paradas de la ruta...")
        ruta_con_paradas = obtener_ruta(primera_ruta['id'])
        print(f"La ruta tiene {len(ruta_con_paradas['paradas'])} paradas")
    
    print("\n4. Obteniendo paradas...")
    paradas = obtener_paradas()
    print(f"Se obtuvieron {len(paradas)} paradas")
    
    if paradas:
        print("\n5. Detalle de la primera parada:")
        primera_parada = paradas[0]
        print(json.dumps(primera_parada, ensure_ascii=False, indent=2))
        
        print("\n6. Buscando paradas cercanas...")
        cercanas = obtener_paradas_cercanas(primera_parada['latitud'], primera_parada['longitud'], 1000)
        print(f"Se encontraron {len(cercanas)} paradas cercanas")
        
        if cercanas:
            print("\n7. Primera parada cercana:")
            print(json.dumps(cercanas[0], ensure_ascii=False, indent=2))

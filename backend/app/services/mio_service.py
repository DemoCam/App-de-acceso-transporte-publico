import json
import os
from pathlib import Path
import requests
from flask import current_app

class MioService:
    """
    Servicio para interactuar con datos del MIO (Metro de Cali)
    Puede obtener datos desde archivos locales o API externa
    """
    
    def __init__(self):
        """Inicializa el servicio MIO"""
        self.data_path = Path(os.path.dirname(os.path.dirname(__file__))) / 'data'
        self.rutas_file = self.data_path / 'rutas_mio.json'
        self.paradas_file = self.data_path / 'paradas_mio.json'
        
        # URLs de API externas (si se requiere)
        self.api_rutas_url = os.environ.get('API_RUTAS_MIO', '')
        self.api_paradas_url = os.environ.get('API_PARADAS_MIO', '')
    
    def obtener_rutas(self, source='local'):
        """
        Obtener rutas del MIO.
        
        Args:
            source: Fuente de datos ('local' o 'api')
            
        Returns:
            Lista de diccionarios con datos de rutas
        """
        if source == 'api' and self.api_rutas_url:
            return self._obtener_rutas_api()
        else:
            return self._obtener_rutas_local()
    
    def obtener_paradas(self, source='local'):
        """
        Obtener paradas del MIO.
        
        Args:
            source: Fuente de datos ('local' o 'api')
            
        Returns:
            Lista de diccionarios con datos de paradas
        """
        if source == 'api' and self.api_paradas_url:
            return self._obtener_paradas_api()
        else:
            return self._obtener_paradas_local()
    
    def _obtener_rutas_local(self):
        """Obtiene rutas desde archivo JSON local"""
        try:
            if self.rutas_file.exists():
                with open(self.rutas_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                current_app.logger.warning(f"Archivo de rutas no encontrado en {self.rutas_file}")
                return []
        except Exception as e:
            current_app.logger.error(f"Error al leer rutas locales: {e}")
            return []
    
    def _obtener_paradas_local(self):
        """Obtiene paradas desde archivo JSON local"""
        try:
            if self.paradas_file.exists():
                with open(self.paradas_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                current_app.logger.warning(f"Archivo de paradas no encontrado en {self.paradas_file}")
                return []
        except Exception as e:
            current_app.logger.error(f"Error al leer paradas locales: {e}")
            return []
    
    def _obtener_rutas_api(self):
        """Obtiene rutas desde API externa"""
        try:
            response = requests.get(self.api_rutas_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            current_app.logger.error(f"Error al obtener rutas de la API: {e}")
            return []
    
    def _obtener_paradas_api(self):
        """Obtiene paradas desde API externa"""
        try:
            response = requests.get(self.api_paradas_url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            current_app.logger.error(f"Error al obtener paradas de la API: {e}")
            return []
    
    def crear_archivo_rutas_local(self, rutas):
        """Guarda rutas en archivo JSON local"""
        try:
            self.data_path.mkdir(exist_ok=True, parents=True)
            with open(self.rutas_file, 'w', encoding='utf-8') as f:
                json.dump(rutas, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            current_app.logger.error(f"Error al guardar rutas locales: {e}")
            return False
    
    def crear_archivo_paradas_local(self, paradas):
        """Guarda paradas en archivo JSON local"""
        try:
            self.data_path.mkdir(exist_ok=True, parents=True)
            with open(self.paradas_file, 'w', encoding='utf-8') as f:
                json.dump(paradas, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            current_app.logger.error(f"Error al guardar paradas locales: {e}")
            return False

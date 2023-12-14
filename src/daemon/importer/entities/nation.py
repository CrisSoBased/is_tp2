import xml.etree.ElementTree as ET
import requests
import urllib.parse

class Nation:
    counter = 0

    def __init__(self, name):
        Nation.counter += 1
        self._id = Nation.counter
        self._name = name
        self._lat = None
        self._lon = None

    def set_geoloc(self, lat, lon):
        self._lat = lat
        self._lon = lon

    def get_geoloc(self, country):
        if country.lower() == 'korea dpr':
            return [0, 0]  # Retorna coordenadas padrão para Korea
        else:
            location = country
            # Remova a barra do final da URL
            url = 'https://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(location) + '&format=json'

            try:
                response = requests.get(url)
                response.raise_for_status()  # Verifica se a resposta da solicitação foi bem-sucedida

                geolocation = response.json()

                if geolocation:
                    return [
                        geolocation[0]['lat'],
                        geolocation[0]['lon']
                    ]
                else:
                    print(f"Geolocalização não encontrada para {country}")
                    return [0, 0]  # Retornar coordenadas padrão ou outra abordagem que fizer sentido

            except requests.exceptions.RequestException as e:
                print(f"Erro na solicitação de geolocalização: {e}")
                return [0, 0]  # Retornar coordenadas padrão ou outra abordagem que fizer sentido

    def to_xml(self):
        
        el = ET.Element("Nation")
        el.set("id", str(self._id))
        el.set("name", self._name)
        el.set("lat", str(self._lat))
        el.set("lon", str(self._lon))
        return el
    
    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def __str__(self):
        return f"name: {self._name}, id: {self._id}, lat: {self._lat}, lon: {self._lon}"

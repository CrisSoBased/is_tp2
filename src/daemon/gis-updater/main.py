import sys
import time
import psycopg2
from pip._vendor import requests
import urllib.parse
POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60
ENTITIES_PER_ITERATION = int(sys.argv[2]) if len(sys.argv) >= 3 else 10


def get_data(nation):
        if nation.lower() == 'korea dpr':
            return [0, 0]  # Retorna coordenadas padrão para Korea
        else:
            location = nation
            # Remova a barra do final da URL
            url = 'https://nominatim.openstreetmap.org/search?q=' + urllib.parse.quote(location) + '&format=json'

            try:
                response = requests.get(url)
                response.raise_for_status()  # Verifica se a resposta da solicitação foi bem-sucedida

                geolocation = response.json()

                if geolocation:
                    return [
                        geolocation[0],
                        geolocation[0]
                    ]
                else:
                    print(f"Geolocalização não encontrada para {nation}")
                    return [0, 0]  # Retornar coordenadas padrão ou outra abordagem que fizer sentido

            except requests.exceptions.RequestException as e:
                print(f"Erro na solicitação de geolocalização: {e}")
                return [0, 0]  # Retornar coordenadas padrão ou outra abordagem que fizer sentido

if __name__ == "__main__":

    while True:
        print(f"Getting up to {ENTITIES_PER_ITERATION} entities without coordinates...")
        # !TODO: 1- Use api-gis two retrieve a fixed amount of entities without coordinates (e.g. 100 entities per iteration, use ENTITIES_PER_ITERATION)
        # Connect to the database
        connection = psycopg2.connect(user="is", password="is", host="db-rel", database="is")

        # Create a cursor to execute queries
        cur = connection.cursor()

        cur.execute(f"select id,name from nation where coordinates is null LIMIT {ENTITIES_PER_ITERATION}")

        nations = cur.fetchall()

        # !TODO: 2- Use the entity information to retrieve coordinates from an external API

        for id, name in nations:
            coordinates = get_data(name)

            # Assuming coordinates is a list of dictionaries
            lon = coordinates[0].get('lon', None)
            lat = coordinates[0].get('lat', None)

            if lon is not None and lat is not None:
                # Update the database query
                query = f"UPDATE nation SET coordinates = ST_SetSRID(ST_MakePoint({str(lon)}, {str(lat)}), 4326) WHERE id = '{id}'"
                cur.execute(query)
            else:
                print("Invalid coordinates format: 'lon' and 'lat' keys are missing.")


        # !TODO: 3- Submit the changes

        connection.commit()

        cur.close()
        connection.close()
        time.sleep(POLLING_FREQ)
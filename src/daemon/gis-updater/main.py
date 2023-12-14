import sys
import time
import psycopg2
from pip._vendor import requests
import urllib.parse
POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60
ENTITIES_PER_ITERATION = int(sys.argv[2]) if len(sys.argv) >= 3 else 10


def get_data(country):
    if country.lower() == 'korea dpr':
            return [0, 0]
    else:
        address = country
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '&format=json'

        coordinates = requests.get(url).json()

        return [
            coordinates[0]["lat"],
            coordinates[0]["lon"]
        ]

if __name__ == "__main__":

    while True:
        print(f"Getting up to {ENTITIES_PER_ITERATION} entities without coordinates...")
        # !TODO: 1- Use api-gis two retrieve a fixed amount of entities without coordinates (e.g. 100 entities per iteration, use ENTITIES_PER_ITERATION)
        # Connect to the database
        connection = psycopg2.connect(user="is", password="is", host="db-rel", database="is")

        # Create a cursor to execute queries
        cur = connection.cursor()

        cur.execute(f"select id,name from countries where geom is null LIMIT {ENTITIES_PER_ITERATION}")

        countries = cur.fetchall()

        # !TODO: 2- Use the entity information to retrieve coordinates from an external API

        for id,name in countries:
            coordinates = get_data(name)

            cur.execute(f"update nation set geom = ST_SetRID(ST_MakePoint({coordinates[0]['lon']},"
                        " {coordinates[0]['lat']}), 4326) where id = {id}")


        # !TODO: 3- Submit the changes

        connection.commit()

        cur.close()
        connection.close()
        time.sleep(POLLING_FREQ)

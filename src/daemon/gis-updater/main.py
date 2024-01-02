import sys
import time
import psycopg2
from pip._vendor import requests
import urllib.parse
import pika
import json
import logging


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
                response.raise_for_status()  #   Verifica se a resposta da solicitação foi bem-sucedida

                geolocation = response.json()

                if geolocation:
                    return [
                        geolocation[0]['lat'],
                        geolocation[0]['lon']
                    ]
                
                else:
                    print(f"Geolocalização não encontrada para {nation}")
                    return [0, 0]  # Retornar coordenadas padrão ou outra abordagem que fizer sentido

            except requests.exceptions.RequestException as e:
                print(f"Erro na solicitação de geolocalização: {e}")
                return [0, 0]  # Retornar coordenadas padrão ou outra abordagem que fizer sentido



rabbitmq_url = "amqp://is:is@rabbitmq:5672/is"
update_queue_name = "update_coor"
tile_api_url = "http://api-gis:8080/api/tile"

logging.basicConfig(level=logging.INFO)

def testapi(): 
    try:
        response = requests.get(tile_api_url)
        response.raise_for_status()
        logging.info(f"Request to {tile_api_url} successful. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error making request to {tile_api_url}: {e}")
        raise  # Re-raise a exceção para que o chamador saiba que algo deu errado



MAX_RETRIES = 5

def callback(ch, method, properties, body):
    try:
        json_data = json.loads(body.decode('utf-8'))
        print(f"Received message: {json_data}")

        id_nation = None
        retries = 0

        while retries < MAX_RETRIES:
            id_nation = get_id_nation_prop(json_data['id_nation'])

            if id_nation is not None:
                break  # Sai do loop se obteve o resultado

            retries += 1
            time.sleep(5)  # Aguarda 5 segundos antes de tentar novamente

        if id_nation is None:
            print(f"Max retries reached for {json_data['id_nation']}. Skipping to the next task.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        print(f"Match found: {json_data['id_nation']}")

        # Verifica se o campo 'coordinates' está presente e não é nulo
        if 'coordinates' in id_nation and id_nation['coordinates']:
            # só mete a passar, pode passar logo para a próxima task
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        else:
            # Se 'coordinates' está ausente ou nulo, chama a função send_to_new_api
            print("Coordinates empty/null, calling send_to_new_api function")
            send_to_new_api(id_nation['id'])

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON message: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def get_id_nation_prop(id_nation):
    try:
        # Fazer uma solicitação à API para obter as informações da nação
        response = requests.get(f"http://api-gis:8080/api/nationProp/{id_nation}")
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error making request to /api/nationProp/{id_nation}: {e}")
        return None



def send_to_new_api(id_country):
    try:
        url = f"http://api-gis:8080/api/entity/{id_country}"
        response = requests.patch(url)
        response.raise_for_status()
        print(f"Request to {url} successful. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {url}: {e}")
        raise


if __name__ == "__main__":
    while True:
        try:
            connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
            channel = connection.channel()

            channel.queue_declare(queue=update_queue_name, durable=True)
            print(f"Waiting for messages from the '{update_queue_name}' queue. To exit press CTRL+C")

            channel.basic_consume(queue=update_queue_name, on_message_callback=callback)

            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            print(f"AMQP Connection Error: {e}. Retrying in 10 seconds.")
            time.sleep(10)
        except KeyboardInterrupt:
            print("Exiting...")
            break
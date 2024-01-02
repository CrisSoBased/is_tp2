import sys, psycopg2
from flask_cors import CORS
from flask import Flask, request, make_response, jsonify
from pip._vendor import requests
import urllib.parse
PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True



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


@app.route('/api/nationProp/<name>', methods=['GET'])
def get_id_nation_prop(name):
    try:
        # Conectar ao banco de dados usando um gerenciador de contexto
        with psycopg2.connect(user="is", password="is", host="db-rel", database="is") as connection:
            with connection.cursor() as cur:
                # Executar a consulta no banco de dados
                query = "SELECT id, ST_AsGeoJSON(coordinates)::json AS coordinates FROM nation WHERE name = %s"
                cur.execute(query, (name,))

                # Obter o resultado da consulta
                result = cur.fetchone()

                if result:
                    # Se houver resultados, retornar o ID e as coordenadas em formato JSON
                    return jsonify({"id": result[0], "coordinates": result[1]})
                else:
                    # Se não houver correspondência, retornar um JSON indicando que não foi encontrado
                    return jsonify({"error": "Nation not found"}), 404

    except Exception as e:
        # Lidar com exceções e retornar um JSON indicando o erro
        return jsonify({"error": f"Error retrieving nation ID: {str(e)}"}), 500
    
    

@app.route('/api/tile', methods=['GET'])
def get_markers():
    ne_lat = request.args.get('neLat')
    ne_lng = request.args.get('neLng')
    sw_lat = request.args.get('swLat')
    sw_lng = request.args.get('swLng')

    # Connect to database
    connection = psycopg2.connect(user="is", password="is", host="db-rel", database="is")

    cur = connection.cursor()

    # Construir a consulta dinamicamente com base nos parâmetros
    if ne_lat is None or ne_lng is None or sw_lat is None or sw_lng is None:
        query = "SELECT id, name, ST_AsGeoJSON(coordinates)::json AS coordinates FROM nation"
        cur.execute(query)
    else:
        query = "SELECT id, name, ST_AsGeoJSON(coordinates)::json AS coordinates FROM nation " \
                "WHERE coordinates && ST_MakeEnvelope(%s, %s, %s, %s)"
        cur.execute(query, (sw_lng, sw_lat, ne_lng, ne_lat))

    markers = []

    for row in cur:
        markers.append({
            "type": "Feature",
            "id": row[0],
            "geometry": row[2],
            "properties": {
                "id": row[0],
                "name": row[1]
            }
        })

    print(markers)

    cur.close()
    connection.close()

    response = make_response(jsonify(markers))

    return response

def get_nation_name_by_id(id_nation):
    try:
        # Conectar ao banco de dados
        connection = psycopg2.connect(user="is", password="is", host="db-rel", database="is")
        cur = connection.cursor()

        # Executar a consulta no banco de dados
        query = "SELECT name FROM nation WHERE id = %s"
        cur.execute(query, (id_nation,))


        # Obter o resultado da consulta
        nation_name = cur.fetchone()[0]  # Assumindo que sempre haverá uma correspondência

        # Fechar conexão
        cur.close()
        connection.close()

        return nation_name

    except Exception as e:
        print(f"Erro durante a consulta ao banco de dados: {str(e)}")
        return "Erro no banco de dados"  # Valor padrão em caso de erro


@app.route('/api/entity/<id>', methods=['PATCH'])
def update_entity(id):
    try:
        
       
        nation_name = get_nation_name_by_id(id)

    
        # Extrair coordenadas do JSON
        coordinates = get_data(nation_name)

        if not coordinates:
            return jsonify({"error": "Coordenadas ausentes no JSON"}), 400

        # Conectar ao banco de dados
        connection = psycopg2.connect(user="is", password="is", host="db-rel", database="is")
        cur = connection.cursor()

        # Executar a atualização no banco de dados
        query = f"UPDATE nation SET coordinates = ST_SetSRID(ST_MakePoint({coordinates[0]}, {coordinates[1]}), 4326) WHERE id = '{id}'"
        cur.execute(query)
        connection.commit()

        # Fechar conexão
        cur.close()
        connection.close()

        return jsonify({"message": f"Coordenadas da entidade {id} atualizadas com sucesso"})

    except Exception as e:
        return jsonify({"error": f"Erro durante a atualização das coordenadas da entidade: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)

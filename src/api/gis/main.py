import sys, psycopg2
from flask_cors import CORS
from flask import Flask, request, make_response, jsonify

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


@app.route('/api/tile', methods=['GET'])
def get_markers():
    ne_lat = request.args.get('neLat')
    ne_lng = request.args.get('neLng')
    sw_lat = request.args.get('swLat')
    sw_lng = request.args.get('swLng')

    # Connect to database
    connection = psycopg2.connect(user="is", password="is", host="db-rel", database="is")

    cur = connection.cursor()

    cur.execute("SELECT id, name, ST_AsGeoJSON(coordinates)::json AS coordinates FROM nation "
            "WHERE coordinates && ST_MakeEnvelope(%s, %s, %s, %s)", (ne_lng, ne_lat, sw_lng, sw_lat))
    
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

@app.route('/api/entity/<id>', methods=['PATCH'])
def update_entity(id, data):
    try:
        # Retrieve JSON data from the request
        data = request.get_json()

        # Extract lon and lat from the JSON data
        lon = data.get('lon', None)
        lat = data.get('lat', None)

        # Conectar ao banco de dados
        connection = psycopg2.connect(user="is", password="is", host="db-rel", database="is")
        cur = connection.cursor()

        # Executar a atualização no banco de dados
        query = f"UPDATE nation SET coordinates = ST_SetSRID(ST_MakePoint({str(lon)}, {str(lat)}), 4326) WHERE id = '{id}'"
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

import sys, psycopg2
from flask import Flask, request, make_response, jsonify

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/markers', methods=['GET'])
def get_markers():
    args = request.args
    neLng = args.get('neLng')
    neLat = args.get('neLat')
    swLng = args.get('swLng')
    swLat = args.get('swLat')

    # Connect to database
    connection = psycopg2.connect(user="is", password="is", host="db-rel", database="is")

    cur = connection.cursor()

    cur.execute("SELECT id, name, ST_Y(coordinates) as latitude, ST_X(coordinates) as longitude FROM nation "
            "WHERE coordinates && ST_MakeEnvelope(%s, %s, %s, %s)", (neLng, neLat, swLng, swLat))
    
    markers = []

    for row in cur:
        markers.append({
            "type": "feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row[2], row[3]]
            },
            "properties": {
                "id": row[0],
                "name": row[1],
                "imgUrl" : "https://cdn-icons-png.flaticon.com/512/535/535239.png"
            }
        })

    print(markers)

    cur.close()
    connection.close()

    response = make_response(jsonify(markers))

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)

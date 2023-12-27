import sys
import xmlrpc.client

from flask import Flask, jsonify, request
PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True

# clubs
@app.route('/api/clubs', methods=['GET'])
def get_clubs():
    print("connecting to server...")
    server = xmlrpc.client.ServerProxy("http://rpc-server:9000")
    result = server.fetch_clubs()
    return jsonify(result)

# players from portugal
@app.route('/api/players_from_portugal', methods=['GET'])
def get_players_from_portugal():
    print("connecting to server...")
    server = xmlrpc.client.ServerProxy("http://rpc-server:9000")
    result = server.fetch_all_players_from_portugal()
    return jsonify(result)


# players CM from france
@app.route('/api/players_cm_from_france', methods=['GET'])
def get_players_cm_from_france():

    print("connecting to server...")
    server = xmlrpc.client.ServerProxy("http://rpc-server:9000")
    result = server.fetch_all_players_CM_from_france()
    return jsonify(result)

# players by nation
@app.route('/api/players_by_nation', methods=['GET'])
def get_players_by_nation():
    nation = request.args.get('nation')

    print("connecting to server...")
    server = xmlrpc.client.ServerProxy("http://rpc-server:9000")
    result = server.fetch_all_players_by_nation(nation)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
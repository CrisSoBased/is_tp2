import signal, sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.string_length import string_length
from functions.string_reverse import string_reverse
from functions.database import fetch_clubs
from functions.database import fetch_all_players_from_portugal
from functions.database import fetch_all_players_CM_from_france
from functions.database import fetch_all_players_by_nation



PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

if __name__ == "__main__":
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    with SimpleXMLRPCServer(('0.0.0.0', PORT), requestHandler=RequestHandler) as server:
        server.register_introspection_functions()

        def signal_handler(signum, frame):
            print("received signal")
            server.server_close()

            # perform clean up, etc. here...
            print("exiting, gracefully")
            sys.exit(0)  

        # signals
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        # register both functions
        server.register_function(string_reverse)
        server.register_function(string_length)
        server.register_function(fetch_clubs)
        server.register_function(fetch_all_players_from_portugal)
        server.register_function(fetch_all_players_CM_from_france)
        server.register_function(fetch_all_players_by_nation)


        # start the server
        print(f"Starting the RPC Server in port {PORT}...")
        server.serve_forever()

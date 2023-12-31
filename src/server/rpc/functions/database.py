import psycopg2

def db_connect():
    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-xml",
                                  database="is")
    return connection

def cursor_connect(connection):
    cursor = connection.cursor()

    return cursor

def fetch_clubs():
    try:
        connection = db_connect()

        cursor = cursor_connect(connection)

        ## Get the athletes names and id
        cursor.execute("""
        SELECT DISTINCT unnest(xpath('//Clubs/Club/@name', xml))::text as club
        FROM imported_documents
        ORDER BY club;
        """)

        results = cursor.fetchall()

        if connection:
            cursor.close()
            connection.close()

            return results
        
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)



def fetch_all_players_from_portugal():
    try:
        connection = db_connect()

        cursor = cursor_connect(connection)

        ## Get the athletes names and id
        cursor.execute("""
        SELECT DISTINCT unnest(xpath('//Nations/Nation[@name="Portugal"]/descendant::Player/@name', xml))::text as player_name
        FROM imported_documents
        ORDER BY player_name;
        """)

        results = cursor.fetchall()

        if connection:
            cursor.close()
            connection.close()

            return results
        
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)



def fetch_all_players_CM_from_france():
    try:
        connection = db_connect()

        cursor = cursor_connect(connection)

        ## Get the athletes names and id
        cursor.execute("""
        SELECT DISTINCT unnest(xpath('//Nations/Nation[@name="France"]/descendant::Player[@position="CM"]/@name', xml))::text as player_name
        FROM imported_documents
        ORDER BY player_name;
        """)

        results = cursor.fetchall()

        if connection:
            cursor.close()
            connection.close()

            return results
        
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)



def fetch_all_players_by_nation(nation):
    try:
        connection = db_connect()
        cursor = cursor_connect(connection)

        # Use o valor do parâmetro nation na consulta
        query = """
        SELECT DISTINCT unnest(xpath('//Nations/Nation[@name="%s"]/descendant::Player/@name', xml))::text as player_name
        FROM imported_documents
        ORDER BY player_name;
        """ % nation

        cursor.execute(query)

        results = cursor.fetchall()

        if connection:
            cursor.close()
            connection.close()

            return results

    except Exception as e:
        # Trate a exceção conforme necessário
        return {"error": str(e)}







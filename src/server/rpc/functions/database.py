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
        SELECT
            xpath('//Player/@name', player_xml)::text AS player_name,
            xpath('//Player/@position', player_xml)::text AS player_position,
            xpath('//Player/@overall', player_xml)::text AS player_overall,
            xpath('//Player/@club', player_xml)::text AS player_club,
            xpath('//Player/@age', player_xml)::text AS player_age,
            xpath('//Player/@url', player_xml)::text AS player_url
        FROM
            imported_documents,
            unnest(xpath('//Country[@name="Portugal"]/Players/Player', xml)) AS player_xml
        WHERE
            xpath('//Country[@name="Portugal"]', xml) IS NOT NULL
        ORDER BY
            player_name;
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
        SELECT
            xpath('//Country/@name', xml)::text AS country_name,
            xpath('//Player/@name', player_xml)::text AS player_name,
            xpath('//Player/@position', player_xml)::text AS player_position,
            xpath('//Player/@overall', player_xml)::text AS player_overall,
            xpath('//Player/@club', player_xml)::text AS player_club,
            xpath('//Player/@age', player_xml)::text AS player_age,
            xpath('//Player/@url', player_xml)::text AS player_url
        FROM
            imported_documents,
            unnest(xpath('//Country[@name="France" and Players/Player/@position="CM"]/Players/Player', xml)) AS player_xml
        WHERE
            xpath('//Country[@name="France"]', xml) IS NOT NULL
        ORDER BY
            country_name, player_name;
        """)

        results = cursor.fetchall()

        if connection:
            cursor.close()
            connection.close()

            return results
        
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)



def fetch_all_players_by_nation():
    try:
        connection = db_connect()

        cursor = cursor_connect(connection)

        ## Get the athletes names and id
        cursor.execute("""
        SELECT
            xpath('//Player/@name', player_xml)::text AS player_name,
            xpath('//Player/@position', player_xml)::text AS player_position,
            xpath('//Player/@overall', player_xml)::text AS player_overall,
            xpath('//Player/@club', player_xml)::text AS player_club,
            xpath('//Player/@age', player_xml)::text AS player_age,
            xpath('//Player/@url', player_xml)::text AS player_url
        FROM
            imported_documents,
            unnest(xpath('//Country[@name="{}"]/Players/Player', xml)) AS player_xml
        WHERE
            xpath('//Country[@name="{}"]', xml) IS NOT NULL
        ORDER BY
            player_name;
        """)

        results = cursor.fetchall()

        if connection:
            cursor.close()
            connection.close()

            return results
        
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch data", error)
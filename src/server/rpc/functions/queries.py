from functions.database import Database

class Queries:
    def __init__(self):
        self.database = Database()

    def _execute_query(self, query, data):
        try:
            result = self.database.selectOne(query, data)
            return result
        finally:
            # Não é necessário chamar disconnect aqui, pois já está sendo tratado na classe Database
            pass

    def fetch_clubs(self):
        database = Database()
        query = """
        SELECT DISTINCT unnest(xpath('//Clubs/Club/@name', xml))::text as club
        FROM imported_documents
        ORDER BY club;
        """

        results = database.selectAll(query)
        database.disconnect()

        formatted_clubs = [f"● {club}" for club in results]

        return formatted_clubs

    def fetch_all_players_from_portugal(self):
        database = Database()

        
        query = """
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
        """

        results = database.selectAll(query)
        database.disconnect()

        formatted_players = [
            {
                "name": player[0],
                "position": player[1],
                "overall": player[2],
                "club": player[3],
                "age": player[4],
                "url": player[5]
            } for player in results
        ]

        return formatted_players

    def fetch_all_players_CM_from_france(self):
        database = Database()

        query = """
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
        """

        results = database.selectAll(query)
        database.disconnect()

        formatted_players = [
            {
                "name": player[0],
                "position": player[1],
                "overall": player[2],
                "club": player[3],
                "age": player[4],
                "url": player[5]
            } for player in results
        ]

        return formatted_players
    
    def fetch_all_players_by_country(self, country):
        database = Database()
        
        query =  """
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
        """.format(country, country)

        results = database.selectAll(query)
        database.disconnect()
        
        formatted_players = [
            {
                "name": player[0],
                "position": player[1],
                "overall": player[2],
                "club": player[3],
                "age": player[4],
                "url": player[5]
            } for player in results
        ]

        return formatted_players

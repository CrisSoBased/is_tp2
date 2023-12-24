import psycopg2

class DBAccessMigrator:
    def connect_connection_xml(self):
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="db-xml", #host="localhost",
                                      #port="5432",
                                      database="is")
        return connection

    def connect_connection_rel(self):
        connection = psycopg2.connect(user="is",
                                      password="is",
                                      host="db-rel",  # host="localhost",
                                      # port="5432",
                                      database="is")
        return connection

    def connect_cursor(self,connection):
        cursor = connection.cursor()

        return cursor

    def nations_to_store(self):
        nations = None
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_xml()

            cursor = self.connect_cursor(connection)

            # Mudar
            cursor.execute(
                "select unnest(xpath('/Olympics/Countries/Country/@id', xml)::text[]) as id, "
                "unnest(xpath('/Olympics/Countries/Country/@name', xml)::text[]) as country_name, "
                "unnest(xpath('/Olympics/Countries/Country/@lat', xml)::text[]) as lat, "
                "unnest(xpath('/Olympics/Countries/Country/@lon', xml)::text[]) as lon "
                "from imported_documents where file_name = '/shared/output/8ec816ba-77e5-4b53-8529-87e8026794f6.xml' "
                "order by country_name;")

            nations = cursor.fetchall()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                return nations


    def clubs_to_store(self):
        clubs = None
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_xml()

            cursor = self.connect_cursor(connection)

            # Mudar
            cursor.execute(
                "select unnest(xpath('/Olympics/Competitions/Competition/@year', xml)::text[]) as year, "
                "unnest(xpath('/Olympics/Competitions/Competition/@city', xml)::text[]) as city "
                "from imported_documents where file_name = '/shared/output/8ec816ba-77e5-4b53-8529-87e8026794f6.xml' "
                "order by year;")

            clubs = cursor.fetchall()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                return clubs


    def players_to_store(self):
        players = None
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_xml()

            cursor = self.connect_cursor(connection)

            # Mudar
            cursor.execute(
                "select unnest(xpath('/Olympics/Athletes/Athlete/@id', xml)::text[]) as id, "
                "unnest(xpath('/Olympics/Athletes/Athlete/@name', xml)::text[]) as name, "
                "unnest(xpath('/Olympics/Athletes/Athlete/@gender', xml)::text[]) as gender, "
                "unnest(xpath('/Olympics/Athletes/Athlete/@country_ref', xml)::text[]) as country "
                "from imported_documents where file_name = '/shared/output/8ec816ba-77e5-4b53-8529-87e8026794f6.xml' "
                "order by name;")

            players = cursor.fetchall()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                return players

    def insert_clubs(self, clubs):
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_rel()

            cursor = self.connect_cursor(connection)

            # Values to be inserted
            values_to_insert = []

            # Append the values we want to insert
            for club in clubs:
                values_to_insert.append((club[0]))

            # Iterate over the values and construct and execute an INSERT statement for each value
            for values in values_to_insert:
                query = "INSERT INTO clubs (name) VALUES (%s)"
                cursor.execute(query, values)

            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()


    def insert_nations(self, nations):
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_rel()

            cursor = self.connect_cursor(connection)

            # Values to be inserted
            values_to_insert = []

            # Append the values we want to insert
            for nation in nations:
                values_to_insert.append((nation[0], nation[1]))
            # Iterate over the values and construct and execute an INSERT statement for each value
            for values in values_to_insert:
                query = "INSERT INTO nations (name) VALUES (%s)"
                cursor.execute(query, values)

            connection.commit()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()


    def insert_players(self, players, nations):
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_rel()

            cursor = self.connect_cursor(connection)

            # Values to be inserted
            values_to_insert = []


            # Append the values we want to insert
            for player in players:
                player_club_uuid = self.get_player_club(player[0])
                player_nation_uuid = self.get_player_nation(player[3])

                if player_nation_uuid is not None and player_club_uuid is not None:
                    values_to_insert.append((player[1],player[2],player_club_uuid[0], player_nation_uuid[0]))

            # Iterate over the values and construct and execute an INSERT statement for each value
            for values in values_to_insert:
                query = "INSERT INTO players (name, gender, competitions_id, country_id) VALUES (%s, %s, %s, %s)"

                cursor.execute(query, values)
            connection.commit()

            print("DONE!!!!")

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data2", error)

        finally:
            if connection:
                cursor.close()
                connection.close()

    def get_player_nation(self, player_nation):
        nation_uuid = None
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_rel()

            cursor = self.connect_cursor(connection)

            query = f"Select id from nations where acronym = '{player_nation}'" 
            cursor.execute(query)

            nation_uuid = cursor.fetchone()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                return nation_uuid


    def get_player_club(self, player_id):
        competition_uuid = None
        connection = None
        cursor = None

        try:
            connection = self.connect_connection_xml()

            cursor = self.connect_cursor(connection)

            query = f"select unnest(xpath('//Olympics/Competitions/Competition[Event/Medals/Medal[@athlete_ref={player_id}]]/@year', xml)::text[]) as year " \
                    f"from imported_documents where file_name = '/shared/output/8ec816ba-77e5-4b53-8529-87e8026794f6.xml' " \
                    f"order by year;"
            cursor.execute(query)
            result = cursor.fetchone()

            competition_uuid = cursor.fetchone()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data athelte competition", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                return competition_uuid


    def get_club_uuid(self):
        club_uuid = None

        connection = None
        cursor = None

        try:
            connection = self.connect_connection_rel()

            cursor = self.connect_cursor(connection)

            query = f"Select id from club"
            cursor.execute(query)

            club_uuid = cursor.fetchone()

        except (Exception, psycopg2.Error) as error:
            print("Failed to fetch data", error)

        finally:
            if connection:
                cursor.close()
                connection.close()
                return club_uuid
import psycopg2

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.user = "is"
        self.password = "is"
        self.host = "is-db"
        self.port = "5432"
        self.database = "is"

    def connect(self):
        if self.connection is None:
            try:
                self.connection = psycopg2.connect(
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port,
                    database=self.database
                )
                self.cursor = self.connection.cursor()
                print("\nConnection established successfully.")
            except psycopg2.Error as error:
                print(f"\nError: {error}")

    def disconnect(self):
        if self.connection:
            try:
                self.cursor.close()
                self.connection.close()
                print("\nDisconnected successfully from the database.")
            except psycopg2.Error as e:
                print(f"\nError: {e}")

    def insert(self, sql_query, data):
        self.connect()
        try:
            self.cursor.execute(sql_query, data)
            self.connection.commit()
            print("\nThe query was successfully executed.")
        except psycopg2.Error as error:
            print(f"\nError: {error}")   


    def selectAll(self, query):
        self.connect()
        with self.cursor as cursor:
            cursor.execute(query)
            result = [row for row in cursor.fetchall()]
        return result

    def selectOne(self, query, data):
        self.connect()
        with self.cursor as cursor:
            cursor.execute(query, data)
            result = cursor.fetchone()
        return result

    def selectAllDict(self, query, data=None):
        self.connect()
        with self.cursor as cursor:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)

            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    
    def selectOneWithoutData(self, query):
        self.connect()
        with self.cursor as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        return result
import sys
import time

import psycopg2
from psycopg2 import OperationalError
from migrator.db_access import DBAccessMigrator

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60


def print_psycopg2_exception(ex):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", ex, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", ex.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", ex.pgerror)
    print("pgcode:", ex.pgcode, "\n")


if __name__ == "__main__":

    db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

    while True:

        # Connect to both databases
        db_org = None
        db_dst = None

        try:
            db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
            db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None or db_org is None:
            continue

        db_access_migrator = DBAccessMigrator
        print("Checking updates...")
        # !TODO: 1- Execute a SELECT query to check for any changes on the table
        cursor_org = db_dst.cursor()
        changes = cursor_org.execute("select * from imported_documents where is_migrated=0")


        # !TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db
        players_data = db_access_migrator.players_to_store()
        print("Players to store:")
        for player in players_data:
            print("Id:", player[0], "Name:", player[1], "Gender:", player[2], "Nation:", player[3])

        nations_data = db_access_migrator.nations_to_store()
        print("Nations data to store:")
        for nation in nations_data:
            print("Id:",nation[0],"Name:", nation[1])

        competitions_data = db_access_migrator.competitions_to_store()
        print("Competitions to store:")
        for competition in competitions_data:
            print("Year:", competition[0], "City:", competition[1])
        # !TODO: 3- Execute INSERT queries in the destination db
        # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
        #          Change the db structure if needed.

        cursor_org = db_dst.cursor()
        cursor_org.execute("UPDATE imported_documents SET is_migrated = 1")

        db_org.close()
        db_dst.close()

        time.sleep(POLLING_FREQ)
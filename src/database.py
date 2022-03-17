from util import connection as bd
from util import insertion_tables as insertion

if __name__ == '__main__':
    global conn
    global cursor

    bd.execute_file("scripts/creation_table.sql")
    insertion.insert_donnees()

    conn, cursor = bd.open_connection()
#allo
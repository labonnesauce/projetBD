from util import connection as bd;

if __name__ == '__main__':
    global connection
    global cursor

    bd.execute_file("scripts/creation_bd.sql")
    bd.execute_file("scripts/creation_table.sql");

    connection, cursor = bd.open_connection()

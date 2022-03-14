import pymysql


def open_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        db="glo_2005_webapp",
        password="Joblo007",
        autocommit=True
    )

    cursor = connection.cursor();

    return connection, cursor


def close_connection_and_cursor(connection, cursor):
    connection.close()
    cursor.close()


def execute_file(path):
    file = open(path, 'r', encoding="utf-8")

    connection, cursor = open_connection()
    listCommands = file.read().split(';')
    for command in listCommands[:-1]:
        cursor.execute(command)

    close_connection_and_cursor(connection, cursor)

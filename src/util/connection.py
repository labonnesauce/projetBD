import pymysql


def open_connection():
    connection = pymysql.connect(
        host="localhost",
        user="newUser",
        db="projet_glo2005",
        password="newUserPassword",
        autocommit=True,
        charset='utf8',
        use_unicode=True
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


def execute_commande_bd(requete, fetchOne):
    conn, cursor = open_connection()
    cursor.execute(requete)

    if fetchOne:
        data = cursor.fetchone()
    else:
        data = cursor.fetchall()
    return data


def execute_sans_resultat(requete):
    conn, cursor = open_connection()
    cursor.execute(requete)

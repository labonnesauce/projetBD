import pymysql.cursors

connection = pymysql.connect(
    host="localhost", user="root", password="VOTRE MOT DE PASSE ICI", db="glo_2005_webapp", autocommit=True)

cursor = connection.cursor()


def insert_todo(text):
    request = """INSERT INTO todo (text) VALUES ("{}");""".format(text)
    cursor.execute(request)


def select_todos():
    request = "SELECT text FROM todo;"
    cursor.execute(request)

    todos = [entry[0] for entry in cursor.fetchall()]

    return todos


if __name__ == '__main__':
    create_table = "CREATE TABLE todo(id integer AUTO_INCREMENT, text varchar(400), PRIMARY KEY(id))"
    cursor.execute(create_table)

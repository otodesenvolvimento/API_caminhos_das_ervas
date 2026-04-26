import sqlite3


def get_db():

    return sqlite3.connect("./sql/database.db")


def create_tables():
    with open("./sql/dump.sql", "r" ) as file:
        sql = file.read()

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.executescript(sql)
    except sqlite3.OperationalError as err:
        print(err)
    finally:
        cursor.close()        
            
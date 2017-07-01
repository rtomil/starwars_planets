import psycopg2
from psycopg2 import extras


def connect_to_DB():
    """Conects to my database. Yes my friend, i have a database."""
    # setup connection string
    connect_str = "dbname='starwars' user='richter' host='localhost' password='richter123ads'"
    # print(connect_str)
    try:
        return psycopg2.connect(connect_str)
    except:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print("or STFU I KNOW!")

if __name__ == '__main__':
    connect_to_DB()
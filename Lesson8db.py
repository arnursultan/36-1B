import psycopg

def get_connection():
    return psycopg.connect(
        dbname="database",
        user="Nursultan",
        password="123456",
        host="localhost",
        port="5433"
    )
import psycopg

def get_connection():
    return psycopg.connect(
        dbname="dbname",
        user="user",
        password="password",
        host="localhost",
        port="5433"
    )
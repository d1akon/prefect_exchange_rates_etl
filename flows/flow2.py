from prefect import flow, task
import psycopg2
from psycopg2 import sql

#----- Flujo de prueba que inserta un Hola Mundo en postgres

@task
def insert_into_postgres():
    conn = psycopg2.connect(
        dbname='mydatabase',
        user='postgres',
        password='postgres',
        host='postgres',
        port=5432
    )
    cur = conn.cursor()
    create_table_query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        )
    """)
    cur.execute(create_table_query)
    insert_query = sql.SQL("""
        INSERT INTO messages (content) VALUES (%s)
    """)
    cur.execute(insert_query, ("Hola Mundo desde Flow 2",))
    conn.commit()
    cur.close()
    conn.close()

@flow(name="Flow2")
def flow2():
    insert_into_postgres()

if __name__ == '__main__':
    flow2()

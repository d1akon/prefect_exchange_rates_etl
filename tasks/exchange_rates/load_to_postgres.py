#----- IMPORTS
from prefect import task
import psycopg2
from psycopg2 import sql

#----- TASKS | FUNCTIONS
@task
def load_to_postgres(df, postgres_config):
    """
    Load exchange rate data from a pandas DataFrame into a PostgreSQL database.

    This task ensures that the 'exchange_rates' table exists in the database,
    deletes any existing records for the same date and base currency, and inserts
    new records from the DataFrame.

    Parameters:
    df (pandas.DataFrame): A DataFrame containing exchange rate data with columns:
        'date', 'base_currency', 'target_currency', 'exchange_rate'.
    postgres_config (dict): A dictionary containing the PostgreSQL connection parameters:
        - 'dbname' (str): The name of the database.
        - 'user' (str): The PostgreSQL user.
        - 'password' (str): The password for the user.
        - 'host' (str): The host address of the PostgreSQL server.
        - 'port' (int or str): The port of the PostgreSQL server.

    Returns:
    None
        
    Raises:
    Exception: If there is an error during the connection, table creation, or data loading,
               the exception is raised after being logged.
    """
    date = df['date'].iloc[0]
    base_currency = df['base_currency'].iloc[0]

    try:
        conn = psycopg2.connect(
            dbname=postgres_config['dbname'],
            user=postgres_config['user'],
            password=postgres_config['password'],
            host=postgres_config['host'],
            port=postgres_config['port']
        )
        conn.autocommit = True

        with conn.cursor() as cursor:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS exchange_rates (
                date DATE,
                base_currency VARCHAR(10),
                target_currency VARCHAR(10),
                exchange_rate FLOAT,
                PRIMARY KEY (date, base_currency, target_currency)
            );
            """
            cursor.execute(create_table_query)
            print("Ensured exchange_rates table exists.")

        conn.autocommit = False

        with conn:
            with conn.cursor() as cursor:
                delete_query = """
                DELETE FROM exchange_rates WHERE date = %s AND base_currency = %s;
                """
                cursor.execute(delete_query, (date, base_currency))
                print(f"Deleted existing data for date {date} and base_currency {base_currency}.")

                insert_query = """
                INSERT INTO exchange_rates (date, base_currency, target_currency, exchange_rate)
                VALUES (%s, %s, %s, %s);
                """
                data_tuples = list(df.itertuples(index=False, name=None))
                cursor.executemany(insert_query, data_tuples)
                print(f"Loaded data into Postgres for date {date} and base_currency {base_currency}.")

    except Exception as e:
        print(f"An error occurred while loading data into Postgres: {e}")
        raise e
    finally:
        conn.close()

import os
import psycopg2
from minio import Minio
from minio.error import S3Error

#----- Testea la conexion con el servicio de postgres
def test_postgres_connection():
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB")
    )
    assert conn is not None
    conn.close()

#----- Testea la conexion con el servicio de minio
def test_minio_connection():
    try:
        #----- Configura el cliente de MinIO utilizando las variables de entorno
        client = Minio(
            endpoint=os.getenv("MINIO_ENDPOINT"),
            access_key=os.getenv("MINIO_ACCESS_KEY"),
            secret_key=os.getenv("MINIO_SECRET_KEY"),
            secure=False
        )
        
        #----- Intenta listar los buckets para verificar la conexión
        buckets = client.list_buckets()
        assert buckets is not None  # Si list_buckets devuelve algo, la conexión está OK
        print(f"MinIO connection successful. Found {len(buckets)} buckets.")
    
    except S3Error as e:
        #----- Si ocurre un error, la conexión falló
        assert False, f"Failed to connect to MinIO: {e}"
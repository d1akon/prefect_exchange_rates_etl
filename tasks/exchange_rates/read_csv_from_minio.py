#----- IMPORTS
from prefect import task
from minio import Minio
import pandas as pd
from io import BytesIO

#----- TASKS | FUNCTIONS
@task
def read_csv_from_minio(minio_config, csv_filename):

    """
    Read a CSV file from a MinIO object storage and load it into a pandas DataFrame.

    This task connects to a MinIO instance using the provided configuration, retrieves
    the specified CSV file from the given bucket, and reads its content into a pandas
    DataFrame.

    Parameters:
    minio_config (dict): A dictionary containing MinIO connection parameters:
                         - endpoint (str): The MinIO server URL.
                         - access_key (str): The access key for the MinIO instance.
                         - secret_key (str): The secret key for the MinIO instance.
                         - bucket_name (str): The name of the bucket where the CSV file is stored.
    csv_filename (str): The name of the CSV file to be retrieved from MinIO.

    Returns:
    pd.DataFrame: A DataFrame containing the content of the CSV file.

    Raises:
    Exception: If an error occurs while retrieving or reading the CSV file from MinIO.
    """

    client = Minio(
        endpoint=minio_config['endpoint'],
        access_key=minio_config['access_key'],
        secret_key=minio_config['secret_key'],
        secure=False
    )

    bucket_name = minio_config['bucket_name']
    response = client.get_object(bucket_name, csv_filename)
    df = pd.read_csv(BytesIO(response.read()))
    response.close()
    response.release_conn()
    print(f"Read {csv_filename} from MinIO.")
    return df

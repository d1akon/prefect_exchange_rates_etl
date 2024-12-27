#----- IMPORTS
from prefect import task
from minio import Minio
from io import BytesIO

#----- TASKS | FUNCTIONS
@task
def save_to_minio(df, date, minio_config):

    """
    Save a pandas DataFrame as a CSV file to a MinIO object storage.

    This task connects to a MinIO instance using the provided configuration, checks if the
    specified bucket exists (and creates it if necessary), and uploads the DataFrame as a CSV
    file into the bucket with a filename based on the provided date.

    Parameters:
    df (pd.DataFrame): The DataFrame to save as a CSV file.
    date (datetime): The date used to generate the filename for the CSV file.
    minio_config (dict): A dictionary containing MinIO connection parameters:
                         - endpoint (str): The MinIO server URL.
                         - access_key (str): The access key for the MinIO instance.
                         - secret_key (str): The secret key for the MinIO instance.
                         - bucket_name (str): The name of the bucket where the file will be saved.

    Returns:
    str: The name of the CSV file that was saved to MinIO.

    Raises:
    Exception: If an error occurs while saving the DataFrame to MinIO.
    """

    client = Minio(
        endpoint=minio_config['endpoint'],
        access_key=minio_config['access_key'],
        secret_key=minio_config['secret_key'],
        secure=False
    )

    bucket_name = minio_config['bucket_name']
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Created bucket '{bucket_name}' in MinIO.")

    csv_data = df.to_csv(index=False).encode('utf-8')
    csv_filename = f"exchange_rates_{date.strftime('%Y-%m-%d')}.csv"

    client.put_object(
        bucket_name=bucket_name,
        object_name=csv_filename,
        data=BytesIO(csv_data),
        length=len(csv_data),
        content_type='application/csv'
    )
    print(f"Saved {csv_filename} to MinIO.")
    return csv_filename

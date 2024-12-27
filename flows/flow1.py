from prefect import flow, task
import boto3

#----- Flujo de prueba que escribe un hola mundo en txt en minio

@task
def write_to_minio():
    s3_client = boto3.client(
        's3',
        endpoint_url='http://minio:9000',
        aws_access_key_id='admin',
        aws_secret_access_key='admin123',
    )
    bucket_name = 'mybucket'
    file_content = 'Hola Mundo desde Flow 1'
    file_name = 'hola_flow1.txt'
    s3_client.create_bucket(Bucket=bucket_name)
    s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
    return bucket_name, file_name

@flow(name="Flow1")
def flow1():
    write_to_minio()

if __name__ == '__main__':
    flow1()

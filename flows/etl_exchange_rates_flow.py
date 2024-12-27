#----- Imports generales
from prefect import flow, task
import os
import yaml
from datetime import datetime, timedelta
#----- Importando los tasks individuales
from tasks.exchange_rates.fetch_exchange_rates import fetch_exchange_rates
from tasks.exchange_rates.save_to_minio import save_to_minio
from tasks.exchange_rates.load_to_postgres import load_to_postgres
from tasks.exchange_rates.read_csv_from_minio import read_csv_from_minio

@flow(name="ETL Exchange Rates Flow")
def etl_exchange_rates_flow(start_date: str = None, end_date: str = None):
    # Cargar configuración
    with open('configs/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    #----- Si no se proporcionan fechas, se correrá para la fecha actual
    if not start_date:
        start_date = config.get('start_date', datetime.today().strftime('%Y-%m-%d'))
    if not end_date:
        end_date = config.get('end_date', datetime.today().strftime('%Y-%m-%d'))
    
    #----- Convertir las fechas a objetos datetime
    try:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Las fechas deben estar en formato YYYY-MM-DD")
    
    #----- Validar que start_date no sea posterior a end_date
    if start_date_obj > end_date_obj:
        raise ValueError("start_date no puede ser posterior a end_date")
    
    date_range = [start_date_obj + timedelta(days=x) for x in range((end_date_obj - start_date_obj).days + 1)]
    
    api_key = os.environ.get('API_KEY')
    if not api_key:
        raise ValueError("API_KEY not found in environment variables.")
    
    #----- Se ejecutan los tasks para cada fecha
    for date in date_range:
        try:
            #--- Obtencion de datos desde API
            df = fetch_exchange_rates.submit(api_key, config['base_currency'], date).result()
            #--- Guardando los datos en minio como .csv
            csv_filename = save_to_minio.submit(df, date, config['minio']).result()
            #--- Leyendo los datos desde minio e insertando finalmente en postgres
            df_from_minio = read_csv_from_minio(config['minio'], csv_filename)
            load_to_postgres.submit(df_from_minio, config['postgres'])
        except Exception as e:
            print(f"An error occurred for date {date.strftime('%Y-%m-%d')}: {e}")


if __name__ == '__main__':
    etl_exchange_rates_flow()

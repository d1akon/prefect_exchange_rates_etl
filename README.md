# Exchange rates ETL:

## Tecnologias utilizadas y arquitectura:

* Prefect: Para la organizacion de los flujos/pipelines y orquestamiento.
* Docker & docker-compose para la contenerización y ejecucion de los servicios.
* MinIO para simulacion de datalake (Similar s3 de AWS|Azure|GCP)
* Postgres para Base de datos.

## Pasos a seguir para ejecutar la aplicacion:

1. Clonar el repositorio

2. Posicionarse en la raiz del proyecto y ejecutar el comando "docker-compose build" para generar la imagen.

3. Una vez finalizada la creacion de la imagen, ejecutar "docker-compose up" para levantar los servicios.

Al ejecutar eso, debería verse en la terminal:

    * El contenedor de postgres levantado correctamente
    * El contenedor de minio levantado correctamente
    * Los tests (ejecutados por el service test_runner) deberían correr los 4 correctamente.
    * El servicio de prefect levantado correctamente. Debería decir en la terminarl: "Agent started! Looking for work from queue(s): default...".

Una vez visto ese mensaje final, ya se puede comenzar a utilizar la aplicacion:

* En http://localhost:4200/ se puede observar la interfaz de prefect, desde donde se van a poder ver los flujos schedulados y ejecutar los mismos y ver los logs de las ejecuciones. Desde esa misma interfaz se podrá ejecutar el pipeline creado.

* En http://localhost:9001/ se puede acceder a la interfaz de minio, pudiendose observar y acceder a los buckets y archivos a medida que se vayan creando por los procesos.

* Se puede acceder al servicio de postgres levantando corriendo los siguientes comandos en una nueva terminal:

		# Para ingresar al contenedor:
		
		docker exec -it postgres psql -U postgres -d mydatabase

		# Para listar todas las tablas disponibles (la mayoria serán tablas internas de prefect)
		
        \dt

		# Para ver los datos de la base de datos:
		
        SELECT * FROM exchange_rates;
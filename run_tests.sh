#----- Esperando 15 segundos que se levante el servicio de prefect
sleep 15
#----- Validando a que prefect esté levantado en el puerto determinado
while ! nc -z prefect 4200; do   
  echo "Esperando a que el servicio Prefect esté disponible..."
  sleep 5
done

pytest --disable-warnings

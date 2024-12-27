#----- Version de prefect para validaciones con librerias
prefect version

#----- Iniciar Prefect Orion en segundo plano
prefect orion start --host 0.0.0.0 &

#----- Esperar a que Orion esté listo
sleep 5

#-----  Construir y aplicar deployments para flow1 y flow2 (flows de prueba)
prefect deployment build flows/flow1.py:flow1 --name flow1-deployment --output deployments/flow1-deployment.yaml
prefect deployment apply deployments/flow1-deployment.yaml

prefect deployment build flows/flow2.py:flow2 --name flow2-deployment --output deployments/flow2-deployment.yaml
prefect deployment apply deployments/flow2-deployment.yaml

#----- Construir y aplicar deployment para el flujo ETL de tasas de cambio
prefect deployment build flows/etl_exchange_rates_flow.py:etl_exchange_rates_flow \
    --name etl-exchange-rates-deployment \
    --output deployments/etl-exchange-rates-deployment.yaml \
    --param start_date=null \
    --param end_date=null \
    --cron "0 2 * * *" \
    --timezone "America/Argentina/Buenos_Aires"

prefect deployment apply deployments/etl-exchange-rates-deployment.yaml

#----- Iniciar el agente de Prefect
prefect agent start --work-queue 'default'

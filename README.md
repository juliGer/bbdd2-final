# Bases de datos 2 - Trabajo Final

## Dataset a utlizar

Para las pruebas se tiene que utilizar el siguiente dataset ya que el modelo esta basado en el dataset [Dataset](https://www.kaggle.com/datasets/dilwong/flightprices). Si el dataset es muy grande lo que se puede hacer es utilizar el fixture que se dejo en el repositorio mas adelante se explica como cargarlo en las bd.

## API - Query endpoints
Para limitar la cantidad agregar al final el parametro limit (esto limita la cantidad a la hora de procesar los datos pero a la hora de retornar se retorna una cantidad fija por cuestiones de rendimiento) por ejemplo `http://localhost:8000/flight-prices/postgres-average-tax/?limit=1000` funciona para todos los siguientes endpoints

1. /flight-prices/mongo-date-diff/

    ```
    Retorna la diferencia de dias entre la fecha de compra y la fecha de vuelo
    ```

2. /flight-prices/mongo-max-date-diff/

    ```
    Retorna el máximo en dias de la diferencia entre la fecha de compra y la fecha de vuelo
    ```

3. /flight-prices/mongo-average-tax/

    ```
    Retorna el promedio de impuestos en el precio
    ```

4. /flight-prices/mongo-search-between-dates/

    ```
    Retorna los vuelos entre dos fechas (searchDate y flightDate)
    ```

5. /flight-prices/postgres-date-diff/

    ```
    Retorna la diferencia de dias entre la fecha de compra y la fecha de vuelo
    ```

6. /flight-prices/postgres-max-date-diff/

    ```
    Retorna el máximo en dias de la diferencia entre la fecha de compra y la fecha de vuelo
    ```

7. /flight-prices/postgres-average-tax/

    ```
    Retorna el promedio de impuestos en el precio
    ```

8. /flight-prices/postgres-search-between-dates/

    ```
    Retorna los vuelos entre dos fechas (searchDate y flightDate)
    ```

## Iniciar la aplicación

1. Posicionarse en la raiz del proyecto
2. Una vez posicionados correr el siguiente comando `docker-compose -f docker-compose.yml up`
3. Cuando termine de levantarse el docker va a ver lo siguiente

![docker-ready](https://cdn.discordapp.com/attachments/1058409529466961970/1058414689102614598/image.png)

4. La app levanta en http://localhost:12000/ 

## Como cargar el dataset (Si se tiene espacio es el ultimo paso)

> :warning: **Este paso puede tardar mucho tiempo incluso dias**: Be very careful here!
1. Descargar el [Dataset](https://www.kaggle.com/datasets/dilwong/flightprices)
2. Para postgres usar el siguiente endpoint `/upload-file/`
3. Para mongo usar el siguiente endpoint `/upload-file/?use_mongo=True`
4. Enviar la key file en el body de tipo file con el csv

![Upload-file](https://cdn.discordapp.com/attachments/1058409529466961970/1058409597309829190/Screenshot_20221230_123607.png)
5. Una vez cargado el dataset ya puede usar la aplicación sin problema :)

## Alternativa paracargar datos en la bd (opcional por falta de espacio)

Si no se tiene el suficiente espacio se pueden usar unos datos de prueba que se cargan de la siguiente manera

1. Una vez levantado el docker abrir otra terminal y correr `docker exec -it bbdd2-final_web_1 bash`
2. Por ultimo correr estos comandos
    - python manage.py loaddata app/fixtures/FlightPrice.json  
    - python manage.py loaddata app/fixtures/FlightPrice.json --database=mongo
    
    Va a ver lo siguiente 
    ![loaddata](https://cdn.discordapp.com/attachments/1058409529466961970/1058423088385097739/image.png)
    Significa que ya esta cargada la data en ambas bases (esto solo carga 1000 objetos) y ya se puede cerrar la terminal
3. Ya puede usar la aplicacón sin problema :)
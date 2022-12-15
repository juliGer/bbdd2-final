#!/bin/sh

python manage.py migrate 
python manage.py migrate --database mongo

echo "------------------------------------------------------------------"
echo "--------- Cargando data en ambas bd espere a que termine ---------"
echo "------------------------------------------------------------------"

echo "---------------------------------------------"
echo "----------- Cargando en postgres ------------"
echo "---------------------------------------------"
python manage.py loaddata app/fixtures/FlightPrice.json

echo "---------------------------------------------"
echo "----------- Cargando en mongo ------------"
echo "---------------------------------------------"
python manage.py loaddata app/fixtures/FlightPrice.json --database mongo

echo "---------------------------------------------"
echo "---- Se cargaron las bases correctamente ----"
echo "---------------------------------------------"

python manage.py runserver 0.0.0.0:8000
from datetime import date
import json
from time import time
from django.db import connections
from django.db.models import DateField, ExpressionWrapper, Max, FloatField, F
from django.db.models.functions import Cast
import pandas as pd


from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import FlightPrice
from app.serializers import ExecutionTimeSerializer, FlightPriceSerializer
from app.utils.db import get_collection_handle, get_db_handle


class UploadViewSet(views.APIView):

    def post(self, request):
        data = request.data
        if not data:
            return Response(data="Request vacio", status=status.HTTP_400_BAD_REQUEST)

        file = data.get('file')

        if not ('csv' in file.content_type):
            return Response(data="Debe ingresar un csv", status=status.HTTP_400_BAD_REQUEST)

        params = {'filepath_or_buffer': file, 'chunksize': 100000}
        for data in pd.read_csv(**params):
            # data = self.date_string_to_date(data)
            # mycol.insert_many(json.loads(data.to_json(orient='records')))
            for objects in json.loads(data.to_json(orient='records')):
                FlightPrice.objects.create(**objects)
                FlightPrice.objects.using('mongo').create(**objects)
        return Response(data={}, status=status.HTTP_200_OK)


class FlightPriceViewSet(viewsets.ModelViewSet):

    queryset = FlightPrice.objects.all()[:20]
    serializer_class = FlightPriceSerializer

    @action(methods=['GET'], detail=False, url_name='mongo-date-diff', url_path='mongo-date-diff')
    def mongo_date_diff(self, request):
        limit = int(request.query_params.get('limit', 10000000))
        db_handle, myclient = get_db_handle('bbdd2', 'localhost', '27017')
        mycol = get_collection_handle(
            db_handle=db_handle, collection_name='app_flightprice')

        list(mycol.aggregate(
            [
                {
                    '$project': {
                        '_id': 0,
                        'id': 1,
                        'result': {
                            '$dateDiff': {
                                'startDate': {
                                    '$dateFromString': {
                                        'dateString': '$searchDate'
                                    }
                                },
                                'endDate': {
                                    '$dateFromString': {
                                        'dateString': '$flightDate'
                                    }
                                },
                                'unit': 'day'
                            }
                        }
                    }
                },
                {'$limit': limit},
            ]
        ))

        return Response({'count': limit})

    @action(methods=['GET'], detail=False, url_name='mongo-max-date-diff', url_path='mongo-max-date-diff')
    def mongo_date_diff(self, request):
        limit = int(request.query_params.get('limit', 10000000))
        db_handle, myclient = get_db_handle('bbdd2', 'localhost', '27017')
        mycol = get_collection_handle(
            db_handle=db_handle, collection_name='app_flightprice')

        list(mycol.aggregate(
            [
                {
                    '$project': {
                        '_id': 0,
                        'result': {
                            '$dateDiff': {
                                'startDate': {
                                    '$dateFromString': {
                                        'dateString': '$searchDate'
                                    }
                                },
                                'endDate': {
                                    '$dateFromString': {
                                        'dateString': '$flightDate'
                                    }
                                },
                                'unit': 'day'
                            }
                        }
                    }
                },
                {'$limit': limit},
                {
                    "$group": {
                        "_id": None,
                        "max": {
                            "$max": "$result"
                        }
                    }
                },
            ]
        ))

        return Response({'count': limit})

    @action(methods=['GET'], detail=False, url_name='mongo-average-tax', url_path='mongo-average-tax')
    def mongo_average_tax(self, request):
        limit = int(request.query_params.get('limit', 10000000))
        db_handle, myclient = get_db_handle('bbdd2', 'localhost', '27017')
        mycol = get_collection_handle(
            db_handle=db_handle, collection_name='app_flightprice')

        list(mycol.aggregate(
            [
                {
                    '$project': {
                        '_id': 0,
                        'porcentaje_impuestos': {
                            '$multiply': [
                                {
                                    '$divide': [
                                        {'$subtract': ['$totalFare', '$baseFare']}, '$baseFare'
                                    ]
                                }, 100
                            ]
                        }
                    }
                },
                {'$limit': limit}
            ]
        ))

        return Response({'count': limit})

    @action(methods=['GET'], detail=False, url_name='mongo-search-between-dates', url_path='mongo-search-between-dates')
    def mongo_search_between_dates(self, request):
        limit = int(request.query_params.get('limit', 10000000))
        db_handle, myclient = get_db_handle('bbdd2', 'localhost', '27017')
        mycol = get_collection_handle(
            db_handle=db_handle, collection_name='app_flightprice')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            Response(data={'Debe ingresar las fechas a buscar'}, status=status.HTTP_400_BAD_REQUEST)

        list(mycol.find({'flightDate': {'$gte': start_date, '$lt': end_date}}, {'_id': 0}))
        return Response({'count': limit})

    @action(methods=['GET'], detail=False, url_name='postgres-date-diff', url_path='postgres-date-diff')
    def postgres_date_diff(self, request):
        limit = int(request.query_params.get('limit', 10000000))
        list(FlightPrice.objects.annotate(result=ExpressionWrapper(
            Cast('flightDate', DateField())-Cast('searchDate', DateField()), output_field=DateField())).values('id', 'result')[:limit])
        return Response({'count': limit})

    @action(methods=['GET'], detail=False, url_name='postgres-max-date-diff', url_path='postgres-max-date-diff')
    def postgres_max_date_diff(self, request):
        limit = int(request.query_params.get('limit', 10000000))
        FlightPrice.objects.annotate(result=ExpressionWrapper(
            Cast('flightDate', DateField())-Cast('searchDate', DateField()), output_field=DateField()))[:limit].values('result').aggregate(Max('result'))
        return Response({'count': limit})

    @action(methods=['GET'], detail=False, url_name='postgres-average-tax', url_path='postgres-average-tax')
    def postgres_average_tax(self, request):
        limit = int(request.query_params.get('limit', 10000000))
        list(FlightPrice.objects.annotate(porcentaje_impuestos=ExpressionWrapper(
            ((F('totalFare')-F('baseFare')) / F('baseFare')) * 100, output_field=FloatField())).values('porcentaje_impuestos')[:limit])
        return Response({'count': limit})

    @action(methods=['GET'], detail=False, url_name='search-between-dates', url_path='search-between-dates')
    def postgres_search_between_dates(self, request):
        limit = int(request.query_params.get('limit', 10000000))
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            Response(data={'Debe ingresar las fechas a buscar'}, status=status.HTTP_400_BAD_REQUEST)

        list(FlightPrice.objects.filter(searchDate__gte=start_date, flightDate__lt=end_date))
        return Response({'count': limit})

import json
from time import time
from django.db.models import Avg
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

        # reader.read_file(file, file.content_type, data['headers'])

        params = {'filepath_or_buffer': file, 'chunksize': 100000}
        for data in pd.read_csv(**params):
            # data = self.date_string_to_date(data)
            # mycol.insert_many(json.loads(data.to_json(orient='records')))
            for objects in json.loads(data.to_json(orient='records')):
                FlightPrice.objects.create(**objects)
                FlightPrice.objects.using('sql').create(**objects)
        return Response(data={}, status=status.HTTP_200_OK)


class FlightPriceViewSet(viewsets.ModelViewSet):

    queryset = FlightPrice.objects.using('sql').all()[:20]
    serializer_class = FlightPriceSerializer

    @action(methods=['GET'], detail=False, url_name='prueba', url_path='prueba')
    def prueba(self, request):
        start_sql_time = time()
        list(FlightPrice.objects.all())
        duration_sql = time() - start_sql_time
        return Response({'time': '%.2f' % duration_sql})

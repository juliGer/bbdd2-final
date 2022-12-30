from django.urls import include, path
from rest_framework.routers import DefaultRouter
from app.api import UploadViewSet, FlightPriceViewSet

app_name = 'app'

router = DefaultRouter()
router.register(r'flight-prices', FlightPriceViewSet)

urlpatterns = [
    path('upload-file/', UploadViewSet.as_view(), name='upload-file')
]

urlpatterns += router.urls

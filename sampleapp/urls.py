from django.urls import path
from .views import image_request

app_name = 'sampleapp'
urlpatterns = [
    path('', image_request, name="image-request")
]

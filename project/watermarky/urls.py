from django.urls import path, include
from .views import *



urlpatterns = [
    path("watermark", watermark_image, name='watermark_image')
]

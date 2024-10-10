from django.urls import path, include, re_path
from django.views.static import serve
from .views import *
from django.conf import settings


urlpatterns = [
    path("", watermark_image, name='watermark_image'),
    path("watermark", watermark_image, name='watermark_image'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

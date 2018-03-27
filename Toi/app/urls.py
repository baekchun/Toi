from django.conf.urls import url, include
from .ViewSets.ImageViewSet import ImageViewSet
from django.views.generic import ListView, DetailView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'image', ImageViewSet, base_name='image')

urlpatterns = [
    url(r'^', include(router.urls)),
]


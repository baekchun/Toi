from django.conf.urls import url, include
from .ViewSets.ImageViewSet import ImageViewSet
from .ViewSets.UserViewSet import UserViewSet
from django.views.generic import ListView, DetailView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'image', ImageViewSet, base_name='image')
router.register(r'users', UserViewSet, base_name='user')

urlpatterns = [
    url(r'^', include(router.urls)),
]


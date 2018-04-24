from django.conf.urls import url, include
from .ViewSets.ImageViewSet import ImageViewSet
from .ViewSets.UserViewSet import UserViewSet
from .ViewSets.UserProfileViewSet import UserProfileViewSet
from django.views.generic import ListView, DetailView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'image', ImageViewSet, base_name='image')
router.register(r'users', UserViewSet, base_name='user')
router.register(r'profile', UserProfileViewSet, base_name='profile')

urlpatterns = [
    url(r'^', include(router.urls)),
]


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('bytes', 'taken_on')


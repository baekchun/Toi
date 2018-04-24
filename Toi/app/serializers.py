from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Image, UserProfile, Stool

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('bytes', 'taken_on')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name')


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user')

class StoolSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Stool
		fiels = ('user', 'bristol_type', 'date', 'contains_blood', 'contains_mucus', 'color_distribution', 'bar_chart')

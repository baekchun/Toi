from ..k_means import kmeans, get_color_names
from ..countBlobs import get_type, count_blobs
from ..models import Image, Stool, UserProfile
from django.contrib.auth.models import User
from ..serializers import ImageSerializer, StoolSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

import pyrebase
import logging
import base64
import json
import cv2

class ImageViewSet(viewsets.ModelViewSet):
    logger = logging.getLogger(__name__)

    @list_route(methods=['post'], url_path='save')
    def save_image(self, request):
        """
        save image from request
        """
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():

            # save the original 
            serializer.save()

            # convert binary string into a base64 image
            output_file = "../images/output.jpg"
            with open(output_file, "wb") as f:
                f.write(base64.b64decode(serializer.validated_data["bytes"]))

            # run analysis and get all the details about the poop
            color_dist, bar, color_dict, contains_blood, contains_mucus = self.get_stool_details(output_file)


            # get user profile object of the API caller
            user_profile = self.get_user_profile_object(request)

            # write the bar chart image 
            cv2.imwrite('bar_chart.png', bar)

            # convert the image into string
            with open('bar_chart.png', "rb") as f:
                encoded_string = base64.b64encode(f.read())

            # encoded_string = encoded_string.decode('ascii')
            
            # firebase config
            config = {
                "apiKey": "AIzaSyBxl_Hn9MFnAIodQAYYUveqE5X7XAgns_0",
                "authDomain": "csie-toi.firebaseapp.com",
                "databaseURL": "https://csie-toi.firebaseio.com",
                "storageBucket": "csie-toi.appspot.com",
            }

            # the actual data that gets sent to firebasea
            data = {
                "bristol_type": get_type(count_blobs(output_file)),
                "date": serializer.data["taken_on"],
                "contains_blood": contains_blood,
                "contains_mucus": contains_mucus,
                "color_distribution": json.dumps(color_dict),
                "bar_chart": encoded_string 
            }
            print (data)
            # firebase = pyrebase.initialize_app(config)
            # db = firebase.database()
            # db.child("stools").push(data)

            # store the image into the database
            return Response("SUCCESS", status=201)
        else:
            # invalid request
            return Response(serializer.errors, status=400)

    def get_stool_details(self, output_file):
        # get color distribution and bar chart from k_means clusterings
        color_dist, bar = kmeans(output_file)

        color_dict = {}

        blood_colors = set(["maroon", "red"])
        mucus_colors = set([])

        contains_blood = False
        contains_mucus = False

        # identify the color name based on the RGB values
        for percentage, rgb in color_dist.items():
            query = ((int(rgb[0]), int(rgb[1]), int(rgb[2])))
            color_name = get_color_names(query)

            # check if blood color is found in your stool
            if color_name in blood_colors:
                contains_blood = True

            if color_name in mucus_colors:
                contains_mucus = True

            color_dict[color_name] = percentage

        return color_dist, bar, color_dict, contains_blood, contains_mucus

    def get_user_profile_object(self, request):
        """
        Retrieve the user profile object, given user name
        """
        username = request.data["username"]

        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
            return user_profile
        except User.DoesNotExist:
            return Response("user name={NAME} not found".format(NAME=username), status=400)

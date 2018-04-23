from ..k_means import kmeans, get_color_names
from ..countBlobs import get_type, count_blobs
from ..models import Image
from ..serializers import ImageSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

import logging
import base64
import json

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    logger = logging.getLogger(__name__)

    @list_route(methods=['post'], url_path='save')
    def save_image(self, request):
        """
        save image from request
        """
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            output_file = "../images/output.jpg"

            # get the type of stool based on Bristol Stool Chart
            count = count_blobs(output_file)
            stool_type = get_type(count)
            message = ""
            message += stool_type + " with color distribution of "

            # convert binary string into a base64 image
            with open(output_file, "wb") as f:
                f.write(base64.b64decode(serializer.data["bytes"]))

            # get color distribution from k_means clustering
            color_dist = kmeans(output_file)

            additional_msg = ""
            results = {}
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

                results[color_name] = percentage

            # add the percentage of each color distribution to the response msg
            for k, v in results.items():
                message += " " + str(int(v * 100)) + "% of " + k + ",  "
            
            if contains_blood:
                message += "\n" + " Blood found in your stool"
            else:
                message += "\n" + " No blood found"

            if contains_mucus:
                message += "\n" + " Mucus found in your stool"
            else:
                message += "\n" + " No mucus found"


            print (message)

            # serializer.save()
            # store the image into the database
            return Response("SUCCESS: " + message, status=201)
        else:
            # invalid request
            return Response(serializer.errors, status=400)

    # def get_IP_address(self, request):
    #     """
    #     get user's IP address
    #     """

    #     from ipware import get_client_ip
    #     ip, is_routable = get_client_ip(request)

    #     # Order of precedence is (Public, Private, Loopback, None)

    #     if ip is None:
    #        print ("Unable to get the client's IP address")
    #     else:
    #         # We got the client's IP address
    #         if is_routable:
    #             print ("Client's IP address is", ip)
    #         else:
    #             print ("Client's IP address is private")

    #     
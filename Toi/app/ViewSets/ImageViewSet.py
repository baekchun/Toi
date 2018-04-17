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

            results = {}
            for percentage, rgb in color_dist.items():
                query = ((int(rgb[0]), int(rgb[1]), int(rgb[2])))
                color_name = get_color_names(query)
                results[color_name] = percentage


            for k, v in results.items():
                message += " " + str(int(v * 100)) + "% of " + k + ",  "
            
            message += "\n"


            print (message)

            # serializer.save()
            # store the image into the database
            return Response("SUCCESS: " + message, status=201)
        else:
            # invalid request
            return Response(serializer.errors, status=400)
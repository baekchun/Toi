from ..models import Image
from ..serializers import ImageSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

import logging

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
            serializer.save()
            # store the image into the database
            return Response("You have successfully stored the image on DB!", status=201)
        else:
        	# invalid request
            return Response(serializer.errors, status=400)
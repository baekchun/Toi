from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.forms import inlineformset_factory
from ..models import UserProfile, Stool
from ..serializers import UserSerializer, UserProfileSerializer
from rest_framework.decorators import detail_route, list_route
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
import logging
import json

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    logger = logging.getLogger(__name__)

    # profile/history

    @list_route(methods=['get'], url_path='history')
    def history(self, request):
        """
        
        """
        user_name = request.query_params.get('username')
        
        try:
            target_user = UserProfile.objects.get(user=User.objects.get(username=user_name))

            all_stools = Stool.objects.filter(user=target_user)
            print (all_stools)
            stool_json = []

            for i in range(len(all_stools)):
                print (i, all_stools[i])
                stool_json.append(
                    {
                        "bristol_type":all_stools[i].bristol_type,
                        "date": all_stools[i].date,
                        "contains_blood": all_stools[i].contains_blood,
                        "contains_mucus": all_stools[i].contains_mucus,
                        "color_distribution": all_stools[i].color_distribution,
                        "bar_chart": all_stools[i].bar_chart
                    }
                )

            print (stool_json)
            return Response(stool_json, status=200)
        
        except:
            return Response(status=400)

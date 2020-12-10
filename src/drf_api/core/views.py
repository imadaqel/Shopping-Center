from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView)

from . serializers import *
from .models import *

# class TestView(APIView):
#     def get(self,request,*args,**kwargs):
#         data = {
#             'name':'Abed',
#             'age':23
#         }
#         return Response(data)

def home(request):
    return HttpResponse("Hello, Django!")

class UserProfileView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"user": detail.user,"stripe_customer_id": detail.stripe_customer_id}, status=HTTP_200_OK)
        


class ItemListView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ItemSerializer
    queryset = Item.objects.all()



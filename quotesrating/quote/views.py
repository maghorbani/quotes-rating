from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.parsers import JSONParser

from .serializers import QuoteSerializer
from .models import Quote, Rate

class QuoteView(ModelViewSet):

    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()
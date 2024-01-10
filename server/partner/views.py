from django.shortcuts import render
from rest_framework import generics
from .models import Partner, PartnerTag
from .serializers import PartnerSerializer, PartnerTagSerializer

class PartnerListCreateView(generics.ListCreateAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

class PartnerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

class PartnerTagListCreateView(generics.ListCreateAPIView):
    queryset = PartnerTag.objects.all()
    serializer_class = PartnerTagSerializer

class PartnerTagRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PartnerTag.objects.all()
    serializer_class = PartnerTagSerializer
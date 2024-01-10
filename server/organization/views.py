from django.shortcuts import render
from rest_framework import generics
from .models import Organization, OrganizationTag
from .serializers import OrganizationSerializer, OrganizationTagSerializer

class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class OrganizationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class OrganizationTagListCreateView(generics.ListCreateAPIView):
    queryset = OrganizationTag.objects.all()
    serializer_class = OrganizationTagSerializer

class OrganizationTagRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrganizationTag.objects.all()
    serializer_class = OrganizationTagSerializer
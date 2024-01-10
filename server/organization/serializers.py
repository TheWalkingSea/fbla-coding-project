from rest_framework import serializers
from .models import Organization, OrganizationTag

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class OrganizationTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationTag
        fields = '__all__'
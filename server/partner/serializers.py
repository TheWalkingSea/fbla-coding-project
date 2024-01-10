from rest_framework import serializers
from .models import Partner, PartnerTag

class PartnerTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerTag
        fields = '__all__'

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'
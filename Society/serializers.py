from rest_framework import serializers
from .models import Society,Society_Secretry

class SocietySerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='', read_only=True)
    class Meta:
        model=Society
        fields='__all__'

class Societysecretry_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Society_Secretry
        fields = '__all__'

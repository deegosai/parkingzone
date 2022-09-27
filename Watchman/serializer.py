from .models import Watchman

from rest_framework import serializers

class Watchman_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Watchman
        fields = '__all__'





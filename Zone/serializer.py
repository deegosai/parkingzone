from rest_framework import serializers

from .models import *

class ParkSlot_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Park_slot
        fields = '__all__'

class ParkSlot_owner_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Park_Slot_Owner
        fields = '__all__'

class ParkSlot_owner_commision_history_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Park_Slot_Owner_Commision_history
        fields = '__all__'


class Booking_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Zone_Booking
        fields = '__all__'

class Booking_history_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Zone_Booking_history
        fields = '__all__'


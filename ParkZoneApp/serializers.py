from rest_framework import serializers
from .models import Admin,Admin_Wallet

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model=Admin
        fields='__all__'

class AdminWalletSeriallizer(serializers.ModelSerializer):
    class Meta:
        model=Admin_Wallet
        fields='__all__'
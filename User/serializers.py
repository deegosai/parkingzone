from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','name','country','age','city','state','email')
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserVehicle
        fields='__all__'

class UserWalletSeriallizer(serializers.ModelSerializer):
    class Meta:
        model=User_Wallet
        fields='__all__'

class UserTransactionSeriallizer(serializers.ModelSerializer):
    class Meta:
        model=User_Transaction_history
        fields='__all__'
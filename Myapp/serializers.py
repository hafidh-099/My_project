from .models import *
#from rest_framework import serializers
from rest_framework import serializers


class FoodItemserializers(serializers.ModelSerializer):
    class Meta:
        model=FoodItem
        fields = '__all__'
        
class Customerserializers(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields = '__all__'
        
class Orderserializers(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields = '__all__'
        
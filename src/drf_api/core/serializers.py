from rest_framework import serializers
from . models import *


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'stripe_customer_id']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['itemName','details', 'price','image','quantity','category']


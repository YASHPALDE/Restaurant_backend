from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Restaurant, MenuItem
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'description')

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
        read_only_fields = ('restaurant',)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        if hasattr(user, 'restaurant'):
            token['restaurant_id'] = user.restaurant.id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        if hasattr(self.user, 'restaurant'):
            data['restaurant_id'] = self.user.restaurant.id
        return data

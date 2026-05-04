from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .models import Restaurant, MenuItem
from .serializers import (
    UserSerializer, 
    RestaurantSerializer, 
    MenuItemSerializer, 
    CustomTokenObtainPairSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RestaurantProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        # Create restaurant if it doesn't exist for the user
        restaurant, created = Restaurant.objects.get_or_create(
            user=self.request.user,
            defaults={'name': f"{self.request.user.username}'s Restaurant"}
        )
        return restaurant

class MenuItemListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return MenuItem.objects.filter(restaurant__user=self.request.user)

    def perform_create(self, serializer):
        restaurant, _ = Restaurant.objects.get_or_create(user=self.request.user)
        serializer.save(restaurant=restaurant)

class MenuItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return MenuItem.objects.filter(restaurant__user=self.request.user)

# Public view for customers
class PublicMenuView(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        restaurant_id = self.kwargs.get('restaurant_id')
        return MenuItem.objects.filter(restaurant_id=restaurant_id, is_available=True)

class PublicRestaurantDetailView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_url_kwarg = 'restaurant_id'

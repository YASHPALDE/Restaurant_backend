from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    RestaurantProfileView,
    MenuItemListCreateView,
    MenuItemRetrieveUpdateDestroyView,
    PublicMenuView,
    PublicRestaurantDetailView
)

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Admin - Profile
    path('admin/profile/', RestaurantProfileView.as_view(), name='admin-profile'),
    
    # Admin - Menu CRUD
    path('admin/menu/', MenuItemListCreateView.as_view(), name='admin-menu-list'),
    path('admin/menu/<int:pk>/', MenuItemRetrieveUpdateDestroyView.as_view(), name='admin-menu-detail'),
    
    # Public - Customer Facing
    path('public/restaurant/<int:restaurant_id>/', PublicRestaurantDetailView.as_view(), name='public-restaurant-detail'),
    path('public/menu/<int:restaurant_id>/', PublicMenuView.as_view(), name='public-menu'),
]

from django.urls import include, path
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.restaurantDashboard, name='restaurant'),
    path('profile/', views.restaurant_profile, name='restaurant_profile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),
    
    # Category CURD
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
]
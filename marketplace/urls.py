from django.urls import include, path

from marketplace import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    
    # vendor detail
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),
    
    # add to cart
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    # decrease item in cart
    path('decrease_cart/<int:food_id>/', views.decrease_cart, name='decrease_cart'),
]
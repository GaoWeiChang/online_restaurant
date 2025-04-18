from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.myAccount),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('customerDashboard/', views.customerDashboard, name='customerDashboard'), # customer dashboard
    path('restaurantDashboard/', views.restaurantDashboard, name='restaurantDashboard'), # restaurant dashboard
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    
    path('restaurant/', include('vendor.urls')), # include vendor urls to accounts urls
    path('customer/', include('customers.urls')),  
]
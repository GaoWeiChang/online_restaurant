from django.urls import path
from accounts import views as AccountView
from . import views

urlpatterns = [
    path('', AccountView.customerDashboard, name='customer'),
    path('profile/', views.cprofile, name='cprofile'),
]

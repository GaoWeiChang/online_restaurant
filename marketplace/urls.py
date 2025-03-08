from django.urls import include, path

from marketplace import views

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
]
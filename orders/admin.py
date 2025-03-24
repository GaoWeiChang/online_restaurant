from django.contrib import admin
from .models import Payment, Order, OrderedFood

# register the model to allow it to be viewed in the admin panel
admin.site.register(Payment) 
admin.site.register(Order)
admin.site.register(OrderedFood)

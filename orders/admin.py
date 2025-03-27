from django.contrib import admin
from .models import Payment, Order, OrderedFood

# admin.TarularInline is used to display the OrderedFood model in the Order model
class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ('order', 'payment', 'user', 'fooditem', 'quantity', 'price', 'amount')
    extra = 0 # remove the extra rows
        
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'phone', 'total', 'payment_method', 'status', 'is_ordered']
    inlines = [OrderedFoodInline]


# register the model to allow it to be viewed in the admin panel
admin.site.register(Payment) 
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedFood)

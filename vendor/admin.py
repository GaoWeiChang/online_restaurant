from django.contrib import admin

from vendor.models import OpeningHour, Vendor

class VendorAdmin(admin.ModelAdmin): # ใช้สำหรับโมเดล Vendor ซึ่งเป็นโมเดลปกติที่สร้างขึ้นเอง
    list_display = ('user', 'vendor_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'vendor_name')

class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'day', 'from_hour', 'to_hour')
    

# Register your models here.
admin.site.register(Vendor, VendorAdmin)
admin.site.register(OpeningHour, OpeningHourAdmin)

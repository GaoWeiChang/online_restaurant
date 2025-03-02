from vendor.models import Vendor

# ทำหน้าที่เพิ่มข้อมูลให้กับ context ที่จะถูกส่งไปยังทุก template โดยอัตโนมัติ โดยไม่ต้องส่งข้อมูลซ้ำๆ ในทุก view
def get_restaurant(request):
    try: # prevent logged out and request anonymous object
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)
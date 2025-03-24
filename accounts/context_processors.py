from django.conf import settings # type: ignore
from accounts.models import UserProfile
from vendor.models import Vendor


# ทำหน้าที่เพิ่มข้อมูลให้กับ context ที่จะถูกส่งไปยังทุก template โดยอัตโนมัติ โดยไม่ต้องส่งข้อมูลซ้ำๆ ในทุก view
def get_restaurant(request):
    try: # prevent logged out and request anonymous object
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)

def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)

def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}
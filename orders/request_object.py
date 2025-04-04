from . import models

# Middleware สร้างตัวแปรกลาง models.request_object ที่เก็บ request ปัจจุบัน เมื่อมีการเรียกใช้ request ใหม่ ทำให้สามารถเข้าถึง request object จากที่อื่นในโค้ดได้โดยไม่ต้องส่งต่อเป็นพารามิเตอร์
def RequestObjectMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        models.request_object = request

        response = get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware

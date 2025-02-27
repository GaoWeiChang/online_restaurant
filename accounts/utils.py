# แยกโค้ดส่วนที่ใช้ซ้ำ 
# เก็บฟังก์ชันช่วยเหลือ (helper functions)

def detectUser(user):
    if user.role == 1:
        redirectUrl = 'restaurantDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'customerDashboard'
        return redirectUrl
    elif user.role==None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
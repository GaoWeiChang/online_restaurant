# แยกโค้ดส่วนที่ใช้ซ้ำ 
# เก็บฟังก์ชันช่วยเหลือ (helper functions)

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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
    
def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request) # ดึงข้อมูลของเว็บไซต์ปัจจุบัน (โดเมน) จากคำขอที่ส่งมา, เพื่อสร้าง URL ที่ถูกต้องในอีเมล์ยืนยัน
    
    # use template HTML เพื่อสร้างเนื้อหาอีเมล์
    message = render_to_string(email_template, # UI site
        { 
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)), # encoded ID
            'token': default_token_generator.make_token(user) # โทเค็นเฉพาะสำหรับยืนยันตัวตน
        })
    to_email = user.email # กำหนดอีเมล์ผู้รับ
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email]) # สร้างออบเจ็กต์อีเมล์ด้วยหัวข้อ เนื้อหา และผู้รับ
    mail.send() # send email to user
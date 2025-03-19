from datetime import time
from django.db import models

from accounts.models import User, UserProfile
from accounts.utils import send_notification

# Create your models here.
class Vendor(models.Model): # Vendor inherited from models.Model
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE) # able to handle nested class
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    # use *args and **kwargs to save parameter in save function
    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update object
            cur_vendor = Vendor.objects.get(pk=self.pk)
            if cur_vendor.is_approved != self.is_approved:
                mail_template = "accounts/emails/admin_approval_email.html"
                context = { 
                    'user' : self.user,
                    'is_approved' : self.is_approved,
                }
                if self.is_approved == True:
                    # send notification email
                    mail_subject = "Congratulations! Your restaurant has been approved."
                    send_notification(mail_subject, mail_template, context)
                else:
                    # send notification email
                    mail_subject = "Sorry, You are not eligible for publishing your food menu on our platform."
                    send_notification(mail_subject, mail_template, context)

        return super(Vendor, self).save(*args, **kwargs) # เรียกฟังก์ชัน save() ของ parent class (models.Model) ที่คลาส Vendor สืบทอดมา

DAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
]    

HOUR_OF_DAY_24 = [(time(h,m).strftime('%I:%M %p'), time(h,m).strftime('%I:%M %p')) for h in range(0,24) for m in [0, 30]]

class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True) # max_length = max string length to keep inside the blank
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)
    
    # Meta class in Django models allows you to customize how your model interacts with the database and Django's systems
    class Meta:
        ordering = ('day', 'from_hour')
        unique_together = ('day', 'from_hour', 'to_hour')
        
    def __str__(self):
        return self.get_day_display() # automatically created by Django for fields that have choices specified
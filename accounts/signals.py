from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from accounts.models import User, UserProfile

'''
เมื่อเกิดการบันทึกข้อมูลลงในฐานข้อมูล Django จะส่งพารามิเตอร์ created
มาพร้อมกับสัญญาณ post_save โดยอัตโนมัติ ค่า created นี้ถูกกำหนดโดยระบบ Django เอง
'''
@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    print(created)
    if created: # ถ้าไม่มี pk หรือ pk เป็น None แสดงว่าเป็นการบันทึกครั้งแรก Django จะกำหนด created = True
        UserProfile.objects.create(user=instance)
        # print('user profile created')
    else: # ถ้ามี pk อยู่แล้ว แสดงว่าเป็นการอัปเดต Django จะกำหนด created = False
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # create user profile if not exist
            UserProfile.objects.create(user=instance)
            # print('Profile not exist, created one')
        # print('user updated')

@receiver(pre_save, sender=User)
def pre_save_create_profile_receiver(sender, instance, **kwargs):
    pass